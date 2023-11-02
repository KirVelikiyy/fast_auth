from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from schemas import UserSchema
from database import get_db
from models import User


async def user_doesnt_exists(user: UserSchema, db: Session = Depends(get_db)) -> User:
    user_dict = user.dict()
    new_user = User(**user_dict)
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User with that e-mail or username already exists'
        )
    return new_user


async def correct_user_id(user_id: int, db: Session = Depends(get_db)) -> User:
    user: User = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid user_id parameter'
        )
    return user
