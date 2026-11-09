from src.models import MeetingRequest, Stand, Ticket


class DatabaseRepository:
    """Контракт репозитория из модели; подключение к БД не выполняется."""

    def __init__(self, connectionUrl: str = "", poolSize: int = 1) -> None:
        self.__connectionUrl = connectionUrl
        self.__poolSize = poolSize

    def findActiveTicket(self, vId: int, exhId: int) -> Ticket:
        return Ticket()

    def save(self, req: MeetingRequest) -> int:
        return 0

    def updateStatus(self, reqId: int, status: str) -> None:
        pass

    def findStandById(self, standId: int) -> Stand:
        return Stand(id=standId)
