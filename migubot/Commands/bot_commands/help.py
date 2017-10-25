import discord
from ..base.command import Command

class Help(Command):
    
    def setup(self):
        self.about = "Exibe todos os meus comandos!"

    def execute(self, client: discord.Client, context: discord.Message, args:dict):
        pass
