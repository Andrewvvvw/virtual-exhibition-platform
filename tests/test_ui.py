import os
import sys
import unittest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import Qt
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication, QLabel, QPushButton

from src.core.app_injector import AppInjector


class UITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])
        cls.app.setQuitOnLastWindowClosed(False)

    def setUp(self):
        self.slotErrors = []
        old_hook = sys.excepthook
        sys.excepthook = lambda _kind, value, _trace: self.slotErrors.append(str(value))
        self.addCleanup(setattr, sys, "excepthook", old_hook)
        self.addCleanup(lambda: self.assertEqual(self.slotErrors, []))
        injector = AppInjector()
        injector.configureServices()
        self.ui = injector.createStandUI()
        self.addCleanup(self.ui.close)
        self.ui.renderStartPage()
        self.app.processEvents()

    def click(self, name):
        button = self.ui.findChild(QPushButton, name)
        self.assertIsNotNone(button, name)
        self.assertTrue(button.isEnabled(), name)
        QTest.mouseClick(button, Qt.MouseButton.LeftButton)
        self.app.processEvents()

    def test_navigation_and_back_buttons_for_every_role(self):
        self.assertEqual(self.ui.stack.count(), 6)
        for role in ("Посетитель", "Экспонент", "Организатор"):
            with self.subTest(role=role):
                self.ui.roleCombo.setCurrentText(role)
                self.click("signInButton")
                self.assertEqual(self.ui.currentPage, "menu")
                self.assertIn(role, self.ui.identityLabel.text())
                self.click("findExhibitionButton")
                self.assertEqual(self.ui.currentPage, "exhibition")
                self.click("exhibitionBackButton")
                self.assertEqual(self.ui.currentPage, "menu")
                self.click("createStandButton")
                self.assertEqual(self.ui.currentPage, "stand")
                self.click("standBackButton")
                self.assertEqual(self.ui.currentPage, "menu")
                self.click("logoutButton")
                self.assertEqual(self.ui.currentPage, "login")

    def test_form_actions_only_navigate_without_validation(self):
        # Пустые поля не блокируют переходы в макете интерфейса.
        self.click("signInButton")
        self.click("findExhibitionButton")
        self.ui.ticketEdit.clear()
        self.click("connectButton")
        self.assertEqual(self.ui.currentPage, "visit")
        self.click("requestMeetingButton")
        self.assertEqual(self.ui.currentPage, "notification")
        self.assertIn("консультацию", self.ui.notificationMessage.text())
        self.click("notificationOkButton")
        self.assertEqual(self.ui.currentPage, "visit")
        self.click("visitMenuButton")
        self.assertEqual(self.ui.currentPage, "menu")
        self.click("createStandButton")
        self.ui.standNumberEdit.clear()
        self.ui.companyEdit.clear()
        self.ui.exhibitEdit.clear()
        self.click("saveStandButton")
        self.assertEqual(self.ui.currentPage, "notification")
        self.click("notificationOkButton")
        self.assertEqual(self.ui.currentPage, "menu")

    def test_visitor_demo_requires_no_typing(self):
        self.assertEqual(self.ui.roleCombo.currentText(), "Посетитель")
        self.assertTrue(self.ui.loginEdit.text())
        self.assertTrue(self.ui.passwordEdit.text())
        self.click("signInButton")
        self.click("findExhibitionButton")
        self.click("connectButton")
        self.assertEqual(self.ui.currentPage, "visit")
        title = self.ui.findChild(QLabel, "exhibitTitle")
        self.assertTrue(title.isVisible())
        self.assertEqual(title.text(), "Контроллер ПЛК-500")
        self.assertIn("2 450 BYN", self.ui.findChild(QLabel, "exhibitPrice").text())
        self.click("requestMeetingButton")
        self.assertEqual(self.ui.currentPage, "notification")
        self.assertIn("14:00", self.ui.notificationMessage.text())
        self.click("notificationOkButton")
        self.assertEqual(self.ui.currentPage, "visit")
        self.click("visitBackButton")
        self.assertEqual(self.ui.currentPage, "exhibition")
        self.click("connectButton")
        self.assertEqual(self.ui.currentPage, "visit")
        self.assertEqual(len(self.ui.findChildren(QLabel, "exhibitTitle")), 1)

    def test_error_notification_returns_to_original_form(self):
        self.click("signInButton")
        self.click("createStandButton")
        self.ui.showErrorMessage("Пример сообщения об ошибке")
        self.assertEqual(self.ui.currentPage, "notification")
        self.click("notificationOkButton")
        self.assertEqual(self.ui.currentPage, "stand")

    def test_exit_from_login_and_notification(self):
        self.click("loginExitButton")
        self.assertFalse(self.ui.isVisible())
        self.ui.renderStartPage()
        self.ui.showSuccessMessage("Проверка")
        self.click("notificationExitButton")
        self.assertFalse(self.ui.isVisible())


if __name__ == "__main__":
    unittest.main()
