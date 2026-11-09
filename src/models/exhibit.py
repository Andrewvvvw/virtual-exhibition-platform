class Exhibit:
    def __init__(self, id: int = 0, title: str = "", price: float = 0.0) -> None:
        self.__id = id
        self.__title = title
        self.__price = price

    def getSpec(self) -> str:
        return ""

    def setPrice(self, p: float) -> None:
        pass
