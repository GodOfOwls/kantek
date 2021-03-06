import logging
from typing import List, Dict

from kantex.md import *
from spamwatch.types import Permission
from telethon.tl.patched import Message
from telethon.tl.types import User

from utils.client import Client
from utils.pluginmgr import k, Command

tlog = logging.getLogger('kantek-channel-log')


# TODO: Make this nice, this is just a skeleton so I have an easy way of creating tokens,
#  preferably clean this up at some point
@k.command('ebgwatch', 'ebg', document=False)
async def sw(client: Client, args: List, kwargs: Dict, event: Command) -> None:
    """Create SpamWatch Tokens"""
    if not client.sw:
        return
    subcommand, *args = args

    result = ''

    if client.sw.permission != Permission.Root:
        await client.respond(event, KanTeXDocument(Section('Insufficient Permission',
                                                           'Root Permission required.')))
    if subcommand == 'token':
        result = await _token(event, client, args, kwargs)
    if result:
        await client.respond(event, result)


async def _token(event, client, args, keyword_args):
    command, *args = args
    msg: Message = event.message
    id = [uid for uid in args if isinstance(uid, int)]
    if not id:
        if msg.is_reply:
            reply_message: Message = await msg.get_reply_message()
            userid = reply_message.from_id
        else:
            return KanTeXDocument(Section('Missing Argument',
                                          'A ID is required.'))
    else:
        id = id[0]
    if command == 'create':
        from spamwatch.types import _permission_map  # pylint: disable = C0415
        permission = keyword_args.get('permission', 'User')
        permission = _permission_map.get(permission)
        token = client.sw.create_token(id, permission)
        return KanTeXDocument(Section('EBG-Watch Token',
                                      KeyValueItem('ID', Code(token.id)),
                                      KeyValueItem('User', Code(token.userid)),
                                      KeyValueItem('Permission', token.permission.name),
                                      KeyValueItem('Token', Code(token.token))),
                              Section('Links',
                                      KeyValueItem('Endpoint', client.sw_url.split('://')[-1]),
                                      KeyValueItem('Documentation', 'docs.spamwat.ch')))

    if command == 'revoke':
        token = client.sw.delete_token(id)
        return KanTeXDocument(Section('EBG-Watch Token',
                                      KeyValueItem('ID', Code(id)),
                                      KeyValueItem('Status', Code('RETIRED'))))

    if command == 'info':
        token = client.sw.get_token(id)
        try:
            user: User = await client.get_entity(token.userid)
            username = user.username
        except:
            username = 'None'
            pass
        active: bool = not token.retired
        return KanTeXDocument(Section('EBG-Watch Token',
                                      KeyValueItem('ID', Code(token.id)),
                                      KeyValueItem('User', Code(token.userid)),
                                      KeyValueItem('Permission', token.permission.name),
                                      KeyValueItem('Active', Code(active)),
                                      KeyValueItem('Username', Code(username))))
