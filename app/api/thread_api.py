import asyncio

from PyQt5.QtCore import QThread


class BookApiThread(QThread):

    def __init__(self):
        super().__init__()
        self.__loop = asyncio.get_event_loop()

