import signal
import sys

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

from src.controllers.meeting_controller import MeetingController
from src.repositories.database_repository import DatabaseRepository
from src.services.meeting_service import MeetingService
from src.services.ticket_service import TicketService
from src.ui.catalog_2d_renderer import Catalog2DRenderer
from src.ui.stand_ui import StandUI


class AppInjector:
    def __init__(self, configPath: str = "") -> None:
        self.__configPath = configPath
        self.__isInitialized = False

    def configureServices(self) -> None:
        if self.__isInitialized:
            return
        repository = DatabaseRepository()
        ticket_service = TicketService(repository)
        meeting_service = MeetingService(repository)
        self.__controller = MeetingController(ticket_service, meeting_service)
        self.__renderer = Catalog2DRenderer()
        self.__isInitialized = True

    def createStandUI(self) -> StandUI:
        self.configureServices()
        return StandUI(self.__controller, self.__renderer)

    @staticmethod
    def main(args: list[str] | None = None) -> int:
        app = QApplication(sys.argv if args is None else args)
        app.setApplicationName("Виртуальные выставки и ярмарки")
        injector = AppInjector()
        injector.configureServices()
        ui = injector.createStandUI()
        ui.renderStartPage()

        # Даём Python обработать Ctrl+C во время цикла событий Qt.
        timer = QTimer()
        timer.timeout.connect(lambda: None)
        timer.start(200)
        old_handler = signal.signal(signal.SIGINT, lambda *_args: app.quit())
        try:
            return app.exec()
        finally:
            signal.signal(signal.SIGINT, old_handler)
            timer.stop()
