# Schemas shared by authentication dependencies and protected routes.

from pydantic import BaseModel


class CurrentUser(BaseModel):
    # Authenticated request principal loaded from the current user record.

    id: str
    name: str
    email: str
    role: str
