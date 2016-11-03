from util import Command
from enum import Enum
import discord
import asyncio

cmdPrefix = '$'
player = {}

# User commands
async def ping(client: discord.Client, context: discord.Message, args):
    await client.send_message(context.channel, 'pong')

async def help(client: discord.Client, context: discord.Message, args):
    str = ''
    for cmd in commandList:
        if cmd != 'help':
            str += '$' + cmd + ': ' + commandList[cmd].about + '\n'
    await client.send_message(context.channel, str)

async def yt(client: discord.Client, context: discord.Message, args):
    class VChannelResponse(Enum):
        # Eu já estou pronto para ação!
        BOT_READY = 0
        # Eu preciso me conectar para atender o pedido.
        BOT_NEED_CONNECT = 1,
        # A pessoa que me chamou não está em um canal válido.
        USER_NOT_IN_CHANNEL = 2,
        # Eu já estou atendendo alguém.
        BOT_IN_USE = 3

    # subcommands
    def checkVChannel(user: discord.Member):
        vChannel = member.voice.voice_channel
        if vChannel is not None and not member.voice.is_afk:
            assert isinstance(vChannel, discord.Channel)
            # permissions = client.user.permissions_in(vChannel)
            # if not(permissions.connect or permissions.speak):
            #    await client.send_message(context.channel, 'Nope.jpg')
            #    return

            # Verifica se eu estou disponível para chamada
            if not client.is_voice_connected(context.server):
                return VChannelResponse.BOT_NEED_CONNECT
            else:
                tmp = client.voice_client_in(context.server)
                if vChannel != tmp:
                    return VChannelResponse.BOT_IN_USE
        else:
            return VChannelResponse.USER_NOT_IN_CHANNEL

    async def play(link):
        try:
            msg = await client.send_message(context.channel, "`Preparando...`")
            player[serverId] = await vClient.create_ytdl_player(
                link,
                after=lambda: ytPlayerCallBack(client, context.server)
            )
            player[serverId].start()
            await  client.edit_message(msg, "`Pronto!`")
        except BaseException as e:
            # Fazer o tratamento das execeções
            print(e)
        return

    async def add(link):
        pass

    async def list():
        pass

    async def next():
        pass

    async def clear():
        pass

    async def remove(index):
        pass

    async def showCurrent():
        if serverId in player.keys():
            if player[serverId].is_playing():
                str = 'Música atual: '
                str += player[serverId].title
            else:
                str = 'Não estou tocando nada no momento.'
        else:
            str = 'Não estou tocando nada no momento.'
        await client.send_message(context.channel, str)

    # end of sub commands definitions
    serverId = context.server.id
    if args is None:
        await showCurrent()
        return
    else:
        if isinstance(context.channel, discord.Channel):
            member = context.author
            vChannel = member.voice.voice_channel
            check = checkVChannel(member)
            if check == VChannelResponse.BOT_NEED_CONNECT:
                vClient = await client.join_voice_channel(vChannel)
                await play(args[0])
            elif check == VChannelResponse.BOT_READY:
                await play(args[0])
            elif check == VChannelResponse.BOT_IN_USE:
                await client.send_message(
                    context.channel,
                    "No momento, estou tocando música em outro canal!"
                )
            elif check == VChannelResponse.USER_NOT_IN_CHANNEL:
                await client.send_message(
                    context.channel,
                    "Você precisa estar em um canal de \
                    voz para usar este comando."
                )

async def stop(client: discord.Client, context: discord.Message, args):
    serverId = context.server.id
    if serverId in player.keys() and player[serverId] is None:
        player[serverId].stop()
        player[serverId] = None

    vClient = client.voice_client_in(context.server)
    await vClient.disconnect()


def ytPlayerCallBack(client: discord.Client, server: discord.Server):
    serverId = server.id
    if serverId in player.keys() and player[serverId] is not None:
        player[serverId] = None

    vClient = client.voice_client_in(server)
    fut = asyncio.run_coroutine_threadsafe(vClient.disconnect(), client.loop)
    try:
        fut.result()
    except:
        pass

# Admin commands
async def shutdown(client: discord.Client, context: discord.Message, args):
    await client.close()

# "$ping - Verifica se eu estou recebendo comandos.  :)\n"
# "$gg - GG!\n"+
# "$yt [link] - toca o áudio de um link do youtube,
# interropendo qualquer execução.\n"
# "$ytq - Mostra o que está tocando.\n"+
# "$ytq [link] - Enfilera a música na playlist atual, caso não tenha nenhuma
# playlist, inicia uma.\n"
# "$ytq list - Mostra o que está tocando, e as músicas enfilerada.\n"
# "$ytq next - Pula para a próxima música da lista.\n"
# "$ytq remove [index] - Remove a música do indice informado.\n"
# "$stop - Para de tocar tudo.
commandList = {
    'help': Command('Ajuda', help),
    'ping': Command('Verifica se eu estou recebendo comandos.  :)', ping),
    'yt': Command('$yt <link> - toca o áudio de um link do youtube, \
        interropendo qualquer execução.', yt),
    'stop': Command('Para a reprodução da música.', stop)
}

adminCommandList = {
    'shutdown': Command('Desativa o bot', shutdown)
}
