from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QWidget

from src.models import Stand
from src.ui.stand_renderer import IStandRenderer


class Catalog2DRenderer(IStandRenderer):
    def __init__(self, stands: list[Stand] | None = None,
                 layoutTemplate: str = "", cardsPerPage: int = 6) -> None:
        super().__init__()
        self.__layoutTemplate = layoutTemplate
        self.__cardsPerPage = cardsPerPage
        self.__stands = list(stands or [])
        self.widget = QWidget()
        self.widget.setObjectName("standCatalog")
        layout = QVBoxLayout(self.widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(18)
        self._standLabel = QLabel()
        self._standLabel.setObjectName("catalogStandLabel")
        self._standLabel.setWordWrap(True)
        layout.addWidget(self._standLabel)

        card = QFrame()
        card.setObjectName("exhibitCard")
        contents = QVBoxLayout(card)
        contents.setContentsMargins(20, 20, 20, 20)
        contents.setSpacing(12)
        device = QLabel("ПЛК-500\n●  ●  ●  ●\nПромышленный контроллер")
        device.setObjectName("exhibitPreview")
        device.setAlignment(Qt.AlignmentFlag.AlignCenter)
        device.setMinimumHeight(100)
        contents.addWidget(device)
        title = QLabel("Контроллер ПЛК-500")
        title.setObjectName("exhibitTitle")
        title.setWordWrap(True)
        contents.addWidget(title)
        description = QLabel(
            "Программируемый логический контроллер для автоматизации "
            "производственных линий и управления оборудованием.\n\n"
            "Питание: 24 В\nДискретные входы: 16\nДискретные выходы: 8\n"
            "Интерфейсы: Ethernet, RS-485")
        description.setObjectName("exhibitDescription")
        description.setWordWrap(True)
        contents.addWidget(description)
        price = QLabel("2 450 BYN")
        price.setObjectName("exhibitPrice")
        contents.addWidget(price)
        layout.addWidget(card)

    def renderStandView(self, standId: int) -> None:
        self._standLabel.setText("Стенд A-104 · ООО БелПромАвтоматика")
