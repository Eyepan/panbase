from database import db
from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from config import JWT_SECRET
import jwt
from auth import oauth2_scheme

router = APIRouter(prefix="", tags=["admin"])


@router.post("/token")
@router.post("/api/admin/login")
def login_admin(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password
    result = db.run_query(
        "SELECT * FROM admins WHERE username = :username", username=username)
    if not result:
        raise HTTPException(status_code=400, detail="Invalid username")
    if not db.verify_password(password, result[0][2]):
        raise HTTPException(status_code=400, detail="Invalid password")
    token = jwt.encode({"id": result[0][0]}, JWT_SECRET, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}


@router.post("/api/admin/register")
def register_admin(username: str, password: str):
    result = db.run_query(
        "SELECT * FROM admins WHERE username = :username", username=username)
    if result:
        raise HTTPException(status_code=400, detail="Username already exists")
    db.run_query("INSERT INTO admins (username, password) VALUES (:username, :password)",
                 username=username, password=db.encrypt(password))
    token = jwt.encode({"id": db.run_query(
        "SELECT * FROM admins WHERE username = :username", username=username)[0][0]}, JWT_SECRET, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}


@router.get("/api/me")
async def who_am_i(token: str = Depends(oauth2_scheme)):
    input = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    result = db.run_query(
        "SELECT * FROM admins WHERE id = :id", id=input['id'])
    if result:
        return {"username": result[0][1]}
    result = db.run_query(
        "SELECT * FROM users WHERE id = :id", id=input['id'])
    if result:

        return {"username": result[0][1]}
    raise HTTPException(status_code=400, detail="Invalid token")
