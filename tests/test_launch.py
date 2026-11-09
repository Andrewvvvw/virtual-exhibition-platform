import os
import subprocess
import sys
import unittest
from pathlib import Path


class LaunchTests(unittest.TestCase):
    def test_module_starts_and_event_loop_exits_on_close_and_ctrl_c(self):
        for action in ("close", "sigint"):
            with self.subTest(action=action):
                code = f'''
import os
import runpy
import signal
import sys
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

original_exec = QApplication.exec

def checked_exec(self):
    windows = [w for w in self.topLevelWidgets() if w.isVisible()]
    assert len(windows) == 1
    assert windows[0].currentPage == 'login'
    if {action!r} == 'close':
        QTimer.singleShot(0, windows[0].close)
    else:
        QTimer.singleShot(0, lambda: os.kill(os.getpid(), signal.SIGINT))
    QTimer.singleShot(3000, lambda: self.exit(99))
    return original_exec()

QApplication.exec = checked_exec
sys.argv = ['src.main']
runpy.run_module('src.main', run_name='__main__')
'''
                result = subprocess.run(
                    [sys.executable, "-c", code],
                    cwd=Path(__file__).resolve().parents[1],
                    env={**os.environ, "QT_QPA_PLATFORM": "offscreen"},
                    capture_output=True, text=True, timeout=10,
                )
                self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
