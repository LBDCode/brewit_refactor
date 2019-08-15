from brewit import db
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import text

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(UUID(as_uuid=True), nullable=False, default=uuid4)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    account_active = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.account_active}')"