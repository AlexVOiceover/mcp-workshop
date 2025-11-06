#!/usr/bin/env python3
"""
Simple MCP Server for creating AI-powered draft replies to unread emails.
This is a minimal example for teaching MCP server basics.
"""

import os
import asyncio
import imaplib
import email
import sys
from email.mime.text import MIMEText
from anthropic import Anthropic

from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio


# Step 1: Create the MCP server instance
app = Server("ai-draft-replies-server")


# Step 2: Define what tools this server provides
@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="create_ai_draft_replies",
            description="Create AI-powered draft replies for all unread emails using conversation context",
            inputSchema={
                "type": "object",
                "properties": {
                    "context_limit": {"type": "number", "description": "Number of emails to include in thread context (default: 10)"}
                }
            }
        )
    ]


# Step 3: Implement the tool functionality
@app.call_tool()
async def create_ai_draft_replies(name: str, arguments: dict) -> list[TextContent]:
    if name != "create_ai_draft_replies":
        raise ValueError(f"Unknown tool: {name}")

    gmail_user = os.getenv("GMAIL_USER")
    gmail_password = os.getenv("GMAIL_APP_PASSWORD")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")

    if not gmail_user or not gmail_password:
        return [TextContent(type="text", text="Error: Set GMAIL_USER and GMAIL_APP_PASSWORD environment variables")]
    if not anthropic_key:
        return [TextContent(type="text", text="Error: Set ANTHROPIC_API_KEY environment variable")]

    context_limit = arguments.get("context_limit", 10)

    try:
        # Connect to Gmail
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(gmail_user, gmail_password)
        mail.select("inbox")

        # Search for unread emails
        _, messages = mail.search(None, "UNSEEN")
        email_ids = messages[0].split()
        if not email_ids:
            return [TextContent(type="text", text="No unread emails found.")]

        print(f"Found {len(email_ids)} unread emails. Processing...", file=sys.stderr, flush=True)

        # Initialize Claude client
        client = Anthropic(api_key=anthropic_key)
        drafts_created = []

        for i, email_id in enumerate(email_ids, 1):
            print(f"[{i}/{len(email_ids)}] Fetching email...", file=sys.stderr, flush=True)
            _, msg_data = mail.fetch(email_id, "(BODY.PEEK[])")
            unread_msg = email.message_from_bytes(msg_data[0][1])

            from_addr = unread_msg.get("From", "Unknown")
            subject = unread_msg.get("Subject", "No Subject")
            print(f"  From: {from_addr}", file=sys.stderr, flush=True)
            print(f"  Subject: {subject}", file=sys.stderr, flush=True)

            # Build conversation thread
            print(f"  Building conversation thread...", file=sys.stderr, flush=True)
            thread = get_conversation_thread(mail, unread_msg, context_limit)
            print(f"  Found {len(thread)} messages in thread", file=sys.stderr, flush=True)

            # Generate AI reply
            print(f"  Generating AI reply...", file=sys.stderr, flush=True)
            ai_reply = generate_ai_reply(client, thread, from_addr)
            print(f"  AI reply generated ({len(ai_reply)} chars)", file=sys.stderr, flush=True)

            # Create draft
            print(f"  Saving draft...", file=sys.stderr, flush=True)
            draft = MIMEText(ai_reply)
            draft["From"] = gmail_user
            draft["To"] = from_addr
            draft["Subject"] = f"Re: {subject}" if not subject.startswith("Re:") else subject

            # Thread the reply
            if unread_msg.get("Message-ID"):
                draft["In-Reply-To"] = unread_msg.get("Message-ID")
                draft["References"] = unread_msg.get("Message-ID")

            mail.append("[Gmail]/Drafts", "", None, draft.as_bytes())
            print(f"  ✓ Draft created!\n", file=sys.stderr, flush=True)
            drafts_created.append(f"AI draft reply to: {from_addr}")

        mail.close()
        mail.logout()

        return [TextContent(type="text", text=f"Created {len(drafts_created)} AI-powered draft replies:\n\n" + "\n".join(drafts_created))]

    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


def get_conversation_thread(mail, unread_msg, context_limit):
    """Get conversation thread using Message-ID headers."""
    thread = []

    # Get the unread message body
    body = extract_body(unread_msg)
    thread.append({
        "from": unread_msg.get("From", "Unknown"),
        "subject": unread_msg.get("Subject", "No Subject"),
        "body": body
    })

    # Try to find previous messages in thread using References header
    references = unread_msg.get("References", "")
    if references:
        # References contains all Message-IDs in the thread
        message_ids = references.split()[-context_limit:]  # Get last N message IDs

        for msg_id in message_ids:
            # Search for email by Message-ID
            _, result = mail.search(None, f'HEADER Message-ID "{msg_id}"')
            found_ids = result[0].split()

            if found_ids:
                _, msg_data = mail.fetch(found_ids[0], "(BODY.PEEK[])")
                msg = email.message_from_bytes(msg_data[0][1])
                body = extract_body(msg)
                thread.insert(0, {
                    "from": msg.get("From", "Unknown"),
                    "subject": msg.get("Subject", "No Subject"),
                    "body": body
                })

    return thread


def extract_body(msg):
    """Extract text body from email message."""
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                payload = part.get_payload(decode=True)
                if payload:
                    body = payload.decode(errors='replace')
                    break
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            body = payload.decode(errors='replace')
    return body.strip()


def generate_ai_reply(client, thread, recipient):
    """Generate AI reply using Claude."""
    # Build conversation context
    context = "Conversation thread:\n\n"
    for i, msg in enumerate(thread, 1):
        context += f"Email {i}:\nFrom: {msg['from']}\nSubject: {msg['subject']}\n\n{msg['body']}\n\n{'='*50}\n\n"

    # Call Claude API
    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": f"{context}\n\nBased on this email conversation, write a professional and helpful reply to {recipient}. Keep it concise and appropriate for the context."
        }]
    )

    return response.content[0].text


# Step 4: Run the server
async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
