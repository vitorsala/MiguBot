import pytest
from unittest import mock

from ..commands.commands_manager import CommandManager

class TestCommandManager():

    def test_command_manager_builder(self):
        manager = CommandManager()
        assert manager is not None
        cmd_list = manager.get_list(False)
        assert len(cmd_list) == 2
        