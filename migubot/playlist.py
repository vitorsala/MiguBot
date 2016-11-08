from .utils import Queue
import asyncio
import discord

serverPlaylists = {}


class PlayList:

    QUEUE = 0
    PLAYER = 1

    def __init__(self, server: discord.Server):
        self.player = None
        self.server = server
        self.queue = Queue()

    def addMusic(self, link):
        self.queue.enqueue(link)

    def removeMusic(self, index):
        if index < self.queue.size():
            self.queue.removeFromIndex(index)

    def peekNext(self):
        if self.queue.size > 0:
            return self.queue.peek()

    def clear(self):
        self.queue.clear()

    async def stop(self):
        self.player.stop()
        self.clear()
        self.player = None

    async def play(self, client, link, vChannel, tChannel):
        self.currentVChannel = vChannel
        self.currentTChannel = tChannel
        try:
            msg = await client.send_message(tChannel, "`Preparando...`")
            self.player = await vChannel.create_ytdl_player(link)
            self.player.volume = 0.5
            # self.player = await vChannel.create_ytdl_player(
            #     link,
            #     after=lambda: self.ytPlayerCallBack(client)
            # )
            await  client.edit_message(msg, "`Pronto!`")
            await client.send_message(tChannel, "`Tocando: " +
                                      self.player.title + "`")
            self.player.start()
        except BaseException as e:
            # Fazer o tratamento das exceções
            print(e)
        return

    async def playNext(self, client):
        next = self.queue.dequeue()
        await self.play(client,
                        next,
                        self.currentVChannel,
                        self.currentTChannel)

    async def update(self, client):
        if self.player is not None:
            if not self.player.is_playing():
                if not self.queue.isEmpty():
                    await self.playNext(client)
                else:
                    self.player = None
                    vClient = client.voice_client_in(self.server)
                    await vClient.disconnect()

    # def ytPlayerCallBack(self, client: discord.Client):
    #     fut = asyncio.run_coroutine_threadsafe(self.check(client), client.loop)
    #     try:
    #         fut.result()
    #     except:
    #         pass
    #
    # async def check(self, client: discord.Client):
    #     print("a")
    #     if not self.queue.isEmpty():
    #         print("b")
    #         await self.playlist.playNext(client)
    #     else:
    #         print("c")
    #         vClient = client.voice_client_in(self.server)
    #         print("d")
    #         await vClient.disconnect()
    #     print("e")

async def playListTask(client: discord.Client):
    await client.wait_until_ready()
    while not client.is_closed:
        for pl in serverPlaylists:
            playlist = serverPlaylists[pl]
            await playlist.update(client)
        await asyncio.sleep(1)
