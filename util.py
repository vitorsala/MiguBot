from enum import Enum
import discord


class YT(Enum):
    QUEUE = 0


class YTQueue:
    def __init__(self, client: discord.Client):
        self.cache = {}
        for server in client.servers:
            self.cache[server.id] = {YT.QUEUE: []}

    def pushMusic(self, guildId: str, link: str):
        self.cache[guildId][YT.QUEUE].append(link)

    def popMusic(self, guildId: str):
        return self.cache[guildId][YT.QUEUE].pop(0)

    def listMusic(self, guildId: str):
        return self.cache[guildId][YT.QUEUE]

    def clearQueue(self, guildId: str):
        self.cache[guildId][YT.QUEUE] = []


class Command:
    def __init__(self, about: str, function):
        self.about = about
        self.function = function


class SubCommand():
    def __init__(self, about: str, function):
        self.about = about
        self.function = function

ytQueue = None
botCache = {}
