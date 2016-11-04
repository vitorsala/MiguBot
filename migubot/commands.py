from .commands_base import commandList
from .commands_base import Command
from .commands_base import SubCommand
from .commands_base import CMD_INDEXER
from .utils import checkVChannel
from .utils import VChannelResponse
from .utils import play
import discord

cmdPrefix = '$'
player = {}


@Command()
async def help(client: discord.Client, context: discord.Message, args):
    str = ''
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
    await client.send_message(context.channel, str)


@Command(about='Verifica se eu estou disponível  :)')
async def ping(client: discord.Client, context: discord.Message, args):
    await client.send_message(context.channel, 'pong')


@Command(about='Commando do player')
async def yt(client: discord.Client, context: discord.Message, args):
    # end of sub commands definitions
    serverId = context.server.id
    if args is None:
        if serverId in player.keys():
            if player[serverId].is_playing():
                str = 'Música atual: '
                str += player[serverId].title
            else:
                str = 'Não estou tocando nada no momento.'
        else:
            str = 'Não estou tocando nada no momento.'
        await client.send_message(context.channel, str)
        return
    else:
        if isinstance(context.channel, discord.Channel):
            member = context.author
            vChannel = member.voice.voice_channel
            check = checkVChannel(client, member, context.server)
            if check == VChannelResponse.BOT_NEED_CONNECT:
                vClient = await client.join_voice_channel(vChannel)
                await play(client, args[0], player, vClient, context.channel,
                           context.server)
            elif check == VChannelResponse.BOT_READY:
                await play(client, args[0], player, vChannel, context.channel,
                           context.server)
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


@SubCommand(parent='yt', about='test')
async def add(client: discord.Client, context: discord.Message, args):
    pass


@Command(about='Faz parar tudo!')
async def stop(client: discord.Client, context: discord.Message, args):
    serverId = context.server.id
    if serverId in player.keys() and player[serverId] is None:
        player[serverId].stop()
        player[serverId] = None

    vClient = client.voice_client_in(context.server)
    await vClient.disconnect()

# Admin commands


@Command(about='Desliga o Bot', adminOnly=True)
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
