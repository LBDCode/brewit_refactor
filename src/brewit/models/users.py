from brewit import db, login_mgr
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from flask_login import UserMixin

@login_mgr.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(UUID(as_uuid=True), nullable=False, default=uuid4)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    account_active = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.account_active}')"