"""Generate Claude Desktop MCP configuration for Pulsar."""

import json
import sys
from pathlib import Path


def generate_config() -> dict:
    """Generate MCP server configuration for claude_desktop_config.json."""
    # Find the Pulsar source directory
    src_dir = Path(__file__).parent.parent
    python_exe = sys.executable

    config = {
        "mcpServers": {
            "pulsar": {
                "command": python_exe,
                "args": ["-m", "mcp_impl.server"],
                "cwd": str(src_dir),
                "env": {
                    "PYTHONPATH": str(src_dir),
                },
            }
        }
    }

    return config


def print_config():
    """Print the configuration for copy-paste."""
    config = generate_config()

    print("\n" + "=" * 60)
    print("Pulsar MCP Configuration")
    print("=" * 60)
    print("\nAdd this to your claude_desktop_config.json:\n")
    print(json.dumps(config, indent=2))
    print("\n" + "=" * 60)
    print("\nFull claude_desktop_config.json path:")
    print("  Windows: %APPDATA%\\Claude\\claude_desktop_config.json")
    print("  macOS: ~/Library/Application Support/Claude/claude_desktop_config.json")
    print("  Linux: ~/.config/Claude/claude_desktop_config.json")
    print("\n" + "=" * 60)

    # Print available tools
    from mcp_impl.tools import get_tool_definitions
    tools = get_tool_definitions()

    print("\nAvailable MCP Tools:")
    print("-" * 40)
    for tool in tools:
        print(f"  - {tool['name']}: {tool['description']}")
    print("\n")


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Generate Pulsar MCP configuration")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw JSON only (for piping)",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="Write config to file",
    )

    args = parser.parse_args()

    config = generate_config()

    if args.json:
        print(json.dumps(config, indent=2))
    elif args.output:
        output_path = Path(args.output)
        if output_path.exists():
            # Merge with existing config
            existing = json.loads(output_path.read_text())
            if "mcpServers" not in existing:
                existing["mcpServers"] = {}
            existing["mcpServers"].update(config["mcpServers"])
            config = existing

        output_path.write_text(json.dumps(config, indent=2))
        print(f"Configuration written to {output_path}")
    else:
        print_config()


if __name__ == "__main__":
    main()
