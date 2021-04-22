from pydantic import BaseModel

# Create User Model


class UserInput(BaseModel):
    login: str
    password: str

# Output User Model


class UserOutput(BaseModel):
    id: int
    login: str
    password: str
