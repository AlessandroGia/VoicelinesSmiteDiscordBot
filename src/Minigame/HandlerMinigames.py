from src.Minigame.MiniGame import MiniGame

from discord import Interaction


class HandlerMinigames:

    def __init__(self):
        self.__minigames: {int: MiniGame} = {}

    def minigame_is_running(self, channel_id: int) -> bool:
        if self.__minigames.get(channel_id):
            return self.__minigames[channel_id].get_is_playing()
        else:
            return False

    def game_is_started(self, channel_id: int) -> bool:
        if self.__minigames.get(channel_id):
            return self.__minigames[channel_id].get_is_started()
        else:
            return False

    def minigame_finished(self, channel_id: int) -> None:
        self.__minigames[channel_id].set_is_playing(False)

    def game_finished(self, channel_id: int) -> None:
        self.__minigames[channel_id].set_is_started(False)

    def add_minigame(self, channel_id: int) -> None:
        self.__minigames[channel_id] = MiniGame()

    def start_minigame(self, channel_id: int) -> None:
        self.__minigames[channel_id].set_is_playing(True)

    def start_game(self, channel_id: int) -> None:
        self.__minigames[channel_id].set_is_started(True)

    # MINIGAME

    def add_player_answered(self, channel_id: int, player_id: int) -> None:
        self.__minigames[channel_id].add_player_answered(player_id)

    def get_players_answered(self, channel_id: int) -> []:
        return self.__minigames[channel_id].get_players_answered()

    def clear_answer(self, channel_id: int) -> None:
        self.__minigames[channel_id].clear_answer()

    def add_player(self, channel_id: int, interaction: Interaction) -> None:
        self.__minigames[channel_id].add_player(interaction)

    def add_point_to_player(self, channel_id: int, player_id: int) -> None:
        self.__minigames[channel_id].add_point_to_player(player_id)

    def get_nickname_per_id(self, channel_id: int, player_id: int) -> str:
        return self.__minigames[channel_id].get_nickname_by_id(player_id)

    def get_players_id(self, channel_id: int) -> [int]:
        return self.__minigames[channel_id].get_players_id()

    def leaderboard(self, channel_id: int) -> []:
        return self.__minigames[channel_id].leaderboard()

