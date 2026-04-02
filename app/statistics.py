from sqlalchemy.orm import Session
from sqlalchemy import func
from app.dbmanager import Identifier, Country, Characteristic

def get_basic_stats(db: Session):
    
    total_identifiers = db.query(Identifier).count()
    total_countries = db.query(Country).count()
    total_characteristics = db.query(Characteristic).count()
    

    types_count = db.query(
        Identifier.identifier_type, 
        func.count(Identifier.identifier_name)
    ).group_by(Identifier.identifier_type).all()
    
    
    types_dict = {t[0]: t[1] for t in types_count if t[0] is not None}

    return {
        "status": "success",
        "total_identifiers": total_identifiers,
        "total_countries": total_countries,
        "total_characteristics": total_characteristics,
        "identifiers_by_type": types_dict
    }