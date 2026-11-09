from collections.abc import Callable

from PySide6.QtCore import QDate, Qt, QTime
from PySide6.QtWidgets import (
    QComboBox, QDateEdit, QFormLayout, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QPushButton, QScrollArea, QStackedWidget, QTimeEdit,
    QVBoxLayout, QWidget,
)

from src.controllers.meeting_controller import MeetingController
from src.ui.stand_renderer import IStandRenderer


class StandUI(QMainWindow):
    """Экраны по макетам и демонстрационный просмотр экспоната."""

    def __init__(self, controller: MeetingController, renderer: IStandRenderer) -> None:
        super().__init__()
        self.__currentStandId = 0
        self.__selectedTimeSlot = ""
        self.__controller = controller
        self.__renderer = renderer
        self._notificationReturn = "menu"
        self.setObjectName("standWindow")
        self.resize(760, 780)
        self.setMinimumSize(560, 620)
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        self._pages: dict[str, QWidget] = {}
        self._buildLoginPage()
        self._buildMenuPage()
        self._buildExhibitionPage()
        self._buildVisitPage()
        self._buildStandPage()
        self._buildNotificationPage()
        self.setStyleSheet("""
            QWidget { background: #f8fafc; color: #18263d; font-size: 15px; }
            QLabel#pageHeading { font-size: 21px; font-weight: 700; padding: 12px 0; }
            QLabel#identity, QLabel#notificationMessage {
                background: white; border: 1px solid #95a4ba;
                border-radius: 6px; padding: 14px;
            }
            QFrame#exhibitCard {
                background: white; border: 1px solid #95a4ba; border-radius: 8px;
            }
            QLabel#exhibitPreview {
                background: #e2e8f0; color: #334155; border-radius: 6px;
                font-size: 19px; font-weight: 700; padding: 12px;
            }
            QLabel#exhibitTitle, QLabel#exhibitPrice {
                font-size: 21px; font-weight: 700;
            }
            QLineEdit, QComboBox, QDateEdit, QTimeEdit {
                background: white; border: 1px solid #8b9bb2; border-radius: 4px;
                padding: 6px; min-height: 20px;
            }
            QPushButton {
                background: #edf2f7; border: 1px solid #6b7d98; border-radius: 5px;
                min-height: 24px; padding: 9px 16px;
            }
            QPushButton[primary="true"] { background: #dbeafe; border: 1px solid #3453ad; }
            QPushButton:hover { background: #cdddf5; }
            QScrollArea { border: none; }
        """)

    def _page(self, key: str, heading: str) -> QVBoxLayout:
        scroll = QScrollArea()
        scroll.setObjectName(f"{key}Page")
        scroll.setWidgetResizable(True)
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(30, 20, 30, 24)
        layout.setSpacing(14)
        title = QLabel(heading)
        title.setObjectName("pageHeading")
        title.setWordWrap(True)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        scroll.setWidget(content)
        self._pages[key] = scroll
        self.stack.addWidget(scroll)
        return layout

    def _button(self, name: str, text: str, callback: Callable,
                primary: bool = False) -> QPushButton:
        button = QPushButton(text)
        button.setObjectName(name)
        button.setProperty("primary", primary)
        button.clicked.connect(lambda _checked=False: callback())
        return button

    def _showPage(self, key: str) -> None:
        titles = {
            "login": "Вход / Регистрация пользователя",
            "menu": "Главное окно платформы",
            "exhibition": "Выставка (подключение)",
            "visit": "Просмотр выставки",
            "stand": "Создание стенда",
            "notification": "Уведомление",
        }
        self.stack.setCurrentWidget(self._pages[key])
        self.setWindowTitle(f"{titles[key]} — Виртуальные выставки и ярмарки")

    @property
    def currentPage(self) -> str:
        return next(key for key, page in self._pages.items()
                    if page is self.stack.currentWidget())

    def _buildLoginPage(self) -> None:
        layout = self._page("login", "Авторизация и регистрация в системе")
        layout.addStretch()
        form = QFormLayout()
        form.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapAllRows)
        form.setVerticalSpacing(20)
        self.loginEdit = QLineEdit("Демо-посетитель")
        self.loginEdit.setObjectName("loginEdit")
        self.loginEdit.setPlaceholderText("Введите логин или ФИО")
        self.passwordEdit = QLineEdit()
        self.passwordEdit.setObjectName("passwordEdit")
        self.passwordEdit.setEchoMode(QLineEdit.EchoMode.Password)
        self.passwordEdit.returnPressed.connect(self._signIn)
        self.roleCombo = QComboBox()
        self.roleCombo.setObjectName("roleCombo")
        self.roleCombo.addItems(["Посетитель", "Экспонент", "Организатор"])
        form.addRow("Логин / ФИО пользователя:", self.loginEdit)
        form.addRow("Пароль:", self.passwordEdit)
        form.addRow("Роль (Посетитель / Экспонент / Организатор):", self.roleCombo)
        layout.addLayout(form)
        layout.addStretch()
        buttons = QHBoxLayout()
        buttons.addWidget(self._button("signInButton", "Войти / Регистрация", self._signIn, True))
        buttons.addWidget(self._button("loginExitButton", "Выход", self.close))
        layout.addLayout(buttons)

    def _buildMenuPage(self) -> None:
        layout = self._page("menu", "Главное окно платформы")
        self.identityLabel = QLabel()
        self.identityLabel.setObjectName("identity")
        self.identityLabel.setTextFormat(Qt.TextFormat.PlainText)
        self.identityLabel.setWordWrap(True)
        layout.addWidget(self.identityLabel)
        layout.addStretch()
        choose = QLabel("Выберите действие:")
        choose.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(choose)
        layout.addWidget(self._button(
            "findExhibitionButton", "Найти выставку (Подключиться / Создать)",
            lambda: self.renderStandPage(1), True))
        layout.addWidget(self._button(
            "createStandButton", "Создать стенд", lambda: self._showPage("stand"), True))
        layout.addStretch()
        layout.addWidget(self._button(
            "logoutButton", "Выйти из аккаунта (Назад)", self.renderStartPage))

    def _buildExhibitionPage(self) -> None:
        layout = self._page("exhibition", "Выставка (подключение)")
        layout.addStretch()
        form = QFormLayout()
        form.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapAllRows)
        form.setVerticalSpacing(20)
        self.exhibitionCombo = QComboBox()
        self.exhibitionCombo.setObjectName("exhibitionCombo")
        self.exhibitionCombo.setEditable(True)
        self.exhibitionCombo.addItem("TechExpo 2026 (ID: 1)")
        self.dateEdit = QDateEdit(QDate(2026, 10, 20))
        self.dateEdit.setObjectName("dateEdit")
        self.dateEdit.setDisplayFormat("dd.MM.yyyy")
        self.dateEdit.setCalendarPopup(True)
        self.slotEdit = QTimeEdit(QTime(14, 0))
        self.slotEdit.setObjectName("slotEdit")
        self.slotEdit.setDisplayFormat("HH:mm")
        self.ticketEdit = QLineEdit("TX-8492")
        self.ticketEdit.setObjectName("ticketEdit")
        parameters = QHBoxLayout()
        parameters.addWidget(self.slotEdit)
        parameters.addWidget(self.ticketEdit)
        form.addRow("Выставка (title / id):", self.exhibitionCombo)
        form.addRow("Дата проведения (startDate):", self.dateEdit)
        form.addRow("Параметры (слот slot / код билета):", parameters)
        layout.addLayout(form)
        layout.addStretch()
        layout.addWidget(self._button(
            "connectButton", "Подключиться / Создать выставку",
            self._connectExhibition, True))
        layout.addWidget(self._button(
            "exhibitionBackButton", "Назад в Главное окно", self._renderMenu))

    def _buildVisitPage(self) -> None:
        layout = self._page("visit", "Выставка · стенд и экспонаты")
        self.visitExhibitionLabel = QLabel()
        self.visitExhibitionLabel.setObjectName("visitExhibitionLabel")
        self.visitExhibitionLabel.setTextFormat(Qt.TextFormat.PlainText)
        self.visitExhibitionLabel.setWordWrap(True)
        layout.addWidget(self.visitExhibitionLabel)
        layout.addWidget(self.__renderer.widget)
        layout.addStretch()
        layout.addWidget(self._button(
            "requestMeetingButton", "Запросить консультацию",
            self._requestDemoMeeting, True))
        buttons = QHBoxLayout()
        buttons.addWidget(self._button(
            "visitBackButton", "Назад к выбору выставки",
            lambda: self._showPage("exhibition")))
        buttons.addWidget(self._button(
            "visitMenuButton", "В главное меню", self._renderMenu))
        layout.addLayout(buttons)

    def _buildStandPage(self) -> None:
        layout = self._page("stand", "Создание стенда")
        layout.addStretch()
        form = QFormLayout()
        form.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapAllRows)
        form.setVerticalSpacing(20)
        self.standNumberEdit = QLineEdit("A-104")
        self.standNumberEdit.setObjectName("standNumberEdit")
        self.companyEdit = QLineEdit("ООО БелПромАвтоматика")
        self.companyEdit.setObjectName("companyEdit")
        self.exhibitEdit = QLineEdit("Контроллер ПЛК-500 / 2450 BYN")
        self.exhibitEdit.setObjectName("exhibitEdit")
        form.addRow("Номер стенда (standNumber):", self.standNumberEdit)
        form.addRow("Компания (companyName):", self.companyEdit)
        form.addRow("Экспонат и цена (title / price):", self.exhibitEdit)
        layout.addLayout(form)
        layout.addStretch()
        layout.addWidget(self._button(
            "saveStandButton", "Сохранить / Создать стенд",
            lambda: self.showSuccessMessage("Стенд успешно создан"), True))
        layout.addWidget(self._button(
            "standBackButton", "Назад в Главное окно", self._renderMenu))

    def _buildNotificationPage(self) -> None:
        layout = self._page("notification", "Уведомление")
        layout.addStretch()
        self.notificationTitle = QLabel()
        self.notificationTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.notificationTitle.setWordWrap(True)
        self.notificationMessage = QLabel()
        self.notificationMessage.setObjectName("notificationMessage")
        self.notificationMessage.setTextFormat(Qt.TextFormat.PlainText)
        self.notificationMessage.setWordWrap(True)
        layout.addWidget(self.notificationTitle)
        layout.addWidget(self.notificationMessage)
        layout.addStretch()
        self.notificationOkButton = self._button(
            "notificationOkButton", "OK (В главное окно)", self._closeNotification, True)
        layout.addWidget(self.notificationOkButton)
        layout.addWidget(self._button(
            "notificationExitButton", "Выход из программы", self.close))

    def renderStartPage(self) -> None:
        self.__currentStandId = 0
        self.__selectedTimeSlot = ""
        self.passwordEdit.setText("demo")
        self._showPage("login")
        self.show()

    def _signIn(self) -> None:
        name = self.loginEdit.text() or "Пользователь"
        self.identityLabel.setText(
            f"Вы вошли как: {name} (Роль: {self.roleCombo.currentText()})")
        self._renderMenu()

    def _renderMenu(self) -> None:
        self._showPage("menu")

    def renderStandPage(self, standId: int) -> None:
        self.__currentStandId = standId
        self.__controller.loadStandDetails(standId)
        self.__renderer.renderStandView(standId)
        self._showPage("exhibition")

    def _connectExhibition(self) -> None:
        if self.roleCombo.currentText() == "Посетитель":
            self.visitExhibitionLabel.setText(self.exhibitionCombo.currentText())
            self.__renderer.renderStandView(self.__currentStandId)
            self._showPage("visit")
        else:
            self.showSuccessMessage("Подключение к выставке / Выставка создана")

    def _requestDemoMeeting(self) -> None:
        self.clickRequestMeeting(
            self.__currentStandId, self.slotEdit.time().toString("HH:mm"))
        self._notificationReturn = "visit"
        self.notificationOkButton.setText("OK (На выставку)")

    def clickRequestMeeting(self, sId: int, slot: str) -> None:
        self.__currentStandId = sId
        self.__selectedTimeSlot = slot
        self.__controller.requestConsultation(0, sId, slot)
        self.showSuccessMessage(f"Заявка на консультацию отправлена. Время: {slot}.")

    def showSuccessMessage(self, msg: str) -> None:
        self._notificationReturn = "menu"
        self.notificationTitle.setText("Операция успешно выполнена!")
        self.notificationMessage.setText(msg)
        self.notificationOkButton.setText("OK (В главное окно)")
        self._showPage("notification")

    def showErrorMessage(self, err: str) -> None:
        if self.currentPage != "notification":
            self._notificationReturn = self.currentPage
        self.notificationTitle.setText("Операция не выполнена")
        self.notificationMessage.setText(err)
        self.notificationOkButton.setText("OK (Назад)")
        self._showPage("notification")

    def _closeNotification(self) -> None:
        self._showPage(self._notificationReturn)
