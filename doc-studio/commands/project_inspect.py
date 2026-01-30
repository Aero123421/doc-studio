#!/usr/bin/env python3
"""
Inspect command - Summarize a project directory for Doc Studio usage.

This is intentionally lightweight: it helps the agent quickly discover existing docs,
brand assets, and repository "signals" before drafting a document.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any, Dict, List


IGNORE_DIRS = {
    ".git",
    ".idea",
    ".vscode",
    ".venv",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
    "out",
    "output",
    ".doc-studio",
    ".next",
    ".nuxt",
    "target",
    "vendor",
    ".mypy_cache",
    ".pytest_cache",
}

DOC_EXTENSIONS = {
    ".md",
    ".txt",
    ".docx",
    ".pptx",
    ".xlsx",
    ".pdf",
}

ASSET_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".svg",
    ".webp",
    ".gif",
    ".ico",
    ".ttf",
    ".otf",
    ".woff",
    ".woff2",
}

BRAND_KEYWORDS = {
    "brand",
    "branding",
    "style",
    "guideline",
    "guidelines",
    "logo",
    "logos",
    "design",
    "colors",
    "colour",
    "palette",
    "typography",
    "font",
    "fonts",
}


def _is_ignored_dir(name: str) -> bool:
    return name in IGNORE_DIRS or name.startswith(".git")


def _detect_signals(root: Path) -> List[str]:
    signals: List[str] = []
    if (root / "package.json").exists():
        signals.append("node")
    if (root / "pnpm-lock.yaml").exists():
        signals.append("pnpm")
    if (root / "yarn.lock").exists():
        signals.append("yarn")
    if (root / "requirements.txt").exists():
        signals.append("python")
    if (root / "pyproject.toml").exists():
        signals.append("python")
    if (root / "poetry.lock").exists():
        signals.append("python-poetry")
    if (root / "Pipfile").exists():
        signals.append("python-pipenv")
    if (root / "go.mod").exists():
        signals.append("go")
    if (root / "Cargo.toml").exists():
        signals.append("rust")
    if (root / "pom.xml").exists() or (root / "build.gradle").exists():
        signals.append("java")
    if (root / "Dockerfile").exists() or (root / "docker-compose.yml").exists():
        signals.append("docker")
    if (root / ".github").exists():
        signals.append("github")
    return sorted(set(signals))


def _walk_files(root: Path, max_depth: int) -> List[Path]:
    files: List[Path] = []
    root = root.resolve()
    for dirpath, dirnames, filenames in os.walk(root):
        dp = Path(dirpath)
        rel = dp.relative_to(root)
        depth = len(rel.parts)
        if depth > max_depth:
            dirnames[:] = []
            continue

        dirnames[:] = [d for d in dirnames if not _is_ignored_dir(d)]

        for fn in filenames:
            files.append(dp / fn)

    return files


def _summarize_tree(root: Path, depth: int, max_entries: int) -> List[str]:
    root = root.resolve()
    entries: List[str] = []
    count = 0

    for dirpath, dirnames, filenames in os.walk(root):
        dp = Path(dirpath)
        rel = dp.relative_to(root)
        d = len(rel.parts)
        if d > depth:
            dirnames[:] = []
            continue
        dirnames[:] = [n for n in dirnames if not _is_ignored_dir(n)]

        indent = "  " * d
        label = "." if d == 0 else rel.parts[-1]
        entries.append(f"{indent}{label}/")
        count += 1
        if count >= max_entries:
            entries.append(f"{indent}... (truncated)")
            break

        # show a few files at this level
        show = sorted([f for f in filenames if not f.startswith(".")])[:5]
        for f in show:
            entries.append(f"{indent}  {f}")
            count += 1
            if count >= max_entries:
                entries.append(f"{indent}... (truncated)")
                break
        if count >= max_entries:
            break

    return entries


def inspect_project(path: str, depth: int, json_output: bool) -> int:
    root = Path(path).resolve()
    if not root.exists() or not root.is_dir():
        print(f"Error: not a directory: {root}")
        return 1

    signals = _detect_signals(root)
    tree = _summarize_tree(root, depth=depth, max_entries=200)
    files = _walk_files(root, max_depth=max(depth, 6))

    docs: List[str] = []
    assets: List[str] = []
    brand_hits: List[str] = []
    readmes: List[str] = []

    for fp in files:
        rel = fp.relative_to(root).as_posix()
        lower = rel.lower()
        suffix = fp.suffix.lower()

        if fp.name.lower().startswith("readme"):
            readmes.append(rel)

        if suffix in DOC_EXTENSIONS:
            docs.append(rel)

        if suffix in ASSET_EXTENSIONS:
            assets.append(rel)

        if any(k in lower for k in BRAND_KEYWORDS):
            if suffix in (DOC_EXTENSIONS | ASSET_EXTENSIONS | {".json", ".yml", ".yaml"}):
                brand_hits.append(rel)

    docs = sorted(docs)[:50]
    assets = sorted(assets)[:50]
    brand_hits = sorted(set(brand_hits))[:50]
    readmes = sorted(readmes)[:20]

    data: Dict[str, Any] = {
        "root": str(root),
        "signals": signals,
        "readmes": readmes,
        "docs": docs,
        "assets": assets,
        "brand_hits": brand_hits,
        "tree": tree,
    }

    if json_output:
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return 0

    print("Project Inspect")
    print("===============")
    print(f"Root: {root}")
    if signals:
        print(f"Signals: {', '.join(signals)}")
    print("")

    if readmes:
        print("README:")
        for p in readmes:
            print(f"- {p}")
        print("")

    if brand_hits:
        print("Brand / style hints (filenames):")
        for p in brand_hits:
            print(f"- {p}")
        print("")

    if docs:
        print("Docs (first 50):")
        for p in docs:
            print(f"- {p}")
        print("")

    if assets:
        print("Assets (first 50):")
        for p in assets:
            print(f"- {p}")
        print("")

    print("Tree (truncated):")
    for ln in tree:
        print(ln)
    print("")

    print("Next steps (suggested):")
    print("- Summarize: project goal, audience, constraints, existing assets")
    print("- Ask: output format, volume, tone, deadline, mandatory content")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect a project directory for Doc Studio usage")
    parser.add_argument("--path", default=".", help="Directory to inspect (default: .)")
    parser.add_argument("--depth", type=int, default=3, help="Tree depth (default: 3)")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    raise SystemExit(inspect_project(args.path, args.depth, args.json))


if __name__ == "__main__":
    main()
