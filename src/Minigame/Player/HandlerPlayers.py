from src.Minigame.Player.Player import Player

from discord import Interaction


class HandlerPlayers:

    def __init__(self) -> None:
        self.__players: [Player] = []
        self.__players_answered: [int] = []

    def add_player_answered(self, player_id: int) -> None:
        self.__players_answered.append(player_id)

    def get_players_answered(self) -> []:
        return self.__players_answered

    def clear_answer(self) -> None:
        self.__players_answered = []

    def get_players(self) -> [Player]:
        return self.__players

    def add_player(self, interaction: Interaction) -> None:
        player = Player(interaction.user.id, interaction.user.display_name)
        self.__players.append(player)

    def add_point_to_player(self, player_id: int) -> None:
        player = self.__get_player_per_id(player_id)
        player.add_point()

    def get_nickname_by_id(self, player_id: int) -> str:
        player = self.__get_player_per_id(player_id)
        return player.get_nickname()

    def get_players_id(self) -> [int]:
        ids = []
        for player in self.__players:
            ids.append(player.get_id())
        return ids

    def __get_player_per_id(self, player_id: int) -> Player:
        for player in self.__players:
            if player.get_id() == player_id:
                return player

    def leaderboard(self):
        players_score = {}
        for player in self.__players:
            players_score[player] = player.get_points()
        return dict(sorted(players_score.items(), key=lambda x: x[1], reverse=True))