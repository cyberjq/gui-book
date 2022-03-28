import asyncio
import sys
from PyQt5.QtWidgets import QApplication
from app.app import Ui_MainWindow
from asyncqt import QEventLoop


def start_app():
    app = QApplication(sys.argv)
    # loop = QEventLoop(app)
    # asyncio.set_event_loop(loop)

    window = Ui_MainWindow()
    window.show()

    app.exec()

    # with loop:
    #     sys.exit(loop.run_forever())


if __name__ == '__main__':
    start_app()


