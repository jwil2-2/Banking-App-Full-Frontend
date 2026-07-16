from pydantic import BaseModel


class CurrentUser(BaseModel):
    id: str
    name: str
    email: str
    role: str
