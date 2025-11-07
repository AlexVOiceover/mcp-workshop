#!/usr/bin/env python3
"""
Simple MCP Server for reading unread emails from Gmail.
This is a minimal example for teaching MCP server basics.
"""

import os
import asyncio
import imaplib
import email
from email.mime.text import MIMEText

from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio


# Step 1: Create the MCP server instance
app = Server("inbox-server")


# Step 2: Define what tools this server provides
@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="get_unread_emails",
            description="Get all unread emails from Gmail inbox",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {"type": "number", "description": "Max emails (default: 10)"}
                }
            }
        ),
        Tool(
            name="create_draft_replies",
            description="Create draft replies for all unread emails",
            inputSchema={"type": "object", "properties": {}}
        )
    ]


# Step 3: Implement the tool functionality
@app.call_tool()
async def get_unread_emails(name: str, arguments: dict) -> list[TextContent]:
    if name != "get_unread_emails":
        raise ValueError(f"Unknown tool: {name}")

    gmail_user = os.getenv("GMAIL_USER")
    gmail_password = os.getenv("GMAIL_APP_PASSWORD")
    if not gmail_user or not gmail_password:
        return [TextContent(type="text", text="Error: Set GMAIL_USER and GMAIL_APP_PASSWORD environment variables")]

    limit = arguments.get("limit", 10)

    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(gmail_user, gmail_password)
        mail.select("inbox")

        # Search for unread emails
        _, messages = mail.search(None, "UNSEEN")
        email_ids = messages[0].split()
        if not email_ids:
            return [TextContent(type="text", text="No unread emails found.")]

        # Get the most recent emails up to limit
        email_ids = email_ids[-limit:]
        unread_emails = []

        for email_id in reversed(email_ids):
            _, msg_data = mail.fetch(email_id, "(BODY.PEEK[])")
            msg = email.message_from_bytes(msg_data[0][1])

            # Get email body
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        payload = part.get_payload(decode=True)
                        if payload:
                            body = payload.decode(errors='replace')[:200]
                        break
            else:
                payload = msg.get_payload(decode=True)
                if payload:
                    body = payload.decode(errors='replace')[:200]

            unread_emails.append(
                f"From: {msg.get('From', 'Unknown')}\n"
                f"Subject: {msg.get('Subject', 'No Subject')}\n\n{body}...\n{'-'*50}"
            )

        mail.close()
        mail.logout()

        return [TextContent(type="text", text=f"Found {len(unread_emails)} unread email(s):\n\n" + "\n\n".join(unread_emails))]

    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


@app.call_tool()
async def create_draft_replies(name: str, arguments: dict) -> list[TextContent]:
    if name != "create_draft_replies":
        raise ValueError(f"Unknown tool: {name}")

    gmail_user = os.getenv("GMAIL_USER")
    gmail_password = os.getenv("GMAIL_APP_PASSWORD")
    if not gmail_user or not gmail_password:
        return [TextContent(type="text", text="Error: Set GMAIL_USER and GMAIL_APP_PASSWORD environment variables")]

    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(gmail_user, gmail_password)
        mail.select("inbox")

        # Search for unread emails
        _, messages = mail.search(None, "UNSEEN")
        email_ids = messages[0].split()
        if not email_ids:
            return [TextContent(type="text", text="No unread emails found.")]

        drafts_created = []

        for email_id in email_ids:
            _, msg_data = mail.fetch(email_id, "(BODY.PEEK[])")
            msg = email.message_from_bytes(msg_data[0][1])

            from_addr = msg.get("From", "Unknown")
            subject = msg.get("Subject", "No Subject")

            # Create draft reply
            draft = MIMEText(f"[PLACEHOLDER: Edit before sending]\n\nThank you for your email.")
            draft["From"] = gmail_user
            draft["To"] = from_addr
            draft["Subject"] = f"Re: {subject}" if not subject.startswith("Re:") else subject

            # Thread the reply
            if msg.get("Message-ID"):
                draft["In-Reply-To"] = msg.get("Message-ID")
                draft["References"] = msg.get("Message-ID")

            mail.append("[Gmail]/Drafts", "", None, draft.as_bytes())
            drafts_created.append(f"Draft reply to: {from_addr}")

        mail.close()
        mail.logout()

        return [TextContent(type="text", text=f"Created {len(drafts_created)} draft replies:\n\n" + "\n".join(drafts_created))]

    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


# Step 4: Run the server
async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
