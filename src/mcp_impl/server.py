"""MCP server implementation using the official SDK."""

import asyncio
import json
import logging
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from core.config import Config
from core.events import EventBus
from serial_comm.manager import SerialManager
from mcp_impl.tools import MCPTools, get_tool_definitions

logger = logging.getLogger(__name__)


async def serve() -> None:
    """Run the MCP server."""
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    logger.info("Starting Pulsar MCP server...")

    # Initialize components
    config = Config()
    events = EventBus()
    await events.start()

    serial_manager = SerialManager(events, config)
    await serial_manager.start()

    tools = MCPTools(serial_manager)

    # Create MCP server
    server = Server("pulsar")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """List available tools."""
        definitions = get_tool_definitions()
        return [
            Tool(
                name=d["name"],
                description=d["description"],
                inputSchema=d["inputSchema"],
            )
            for d in definitions
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
        """Call a tool with the given arguments."""
        logger.debug("Tool call: %s with %s", name, arguments)

        try:
            # Get tool method
            method = getattr(tools, name, None)
            if not method:
                return [TextContent(
                    type="text",
                    text=json.dumps({"error": f"Unknown tool: {name}"}),
                )]

            # Call the tool
            result = await method(**arguments)

            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2),
            )]

        except Exception as e:
            logger.exception("Tool error: %s", e)
            return [TextContent(
                type="text",
                text=json.dumps({"error": str(e)}),
            )]

    # Run the server
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())

    # Cleanup
    await serial_manager.stop()
    await events.stop()


def main() -> None:
    """Entry point for MCP server."""
    asyncio.run(serve())


if __name__ == "__main__":
    main()
