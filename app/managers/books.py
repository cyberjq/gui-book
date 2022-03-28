from PyQt5 import QtWidgets

from app.api.sync_api import SyncBookApi
from app.error import show_error
from app.models.books import BooksModel


class BookManager:

    def __init__(self, main_window):
        self.__books = []
        self.__book_api = SyncBookApi()
        self.__main_window = main_window

        self.__table_view: QtWidgets.QTableView = main_window.booksTableView
        self.__table_view.clicked.connect(self.__select_changed)

        self.__name_line_edit: QtWidgets.QLineEdit = main_window.nameLineEdit
        self.__printing_year_line_edit: QtWidgets.QLineEdit = main_window.printingYearLineEdit
        self.__isbn_line_edit: QtWidgets.QLineEdit = main_window.isbnLineEdit

        self.__filter_name: QtWidgets.QLineEdit = main_window.filterNameLineEdit
        self.__filter_year_start: QtWidgets.QLineEdit = main_window.filterYearStartLineEdit
        self.__filter_year_end: QtWidgets.QLineEdit = main_window.filterYearEndLIneEdit

        self.__add_button: QtWidgets.QPushButton = main_window.addBookPushButton
        # self.__update_button: QtWidgets.QPushButton = main_window.updateBookPushButton
        self.__delete_button: QtWidgets.QPushButton = main_window.deleteBookPushButton
        self.__filter_button: QtWidgets.QPushButton = main_window.filterBookPushButton
        self.__refresh_button: QtWidgets.QPushButton = main_window.refreshBookPushButton

        self.__subject_combobox: QtWidgets.QComboBox = main_window.subjectComboBox
        self.__author_combobox: QtWidgets.QComboBox = main_window.authorComboBox
        self.__publishing_house_combobox: QtWidgets.QComboBox = main_window.publishingHouseComboBox

        self.__add_button.clicked.connect(self.__add)
        # self.__update_button.clicked.connect(self.__update)
        self.__delete_button.clicked.connect(self.__delete)
        self.__refresh_button.clicked.connect(self.__refresh)
        self.__filter_button.clicked.connect(self.__filter)

        self.__init_data()
        self.__refresh()

        self.__selected_book = {}

    def __init_data(self):
        self.__authors = self.__book_api.get_authors()
        self.__subjects = self.__book_api.get_subjects()
        self.__publishing_houses = self.__book_api.get_publishing_houses()
        self.__refresh_combobox()

    def __refresh_combobox(self):
        self.__author_combobox.clear()
        self.__subject_combobox.clear()
        self.__publishing_house_combobox.clear()

        for i, a in enumerate(self.__authors):
            self.__author_combobox.addItem(f"{a['last_name']} {a['first_name']} {a['middle_name']}", a)
            self.__author_combobox.setItemChecked(i, False)

        for i, s in enumerate(self.__subjects):
            self.__subject_combobox.addItem(str(s["name"]), s)
            self.__subject_combobox.setItemChecked(i, False)

        for i, ph in enumerate(self.__publishing_houses):
            self.__publishing_house_combobox.addItem(str(ph["name"]), ph)

    def __check_fields(self, **kwargs):
        if not kwargs.get("name"):
            show_error("Не указано название книги")
            return False

        elif not kwargs.get("isbn"):
            show_error("Не указан ISBN")
            return False

        elif kwargs.get("printing_year") and not kwargs.get("printing_year").isdigit():
            show_error("Год публикации только целое число")
            return False

        elif not kwargs.get("publishing_house"):
            show_error("Не выбрано издательство")
            return False

        elif not kwargs.get("authors"):
            show_error("Нужно выбрать хотя бы одного автора")
            return False

        elif not kwargs.get("subjects"):
            show_error("Нужно выбрать хотя бы один жанр")
            return False

        return True

    def __add(self):
        name = self.__name_line_edit.text()
        isbn = self.__isbn_line_edit.text()
        printing_year = self.__printing_year_line_edit.text()

        authors = [self.__author_combobox.itemData(i) for i in range(self.__author_combobox.count())
                   if self.__author_combobox.itemChecked(i)]

        subjects = [self.__subject_combobox.itemData(i) for i in range(self.__subject_combobox.count())
                    if self.__subject_combobox.itemChecked(i)]

        publishing_house = self.__publishing_house_combobox.currentData()

        is_ok = self.__check_fields(name=name, isbn=isbn, printing_year=printing_year,
                                    publishing_house=publishing_house, authors=authors, subjects=subjects)
        if not is_ok:
            return

        book = {
            "name": name,
            "printing_year": printing_year,
            "isbn": isbn,
            "publishing_house_id": publishing_house["pub_house_id"],
            "publishing_house": publishing_house,
            "subjects": subjects,
            "authors": authors
        }

        self.__book_api.create_book(book)
        self.__refresh()

    def __select_changed(self, item):

        indexes = self.__table_view.selectedIndexes()
        book_id = indexes[0].data()
        if self.__books:
            self.__selected_book = [b for b in self.__books if b["book_id"] == book_id][-1]

        # self.__name_line_edit.setText(self.__selected_book["name"])
        # self.__printing_year_line_edit.setText(str(self.__selected_book["printing_year"]))
        # self.__isbn_line_edit.setText(self.__selected_book["isbn"])
        #
        # author_ids = [a["author_id"] for a in self.__selected_book["authors"]]
        # for i in range(self.__author_combobox.count()):
        #     data = self.__author_combobox.itemData(i)
        #     if data["author_id"] in author_ids:
        #         self.__author_combobox.setItemChecked(i, True)
        #     else:
        #         self.__author_combobox.setItemChecked(i, False)
        #
        # subject_ids = [s["subject_id"] for s in self.__selected_book["subjects"]]
        # for i in range(self.__subject_combobox.count()):
        #     data = self.__subject_combobox.itemData(i)
        #     if data["subject_id"] in subject_ids:
        #         self.__subject_combobox.setItemChecked(i, True)
        #     else:
        #         self.__subject_combobox.setItemChecked(i, False)
        #
        # for i in range(self.__publishing_house_combobox.count()):
        #     data = self.__publishing_house_combobox.itemData(i)
        #     if data["pub_house_id"] == self.__selected_book["publishing_house"]["pub_house_id"]:
        #         self.__subject_combobox.setCurrentText(self.__selected_book["publishing_house"]["name"])

    def __filter(self):
        year_start = self.__filter_year_start.text()
        year_end = self.__filter_year_end.text()
        name = self.__filter_name.text()

        if not name and not year_end and not year_start:
            show_error("Заполните одно хотя быполе для фильтрации")
            return

        if year_start and not year_start.isdigit():
            show_error("Поле 'Год издания с...' принимает только целое число")
            return


        if year_end and not year_end.isdigit():
            show_error("Поле 'Год издания до...' принимает только целое число")
            return


        self.__books = self.__book_api.filter_book({"name": name, "printing_year_start": year_start,
                                                    "printing_year_end": year_end})
        self.__refresh(is_actual=False)

    def __update(self):
        name = self.__name_line_edit.text()
        isbn = self.__isbn_line_edit.text()
        printing_year = self.__printing_year_line_edit.text()

        authors = [self.__author_combobox.itemData(i) for i in range(self.__author_combobox.count())
                   if self.__author_combobox.itemChecked(i)]

        subjects = [self.__subject_combobox.itemData(i) for i in range(self.__subject_combobox.count())
                    if self.__subject_combobox.itemChecked(i)]

        publishing_house = self.__publishing_house_combobox.currentData()

        is_ok = self.__check_fields(name=name, isbn=isbn, printing_year=printing_year,
                                    publishing_house=publishing_house, authors=authors, subjects=subjects)
        if not is_ok:
            return

        self.__selected_book["name"] = name
        self.__selected_book["printing_year"] = printing_year
        self.__selected_book["isbn"] = isbn
        self.__selected_book["publishing_house_id"] = publishing_house["pub_house_id"]
        self.__selected_book["publishing_house"] = publishing_house
        self.__selected_book["subjects"] = subjects
        self.__selected_book["authors"] = authors
        self.__book_api.update_book(self.__selected_book)
        self.__refresh()

    def __delete(self):
        if not self.__selected_book:
            show_error("Не выбрана строка для удаления")

        self.__book_api.delete_book(self.__selected_book)
        self.__refresh()
        self.__selected_book = {}

    @staticmethod
    def __get_books_data(books):
        return [
            {
                "book_id": book["book_id"],
                "name": book["name"],
                "printing_year": book["printing_year"],
                "isbn": book["isbn"],
                "authors": "; ".join(
                    [f"{a['last_name']} {a['first_name']} {a['middle_name']}" for a in book["authors"]]),
                "subjects": "; ".join([s['name'] for s in book["subjects"]]),
                "publishing_house": book["publishing_house"]["name"]
            } for book in books
        ]

    def __refresh(self, book: dict = None, is_actual: bool = True):
        if is_actual:
            self.__books = self.__book_api.get_books()

        if self.__books:
            data = self.__get_books_data(self.__books)
            model = BooksModel(data)
            self.__table_view.setModel(model)
            self.__table_view.clearSelection()
        else:

            show_error("Нет данных удовлетворяющих запросу")

            model = BooksModel([
                {
                    "book_id": "",
                    "name": "",
                    "printing_year": "",
                    "isbn": "",
                    "authors": "",
                    "subjects": "",
                    "publishing_house": ""
                }
            ])

            self.__table_view.setModel(model)
            self.__table_view.clearSelection()

        self.__refresh_combobox()
