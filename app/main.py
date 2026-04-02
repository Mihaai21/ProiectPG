from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Identifier
from app.schemas import IdentifierCreate, IdentifierResponse, IdentifierUpdate

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Identifiers API"}

@app.post("/identifiers/", response_model=IdentifierResponse)
def create_identifier(identifier: IdentifierCreate, db: Session = Depends(get_db)):
    existing_identifier = db.query(Identifier).filter(
        Identifier.identifier_name == identifier.identifier_name
    ).first()

    if existing_identifier is not None:
        raise HTTPException(status_code=400, detail="Identifier already exists")

    db_identifier = Identifier(**identifier.model_dump())
    db.add(db_identifier)
    db.commit()
    db.refresh(db_identifier)
    return db_identifier

@app.get("/identifiers/", response_model=list[IdentifierResponse])
def read_all_identifiers(db: Session = Depends(get_db)):
    identifiers = db.query(Identifier).all()
    return identifiers

@app.get("/identifiers/{identifier_name}", response_model=IdentifierResponse)
def read_identifier(identifier_name: str, db: Session = Depends(get_db)):
    identifier = db.query(Identifier).filter(
        Identifier.identifier_name == identifier_name
    ).first()

    if identifier is None:
        raise HTTPException(status_code=404, detail="Identifier not found")

    return identifier

@app.put("/identifiers/{identifier_name}", response_model=IdentifierResponse)
def update_identifier(identifier_name: str, identifier: IdentifierCreate, db: Session = Depends(get_db)):
    db_identifier = db.query(Identifier).filter(
        Identifier.identifier_name == identifier_name
    ).first()

    if db_identifier is None:
        raise HTTPException(status_code=404, detail="Identifier not found")

    for key, value in identifier.model_dump().items():
        setattr(db_identifier, key, value)

    db.commit()
    db.refresh(db_identifier)
    return db_identifier

@app.patch("/identifiers/{identifier_name}", response_model=IdentifierResponse)
def patch_identifier(identifier_name: str, identifier_update: IdentifierUpdate, db: Session = Depends(get_db)):
    db_identifier = db.query(Identifier).filter(
        Identifier.identifier_name == identifier_name
    ).first()

    if db_identifier is None:
        raise HTTPException(status_code=404, detail="Identifier not found")

    if identifier_update.description is not None:
        db_identifier.description = identifier_update.description
    if identifier_update.identifier_type is not None:
        db_identifier.identifier_type = identifier_update.identifier_type

    db.commit()
    db.refresh(db_identifier)
    return db_identifier

@app.delete("/identifiers/{identifier_name}")
def delete_identifier(identifier_name: str, db: Session = Depends(get_db)):
    db_identifier = db.query(Identifier).filter(
        Identifier.identifier_name == identifier_name
    ).first()

    if db_identifier is None:
        raise HTTPException(status_code=404, detail="Identifier not found")

    db.delete(db_identifier)
    db.commit()
    return {"detail": "Identifier deleted"}