#!/usr/bin/env python3
"""
Simple MCP Server for sending emails via Gmail.
This is a minimal example for teaching MCP server basics.
"""

import os
import asyncio
import smtplib
from email.mime.text import MIMEText

from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio


# Step 1: Create the MCP server instance
app = Server("email-server")


# Step 2: Define what tools this server provides
@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="send_email",
            description="Send an email using Gmail",
            inputSchema={
                "type": "object",
                "properties": {
                    "to": {"type": "string", "description": "Recipient email"},
                    "subject": {"type": "string", "description": "Email subject"},
                    "body": {"type": "string", "description": "Email body"}
                },
                "required": ["to", "subject", "body"]
            }
        )
    ]


# Step 3: Implement the tool functionality
@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name != "send_email":
        raise ValueError(f"Unknown tool: {name}")

    # Get credentials from environment variables
    gmail_user = os.getenv("GMAIL_USER")
    gmail_password = os.getenv("GMAIL_APP_PASSWORD")

    if not gmail_user or not gmail_password:
        return [TextContent(
            type="text",
            text="Error: Set GMAIL_USER and GMAIL_APP_PASSWORD environment variables"
        )]

    try:
        # Create and send the email
        msg = MIMEText(arguments["body"])
        msg["From"] = gmail_user
        msg["To"] = arguments["to"]
        msg["Subject"] = arguments["subject"]

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(gmail_user, gmail_password)
            server.send_message(msg)

        return [TextContent(type="text", text=f"Email sent to {arguments['to']}")]

    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


# Step 4: Run the server
async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
