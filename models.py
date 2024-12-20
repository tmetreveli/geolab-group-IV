# SQL - structured Query Language
from flask_login import UserMixin

from extensions import db, app, login_manager
from werkzeug.security import generate_password_hash, check_password_hash




class Dog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    colour = db.Column(db.String(80), unique=False, nullable=False)
    mood = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return f"{self.id}: {self.name}"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    role = db.Column(db.String(), default="guest")
    
    def __init__(self, username, password, role="guest"):
        self.username = username
        self.password = generate_password_hash(password)
        self.role = role

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"{self.id}: {self.username}"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == '__main__':
    dogs = [{"name": "dog1.jpeg", "colour": "golden", "mood": "happy", "id": 0},
            {"name": "dog2.jpeg", "colour": "black", "mood": "excited", "id": 1},
            {"name": "dog3.jpeg", "colour": "brown", "mood": "playful", "id": 2},
            {"name": "dog2.jpeg", "colour": "White", "mood": "Annoyed", "id": 3}
            ]
    with app.app_context():
        db.create_all()
        for dog in dogs:
            new_dog = Dog(name=dog["name"], colour=dog["colour"], mood=dog["mood"])
            db.session.add(new_dog)
            db.session.commit()

        user = User(username="user", password="123")
        admin = User(username="admin", password="admin123", role="admin")
        db.session.add(user)
        db.session.add(admin)
        db.session.commit()
