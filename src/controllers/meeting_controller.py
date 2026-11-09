from src.models import Stand
from src.services.meeting_service import MeetingService
from src.services.ticket_service import TicketService


class MeetingController:
    def __init__(self, ticketService: TicketService, meetingService: MeetingService,
                 maxAttachmentMb: int = 10, sessionTimeoutSec: int = 1800) -> None:
        self.__maxAttachmentMb = maxAttachmentMb
        self.__sessionTimeoutSec = sessionTimeoutSec
        self.__ticketService = ticketService
        self.__meetingService = meetingService

    def requestConsultation(self, vId: int, sId: int, slot: str) -> None:
        pass

    def loadStandDetails(self, standId: int) -> Stand:
        return Stand(id=standId)
