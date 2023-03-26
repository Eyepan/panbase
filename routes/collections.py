from database import db
from fastapi import Depends, HTTPException, APIRouter
from auth import oauth2_scheme, get_token_owner_type
router = APIRouter(prefix="/api/collections", tags=["collections"])

Column = ['cid', 'name', 'type', 'notnull', 'dflt_value', 'pk']


@router.get("/all")
@router.get("")
async def get_collections(token: str = Depends(oauth2_scheme)):
    if get_token_owner_type(token) == "USER":
        raise HTTPException(
            status_code=403, detail="A user isn't allowed to access this endpoint")
    return [r[0] for r in db.run_query(
        "SELECT name FROM sqlite_schema WHERE type = 'table' AND name NOT LIKE 'sqlite_%' AND name NOT LIKE 'admins' AND name NOT LIKE 'salt'")]


@router.get("/{collection_name}")
async def get_collection(collection_name: str, token: str = Depends(oauth2_scheme)):
    if get_token_owner_type(token) == "USER":
        raise HTTPException(
            status_code=403, detail="A user isn't allowed to access this endpoint")
    contents = db.run_query(f"SELECT * FROM {collection_name}")
    columns = db.run_query(f"PRAGMA table_info({collection_name})")
    columns = [dict(zip(Column, column)) for column in columns]
    contents = [dict(zip([column['name'] for column in columns], content))
                for content in contents]
    return {"name": collection_name, "contents": contents, "columns": columns}
