from fastapi import HTTPException
from config import JWT_SECRET
import jwt
from fastapi.security import OAuth2PasswordBearer
from database import db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_token_owner_type(token):
    try:
        input = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        result = db.run_query(
            f"SELECT * FROM admins WHERE id = :id", id=input['id'])
        if result:
            return "ADMIN"
        result = db.run_query(
            f"SELECT * FROM users WHERE id = :id", id=input['id'])
        if result:
            return "USER"
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=400, detail="Invalid token")
    raise HTTPException(status_code=400, detail="Invalid token")
