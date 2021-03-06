import routeros
from kantex.md import *

from utils.client import Client
from utils.config import Config
from utils.pluginmgr import k


@k.command('mikrotik', document=False)
async def mikrotik() -> None:
    """Random convenience functions for the bot developers.

    These are unsupported. Don't try to get support for them.
    """
    pass


@mikrotik.subcommand()
async def get_addr(client: Client, args, kwargs) -> KanTeXDocument:
    config = Config()
    try:
        router = routeros.login(config.mikrotik_user, config.mikrotik_passwd, args[0])
        res = router('/ip/address/print')

        sec = Section('Addressen')
        for i in res:
            sec.append(KeyValueItem(i['interface'], Code(i['address'])))

        return KanTeXDocument(sec)
    except:
        pass

@mikrotik.subcommand()
async def get_route(client: Client, args, kwargs) -> KanTeXDocument:
    config = Config()
    try:
        router = routeros.login(config.mikrotik_user, config.mikrotik_passwd, args[0])
        res = router('/ip/route/print')

        sec = Section('Routen')
        for i in res:
            sec.append(KeyValueItem(i['dst-address'], Code(i['gateway-status'].replace('reachable', ''))))

        return KanTeXDocument(sec)
    except:
        pass

@mikrotik.subcommand()
async def firewall(client: Client, args, kwargs) -> KanTeXDocument:
    config = Config()
    # noinspection PyCallByClass
    try:
        router = routeros.login(config.mikrotik_user, config.mikrotik_passwd, args[0])

        res = router('/ip/firewall/filter/add',
                     **{'action': args[1], 'protocol': args[2], 'chain': 'forward', 'src-address': args[3]})

        sec = Section('OK')
        sec.append(KeyValueItem('Returncode', Code(res)))
        return KanTeXDocument(sec)
    except:
        pass
