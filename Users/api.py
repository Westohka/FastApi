# RestApi for working with users

from datetime import timedelta
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from Utils import Hash

from .token import ACCESS_TOKEN_EXPIRE_MINUTES, TokenController
from .service import UserInput, UserOutput, UserService

router = APIRouter()


@router.post('/usr', response_model=UserOutput, tags=["Users"])
async def user(data: UserInput) -> UserOutput:
    data.password = Hash.crypt(data.password)
    new_user = await UserService.insert(data)

    return new_user


@router.post('/login', tags=["Users_auth"])
async def login(data: OAuth2PasswordRequestForm = Depends()):
    user_info = await UserService.infoByLogin(data.username)

    if not user_info or not Hash.verify(user_info.password, data.password):
        raise HTTPException(status_code=404, detail="Auth error")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = TokenController.create_access_token(data={
        "sub": user_info.login
    }, expires_delta=access_token_expires)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
