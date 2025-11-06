# MCP Workshop - Gmail Servers

Welcome to the MCP Workshop! This repository contains simple, educational examples of MCP (Model Context Protocol) servers for working with Gmail.

## What is MCP?

MCP (Model Context Protocol) allows AI assistants like Claude to interact with external tools and services. These servers expose tools that Claude can use to perform actions on your behalf.

## Workshop Structure

This workshop includes two progressively simple MCP servers:

### 01_send_email
A server that sends emails via Gmail SMTP.

**Tool:** `send_email` - Send an email to a recipient

[View Instructions →](./01_send_email/README.md)

### 02_retrieve_unread
A server that retrieves unread emails via Gmail IMAP and creates draft replies.

**Tools:**
- `get_unread_emails` - Get unread emails from your inbox
- `create_draft_replies` - Create draft replies with placeholder text

[View Instructions →](./02_retrieve_unread/README.md)

### 03_ai_draft_replies
A server that creates AI-powered draft replies using Claude to analyze conversation context.

**Tool:** `create_ai_draft_replies` - Create contextual draft replies using AI

[View Instructions →](./03_ai_draft_replies/README.md)


