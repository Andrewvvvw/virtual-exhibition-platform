from abc import ABC, abstractmethod

from PySide6.QtWidgets import QWidget


class IStandRenderer(ABC):
    widget: QWidget

    def __init__(self, viewportScale: float = 1.0) -> None:
        self.viewportScale = viewportScale

    @abstractmethod
    def renderStandView(self, standId: int) -> None:
        pass
