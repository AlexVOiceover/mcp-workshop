"""Email processing utilities."""

import email


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
