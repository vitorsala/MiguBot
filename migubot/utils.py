from copy import deepcopy
import discord


class Queue:
    def __init__(self, elements=None):
        if elements is not None and isinstance(elements, list):
            self.queue = elements
        else:
            self.queue = []

    def enqueue(self, element):
        self.queue.append(element)

    def dequeue(self):
        if self.size() == 0:
            return None
        r = self.queue[0]
        del self.queue[0]
        return r

    def peek(self):
        if self.size() == 0:
            return None
        return self.queue[0]

    def getList(self):
        return deepcopy(self.queue)

    def removeFromIndex(self, index):
        if index < self.size():
            del self.queue[index]

    def clear(self):
        self.queue = []

    def size(self):
        return len(self.queue)

    def isEmpty(self):
        return self.size() == 0


class VChannelResponse:
    # Eu já estou pronto para ação!
    BOT_READY = 0
    # Eu preciso me conectar para atender o pedido.
    BOT_NEED_CONNECT = 1,
    # A pessoa que me chamou não está em um canal válido.
    USER_NOT_IN_CHANNEL = 2,
    # Eu já estou atendendo alguém.
    BOT_IN_USE = 3
    # Eu não posso entrar!
    BOT_CANNOT_JOIN = 4


def checkVChannel(client: discord.Client,
                  member: discord.Member,
                  server: discord.Server):
    vChannel = member.voice.voice_channel
    if vChannel is not None and not member.voice.is_afk:
        assert isinstance(vChannel, discord.Channel)
        # permissions = client.user.permissions_in(vChannel)
        # if not(permissions.connect or permissions.speak):
        #    return VChannelResponse.BOT_CANNOT_JOIN

        # Verifica se eu estou disponível para chamada
        if not client.is_voice_connected(server):
            return VChannelResponse.BOT_NEED_CONNECT
        else:
            tmp = client.voice_client_in(server)
            if vChannel != tmp:
                return VChannelResponse.BOT_IN_USE
    else:
        return VChannelResponse.USER_NOT_IN_CHANNEL
