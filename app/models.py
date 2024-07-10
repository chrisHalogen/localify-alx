from . import db
from flask_login import UserMixin


# class User(UserMixin, db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50), unique=True, nullable=False)
#     email = db.Column(db.String(50), unique=True, nullable=False)
#     password = db.Column(db.String(255), nullable=False)
#     role = db.Column(db.String(20), nullable=False, default="user")


class User(
    UserMixin,
    db.Model,
):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_business = db.Column(db.Boolean, default=False, nullable=False)
    role = db.Column(db.String(20), nullable=False, default="user")

    businesses = db.relationship("Business", backref="owner", lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"

    def isAbusiness(self):
        return bool(self.is_business)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)

    businesses = db.relationship("Business", backref="category", lazy=True)

    def __repr__(self):
        return f"<Category {self.name}>"


class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    address = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(255), nullable=True)
    state = db.Column(db.String(255), nullable=True)
    zip_code = db.Column(db.String(255), nullable=True)
    phone_number = db.Column(db.String(255), nullable=True)
    website = db.Column(db.String(255), nullable=True)
    logo = db.Column(db.String(255), nullable=True)
    cover_photo = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<Business {self.name}>"

    def to_dict(self):
        return {
            "id": self.id,
            "category": self.category.name,
            "name": self.name,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "zip_code": self.zip_code,
            "phone_number": self.phone_number,
            "website": self.website,
            "description": self.description,
            "cover_photo": self.cover_photo,
        }
