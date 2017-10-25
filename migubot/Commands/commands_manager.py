from .bot_commands import *
from .base.command import Command

class CommandManager:
    def __init__(self):
        self._command_list = []
        self.generate_command_list()

    def get_list(self, admin:bool) -> list:
        return [cmd for cmd in self._command_list if cmd.admin_only == False or cmd.admin_only == admin]

    def generate_command_list(self):
        _cmd_class_list = Command.__subclasses__()
        self._command_list = [cmd_class() for cmd_class in _cmd_class_list]
