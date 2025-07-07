import fastapi as _fastapi
from typing import TYPE_CHECKING, List
import sqlalchemy.orm  as _orm

import schemas as _schemas
import services as _services

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

app = _fastapi.FastAPI()

@app.post("/api/contacts/", response_model=_schemas.Contact)
async def create_contact(
    contact: _schemas.CreateContact, 
    db: _orm.Session=_fastapi.Depends(_services.get_db)
):
    return await _services.create_contact(contact=contact, db=db)