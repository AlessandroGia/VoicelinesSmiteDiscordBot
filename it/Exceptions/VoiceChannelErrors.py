from discord.app_commands import AppCommandError


class GodMancanteError(AppCommandError):
    pass


class UserNonConnessoError(AppCommandError):
    pass


class BotGiaConnessoError(AppCommandError):
    pass


class BotNonPresenteError(AppCommandError):
    pass


class UserNonStessoCanaleBotError(AppCommandError):
    pass

