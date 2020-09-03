"""Plugin to log all admin reports."""
from html import escape

import re
from telethon import events
from telethon.errors import MessageIdInvalidError
from telethon.events import NewMessage
from telethon.tl.custom import Message
from telethon.tl.types import Channel, User
from telethon.utils import get_display_name

from utils.client import Client

__version__ = '0.1.0'

from utils.pluginmgr import k

log_message_template = '''
A user is requesting admin assistance in a group.
Group: <a href="https://t.me/{chat_link}">{chat_title}</a> (#chat{chat_id})
Reporter: <a href="tg://user?id={reporter_id}">{reporter_name}</a> (#id{reporter_id})
Remark: <code>{remark}</code>
'''

log_reply_template = '''
Reportee: <a href="tg://user?id={reportee_id}">{reportee_name}</a> (#id{reportee_id})
<a href="https://t.me/c/{log_message}">View Reported Message</a>
'''


@k.event(events.MessageEdited(outgoing=False))
@k.event(events.NewMessage(outgoing=False), name='reppelports')
async def admin_reports(event: NewMessage.Event) -> None:
    if not event.is_group:
        return

    msg: Message = event.message
    client: Client = event.client
    chat: Channel = await event.get_chat()
    user: User = await event.get_sender()
    reply: Message = await event.get_reply_message()
    if chat.id == 1187874753:
        return

    if chat.id == -1001187874753:
        return

    # pattern = r'[/!]report|[\s\S]*@admins?'

    finder = re.compile(r'[/!]report|[\s\S]*@admins?')

    if not finder.search(msg.text):
        return

    logged_reply = None
    if reply:
        try:
            logged_reply = await reply.forward_to(-1001187874753)
        except MessageIdInvalidError:
            pass

    chat_link = getattr(chat, 'username', None) or f'c/{chat.id}'
    log_messsage = log_message_template.format(chat_link=f'{chat_link}/{event.id}',
                                               chat_title=escape(get_display_name(chat)),
                                               chat_id=chat.id, reporter_id=user.id,
                                               reporter_name=escape(get_display_name(user)),
                                               remark=event.text)

    if logged_reply:
        logged_reply_chat: Channel = await logged_reply.get_chat()
        reply_user: User = await reply.get_sender()
        logged_link = f'{logged_reply_chat.id}/{logged_reply.id}'
        log_messsage += log_reply_template.format(reportee_id=reply_user.id,
                                                  reportee_name=escape(
                                                      get_display_name(reply_user)),
                                                  log_message=logged_link)

    await client.send_message(-1001187874753, log_messsage,
                              parse_mode='html', link_preview=False)
