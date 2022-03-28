from datetime import datetime

from pip._vendor import requests
from config import config


class SyncBookApiMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Данная реализация не учитывает возможное изменение передаваемых
        аргументов в `__init__`.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class SyncBookApi(metaclass=SyncBookApiMeta):

    def __init__(self):
        self.__session = requests.Session()

    def __execute_response(self, response, **kwargs):
        if response.status_code == 200:
            data = response.json()

            return data

        return None

    def get_subjects(self, subject_id: int = None):

        if subject_id is None:
            subject_id = ""

        response = self.__session.get(f"{config.URL_SUBJECTS}{subject_id}")
        return self.__execute_response(response)

    def create_subject(self, subject: dict = None):
        response = self.__session.post(f"{config.URL_SUBJECTS}", json=subject)
        return self.__execute_response(response)

    def update_subject(self, subject: dict = None):
        response = self.__session.put(f"{config.URL_SUBJECTS}", json=subject)
        return self.__execute_response(response)

    def delete_subject(self, subject: dict = None):
        response = self.__session.delete(f"{config.URL_SUBJECTS}", json=subject)
        return self.__execute_response(response)

    def get_authors(self, author_id: int = None):

        if author_id is None:
            author_id = ""

        response = self.__session.get(f"{config.URL_AUTHORS}{author_id}")
        return self.__execute_response(response)

    def create_author(self, author: dict = None):
        response = self.__session.post(f"{config.URL_AUTHORS}", json=author)
        return self.__execute_response(response)

    def update_author(self, author: dict = None):
        response = self.__session.put(f"{config.URL_AUTHORS}", json=author)
        return self.__execute_response(response)

    def delete_author(self, author: dict = None):
        response = self.__session.delete(f"{config.URL_AUTHORS}", json=author)
        return self.__execute_response(response)

    def get_publishing_houses(self, ph_id: int = None):

        if ph_id is None:
            ph_id = ""

        response = self.__session.get(f"{config.URL_PUBLISHING_HOUSES}{ph_id}")
        return self.__execute_response(response)

    def create_publishing_house(self, publishing_house: dict = None):
        response = self.__session.post(f"{config.URL_PUBLISHING_HOUSES}", json=publishing_house)
        return self.__execute_response(response)

    def update_publishing_house(self, publishing_house: dict = None):
        response = self.__session.put(f"{config.URL_PUBLISHING_HOUSES}", json=publishing_house)
        return self.__execute_response(response)

    def delete_publishing_house(self, publishing_house: dict = None):
        response = self.__session.delete(f"{config.URL_PUBLISHING_HOUSES}", json=publishing_house)
        return self.__execute_response(response)

    def get_warehouses(self, warehouse_id: int = None):

        if warehouse_id is None:
            warehouse_id = ""

        response = self.__session.get(f"{config.URL_WAREHOUSES}{warehouse_id}")
        return self.__execute_response(response)

    def create_warehouse(self, warehouse: dict = None):
        response = self.__session.post(f"{config.URL_WAREHOUSES}", json=warehouse)
        return self.__execute_response(response)

    def update_warehouse(self, warehouse: dict = None):
        response = self.__session.put(f"{config.URL_WAREHOUSES}", json=warehouse)
        return self.__execute_response(response)

    def delete_warehouse(self, warehouse: dict = None):
        response = self.__session.delete(f"{config.URL_WAREHOUSES}", json=warehouse)
        return self.__execute_response(response)

    def get_books(self, book_id: int = None):

        if book_id is None:
            book_id = ""

        response = self.__session.get(f"{config.URL_BOOKS}{book_id}")
        return self.__execute_response(response)

    def create_book(self, book: dict = None):
        response = self.__session.post(f"{config.URL_BOOKS}", json=book)
        return self.__execute_response(response)

    def update_book(self, book: dict = None):
        response = self.__session.put(f"{config.URL_BOOKS}", json=book)
        return self.__execute_response(response)

    def delete_book(self, book: dict = None):
        response = self.__session.delete(f"{config.URL_BOOKS}", json=book)
        return self.__execute_response(response)

    def filter_book(self, filter: dict = None):

        filter = {k: v for k, v in filter.items() if v}

        response = self.__session.post(f"{config.URL_BOOKS}{'filters/'}", json=filter)
        return self.__execute_response(response)


