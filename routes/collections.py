from typing import Dict, List
from pydantic import BaseModel
from database import db
from fastapi import Depends, HTTPException, APIRouter
from auth import oauth2_scheme, get_token_owner_type
router = APIRouter(prefix="/api/collections", tags=["collections"])

Column = ['cid', 'name', 'type', 'notnull', 'dflt_value', 'pk']

# {
# 	collection_name: "apple",
# 	columns: [
# 		{
# 		  cid: 0,
# 		  name: "id",
# 		  type: "INTEGER",
# 		  notnull: 0,		// optional
# 		  dflt_value: null,	// optional
# 		  pk: 1				// optional
# 		},
# 	]
# }


class ColumnType(BaseModel):
    name: str
    type: str
    notnull: bool = False
    dflt_value: str = None
    pk: bool = False


class NewCollection(BaseModel):
    collection_name: str
    columns: List[ColumnType]


class Collection(BaseModel):
    collection_name: str
    columns: List[ColumnType]
    contents: List[Dict]


@router.get("/all")
@router.get("")
async def get_collections(token: str = Depends(oauth2_scheme)):
    if get_token_owner_type(token) == "USER":
        raise HTTPException(
            status_code=403, detail="A user isn't allowed to access this endpoint")
    return [r[0] for r in db.run_query(
        "SELECT name FROM sqlite_schema WHERE type = 'table' AND name NOT LIKE 'sqlite_%' AND name NOT LIKE 'admins' AND name NOT LIKE 'salt'")]


@router.get("/{collection_name}")
async def get_collection(collection_name: str, token: str = Depends(oauth2_scheme)) -> Collection:
    if get_token_owner_type(token) == "USER":
        raise HTTPException(
            status_code=403, detail="A user isn't allowed to access this endpoint")
    contents = db.run_query(f"SELECT * FROM {collection_name}")
    columns = db.run_query(f"PRAGMA table_info({collection_name})")
    columns = [dict(zip(Column, column)) for column in columns]
    contents = [dict(zip([column['name'] for column in columns], content))
                for content in contents]
    return Collection(collection_name=collection_name, columns=columns, contents=contents)


@router.post("")
async def create_new_collection(content: NewCollection, token: str = Depends(oauth2_scheme)):
    if get_token_owner_type(token) == "USER":
        raise HTTPException(
            status_code=403, detail="A user isn't allowed to access this endpoint")
    columns_str = ", ".join(
        [f"{column.name} {column.type} {'NOT NULL' if column.notnull else ''} {'DEFAULT ' + column.dflt_value if column.dflt_value else ''} {'PRIMARY KEY' if column.pk else ''}" for column in content.columns])
    db.run_query(
        f"CREATE TABLE {content.collection_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, {columns_str})")
