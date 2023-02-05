from discord.app_commands import AppCommandError


class NoVoicesError(AppCommandError):
    pass


class NoVoicesGodError(AppCommandError):
    pass


class VoicesGodError(AppCommandError):
    pass


class NoVoicesSkinError(AppCommandError):
    pass


class NoVGSError(AppCommandError):
    pass