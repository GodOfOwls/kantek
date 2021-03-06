import json
import logging
import subprocess
import time
from typing import Dict

from kantex.md import *

from utils.client import Client
from utils.pluginmgr import k, Command

tlog = logging.getLogger('kantek-channel-log')


@k.command('system')
async def system(client: Client, event: Command) -> KanTeXDocument:
    """Collect stats about the system where kantek is running

    Examples:
        {cmd}
    """
    waiting_message = await client.respond(event, 'Collecting stats. This might take a while.')
    start_time = time.time()

    try:
        fetch = subprocess.run(['owlfetch', '--json'], stdout=subprocess.PIPE)

    except FileNotFoundError:
        response = KanTeXDocument(Section(Bold('Neofetch Version 5 or higher Binary couldnt be found. please get it '
                                               'from https://github.com/dylanaraps/neofetch/releases '
                                               'and drop it (the binary file named neofetch) in /usr/local/bin and '
                                               'rename it to owlfetch, '
                                               'also make sure to set the rights so it can be executed.')))
        return response

    system_info: Dict = json.loads(fetch.stdout)
    stop_time = time.time() - start_time


    response = KanTeXDocument(

        Section(Bold(f'Stats for Kanteksystem'),

                SubSection('Hardware',
                           KeyValueItem('Host', system_info['Host']),
                           KeyValueItem('CPU', system_info['CPU']),
                           KeyValueItem('GPU', system_info.get('GPU', 'None')),
                           KeyValueItem('Memory', system_info['Memory']),
                           KeyValueItem('Uptime', system_info['Uptime'])),
                SubSection('Software',
                           KeyValueItem('OS', system_info['OS']),
                           KeyValueItem('Kernel', system_info['Kernel']),
                           KeyValueItem('Terminal', system_info.get('Terminal', 'None')),
                           KeyValueItem('Shell', system_info['Shell']),
                           KeyValueItem('Packages', system_info['Packages'])),

                Italic(f'Took {stop_time:.02f}s')))

    await waiting_message.delete()
    return response
