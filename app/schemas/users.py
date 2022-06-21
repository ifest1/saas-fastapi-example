from pydantic import BaseModel


class UserSignIn(BaseModel):
    email: str
    password: str


class UserSignUp(BaseModel):
    first_name: str
    surname: str
    email: str
    password: str
