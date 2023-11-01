from fastapi import HTTPException, status, Depends
from schemas import UserSchema
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import get_db
from models import User


async def user_doesnt_exists(user: UserSchema, db: Session = Depends(get_db)):
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
