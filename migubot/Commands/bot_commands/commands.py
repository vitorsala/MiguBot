# import discord

# from ..variables import COMMANDS
# from ..base.command import Command
# from ..base.sub_command import SubCommand
# from ..base.commands_utils import CMD_INDEXER

# from ...utils.queue import Queue
# from ...utils.vChannelUtils import VChannelResponse
# from ...utils.vChannelUtils import VChannelUtils
# from ...utils.playlist import serverPlaylists

# class BotCommands:
#     def __init__(self):
#         pass

#     @Command()
#     async def help(self, client: discord.Client, context: discord.Message, args):
#         output = '```\n'
#         for cmd in sorted(COMMANDS):
#             if cmd != 'help':
#                 cmd_args = COMMANDS.command_list[cmd][CMD_INDEXER.ARGS]
#                 about = COMMANDS.command_list[cmd][CMD_INDEXER.ABOUT]
#                 if about is not None:
#                     output += '$' + cmd
#                     if cmd_args is not None:
#                         output += ' ' + cmd_args
#                     output += ': ' + about + '\n'
                    
#                 size = len(COMMANDS.command_list[cmd][CMD_INDEXER.SUBCOMMANDS])
#                 if size > 0:
#                     for subcmd in sorted(COMMANDS.command_list[cmd][CMD_INDEXER.SUBCOMMANDS]):
#                         item = COMMANDS.command_list[cmd][CMD_INDEXER.SUBCOMMANDS][subcmd]
#                         cmd_args = item[CMD_INDEXER.ARGS]
#                         about = item[CMD_INDEXER.ABOUT]
#                         if about is not None:
#                             output += '$' + cmd + ' ' + subcmd
#                             if cmd_args is not None:
#                                 output += ' ' + cmd_args
#                             output += ': ' + about + '\n'
#         output += '```'
#         await client.send_message(context.channel, output)

#     @Command(about='Verifica se eu estou disponível  :)')
#     async def ping(self, client: discord.Client, context: discord.Message, args):
#         await client.send_message(context.channel, 'pong')

#     @Command(about='Mostra a música atual')
#     async def song(self, client: discord.Client, context: discord.Message, args):
#         server_id = context.server.id
#         pl = serverPlaylists[server_id]
#         output = ''
#         if pl.player is not None and pl.player.is_playing():
#             output = 'Música atual: '
#             output += pl.getCurrentMusic() + '\n'
#         else:
#             output = 'Não estou tocando nada no momento.'
#         await client.send_message(context.channel, output)
#         return

#     @Command(about='Lista as músicas na fila')
#     async def listsong(self, client: discord.Client, context: discord.Message, args):
#         _server_id = context.server.id
#         _playlist = serverPlaylists[_server_id]
#         output = '```\n'
#         msg = await client.send_message(context.channel, '`Carregando infos.`')
#         if _playlist.player is not None and _playlist.player.is_playing():
#             output += '\nMúsica atual: '
#             output += _playlist.getCurrentMusic() + '\n\n'
#             _song_list = _playlist.getMusicList()
#             _song_list_len = len(_song_list)
#             if _song_list_len > 0:
#                 output += 'Músicas na fila:\n'
#                 for i in range(0, len(_song_list)):
#                     output += str(i + 1) + ': ' + _song_list[i] + '\n'
#             else:
#                 output += 'Fila vazia.'
#         else:
#             output = 'Não estou tocando nada no momento.'
#         output += '\n```'
#         await client.edit_message(msg, output)

#     @Command(about='Mostra qual é a próxima música')
#     async def nextsong(self, client: discord.Client, context: discord.Message, args):
#         _server_id = context.server.id
#         _playlist = serverPlaylists[_server_id]
#         output = ''
#         msg = await client.send_message(context.channel, '`Carregando infos.`')
#         if _playlist.player is not None and _playlist.player.is_playing():
#             _next_song = _playlist.peekNext()
#             if _next_song is not None:
#                 output += 'Próxima música: ' + _next_song
#             else:
#                 output += 'Fila vazia.'
#         else:
#             output += 'Não estou tocando nada no momento.'
#         await client.edit_message(msg, output)

#     @Command(args='<link>', about='Toca a música dado um link do youtube')
#     async def play(self, client: discord.Client, context: discord.Message, args):
#         if isinstance(context.channel, discord.Channel) and args is not None:
#             server_id = context.server.id
#             member = context.author
#             voice_channel = member.voice.voice_channel
#             check = VChannelUtils.check_voice_channel(client, member, context.server)
#             _playlist = serverPlaylists[server_id]
#             _playlist.clear()
#             if check == VChannelResponse.BOT_NEED_CONNECT:
#                 voice_channel = await client.join_voice_channel(voice_channel)
#                 await _playlist.play(client, args[0],
#                             voice_channel, context.channel)
#             elif check == VChannelResponse.BOT_READY:
#                 await _playlist.play(client, args[0],
#                             voice_channel, context.channel)
#             elif check == VChannelResponse.BOT_IN_USE:
#                 await client.send_message(
#                     context.channel,
#                     "No momento, estou tocando música em outro canal!"
#                 )
#             elif check == VChannelResponse.USER_NOT_IN_CHANNEL:
#                 await client.send_message(
#                     context.channel,
#                     "Você precisa estar em um canal de \
#                     voz para usar este comando."
#                 )

#     @Command(args='<link>', about='Adiciona uma música na fila')
#     async def addsong(self, client: discord.Client, context: discord.Message, args):
#         if args is not None:
#             server_id = context.server.id
#             playlist = serverPlaylists[server_id]
#             if playlist.player is None:
#                 await client.send_message(
#                     context.channel,
#                     "Não há nenhuma playlist ativa, use `$yt play <link>` para iniciar uma nova."
#                 )
#                 return
#             else:
#                 server_id = context.server.id
#                 playlist = serverPlaylists[server_id]
#                 playlist.addMusic(args[0])
#                 await client.send_message(
#                     context.channel,
#                     "Link adicionado na fila."
#                 )

#     @Command(args='<index>', about='Remove uma música da lista')
#     async def remsong(self, client: discord.Client, context: discord.Message, args):
#         if len(args) != 1:
#             await client.send_message(context.channel, '$remsong <index>')
#             return
#         server_id = context.server.id
#         playlist = serverPlaylists[server_id]
#         output = ''
#         selected = int(args[0])
#         selected -= 1
#         if playlist.player is not None and playlist.player.is_playing():
#             if playlist.removeMusic(selected):
#                 output = 'Música removido.'
#             else:
#                 output = 'Erro ao remover a música.'
#         else:
#             output = 'Não estou tocando nada no momento.'
#         await client.send_message(context.channel, output)

#     @Command(about='Faz parar a reprodução de música!')
#     async def stop(self, client: discord.Client, context: discord.Message, args):
#         server_id = context.server.id
#         playlist = serverPlaylists[server_id]
#         vClient = client.voice_client_in(context.server)
#         playlist.stop()
#         await vClient.disconnect()

#     @Command(about='BATATA!')
#     async def batata(self, client: discord.Client, context: discord.Message, args):
#         await client.send_message(context.channel,
#                                 'http://i.imgur.com/jzYecG5.jpg')


#     # Admin commands

#     @Command(about='Desliga o Bot', adminOnly=True)
#     async def shutdown(self, client: discord.Client, context: discord.Message, args):
#         await client.close()
