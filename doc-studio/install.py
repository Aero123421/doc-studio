#!/usr/bin/env python3
"""
Doc Studio Skill Installer
Installs skill to various AI coding assistant CLI tools
"""

import os
import sys
import shutil
import argparse
from pathlib import Path


CLI_TOOLS = {
    "claude-code": {
        "name": "Claude Code",
        "config_dir": {
            "windows": "~/.claude/Skills",
            "darwin": "~/.claude/skills",
            "linux": "~/.claude/skills",
        },
        "adapter": "claude-code",
    },
    "codex": {
        "name": "Codex CLI",
        "config_dir": {
            "windows": "~/.codex/skills",
            "darwin": "~/.codex/skills",
            "linux": "~/.codex/skills",
        },
        "adapter": "codex",
    },
    "gemini": {
        "name": "Gemini CLI",
        "config_dir": {
            "windows": "~/.gemini/skills",
            "darwin": "~/.gemini/skills",
            "linux": "~/.gemini/skills",
        },
        "adapter": "gemini",
    },
    "opencode": {
        "name": "OpenCode",
        "config_dir": {
            "windows": "~/.opencode/skills",
            "darwin": "~/.opencode/skills",
            "linux": "~/.opencode/skills",
        },
        "adapter": "opencode",
    },
}


def get_platform():
    """Get current platform"""
    if sys.platform.startswith("win"):
        return "windows"
    elif sys.platform == "darwin":
        return "darwin"
    else:
        return "linux"


def expand_path(path: str) -> Path:
    """Expand user home in path"""
    return Path(path).expanduser()


def install_skill(cli_tool: str, symlink: bool = False):
    """Install skill to specific CLI tool"""
    if cli_tool not in CLI_TOOLS:
        print(f"Error: Unknown CLI tool '{cli_tool}'")
        print(f"Available: {', '.join(CLI_TOOLS.keys())}")
        return False

    tool_info = CLI_TOOLS[cli_tool]
    platform = get_platform()

    config_dir = expand_path(tool_info["config_dir"][platform])
    skill_dir = config_dir / "doc-studio"

    print(f"Installing Doc Studio Skill for {tool_info['name']}...")
    print(f"Target directory: {skill_dir}")

    # Check if already installed
    if skill_dir.exists():
        print(f"Skill already installed. Updating...")
        shutil.rmtree(skill_dir)

    # Create parent directory
    config_dir.mkdir(parents=True, exist_ok=True)

    # Get source directory
    script_dir = Path(__file__).parent
    adapter_dir = script_dir / "adapters" / tool_info["adapter"]

    if symlink:
        # Create symlink for development
        skill_dir.symlink_to(script_dir, target_is_directory=True)
        print(f"Created symlink: {skill_dir} -> {script_dir}")
    else:
        # Copy whole skill folder (exclude generated outputs/caches)
        def _ignore(_, names):
            ignore = {"__pycache__", ".pytest_cache", "output"}
            return [n for n in names if n in ignore]

        shutil.copytree(script_dir, skill_dir, ignore=_ignore)

        # Overlay tool-specific adapter manifest to skill root (if provided)
        if adapter_dir.exists():
            for item in adapter_dir.iterdir():
                if item.is_file():
                    shutil.copy2(item, skill_dir / item.name)

        print(f"Copied skill files to: {skill_dir}")

    # Verify installation
    verify_file = skill_dir / "SKILL.md"
    if verify_file.exists():
        print(f"[OK] Successfully installed for {tool_info['name']}")
        return True
    else:
        print(f"[NG] Installation failed")
        return False


def uninstall_skill(cli_tool: str):
    """Uninstall skill from specific CLI tool"""
    if cli_tool not in CLI_TOOLS:
        print(f"Error: Unknown CLI tool '{cli_tool}'")
        return False

    tool_info = CLI_TOOLS[cli_tool]
    platform = get_platform()

    config_dir = expand_path(tool_info["config_dir"][platform])
    skill_dir = config_dir / "doc-studio"

    print(f"Uninstalling Doc Studio Skill from {tool_info['name']}...")

    if skill_dir.exists():
        if skill_dir.is_symlink():
            skill_dir.unlink()
        else:
            shutil.rmtree(skill_dir)
        print(f"[OK] Successfully uninstalled")
        return True
    else:
        print(f"Skill not installed")
        return False


def check_installation(cli_tool: str) -> bool:
    """Check if skill is installed"""
    if cli_tool not in CLI_TOOLS:
        return False

    tool_info = CLI_TOOLS[cli_tool]
    platform = get_platform()

    config_dir = expand_path(tool_info["config_dir"][platform])
    skill_dir = config_dir / "doc-studio"

    return skill_dir.exists()


def main():
    parser = argparse.ArgumentParser(description="Install Doc Studio Skill")
    parser.add_argument(
        "action",
        choices=["install", "uninstall", "status", "all"],
        help="Action to perform"
    )
    parser.add_argument(
        "--cli", "-c",
        choices=list(CLI_TOOLS.keys()),
        help="Specific CLI tool (default: all)"
    )
    parser.add_argument(
        "--symlink", "-s",
        action="store_true",
        help="Create symlink instead of copy (for development)"
    )

    args = parser.parse_args()

    if args.action == "install":
        if args.cli:
            success = install_skill(args.cli, args.symlink)
            sys.exit(0 if success else 1)
        else:
            # Install for all
            results = []
            for tool in CLI_TOOLS.keys():
                success = install_skill(tool, args.symlink)
                results.append((tool, success))
                print()

            print("Installation Summary:")
            for tool, success in results:
                status = "OK" if success else "NG"
                print(f"  {status} {CLI_TOOLS[tool]['name']}")

    elif args.action == "uninstall":
        if args.cli:
            success = uninstall_skill(args.cli)
            sys.exit(0 if success else 1)
        else:
            for tool in CLI_TOOLS.keys():
                uninstall_skill(tool)

    elif args.action == "status":
        print("Doc Studio Skill Installation Status:")
        print()
        for tool in CLI_TOOLS.keys():
            installed = check_installation(tool)
            status = "Installed" if installed else "Not installed"
            print(f"  {CLI_TOOLS[tool]['name']:<20} {status}")

    elif args.action == "all":
        # Show status and offer to install
        print("Current status:")
        for tool in CLI_TOOLS.keys():
            installed = check_installation(tool)
            status = "Installed" if installed else "Not installed"
            print(f"  {CLI_TOOLS[tool]['name']:<20} {status}")


if __name__ == "__main__":
    main()
