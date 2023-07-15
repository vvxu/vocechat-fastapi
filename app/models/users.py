from typing import Union
from pydantic import BaseModel


# user
# user model
class UserLogin(BaseModel):
    username: str
    password: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class UserInfo(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserInDB(UserInfo):
    hashed_password: str

