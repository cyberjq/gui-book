import typing
from pydantic import BaseSettings, Field, BaseModel


class AppConfig(BaseModel):
    """Application configurations."""
    debug: typing.Optional[bool] = False


class GlobalConfig(BaseSettings):
    """Global configurations."""

    ENV_STATE: typing.Optional[str] = Field(None, env="ENV_STATE")

    URL_SUBJECTS: typing.Optional[str] = Field(None, env="URL_SUBJECTS")
    URL_AUTHORS: typing.Optional[str] = Field(None, env="URL_AUTHORS")
    URL_BOOKS: typing.Optional[str] = Field(None, env="URL_BOOKS")
    URL_WAREHOUSES: typing.Optional[str] = Field(None, env="URL_WAREHOUSES")
    URL_PUBLISHING_HOUSES: typing.Optional[str] = Field(None, env="URL_PUBLISHING_HOUSES")

    # app config
    APP_CONFIG: AppConfig = AppConfig()

    def __init__(self, **values: typing.Any):
        super().__init__(**values)

        if self.ENV_STATE == "dev":
            self.APP_CONFIG = AppConfig(debug=True)

    class Config:
        """Loads the dotenv file."""
        env_file: str = ".env"


class DevConfig(GlobalConfig):
    """Development configurations."""

    URL_API_DEV: typing.Optional[str] = Field(None, env="URL_API_DEV")

    def __init__(self, **values: typing.Any):
        super().__init__(**values)
        self.URL_AUTHORS = self.URL_API_DEV + self.URL_AUTHORS
        self.URL_SUBJECTS = self.URL_API_DEV + self.URL_SUBJECTS
        self.URL_BOOKS = self.URL_API_DEV + self.URL_BOOKS
        self.URL_WAREHOUSES = self.URL_API_DEV + self.URL_WAREHOUSES
        self.URL_PUBLISHING_HOUSES = self.URL_API_DEV + self.URL_PUBLISHING_HOUSES


class ProdConfig(GlobalConfig):
    """Production configurations."""

    URL_API_PROD: typing.Optional[str] = Field(None, env="URL_API_PROD")


    def __init__(self, **values: typing.Any):
        super().__init__(**values)
        self.URL_AUTHORS = self.URL_API_PROD + self.URL_AUTHORS
        self.URL_SUBJECTS = self.URL_API_PROD + self.URL_SUBJECTS
        self.URL_BOOKS = self.URL_API_PROD + self.URL_BOOKS
        self.URL_WAREHOUSES = self.URL_API_PROD + self.URL_WAREHOUSES
        self.URL_PUBLISHING_HOUSES = self.URL_API_PROD + self.URL_PUBLISHING_HOUSES


class FactoryConfig:
    """Returns a config instance dependending on the ENV_STATE variable."""

    def __init__(self, env_state: typing.Optional[str]):
        self.env_state = env_state

    def __call__(self):
        if self.env_state == "dev":
            return DevConfig()

        elif self.env_state == "prod":
            return ProdConfig()


config = FactoryConfig(GlobalConfig().ENV_STATE)()