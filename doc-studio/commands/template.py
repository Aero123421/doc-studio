#!/usr/bin/env python3
"""
Template command - Manage document templates
"""

import sys
import json
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.template import TemplateManager


def main():
    parser = argparse.ArgumentParser(description="Manage templates")
    parser.add_argument("action", choices=["list", "info", "create", "edit", "export", "import"],
                       help="Action to perform")
    parser.add_argument("--name", "-n", help="Template name")
    parser.add_argument("--format", "-f", choices=["pdf", "pptx", "docx", "xlsx", "html"],
                       help="Filter by format")
    parser.add_argument("--display-name", help="Display name (for create)")
    parser.add_argument("--description", "-d", help="Description (for create)")
    parser.add_argument("--base", "-b", help="Base template (for create)")
    parser.add_argument("--output", "-o", help="Output path (for export)")
    parser.add_argument("--input", "-i", help="Input file (for import)")

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
