from .commands_base import CMD_INDEXER
from .commands_base import commandList
from .commands_base import adminCommandList
from .commands import *
from .playlist import PlayList
from .playlist import serverPlaylists
from .playlist import playListTask
import random
import discord
import sys
import logging
import asyncio
import time
import json

client = discord.Client()
auth = None
with open('config/auth.json') as data_file:
    auth = json.load(data_file)

logger = logging.getLogger('discord')
assert isinstance(logger, logging.Logger)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='discord.log',
    encoding='utf-8', mode='w'
)
handler.setFormatter(
    logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s')
)
logger.addHandler(handler)

cmdPrefix = '$'
heat = 0

if not discord.opus.is_loaded():
    discord.opus.load_opus('opus')


@client.event
async def on_message(message: discord.Message) -> None:
    global heat
    if message.author == client.user:
        return

    # Meme area
    if message.content == '(╯°□°）╯︵ ┻━┻':
        heat += 0.1
        eg = (random.random() * heat >= 0.9)
        str = ''
        if not eg:
            str += '┬─┬ノ(° -°ノ)'
        else:
            heat = 0
            str += 'ノ┬─┬ノ ︵ ( \\o°o)\\'
        await client.send_message(message.channel, str)
        return
    else:
        heat = 0
    # the end

    content = message.content.strip()
    if content[0] != cmdPrefix:
        return

    # if message.server is None or message.server.id != auth['consoleServer']:
    #     await client.send_message(
    #         message.channel,
    #         '(ง •̀\_•́)ง Em breve, serei um bot funcional! (ง •̀\_•́)ง'
    #     )
    #     return

    content = content[1:].split(' ')
    cmd = content[0]

    if (len(content) > 1):
        args = content[1:]
    else:
        args = None

    if cmd in commandList:
        # Verifica se o comando veio com um sub-comando
        subcmds = commandList[cmd][CMD_INDEXER.SUBCOMMANDS]
        if args is not None and args[0] in subcmds:
            f = args[0]
            if (len(args) > 1):
                args = args[1:]
            else:
                args = None
            await subcmds[f][CMD_INDEXER.FUNCTION](client, message, args)
        else:
            await commandList[cmd][CMD_INDEXER.FUNCTION](client, message, args)

    elif (
        cmd in adminCommandList and
        message.server is not None and
        message.server.id == auth['consoleServer']
    ):
        subcmds = adminCommandList[cmd][CMD_INDEXER.SUBCOMMANDS]
        if args is not None and args[0] in subcmds:
            f = args[0]
            if (len(args) > 1):
                args = args[1:]
            else:
                args = None
            await subcmds[f][CMD_INDEXER.FUNCTION](client, message, args)
        else:
            await adminCommandList[cmd][CMD_INDEXER.FUNCTION](
                client,
                message,
                args
            )
    else:
        await client.send_message(message.channel, 'Comando não encontrado')


@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name=auth['state']))
    print('Logged in as')
    print(client.user.name)
    print('\nConnected to servers:')
    for server in client.servers:
        serverPlaylists[server.id] = PlayList(server)
        print(server.name)
    print('------')


client.loop.create_task(playListTask(client))
client.run(auth['discordToken'])

# Clean
logger.removeHandler(handler)
logger = None
client = None
