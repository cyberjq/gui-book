from PyQt5.QtWidgets import QMessageBox


def show_error(text: str, title: str = "Ошибка"):
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(text)
    msg.setIcon(QMessageBox.Warning)
    msg.show()
    msg.exec()
    return