from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.core.security import create_access_token
from app.crud.user import authenticate_user
from app.database import get_db
from app.models.user import User
from app.schemas.auth import LoginOut
from app.schemas.user import UserOut

router = APIRouter(prefix="/auth", tags=["Autenticación"])


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/login", response_model=LoginOut)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db),
):
    user = authenticate_user(db, data.email, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token({"sub": str(user.id)})
    return LoginOut(access_token=token, user=UserOut.model_validate(user))


@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    return current_user
