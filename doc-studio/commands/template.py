#!/usr/bin/env python3
"""
Template command - Manage document templates
"""

import sys
import json
import argparse
import shutil
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.template import TemplateManager
from core.generator import DocumentGenerator


def _find_builtin_script(templates_path: Path, template_name: str) -> Path | None:
    for _fmt, mapping in DocumentGenerator.TEMPLATE_SCRIPTS.items():
        if template_name in mapping:
            return templates_path / mapping[template_name]
    return None


def main():
    parser = argparse.ArgumentParser(description="Manage templates")
    parser.add_argument("action", choices=["list", "info", "clone", "create", "edit", "export", "import"],
                       help="Action to perform")
    parser.add_argument("--name", "-n", help="Template name")
    parser.add_argument("--format", "-f", choices=["pdf", "pptx", "docx", "xlsx", "html"],
                       help="Filter by format")
    parser.add_argument("--display-name", help="Display name (for create)")
    parser.add_argument("--description", "-d", help="Description (for create)")
    parser.add_argument("--base", "-b", help="Base template (for create)")
    parser.add_argument("--output", "-o", help="Output path (for export)")
    parser.add_argument("--input", "-i", help="Input file (for import)")
    parser.add_argument("--from", dest="from_", help="Source builtin template name (for clone)")
    parser.add_argument("--to", help="Destination template filename/path (for clone)")
    parser.add_argument("--force", action="store_true", help="Overwrite destination if it exists (for clone)")

    args = parser.parse_args()

    manager = TemplateManager()

    if args.action == "list":
        templates = manager.list_templates(format_filter=args.format)
        print(f"{'Name':<20} {'Display Name':<25} {'Formats':<20}")
        print("-" * 65)
        for t in templates:
            print(f"{t.name:<20} {t.display_name:<25} {', '.join(t.formats):<20}")

    elif args.action == "info":
        if not args.name:
            print("Error: --name required")
            sys.exit(1)

        template = manager.get_template(args.name)
        if template:
            print(json.dumps(template.to_dict(), indent=2, ensure_ascii=False))
        else:
            print(f"Template not found: {args.name}")
            sys.exit(1)

    elif args.action == "create":
        if not args.name or not args.display_name:
            print("Error: --name and --display-name required")
            sys.exit(1)

        path = manager.create_template(
            name=args.name,
            display_name=args.display_name,
            description=args.description or "",
            base_template=args.base
        )
        print(f"Created template: {path}")

    elif args.action == "clone":
        if not args.from_ or not args.to:
            print("Error: --from and --to required")
            sys.exit(1)

        src = _find_builtin_script(manager.templates_path, args.from_)
        if not src or not src.exists():
            print(f"Error: Builtin template not found: {args.from_}")
            print("Tip: run `python scripts/template.py list` to see available names.")
            sys.exit(1)

        dst_raw = Path(args.to)
        if not dst_raw.suffix:
            dst_raw = dst_raw.with_suffix(src.suffix)

        if dst_raw.is_absolute():
            dst = dst_raw
        elif dst_raw.parent == Path("."):
            stem = dst_raw.stem
            if not stem.startswith("custom_"):
                stem = f"custom_{stem}"
            dst = manager.templates_path / f"{stem}{src.suffix}"
        else:
            dst = (Path.cwd() / dst_raw).resolve()

        dst.parent.mkdir(parents=True, exist_ok=True)

        if dst.exists() and not args.force:
            print(f"Error: Destination already exists: {dst}")
            print("Tip: pass --force to overwrite.")
            sys.exit(1)

        shutil.copy2(src, dst)
        print(f"Cloned: {src} -> {dst}")
        print("Next: edit the cloned template to match your content and structure.")

    elif args.action == "edit":
        print("Edit is not implemented yet. Open the template file in your editor.")
        print("Tip: use `python scripts/template.py info --name <template>` to locate it.")

    elif args.action == "export":
        if not args.name:
            print("Error: --name required")
            sys.exit(1)

        output = args.output or "."
        path = manager.export_template(args.name, output)
        print(f"Exported to: {path}")

    elif args.action == "import":
        if not args.input:
            print("Error: --input required")
            sys.exit(1)

        path = manager.import_template(args.input)
        print(f"Imported to: {path}")


if __name__ == "__main__":
    main()
