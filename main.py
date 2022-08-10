from it.VoiceChannel.VoiceChannel import VoiceChannel
from discord import Object, Intents, ext
from dotenv import load_dotenv

import os


class VoicelinesDiscordBot(ext.commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=Intents.all())
        self.vc = VoiceChannel(self)

    async def setup_hook(self) -> None:
        await self.load_extension(f"it.Cogs.VoiceChannelCog")
        await self.load_extension(f"it.Cogs.MinigameCog")

    async def on_ready(self):
        await self.tree.sync(guild=Object(id=928785387239915540))
        print("{} si e' connesso a discord!".format(self.user))


if __name__ == "__main__":
    load_dotenv()
    VoicelinesDiscordBot().run(os.getenv("DISCORD_TOKEN"))

