from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
    status,
)

from sqlalchemy import select

from sqlalchemy.orm import Session

from ..database import get_db

from ..models import User

from ..schemas import (
    RegisterRequest,
    LoginRequest,
)

from ..auth import (
    hash_password,
    verify_password,
    set_auth_cookie,
    clear_auth_cookie,
)

from ..dependencies import get_current_user


router = APIRouter(
    tags=["Authentication"]
)


@router.post("/register")
def register(
    payload: RegisterRequest,
    response: Response,
    db: Session = Depends(get_db),
):

    email = payload.email.lower()

    existing_user = db.scalar(
        select(User).where(
            User.email == email
        )
    )

    if existing_user:

        raise HTTPException(
            status_code=409,
            detail="An account with this email already exists",
        )

    user = User(
        name=payload.name.strip(),
        email=email,
        password_hash=hash_password(
            payload.password
        ),
    )

    db.add(user)

    db.commit()

    db.refresh(user)

    set_auth_cookie(
        response,
        user.id,
    )

    return {
        "message": "Registration successful",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
        },
    }


@router.post("/login")
def login(
    payload: LoginRequest,
    response: Response,
    db: Session = Depends(get_db),
):

    user = db.scalar(
        select(User).where(
            User.email == payload.email.lower()
        )
    )

    if (
        not user
        or not verify_password(
            payload.password,
            user.password_hash,
        )
    ):

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    set_auth_cookie(
        response,
        user.id,
    )

    return {
        "message": "Login successful",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
        },
    }


@router.get("/logout")
def logout(
    response: Response,
):

    clear_auth_cookie(
        response
    )

    return {
        "message": "Logged out"
    }


@router.get("/session-info")
def session_info(
    user: User = Depends(
        get_current_user
    ),
):

    return {
        "authenticated": True,
        "user_id": user.id,
        "name": user.name,
        "email": user.email,
    }


@router.get("/session-data")
def session_data(
    user: User = Depends(
        get_current_user
    ),
):

    return {
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
        }
    }