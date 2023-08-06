from enum import Enum
from typing import Dict, Iterable, TypeVar

from pydantic.main import BaseModel

from src import HttpRequest
from src.client import HttpClient, HttpMethod
from src.notion.endpoints import NotionEndpoint
from src.notion.endpoints.databases import DatabaseEndPoint

T = TypeVar("T")


class NotionDomain(str, Enum):
    Databases = ("databases",)
    Users = "users"


class NotionDatabase(BaseModel):
    def to_iterable(self) -> Iterable:
        return []


class NotionService:
    def __init__(self, client: HttpClient):
        self.endpoint_map: Dict[str, NotionEndpoint] = {
            "databases": DatabaseEndPoint(client),
        }

    @property
    def databases(self) -> DatabaseEndPoint:
        return self.endpoint_map["databases"]
