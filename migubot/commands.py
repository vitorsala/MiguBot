from .commands_base import commandList
from .commands_base import Command
from .commands_base import SubCommand
from .commands_base import CMD_INDEXER
from .utils import checkVChannel
from .utils import VChannelResponse
from .playlist import serverPlaylists
import discord


@Command()
async def help(client: discord.Client, context: discord.Message, args):
    str = '```\n'
    for cmd in commandList:
        if cmd != 'help':
            about = commandList[cmd][CMD_INDEXER.ABOUT]
            if about is not None:
                str += '$' + cmd + ': ' + about + '\n'
            if len(commandList[cmd][CMD_INDEXER.SUBCOMMANDS]) > 0:
                for subcmd in commandList[cmd][CMD_INDEXER.SUBCOMMANDS]:
                    item = commandList[cmd][CMD_INDEXER.SUBCOMMANDS][subcmd]
                    about = item[CMD_INDEXER.ABOUT]
                    if about is not None:
                        str += '$' + cmd + ' ' + subcmd + ': ' + about + '\n'
    str += '```'
    await client.send_message(context.channel, str)


@Command(about='Verifica se eu estou disponível  :)')
async def ping(client: discord.Client, context: discord.Message, args):
    await client.send_message(context.channel, 'pong')


@Command(about='Commando do player')
async def yt(client: discord.Client, context: discord.Message, args):
    # end of sub commands definitions
    serverId = context.server.id
    pl = serverPlaylists[serverId]
    if pl.player is not None and pl.player.is_playing():
        str = 'Música atual: '
        str += pl.player.title
    else:
        str = 'Não estou tocando nada no momento.'
    await client.send_message(context.channel, str)
    return


@SubCommand(parent='yt', about='Toca a música dado um link do youtube')
async def play(client: discord.Client, context: discord.Message, args):
    if isinstance(context.channel, discord.Channel) and args is not None:
        serverId = context.server.id
        member = context.author
        vChannel = member.voice.voice_channel
        check = checkVChannel(client, member, context.server)
        pl = serverPlaylists[serverId]
        if check == VChannelResponse.BOT_NEED_CONNECT:
            vChannel = await client.join_voice_channel(vChannel)
            await pl.play(client, args[0],
                          vChannel, context.channel)
        elif check == VChannelResponse.BOT_READY:
            await pl.play(client, args[0],
                          vChannel, context.channel)
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


@SubCommand(parent='yt', about='Adiciona uma música na fila')
async def add(client: discord.Client, context: discord.Message, args):
    if args is not None:
        serverId = context.server.id
        pl = serverPlaylists[serverId]
        if pl.player is None:
            await client.send_message(
                context.channel,
                "Não há nenhuma playlist ativa, use `$yt play <link>` para iniciar uma nova."
            )
            return
        else:
            serverId = context.server.id
            pl = serverPlaylists[serverId]
            pl.addMusic(args[0])
            await client.send_message(
                context.channel,
                "Link adicionado na fila."
            )


@Command(about='Faz parar tudo!')
async def stop(client: discord.Client, context: discord.Message, args):
    serverId = context.server.id
    pl = serverPlaylists[serverId]
    vClient = client.voice_client_in(context.server)
    await pl.stop()
    await vClient.disconnect()


@Command(about='BATATA!')
async def batata(client: discord.Client, context: discord.Message, args):
    await client.send_message(context.channel,
                              'http://i.imgur.com/jzYecG5.jpg')
# Admin commands


@Command(about='Desliga o Bot', adminOnly=True)
async def shutdown(client: discord.Client, context: discord.Message, args):
    await client.close()
