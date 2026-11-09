from src.models import Ticket
from src.repositories.database_repository import DatabaseRepository


class TicketService:
    def __init__(self, repository: DatabaseRepository, ticketPrefix: str = "TX",
                 maxTicketsPerUser: int = 10) -> None:
        self.__ticketPrefix = ticketPrefix
        self.__maxTicketsPerUser = maxTicketsPerUser
        self.__repository = repository

    def validateTicket(self, vId: int, exhId: int) -> bool:
        return False

    def issueTicket(self, vId: int, exhId: int) -> Ticket:
        return Ticket()
