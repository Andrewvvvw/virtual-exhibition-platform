from src.repositories.database_repository import DatabaseRepository


class MeetingService:
    def __init__(self, repository: DatabaseRepository, storageUrl: str = "",
                 slotDurationMin: int = 30) -> None:
        self.__storageUrl = storageUrl
        self.__slotDurationMin = slotDurationMin
        self.__repository = repository

    def uploadAttachment(self, file: str) -> str:
        return ""

    def createMeeting(self, vId: int, sId: int, slot: str) -> int:
        return 0

    def confirmMeeting(self, reqId: int) -> None:
        pass

    def notifyNewRequest(self, reqId: int, slot: str) -> None:
        pass
