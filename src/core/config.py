import enum
import logging
import typing

import pydantic

PROJECT_NAME = "aggregated_newsletters"
API_VERSION = "1"
API_PREFIX = f"/api/v{API_VERSION}"

origins = ["*"]


class Environment(str, enum.Enum):
    PROD = "PROD"
    DEV = "DEV"
    STAGING = "STAGE"
    CICD = "CICD"

    @staticmethod
    def from_str(label: typing.Optional[str]) -> "Environment":
        if label is not None:
            if label.upper() in ("PROD", "PRODUCTIVE"):
                return Environment.PROD
            elif label.upper() in ("STG", "STAGING"):
                return Environment.STAGING
            elif label.upper() in ("CICD"):
                return Environment.CICD
        return Environment.DEV

    @staticmethod
    def get_log_level(environment: "Environment") -> int:
        if environment == Environment.DEV:
            return logging._nameToLevel["DEBUG"]  # type: ignore
        return logging._nameToLevel["INFO"]  # type: ignore


class AppConfig(pydantic.BaseSettings):
    environment: Environment

    database_url: str
    database_schema: str | None

    vector_size: int = 384

    @pydantic.validator("environment")
    @staticmethod
    def validate_env(val: str) -> Environment:
        return Environment.from_str(val)

    @property
    def logger_level(self) -> int:
        return Environment.get_log_level(self.environment)  # type: ignore


settings = AppConfig(_env_file=".env", _env_file_encoding="utf-8")  # type: ignore
