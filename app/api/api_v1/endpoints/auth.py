from fastapi import APIRouter, HTTPException
from ormar import NoMatch

from app.core.auth import authenticate, create_access_token
from app.core.security import get_password_hash
from app.models.users import User, UserSignIn, UserSignUp

router = APIRouter()


@router.post("/signup", response_model=User, status_code=201)
async def signup(user: UserSignUp):
    try:
        user_exists = await User.objects.get(email=user.email)
        if user_exists:
            raise HTTPException(status_code=400, detail="There is already an user using this email.")
    except NoMatch:
        password_hash = get_password_hash(user.password)
        user = User(first_name=user.first_name, surname=user.surname, email=user.email, hashed_password=password_hash)
        await user.save()
        return user


@router.post("/token", status_code=201)
async def signin(user: UserSignIn):
    if not authenticate(user):
        raise HTTPException(status_code=400, detail="Incorrect username or password.")
    return {"access_token": create_access_token(sub=user.email), "token_type": "bearer"}
