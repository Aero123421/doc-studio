#!/usr/bin/env python3
"""
Generate command - Main entry point for document generation
"""

import sys
import json
import argparse
from pathlib import Path

# Add core to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.generator import DocumentGenerator, GenerationConfig, DocumentFormat, EngineType
from core.config import ConfigManager


def main():
    parser = argparse.ArgumentParser(description="Generate document")
    parser.add_argument("format", choices=["pdf", "pptx", "docx", "xlsx", "html"],
                       help="Output format")
    parser.add_argument("template", help="Template name")
    parser.add_argument("output", help="Output filename")
    parser.add_argument("--data", "-d", type=str,
                       help="JSON data for template (inline JSON string)")
    parser.add_argument("--data-file", type=str,
                       help="JSON data for template (file path)")
    parser.add_argument("--engine", "-e",
                       choices=["auto", "playwright", "reportlab", "weasyprint",
                               "fpdf2", "python-pptx", "python-docx", "xlsxwriter"],
                       default="auto", help="Generation engine")
    parser.add_argument("--language", "-l", default="ja", help="Document language")
    parser.add_argument("--color-scheme", "-c", default="business", help="Color scheme")
    parser.add_argument("--page-size", "-p", default="A4", help="Page size")
    parser.add_argument("--config", help="Config file path")

    args = parser.parse_args()

    try:
        # Parse data
        if args.data and args.data_file:
            print("Error: Use either --data or --data-file (not both)")
            sys.exit(1)

        if args.data_file:
            data_path = Path(args.data_file)
            if not data_path.exists():
                print(f"Error: Data file not found: {data_path}")
                sys.exit(1)
            data = json.loads(data_path.read_text(encoding="utf-8"))
        elif args.data:
            try:
                data = json.loads(args.data)
            except json.JSONDecodeError:
                print(f"Error: Invalid JSON data: {args.data}")
                sys.exit(1)
        else:
            data = {}

        # Load config
        config_manager = ConfigManager(args.config)
        config_manager.load()

        # Create generator
        generator = DocumentGenerator()

        # Determine engine
        engine = None if args.engine == "auto" else EngineType(args.engine)

        # Resolve output path
        output_path = Path(args.output)
        if not output_path.suffix:
            suffix_map = {
                "pdf": ".pdf",
                "pptx": ".pptx",
                "docx": ".docx",
                "xlsx": ".xlsx",
                "html": ".html",
            }
            output_path = output_path.with_suffix(suffix_map.get(args.format, ""))

        # If only a filename was given, place it under configured output dir.
        if output_path.parent == Path("."):
            out_dir = config_manager.get_output_path(args.format)
            output_path = out_dir / output_path.name

        # Create generation config
        gen_config = GenerationConfig(
            format=DocumentFormat(args.format),
            template=args.template,
            output_path=str(output_path),
            data=data,
            engine=engine,
            language=args.language,
            color_scheme=args.color_scheme,
            page_size=args.page_size,
        )

        # Generate
        output_file = generator.generate(gen_config)
        print(f"Generated: {output_file}")

        # Run preflight if enabled
        if config_manager.is_preflight_enabled():
            from core.preflight import PreflightChecker
            checker = PreflightChecker()
            result = checker.check(output_file)

            if result["summary"]["warnings"] > 0:
                print(f"Warnings: {result['summary']['warnings']}")
            if result["summary"]["errors"] > 0:
                print(f"Errors: {result['summary']['errors']}")
                sys.exit(1)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
