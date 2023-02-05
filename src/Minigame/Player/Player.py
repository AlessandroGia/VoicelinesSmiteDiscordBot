class Player:
    def __init__(self, id: int, nickname: str) -> None:
        self.__id: int = id
        self.__points: int = 0
        self.__nickname: str = nickname

    def get_id(self) -> int:
        return self.__id

    def get_points(self) -> int:
        return self.__points

    def get_nickname(self) -> str:
        return self.__nickname

    def add_point(self) -> None:
        self.__points += 1

