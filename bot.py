from commands import *
from util import YTQueue
import discord
import util
import commands
import sys
import logging
import asyncio
import time
import json

with open('auth.json') as data_file:
    auth = json.load(data_file)


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='discord.log',
    encoding='utf-8', mode='w'
)
handler.setFormatter(
    logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s')
)
logger.addHandler(handler)
consoleLoop = asyncio.new_event_loop()
client = discord.Client()
cmdPrefix = '$'

threads = []


@client.event
async def on_message(message: discord.Message) -> None:
    if message.author == client.user:
        return

    content = message.content.strip()
    if content[0] != cmdPrefix:
        return

    if message.server is None or message.server.id != auth['consoleServer']:
        await client.send_message(
            message.channel,
            '(ง •̀\_•́)ง Em breve, serei um bot funcional! (ง •̀\_•́)ง'
        )
        return

    content = content[1:].split(' ')
    cmd = content[0]

    if (len(content) > 1):
        args = content[1:]
    else:
        args = None

    if cmd in commandList:
        await commandList[cmd].function(client, message, args)
    elif (
        cmd in adminCommandList and
        message.server is not None and
        message.server.id == auth['consoleServer']
    ):
        await adminCommandList[cmd].function(client, message, args)
    else:
        await client.send_message(message.channel, 'Comando não encontrado')


@client.event
async def on_ready():
    util.ytQueue = YTQueue(client)
    await client.change_presence(game=discord.Game(name=auth['state']))
    print('Logged in as')
    print(client.user.name)
    print('\nConnected to servers:')
    for server in client.servers:
        print(server.name)
    print('------')


# async def console():
#     await client.wait_until_ready()
#     while not client.is_closed:
#         ctx = input('MiguBot > ').split(' ')
#         cmd = ctx[0]
#         if len(ctx) > 1:
#             args = ctx[1:]
#         else:
#             args = None
#         if cmd in adminCommandList:
#             adminCommandList[cmd](client, None, args)

if not discord.opus.is_loaded():
    # the 'opus' library here is opus.dll on windows
    # or libopus.so on linux in the current directory
    # you should replace this with the location the
    # opus library is located in and with the proper filename.
    # note that on windows this DLL is automatically provided for you
    discord.opus.load_opus('opus')

client.run(auth['discordToken'])
