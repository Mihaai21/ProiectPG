from app.database import SessionLocal
from app.models import Identifier

db = SessionLocal()

rows = db.query(Identifier).all()

for r in rows:
    print(r.identifier_name, r.description)

db.close()