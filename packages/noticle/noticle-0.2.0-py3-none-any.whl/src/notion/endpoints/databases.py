from datetime import datetime
from typing import Any, List, Literal, Optional

from pydantic.main import BaseModel

from src import HttpRequest
from src.notion.endpoints import NotionEndpoint, RequestDTO
from src.types import DictType, Id

NotionPropertyType = Literal["multi_select", "date", "checkbox", "title"]


class RowProperty(BaseModel):
    key: str
    type: NotionPropertyType
    value: Any


class Row(BaseModel):
    object: str
    id: str
    created_time: datetime
    properties: List[RowProperty]


class DatabaseModel(BaseModel):
    next_cursor: Optional[str]
    has_more: bool
    result: List[Row]


class DatabaseRequestDTO(RequestDTO):
    # MEMO: filter condition ref: [https://developers.notion.com/reference/post-database-query-filter]
    filter: Optional[DictType]
    sorts: Optional[List[DictType]]
    start_cursor: Optional[str]
    page_size: Optional[int] = 100


# So Concrete and Vulnerable!
class DatabaseResponseBuilder:
    @classmethod
    def build(cls, api_response: DictType) -> DatabaseModel:
        rows = [cls._build_row(row) for row in api_response["results"]]
        return DatabaseModel(
            next_cursor=api_response["next_cursor"],
            has_more=api_response["has_more"],
            result=rows,
        )

    @classmethod
    def _build_row(cls, row: DictType) -> Row:
        return Row(
            object=row["object"],
            id=row["id"],
            created_time=row["created_time"],
            properties=[
                cls._build_property(key, obj)
                for key, obj in list(
                    zip(row["properties"].keys(), row["properties"].values())
                )
            ],
        )

    @classmethod
    def _build_property(cls, key: str, obj: DictType) -> RowProperty:
        return RowProperty(
            key=key, type=obj["type"], value=cls._get_property_value(obj)
        )

    @classmethod
    def _get_property_value(cls, obj: DictType) -> Any:
        """
        property type에 따라 형태가 다름
        :param obj:
            # type: title
                {'type': 'title', 'title': [{'type': 'text', 'text': {'content': '...', ...}, 'plain_text': '...', ...}]
            # type: date
                {'type': 'date', 'date': {'start': '...', 'end': '...', 'timezone': '...'}}
            # type: multi_select
                {'id': 'multi_select', 'multi_select': ['...', ...]}


        :return: str
        """
        type = obj["type"]
        if type == "title":
            return obj["title"][0]["plain_text"] if obj["title"] else ""
        else:
            return obj[type]


class DatabaseEndPoint(NotionEndpoint):
    path_prefix = "databases"

    def retrieve(self, id: Id):
        return True

    def query(self, id: Id, body: DatabaseRequestDTO = None) -> DatabaseModel:
        response = self.client.request(
            http_request=HttpRequest(
                path=f"{self.path_prefix}/{id}/query",
                method="POST",
                body=body.json() if body else None,
            )
        )
        return DatabaseResponseBuilder.build(api_response=response.json())

    def update(self, body: RequestDTO):
        pass

    def create(self, body: RequestDTO):
        pass
