from enum import Enum
import discord

class VChannelResponse(Enum):
    """
    Enum para os estados do bot.
    """
    # I'm ready to action!
    BOT_READY = 0
    # I need to connect to an channel in order to attend.
    BOT_NEED_CONNECT = 1,
    # The person calling me is not, currently, connected to any channel
    USER_NOT_IN_CHANNEL = 2,
    # I'm already in use
    BOT_IN_USE = 3
    # I can't join channel
    BOT_CANNOT_JOIN = 4

class VChannelUtils:
    """
    classe de apoio para o uso de vchannel.
    """
    @staticmethod
    def check_voice_channel(client: discord.Client,
                            member: discord.Member,
                            server: discord.Server):
        """
        check voice channel conditions
        """
        __vchannel = member.voice.voice_channel
        if __vchannel is not None and not member.voice.is_afk:
            assert isinstance(__vchannel, discord.Channel)
            # permissions = client.user.permissions_in(vChannel)
            # if not(permissions.connect or permissions.speak):
            #    return VChannelResponse.BOT_CANNOT_JOIN

            # Verifica se eu estou disponível para chamada
            if not client.is_voice_connected(server):
                return VChannelResponse.BOT_NEED_CONNECT
            else:
                tmp = client.voice_client_in(server)
                if __vchannel != tmp:
                    return VChannelResponse.BOT_IN_USE
        else:
            return VChannelResponse.USER_NOT_IN_CHANNEL
