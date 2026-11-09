from src.models.exhibit import Exhibit


class Stand:
    def __init__(self, id: int = 0, standNumber: str = "", companyName: str = "",
                 rentalStatus: str = "", exhibits: list[Exhibit] | None = None) -> None:
        self.__id = id
        self.__standNumber = standNumber
        self.__companyName = companyName
        self.__rentalStatus = rentalStatus
        self.__exhibits = list(exhibits or [])

    def publishStand(self) -> None:
        pass

    def isAvailable(self) -> bool:
        return False
