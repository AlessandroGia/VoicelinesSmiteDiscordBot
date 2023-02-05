from discord import Object, Interaction, app_commands, ext

from src.Checks.VoiceChannelChecks import check_voice_channel
from src.Exceptions.VoiceChannelErrors import *
from src.Exceptions.TreesExceptions import *
from src.Embed.Embed import Embed

from typing import List


class VoiceChannelCog(ext.commands.Cog):

    def __init__(self, bot: ext.commands.Bot):
        self.__embed = Embed()
        self.__vc = bot.vc
        self.__autocomplete_vgs = [
            "Ability 1", "Ability 2", "Ability 3", "Ability 4",
            "Select", "Intro", "Movement", "Health Low",
            "Ward Placed", "Death", "Kill Tower",
            "Kill Streak", "Purchase Notrecommended",
            "Purchase Recommended", "Purchase Consumable", "Kill Jungleboss"
        ]

    ##
    # VOICELINES COMMAND
    ##

    @app_commands.command(
        name="voicelines",
        description="Mostra le voicelines delle skin di un god"
    )
    @app_commands.describe(
        god="Nome del god",
    )
    async def voicelines(self, interaction: Interaction, god: str):
        god, skins = self.__vc.voicelines(interaction, god)
        await interaction.response.send_message(embed=self.__embed.embed(skins, god))

    ##
    # JOIN COMMAND
    ##

    @app_commands.command(
        name="join",
        description="Fa entrare il bot nel VC"
    )
    @check_voice_channel()
    async def join(self, interaction: Interaction):

        await self.__vc.join(interaction)
        await interaction.response.send_message(embed=self.__embed.embed(
            "**Bot entrato in** : _{}_".format(interaction.user.voice.channel)
        ))

    ##
    # LEAVE COMMAND
    ##

    @app_commands.command(
        name="leave",
        description="Fa uscire il bot dal VC"
    )
    @check_voice_channel()
    async def leave(self, interaction: Interaction):
        await self.__vc.leave(interaction)
        await interaction.response.send_message(embed=self.__embed.embed(
            "**Bot Uscito da** : _{}_".format(interaction.user.voice.channel)
        ))

    ##
    # PLAY COMMAND
    ##

    @app_commands.command(
        name="play",
        description="Riproduce voicelines"
    )
    @app_commands.describe(
        god="Nome del god",
        skin="Nome della skin",
        vgs="Vgs da riprodurre"
    )
    @check_voice_channel()
    async def play(self, interaction: Interaction, god: str = "", skin: str = "", vgs: str = ""):
        god, skin, vgs = self.__vc.play(interaction, god, skin, vgs)
        await interaction.response.send_message(
            embed=self.__embed.embed(
                "**{}**, {} : _{}_".format(
                    god.replace("_", " ").capitalize(),
                    skin.replace("_", " ").capitalize(),
                    vgs.replace("_", " ").lower()
                )
            ))

    @play.autocomplete("vgs")
    async def vgs_autocomplete(self, interaction: Interaction, current_vgs: str) -> List[app_commands.Choice[str]]:
        return [
            app_commands.Choice(name=vgs, value=vgs)
            for vgs in self.__autocomplete_vgs if current_vgs.lower() in vgs.lower()
        ]

    ##
    # HANDLING EXCEPTIONS
    ##

    @play.error
    async def play_error(self, interaction: Interaction, error):
        if isinstance(error, UserNonConnessoError):
            await interaction.response.send_message(embed=self.__embed.error("Non sei connesso a nessun canale vocale"))
        elif isinstance(error, BotNonPresenteError):
            await interaction.response.send_message(embed=self.__embed.error("Il bot non e' presente nel server"))
        elif isinstance(error, UserNonStessoCanaleBotError):
            await interaction.response.send_message(embed=self.__embed.error("Non sei nello stesso canale del bot"))
        elif isinstance(error, NoVoicesError):
            await interaction.response.send_message(embed=self.__embed.error("Non sono presenti voicelines"))
        elif isinstance(error, NoVoicesGodError):
            await interaction.response.send_message(embed=self.__embed.error("Questo god non ha voicelines"))
        elif isinstance(error, NoVoicesSkinError):
            await interaction.response.send_message(embed=self.__embed.error("Questa skin non ha voicelines"))
        elif isinstance(error, NoVGSError):
            await interaction.response.send_message(embed=self.__embed.error("Questa vgs non esiste"))
        elif isinstance(error, GodMancanteError):
            await interaction.response.send_message(embed=self.__embed.error("Devi inserire un god"))

    @voicelines.error
    async def voicelines_error(self, interaction: Interaction, error):
        if isinstance(error, NoVoicesError):
            await interaction.response.send_message(embed=self.__embed.error("Non sono presenti voicelines"))
        elif isinstance(error, NoVoicesGodError):
            await interaction.response.send_message(embed=self.__embed.error("Questo god non ha voicelines"))
        elif isinstance(error, NoVoicesSkinError):
            await interaction.response.send_message(embed=self.__embed.error("Questa skin non ha voicelines"))
        elif isinstance(error, NoVGSError):
            await interaction.response.send_message(embed=self.__embed.error("Questa vgs non esiste"))

    @leave.error
    async def leave_error(self, interaction: Interaction, error):
        if isinstance(error, UserNonConnessoError):
            await interaction.response.send_message(embed=self.__embed.error("Non sei connesso a nessun canale vocale"))
        elif isinstance(error, BotNonPresenteError):
            await interaction.response.send_message(embed=self.__embed.error("Il bot non e' presente nel server"))
        elif isinstance(error, UserNonStessoCanaleBotError):
            await interaction.response.send_message(embed=self.__embed.error("Non sei nello stesso canale del bot"))
        elif isinstance(error, NoVoicesError):
            await interaction.response.send_message(embed=self.__embed.error("Non sono presenti voicelines"))

    @join.error
    async def join_error(self, interaction: Interaction, error):
        if isinstance(error, UserNonConnessoError):
            await interaction.response.send_message(embed=self.__embed.error("Non sei connesso a nessun canale vocale"))
        elif isinstance(error, BotGiaConnessoError):
            await interaction.response.send_message(embed=self.__embed.error("Bot gia' connesso"))
        elif isinstance(error, NoVoicesError):
            await interaction.response.send_message(embed=self.__embed.error("Non sono presenti voicelines"))


async def setup(bot: ext.commands.Bot):
    await bot.add_cog(VoiceChannelCog(bot), guilds=[Object(id=928785387239915540)])
