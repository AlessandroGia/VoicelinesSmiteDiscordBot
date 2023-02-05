from discord import FFmpegPCMAudio, Interaction, ext

from src.Exceptions.TreesExceptions import NoVoicesError
from src.VoiceChannel.LocalVoices import LocalVoices

import asyncio


class VoiceState:

    TIMEOUT = 900  # Secondi

    def __init__(self, bot: ext.commands.Bot) -> None:
        self.__bot = bot
        self.__voice = None
        self.__timeout = None
        self.__local_voices = LocalVoices()
        self.__flag_timeout = asyncio.Event()

    def __trigger(self, error=False) -> None:
        self.__flag_timeout.set()

    def __exitafter(self, error=False) -> None:
        self.__bot.loop.create_task(self.__exit())

    async def __exit(self) -> None:
        await self.__voice.disconnect()
        self.__voice = None
        self.__timeout.cancel()

    async def __timeout_(self) -> None:
        while True:
            try:
                self.__flag_timeout.clear()
                await asyncio.wait_for(self.__flag_timeout.wait(), timeout=self.TIMEOUT)
            except asyncio.TimeoutError:
                self.__bot.loop.create_task(self.leave())
                return

    def __playaudio(self, source: str) -> None:
        if self.__voice.is_playing() or self.__voice.is_paused():
            self.__voice.stop()
        self.__voice.play(FFmpegPCMAudio(source), after=self.__trigger)

    async def join(self, interaction: Interaction) -> None:
        self.__voice = await interaction.user.voice.channel.connect()
        self.__timeout = self.__bot.loop.create_task(self.__timeout_())
        try:
            url, god, skin, vgs = self.__local_voices.getvgs("*", "*", "vvgh", flag=True)
        except NoVoicesError:
            pass
        else:
            self.__playaudio(url)

    def play(self, god: str, skin: str, vgs: str) -> []:
        url, god, skin, vgs = self.__local_voices.getvgs(god, skin, vgs)
        self.__playaudio(url)
        return god, skin, vgs

    async def leave(self) -> None:
        if self.__voice.is_playing() or self.__voice.is_paused():
            self.__voice.stop()
        try:
            url, god, skin, vgs = self.__local_voices.getvgs("*", "*", "vvgb", flag=True)
        except NoVoicesError:
            self.__exitafter()
        else:
            audio = FFmpegPCMAudio(url)
            self.__voice.play(audio, after=self.__exitafter)

    def voicelines(self, god: str) -> [str, str]:
        return self.__local_voices.voicelines(god)
