import os
import json
from typing import Any

from dotenv import load_dotenv
from imap_tools import MailBox, AND
from langchain_core.tools import tool

load_dotenv()

IMAP_HOST = os.getenv('IMAP_HOST')
IMAP_USER = os.getenv('IMAP_USER')
PASSWORD = os.getenv('IMAP_PASSWORD')
IMAP_FOLDER = os.getenv('IMAP_FOLDER', 'INBOX')
IMAP_PORT = int(os.getenv('IMAP_PORT', 993))

def connect():
    mailbox = MailBox(IMAP_HOST, port=IMAP_PORT)
    mailbox.login(IMAP_USER, PASSWORD)
    mailbox.folder.set(IMAP_FOLDER)
    return mailbox


@tool
def list_unread_emails():
    """Return a bullet list of every UNREAD message's UID, subject, date and sender"""

    print('List Unread Emails Tool Called')

    with connect() as mb:
        unread = list(mb.fetch(criteria=AND(seen=False), headers_only=True, mark_seen=False, limit=3, reverse=True))

    if not unread:
        return 'You have no unread messages.'

    unread = unread[:3]

    response = json.dumps([
        {
            'uid': mail.uid,
            'date': mail.date.astimezone().strftime('%Y-%m-%d %H:%M'),
            'subject': mail.subject,
            'sender': mail.from_
        } for mail in unread
    ])

    return response


def get_summarize_tool(raw_llm):
    @tool
    def summarize_email(uid: Any):
        """Summarize a single e-mail given it's IMAP UID. Return a short summary of the e-mails content / body in plain text."""
        print('Summarize E-Mail Tool Called on', uid)

        with connect() as mb:
            mail = next(mb.fetch(AND(uid=uid), mark_seen=False), None)

            if not mail:
                return f'Could not summarize e-mail with UID {uid}.'

            prompt = (
                "Summarize this e-mail concisely:\n\n"
                f"Subject: {mail.subject}\n"
                f"Sender: {mail.from_}\n"
                f"Date: {mail.date}\n\n"
                f"{mail.text or mail.html}"
            )

            return raw_llm.invoke(prompt).content

    return summarize_email