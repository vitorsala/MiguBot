# Lista é preenchida de acordo com os decorators
commandList = {}
adminCommandList = {}


class CMD_INDEXER:
    FUNCTION = 0
    ABOUT = 1
    SUBCOMMANDS = 2
    ARGS = 3


class Command:
    def __init__(self, args=None, about=None, adminOnly=False):
        self.args = args
        self.about = about
        self.adminOnly = adminOnly

    def __call__(self, f):
        registerCommand(f.__name__, self.args, self.about, self.adminOnly, f)

        def wrapper(client, context, args):
            f(client, context, args)
        return wrapper


class SubCommand:
    def __init__(self, parent, args=None, about=None, adminOnly=False):
        self.parent = parent
        self.args = args
        self.about = about
        self.adminOnly = adminOnly

    def __call__(self, f):
        registerSubCommand(
            self.parent,
            f.__name__,
            self.args,
            self.about,
            self.adminOnly,
            f
        )

        def wrapper(client, context, args):
            f(client, context, args)
        return wrapper


def registerCommand(cmd, args=None, about=None, admin=True, func=None):
    cmdlist = {}
    if admin is True:
        cmdlist = adminCommandList
    else:
        cmdlist = commandList
    assert isinstance(cmdlist, dict)
    if cmd not in cmdlist:
        cmdlist[cmd] = {}
        cmdlist[cmd][CMD_INDEXER.SUBCOMMANDS] = {}
    cmdlist[cmd][CMD_INDEXER.FUNCTION] = func
    cmdlist[cmd][CMD_INDEXER.ARGS] = args
    cmdlist[cmd][CMD_INDEXER.ABOUT] = about


def registerSubCommand(parentCmd, cmd, args=None, about=None,
                       admin=True, func=None):
    cmdlist = {}
    if admin is True:
        cmdlist = adminCommandList
    else:
        cmdlist = commandList
    if parentCmd not in cmdlist:
        cmdlist[parentCmd] = {}
        cmdlist[parentCmd][CMD_INDEXER.FUNCTION] = None
        cmdlist[parentCmd][CMD_INDEXER.ABOUT] = None
        cmdlist[parentCmd][CMD_INDEXER.ARGS] = None
    subcmd = {}
    subcmd[CMD_INDEXER.FUNCTION] = func
    subcmd[CMD_INDEXER.ABOUT] = about
    subcmd[CMD_INDEXER.ARGS] = args
    cmdlist[parentCmd][CMD_INDEXER.SUBCOMMANDS][cmd] = subcmd
