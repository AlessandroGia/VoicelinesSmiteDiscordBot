from it.Minigame.Player.HandlerPlayers import HandlerPlayers

from discord import Interaction


class MiniGame:
    def __init__(self) -> None:
        self.__is_playing: bool = False
        self.__is_started: bool = False
        self.__handler_players: HandlerPlayers = HandlerPlayers()

    def set_is_playing(self, is_playing: bool) -> None:
        self.__is_playing = is_playing

    def get_is_playing(self) -> bool:
        return self.__is_playing

    def set_is_started(self, is_started: bool) -> None:
        self.__is_started = is_started

    def get_is_started(self) -> bool:
        return self.__is_started

    # HANDLER PLAYERS

    def add_player_answered(self, player_id: int) -> None:
        self.__handler_players.add_player_answered(player_id)

    def get_players_answered(self) -> []:
        return self.__handler_players.get_players_answered()

    def clear_answer(self) -> None:
        self.__handler_players.clear_answer()

    def add_player(self, interaction: Interaction) -> None:
        self.__handler_players.add_player(interaction)

    def add_point_to_player(self, player_id: int) -> None:
        self.__handler_players.add_point_to_player(player_id)

    def get_nickname_per_id(self, player_id: int) -> str:
        return self.__handler_players.get_nickname_by_id(player_id)

    def get_players_id(self) -> [int]:
        return self.__handler_players.get_players_id()

    def leaderboard(self) -> []:
        return self.__handler_players.leaderboard()
