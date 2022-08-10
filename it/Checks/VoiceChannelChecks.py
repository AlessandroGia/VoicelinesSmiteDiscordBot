from discord import app_commands, utils, Interaction

from it.Exceptions.VoiceChannelErrors import *


def __channel_connected_to(interaction: Interaction):
    return utils.get(interaction.client.voice_clients, guild=interaction.guild)


def check_voice_channel():
    def predicate(interaction: Interaction) -> bool:
        if not interaction.user.voice:
            raise UserNonConnessoError

        if interaction.command.name == "join":
            if __channel_connected_to(interaction):
                raise BotGiaConnessoError

        else:
            if not __channel_connected_to(interaction):
                raise BotNonPresenteError

            if not interaction.user.voice.channel == __channel_connected_to(interaction).channel:
                raise UserNonStessoCanaleBotError

        return True
    return app_commands.check(predicate)
