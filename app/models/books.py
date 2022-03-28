from PyQt5.QtCore import QAbstractTableModel, Qt


class BooksModel(QAbstractTableModel):

    def __init__(self, data):
        super().__init__()
        self.__data = data
        self.__columns = ["Ид книги", "Название", "Год издания", "ISBN", "Авторы", "Жанры", "Издательство"]

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return list(self.__data[index.row()].values())[index.column()] if self.__data else list()

    def rowCount(self, index):
        # The length of the outer list.
        return len(self.__data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self.__data[0])

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self.__columns[section])

            # if orientation == Qt.Vertical:
            #     return str(self._data.index[section])
