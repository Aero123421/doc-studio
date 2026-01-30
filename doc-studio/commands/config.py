#!/usr/bin/env python3
"""
Config command - Manage skill configuration
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.config import ConfigManager


def main():
    parser = argparse.ArgumentParser(description="Manage configuration")
    parser.add_argument("action", choices=["get", "set", "reset", "show", "validate", "init"],
                       help="Configuration action")
    parser.add_argument("--key", "-k", help="Configuration key")
    parser.add_argument("--value", "-v", help="Configuration value")
    parser.add_argument("--global", "-g", dest="global_", action="store_true",
                       help="Use global config (not project)")

    args = parser.parse_args()

    if args.global_:
        config_manager = ConfigManager()
    else:
        # Try to find project config
        project_config = Path.cwd() / ".doc-studio"
        if project_config.exists():
            config_manager = ConfigManager(str(project_config))
        else:
            config_manager = ConfigManager()

    if args.action == "get":
        if not args.key:
            print("Error: --key required")
            sys.exit(1)

        value = config_manager.get(args.key)
        print(f"{args.key} = {value}")

    elif args.action == "set":
        if not args.key or args.value is None:
            print("Error: --key and --value required")
            sys.exit(1)

        config_manager.set(args.key, args.value)
        print(f"Set {args.key} = {args.value}")

    elif args.action == "reset":
        config_manager.reset()
        print("Configuration reset to defaults")

    elif args.action == "show":
        print(config_manager.show())

    elif args.action == "validate":
        errors = config_manager.validate()
        if errors:
            print("Validation errors:")
            for error in errors:
                print(f"  - {error}")
            sys.exit(1)
        else:
            print("Configuration is valid")

    elif args.action == "init":
        path = config_manager.create_project_config()
        print(f"Created project config: {path}")


if __name__ == "__main__":
    main()
