from discord import Object, Interaction, ButtonStyle, app_commands, ext, ui

from it.Checks.VoiceChannelChecks import check_voice_channel
from it.Minigame.HandlerMinigames import HandlerMinigames
from it.Exceptions.VoiceChannelErrors import *
from it.Embed.Embed import Embed

from asyncio import sleep


class ButtonToPlay(ui.Button):

    def __init__(self, handler_minigames: HandlerMinigames) -> None:
        super().__init__(label="Gioca", style=ButtonStyle.green)
        self.__handler_minigames = handler_minigames
        self.__embed = Embed()

    async def callback(self, interaction: Interaction) -> None:
        if interaction.user.id not in self.__handler_minigames.get_players_id(interaction.channel_id):
            self.__handler_minigames.add_player(interaction.channel_id, interaction)
            await interaction.response.send_message(embed=self.__embed.embed("***Ti sei iscritto!***"), ephemeral=True)
        else:
            await interaction.response.send_message(embed=self.__embed.error("Ti sei gia' iscritto!"), ephemeral=True)


class MinigameCog(ext.commands.Cog):

    __TIMERSTARTGAME = 10
    __TIMERPERGAME = 8
    __TIMERPERGOD = 15

    def __init__(self, bot: ext.commands.Bot) -> None:
        self.__loop = bot.loop
        self.__embed = Embed()
        self.__handler_minigames = HandlerMinigames()
        self.__vc = bot.vc
        self.__god = None
        print()

    group = app_commands.Group(name="minigame", description="YASUO")

    @staticmethod
    async def __timer() -> None:
        await sleep(10000)

    async def __send_embed(self, interaction: Interaction, mess: str, ephemeral: bool = False, footer: str = " ") -> None:
        await interaction.followup.send(
            embed=self.__embed.embed(mess, footer=footer),
            ephemeral=ephemeral
        )

    async def __send_error(self, interaction: Interaction, mess: str, ephemeral: bool = False) -> None:
        await interaction.followup.send(
            embed=self.__embed.error(mess),
            ephemeral=ephemeral
        )

    async def __game(self, interaction: Interaction, num_round: int, rounds: int) -> None:

        emb_mes = await interaction.followup.send(
            embed=self.__embed.embed("***Il round {} di {}, inziera' tra {} secondi.***".format(num_round, rounds, self.__TIMERPERGAME),
                                     footer="/minigame risposta [risposta]")
        )
        for i in range(self.__TIMERPERGAME - 1):
            await sleep(1)
            await emb_mes.edit(
                embed=self.__embed.embed("***Il round {} di {}, inziera' tra {} secondi.***".format(num_round, rounds, self.__TIMERPERGAME - (i+1)),
                                     footer="/minigame risposta [risposta]")
            )
        await sleep(1)

        self.__god, skin, vgs = self.__vc.play(interaction, "*", "*", "*")
        self.__handler_minigames.start_game(interaction.channel_id)

        emb_mes = await interaction.followup.send(
            embed=self.__embed.embed("***{} secondi per rispondere.***".format(self.__TIMERPERGOD),
                                     footer="/minigame risposta [risposta]")
        )
        for i in range(self.__TIMERPERGOD - 1):
            await sleep(1)
            await emb_mes.edit(
                embed=self.__embed.embed("***{} secondi per rispondere.***".format(self.__TIMERPERGOD - (i+1)),
                                         footer="/minigame risposta [risposta]")
            )
        await sleep(1)

        await self.__send_embed(interaction, "**{}**, {} : _{}_".format(
                    self.__god.replace("_", " ").capitalize(),
                    skin.replace("_", " ").capitalize(),
                    vgs.replace("_", " ").lower()
                ))
        self.__handler_minigames.game_finished(interaction.channel_id)
        self.__handler_minigames.clear_answer(interaction.channel_id)

    @group.command(
        name="start",
        description="Avvia il minigame"
    )
    @app_commands.describe(
        rounds="Numero di round del minigame, default: 5"
    )
    @check_voice_channel()
    async def minigame(self, interaction: Interaction, rounds: int = 5):

        if self.__handler_minigames.minigame_is_running(interaction.channel_id):
            await self.__send_error(interaction, "Il minigame e' gia in corso!", ephemeral=True)
        else:
            self.__handler_minigames.add_minigame(interaction.channel_id)
            self.__handler_minigames.start_minigame(interaction.channel_id)

            btn = ButtonToPlay(self.__handler_minigames)
            view = ui.View()
            view.add_item(btn)

            await interaction.response.send_message(
                embed=self.__embed.embed("***Il minigame iniziera' tra {} secondi.***".format(self.__TIMERSTARTGAME)),
                view=view
            )
            for i in range(self.__TIMERSTARTGAME - 1):
                await sleep(1)
                await interaction.edit_original_message(
                    embed=self.__embed.embed(
                        "***Il minigame iniziera' tra {} secondi.***".format(self.__TIMERSTARTGAME - (i+1))
                    ),
                    view=view
                )
            await sleep(1)
            if self.__handler_minigames.get_players_id(interaction.channel_id):
                await interaction.edit_original_message(
                    embed=self.__embed.error("Iscrizioni terminate!"),
                    view=None
                )
                for round in range(rounds):
                    await self.__game(interaction, round + 1, rounds)
                players_score = self.__handler_minigames.leaderboard(interaction.channel_id)
                leadboard = "\t***CLASSIFICA***\n"
                for c, player_score in enumerate(players_score):
                    leadboard += "***{}.*** **{}** : _{}_\n".format(c + 1, player_score.get_nickname(), player_score.get_points())
                await self.__send_embed(interaction, leadboard)
            else:
                await interaction.edit_original_message(
                    embed=self.__embed.error("Nessun partecipante al minigame!"),
                    view=None
                )
            self.__handler_minigames.minigame_finished(interaction.channel_id)

    ##
    # GOD SELECTION
    ##

    @group.command(
        name="risposta",
        description="Inserisci la risposta al minigame"
    )
    @app_commands.describe(
        answer="Il nome del god da inserire"
    )
    async def god(self, interaction: Interaction, answer: str):
        channel_id = interaction.channel_id
        player_id = interaction.user.id
        if self.__handler_minigames.minigame_is_running(interaction.channel_id):
            if player_id in self.__handler_minigames.get_players_id(channel_id):
                if self.__handler_minigames.game_is_started(channel_id):
                    if player_id not in self.__handler_minigames.get_players_answered(channel_id):
                        self.__handler_minigames.add_player_answered(channel_id, player_id)
                        if self.__god.replace("_", " ").lower() == answer.lower():
                            self.__handler_minigames.add_point_to_player(channel_id, player_id)
                        await interaction.response.send_message(
                            embed=self.__embed.embed("***Hai risposto*** : _{}_".format(answer)),
                            ephemeral=True
                        )
                    else:
                        await interaction.response.send_message(
                            embed=self.__embed.error("Hai gia inserito la tua risposta!"),
                            ephemeral=True
                        )
                else:
                    await interaction.response.send_message(
                        embed=self.__embed.error("Il round non e' ancora iniziato!"),
                        ephemeral=True
                    )
            else:
                await interaction.response.send_message(
                    embed=self.__embed.error("Non stai partecipando al minigame!"),
                    ephemeral=True
                )
        else:
            await interaction.response.send_message(
                embed=self.__embed.error("Il minigame non e' stato ancora avviato!"),
                ephemeral=True
            )

    @minigame.error
    async def minigame_start_error(self, interaction: Interaction, error):
        if isinstance(error, UserNonConnessoError):
            await interaction.response.send_message(embed=self.__embed.error("Non sei connesso a nessun canale vocale!"))
        elif isinstance(error, BotNonPresenteError):
            await interaction.response.send_message(embed=self.__embed.error("Il bot non e' presente nel server!"))
        elif isinstance(error, UserNonStessoCanaleBotError):
            await interaction.response.send_message(embed=self.__embed.error("Non sei nello stesso canale del bot! "))


async def setup(bot: ext.commands.Bot) -> None:
    await bot.add_cog(MinigameCog(bot), guilds=[Object(id=928785387239915540)])
