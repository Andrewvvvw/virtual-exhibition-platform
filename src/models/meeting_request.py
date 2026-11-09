class MeetingRequest:
    def __init__(self, id: int = 0, slot: str = "", status: str = "") -> None:
        self.__id = id
        self.__slot = slot
        self.__status = status

    def confirm(self) -> None:
        pass

    def reject(self) -> None:
        pass
