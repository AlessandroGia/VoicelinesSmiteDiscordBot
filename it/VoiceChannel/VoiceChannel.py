from discord.ext.commands import Bot
from discord import Interaction

from it.Exceptions.VoiceChannelErrors import GodMancanteError
from it.VoiceChannel.VoiceState import VoiceState


class VoiceChannel:

    def __init__(self, bot: Bot) -> None:
        self.__voice_states = {}
        self.__bot = bot

    def __get_voicestate(self, interaction: Interaction) -> VoiceState:
        if interaction.guild_id not in self.__voice_states:
            self.__voice_states[interaction.guild_id] = VoiceState(self.__bot)
        return self.__voice_states[interaction.guild.id]

    async def join(self, interaction: Interaction) -> None:
        voice = self.__get_voicestate(interaction)
        await voice.join(interaction)

    def play(self, interaction: Interaction, god: str, skin: str, vgs: str) -> []:
        if not god and (skin or vgs):
            raise GodMancanteError
        elif god and not skin and not vgs:
            skin = "*"  # skin = "default"
            vgs = "*"
        elif god and not skin and vgs:
            skin = "default"
        elif god and skin and not vgs:
            vgs = "*"
        elif not god and not skin and not vgs:
            god = "*"
            skin = "*"
            vgs = "*"
        voice = self.__get_voicestate(interaction)
        god, skin, vgs = voice.play(god, skin, vgs)
        return god, skin, vgs

    async def leave(self, interaction: Interaction) -> None:
        voice = self.__get_voicestate(interaction)
        await voice.leave()

    def voicelines(self, interaction: Interaction, god: str) -> [str, str]:
        voice = self.__get_voicestate(interaction)
        return voice.voicelines(god)
