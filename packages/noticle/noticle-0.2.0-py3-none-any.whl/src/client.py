from types import TracebackType
from typing import Optional, Type

import httpx
from pydantic.class_validators import validator
from pydantic.env_settings import BaseSettings
from pydantic.fields import Field
from pydantic.main import BaseModel
from pydantic.networks import HttpUrl

from src import HttpMethod, HttpRequest
from src.logger import create_logger
from src.types import DictType


class HttpOptions(BaseSettings):
    base_url_: HttpUrl = Field(
        default="https://api.notion.com/v1/", env="NOTION_API_URL"
    )
    auth_token: str = Field(..., env="NOTION_API_KEY")
    notion_version: str = "2021-08-16"

    @property
    def base_url(self) -> str:
        return (
            self.base_url_.rstrip("/")
            if self.base_url_.endswith("/")
            else self.base_url_
        )


class HttpClient:
    def __init__(self, options: HttpOptions, client: httpx.Client):
        self.options = options
        self.client = client
        self.logger = create_logger()

        self.client.timeout = 100

    def __enter__(self):
        self.client.__enter__()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        self.client.__exit__(exc_type, exc_value, traceback)

    def request(self, http_request: HttpRequest) -> httpx.Response:
        request = self._build_request(http_request)

        self.logger.info(
            f"------REQUEST------"
            f"URL: {self.options.base_url}/{http_request.path}"
            f"METHOD: {http_request.method}"
            f"BODY: {http_request.body}"
            f"HEADERS: {http_request.headers}"
        )
        response = self.client.send(request=request)
        return response

    def _build_request(self, http_request: HttpRequest) -> httpx.Request:
        return self.client.build_request(
            method=http_request.method,
            url=f"{self.options.base_url}/{http_request.path}",
            params=http_request.query,
            json=http_request.body,
            headers=http_request.headers,
        )

    @property
    def headers(self) -> httpx.Headers:
        return self.client.headers

    @headers.setter
    def headers(self, headers: DictType) -> None:
        self.client.headers = httpx.Headers(headers)
