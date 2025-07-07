import fastapi as _fastapi
from typing import TYPE_CHECKING, List
import sqlalchemy.orm  as _orm

import schemas as _schemas
import services as _services

# Import Session type only for type checking to avoid circular imports
if TYPE_CHECKING:
    from sqlalchemy.orm import Session

# Create a FastAPI application instance
app = _fastapi.FastAPI()

# Define a POST route for creating a new contact
@app.post("/api/contacts/", response_model=_schemas.Contact)
async def create_contact(
    # Automatically parse and validate request body into a CreateContact schema object
    contact: _schemas.CreateContact, 
    
    # Inject a database session using FastAPI's dependency injection system
    db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    # Call the async service function to create a contact in the database
    # and return the result as a Contact schema (converted to JSON by FastAPI)
    return await _services.create_contact(contact=contact, db=db)

@app.get("/api/contacts/", response_model=List[_schemas.Contact])
async def get_contact(db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.get_all_contacts(db=db)

@app.get("/api/contacts/{contact_id}/", response_model=_schemas.Contact)
async def get_contact(contact_id: int, db:_orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.get_contacts(contact_id=contact_id, db=db)

@app.delete("/api/contacts/{contact_id}/")
async def delete_contact(contact_id: int, db:_orm.Session = _fastapi.Depends(_services.get_db)):
    contact = await _services.get_contacts(db = db, contact_id=contact_id)
    if contact is None:
        raise _fastapi.HTTPException(status_code=404, detail="User does not Exist")
    
    await _services.delete_contact(contact, db=db)
    return "User deleted successfully"