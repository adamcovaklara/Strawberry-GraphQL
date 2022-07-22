from typing import List, Union, Any, Optional

import strawberry
from strawberry.types import Info
from strawberry.asgi import GraphQL
from strawberry.dataloader import DataLoader

from starlette.requests import Request
from starlette.websockets import WebSocket
from starlette.responses import Response


@strawberry.type
class User:
    id: strawberry.ID


async def load_users(keys) -> List[User]:
    return [User(id=key) for key in keys]


class MyGraphQL(GraphQL):
    async def get_context(self, request: Union[Request, WebSocket], response: Optional[Response]) -> Any:
        return {
            "user_loader": DataLoader(load_fn=load_users)
        }


@strawberry.type
class Query:
    @strawberry.field
    async def get_user(self, info: Info, id: strawberry.ID) -> User:
        return await info.context["user_loader"].load(id)


schema = strawberry.Schema(query=Query)
app = MyGraphQL(schema)
