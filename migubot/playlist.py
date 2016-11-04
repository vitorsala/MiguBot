from .utils import Queue

serverPlaylists = {}


class PlayList:

    QUEUE = 0
    PLAYER = 1

    def __init__(self, serverId, player):
        self.player = player
        self.sId = serverId
        self.queue = Queue()

    def addMusic(self, link):
        pass

    def removeMusic(self, index):
        pass

    def peekNext(self):
        pass

    def clear(self):
        pass
