import discord
from ..base.command import Command

class Ping(Command):

    def setup(self):
        self.about = "Verifica se eu estou disponível.  :)"

    async def execute(self, client: discord.Client, context: discord.Message, args:dict):
        await client.send_message(context.channel, 'pong')
