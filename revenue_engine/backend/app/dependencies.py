from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session
from .db import get_db
from .models import User
from .security import decode_token

def db(): return Depends(get_db)

def current_user(authorization: str|None=Header(default=None), session: Session=Depends(get_db)):
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(401,"Authentication required")
    try: payload=decode_token(authorization.split(" ",1)[1])
    except Exception: raise HTTPException(401,"Invalid or expired token")
    user=session.query(User).filter(User.email==payload["sub"],User.active.is_(True)).first()
    if not user: raise HTTPException(401,"User not found or inactive")
    return user
