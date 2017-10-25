import discord

class Command:
    def __init__(self):
        self.cmd = self.__class__.__name__.lower()
        self.admin_only = False
        self.about = "Este comando não tem descrição. :("

    def setup(self):
        pass

    async def execute(self, client: discord.Client, context: discord.Message, args:dict): 
        pass

    def cleanup(self):
        pass
        