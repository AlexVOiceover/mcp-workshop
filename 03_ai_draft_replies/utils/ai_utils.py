"""AI reply generation utilities."""


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
