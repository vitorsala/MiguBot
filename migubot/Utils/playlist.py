from .utils import Queue
import asyncio
import discord
import youtube_dl

serverPlaylists = {}
ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})


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
            return True
        else:
            return False

    def getCurrentMusic(self):
        if self.player.is_playing():
            return self.player.title
        else:
            return None

    def peekNext(self):
        if self.queue.size() > 0:
            return self.getLinkTitle(self.queue.peek())
        else:
            return None

    def getMusicList(self):
        if self.queue.isEmpty():
            return []
        res = self.queue.getList()
        for i in range(0, self.queue.size()):
            res[i] = self.getLinkTitle(res[i])
        return res

    def clear(self):
        self.queue.clear()

    def stop(self):
        self.player.stop()
        self.clear()
        self.player = None

    def getLinkTitle(self, url):
        infos = ydl.extract_info(url, download=False)
        return infos['title']

    async def play(self, client, link, vChannel, tChannel):
        self.currentVChannelClient = vChannel
        self.currentTChannel = tChannel
        try:
            msg = await client.send_message(tChannel, "`Preparando...`")
            self.player = await vChannel.create_ytdl_player(link)
            self.player.volume = 0.5
            await client.edit_message(msg, "`Pronto!`")
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
                        self.currentVChannelClient,
                        self.currentTChannel)

    async def update(self, client):
        async def stopFunction():
            self.stop()
            await self.currentVChannelClient.disconnect()
            return

        if self.player is not None:
            if self.player.is_playing():
                vChannel = self.currentVChannelClient.channel
                if len(vChannel.voice_members) == 1:
                    await stopFunction()
                    return
            else:
                if self.queue.isEmpty():
                    await stopFunction()
                    return
                else:
                    await self.playNext(client)
                    return

async def playListTask(client: discord.Client):
    await client.wait_until_ready()
    while not client.is_closed:
        for pl in serverPlaylists:
            playlist = serverPlaylists[pl]
            await playlist.update(client)
        await asyncio.sleep(1)
