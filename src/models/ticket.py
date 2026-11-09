class Ticket:
    def __init__(self, id: int = 0, accessCode: str = "", status: str = "") -> None:
        self.__id = id
        self.__accessCode = accessCode
        self.__status = status

    def isActive(self) -> bool:
        return False

    def revoke(self) -> None:
        pass
