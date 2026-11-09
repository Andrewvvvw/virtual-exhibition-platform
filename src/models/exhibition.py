from src.models.stand import Stand


class Exhibition:
    def __init__(self, id: int = 0, title: str = "", startDate: str = "",
                 status: str = "", stands: list[Stand] | None = None) -> None:
        self.__id = id
        self.__title = title
        self.__startDate = startDate
        self.__status = status
        self.__stands = list(stands or [])

    def isOpen(self) -> bool:
        return False

    def activate(self) -> None:
        pass
