
import asyncio
import functools
import ujson
import aiohttp

from config import config


class AsyncBookApiMeta(type):
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


class AsyncBookApi:
    """ Класс для работы с запросами к апи вятгу """

    def __init__(self):
        self.__session = aiohttp.ClientSession()


    def session_init(func):

        @functools.wraps(func)
        async def session_init(*args, **kwargs):
            self = args[0]
            if not self.__session or self.__session.closed:
                self.__session = aiohttp.ClientSession(
                    loop=asyncio.get_event_loop(),
                    json_serialize=ujson.dumps)

            return await func(*args, **kwargs)
        return session_init

    async def __session_close(self):
        if self.__session:
            await self.__session.close()

    async def __execute_response(self, response, **kwargs):
        if response.status == 200:
            data = await response.json()
            response.close()

            return data

        response.close()
        return None

    # @session_init
    async def get_subjects(self, subject_id: int = None):

        try:
            if subject_id is None:
                subject_id = ""

            response = await self.__session.get(f"{config.URL_SUBJECTS}{subject_id}")
            return await self.__execute_response(response)
        except Exception as e:
            print("HI")

    # @session_init
    async def create_subject(self, subject: dict = None):
        response = await self.__session.post(f"{config.URL_SUBJECTS}", json=subject)
        print(response)
        return await self.__execute_response(response)

    # @session_init
    async def update_subject(self, subject: dict = None):
        response = await self.__session.put(f"{config.URL_SUBJECTS}", json=subject)
        return await self.__execute_response(response)

    # @session_init
    async def delete_subject(self, subject: dict = None):
        response = await self.__session.delete(f"{config.URL_SUBJECTS}", json=subject)
        return await self.__execute_response(response)

