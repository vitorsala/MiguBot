from .commands_base import commandList
from .commands_base import Command
# from .commands_base import SubCommand
from .commands_base import CMD_INDEXER
from .utils import checkVChannel
from .utils import VChannelResponse
from .playlist import serverPlaylists
import discord


@Command()
async def help(client: discord.Client, context: discord.Message, args):
    output = '```\n'
    for cmd in sorted(commandList):
        if cmd != 'help':
            cmdArgs = commandList[cmd][CMD_INDEXER.ARGS]
            about = commandList[cmd][CMD_INDEXER.ABOUT]
            if about is not None:
                output += '$' + cmd
                if cmdArgs is not None:
                    output += ' ' + cmdArgs
                output += ': ' + about + '\n'
            if len(commandList[cmd][CMD_INDEXER.SUBCOMMANDS]) > 0:
                for subcmd in sorted(commandList[cmd][CMD_INDEXER.SUBCOMMANDS]):
                    item = commandList[cmd][CMD_INDEXER.SUBCOMMANDS][subcmd]
                    cmdArgs = item[CMD_INDEXER.ARGS]
                    about = item[CMD_INDEXER.ABOUT]
                    if about is not None:
                        output += '$' + cmd + ' ' + subcmd
                        if cmdArgs is not None:
                            output += ' ' + cmdArgs
                        output += ': ' + about + '\n'
    output += '```'
    await client.send_message(context.channel, output)


@Command(about='Verifica se eu estou disponível  :)')
async def ping(client: discord.Client, context: discord.Message, args):
    await client.send_message(context.channel, 'pong')


@Command(about='Mostra a música atual')
async def song(client: discord.Client, context: discord.Message, args):
    serverId = context.server.id
    pl = serverPlaylists[serverId]
    output = ''
    if pl.player is not None and pl.player.is_playing():
        output = 'Música atual: '
        output += pl.getCurrentMusic() + '\n'
    else:
        output = 'Não estou tocando nada no momento.'
    await client.send_message(context.channel, output)
    return


@Command(about='Lista as músicas na fila')
async def listsong(client: discord.Client, context: discord.Message, args):
    serverId = context.server.id
    pl = serverPlaylists[serverId]
    output = '```\n'
    msg = await client.send_message(context.channel, '`Carregando infos.`')
    if pl.player is not None and pl.player.is_playing():
        output += '\nMúsica atual: '
        output += pl.getCurrentMusic() + '\n\n'
        sl = pl.getMusicList()
        if len(sl) > 0:
            output += 'Músicas na fila:\n'
            for i in range(0, len(sl)):
                output += str(i + 1) + ': ' + sl[i] + '\n'
        else:
            output += 'Fila vazia.'
    else:
        output = 'Não estou tocando nada no momento.'
    output += '\n```'
    await client.edit_message(msg, output)


@Command(about='Mostra qual é a próxima música')
async def nextsong(client: discord.Client, context: discord.Message, args):
    serverId = context.server.id
    pl = serverPlaylists[serverId]
    output = ''
    msg = await client.send_message(context.channel, '`Carregando infos.`')
    if pl.player is not None and pl.player.is_playing():
        n = pl.peekNext()
        if n is not None:
            output += 'Próxima música: ' + n
        else:
            output += 'Fila vazia.'
    else:
        output += 'Não estou tocando nada no momento.'
    await client.edit_message(msg, output)


@Command(args='<link>', about='Toca a música dado um link do youtube')
async def play(client: discord.Client, context: discord.Message, args):
    if isinstance(context.channel, discord.Channel) and args is not None:
        serverId = context.server.id
        member = context.author
        vChannel = member.voice.voice_channel
        check = checkVChannel(client, member, context.server)
        pl = serverPlaylists[serverId]
        pl.clear()
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


@Command(args='<link>', about='Adiciona uma música na fila')
async def addsong(client: discord.Client, context: discord.Message, args):
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


@Command(args='<index>', about='Remove uma música da lista')
async def remsong(client: discord.Client, context: discord.Message, args):
    if len(args) != 1:
        await client.send_message(context.channel, '$remsong <index>')
        return
    serverId = context.server.id
    pl = serverPlaylists[serverId]
    output = ''
    selected = int(args[0])
    selected -= 1
    if pl.player is not None and pl.player.is_playing():
        if pl.removeMusic(selected):
            output = 'Música removido.'
        else:
            output = 'Erro ao remover a música.'
    else:
        output = 'Não estou tocando nada no momento.'
    await client.send_message(context.channel, output)


@Command(about='Faz parar a reprodução de música!')
async def stop(client: discord.Client, context: discord.Message, args):
    serverId = context.server.id
    pl = serverPlaylists[serverId]
    vClient = client.voice_client_in(context.server)
    pl.stop()
    await vClient.disconnect()


@Command(about='BATATA!')
async def batata(client: discord.Client, context: discord.Message, args):
    await client.send_message(context.channel,
                              'http://i.imgur.com/jzYecG5.jpg')


# Admin commands


@Command(about='Desliga o Bot', adminOnly=True)
async def shutdown(client: discord.Client, context: discord.Message, args):
    await client.close()
