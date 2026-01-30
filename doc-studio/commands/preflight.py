#!/usr/bin/env python3
"""
Preflight command - Quality checks for documents
"""

import sys
import json
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.preflight import PreflightChecker


def main():
    parser = argparse.ArgumentParser(description="Run preflight checks")
    parser.add_argument("file", help="Document file to check")
    parser.add_argument("--checks", "-c", nargs="+",
                       choices=["fonts", "images", "links", "colors", "accessibility", "all"],
                       default=["all"], help="Checks to run")
    parser.add_argument("--fix", "-f", action="store_true",
                       help="Attempt to auto-fix issues")
    parser.add_argument("--json", "-j", action="store_true",
                       help="Output JSON format")

    args = parser.parse_args()

    checker = PreflightChecker()

    # Convert 'all' to specific checks
    checks = args.checks
    if "all" in checks:
        checks = list(checker.SUPPORTED_CHECKS.keys())

    result = checker.check(args.file, checks=checks, fix_issues=args.fix)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Preflight Check Results")
        print(f"======================")
        print(f"File: {args.file}")
        print(f"Success: {'Yes' if result['success'] else 'No'}")
        print(f"")
        print(f"Summary:")
        print(f"  Total: {result['summary']['total']}")
        print(f"  Errors: {result['summary']['errors']}")
        print(f"  Warnings: {result['summary']['warnings']}")
        print(f"  Info: {result['summary']['info']}")
        print(f"")

        if result['results']:
            print(f"Details:")
            for r in result['results']:
                print(f"  [{r['severity'].upper()}] {r['check_name']}: {r['message']}")
                if r.get('fix_suggestion'):
                    print(f"    Suggestion: {r['fix_suggestion']}")

    sys.exit(0 if result['success'] else 1)


if __name__ == "__main__":
    main()
