from . import db, bcrypt
from .models import User, Business
import os
from werkzeug.utils import secure_filename
import requests
from datetime import datetime


def user_exists(username, email):
    return (
        db.session.query(User.id)
        .filter((User.username == username) | (User.email == email))
        .first()
        is not None
    )


def create_user(username, email, password):
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    user = User(
        username=username, password=hashed_password, email=email, is_business=False
    )
    db.session.add(user)
    db.session.commit()


def user_to_dict(user):
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_business": user.is_business,
    }


def save_file(file_path, new_filename):
    try:
        # Open the file in read binary mode
        with open(file_path, "rb") as file:
            file_data = file.read()

        # Get the full path to the static folder and create the file
        # static_folder = os.path.join(app.static_folder, new_filename)
        upload_folder = os.path.join(os.getcwd(), "app", "static", "uploads")
        with open(upload_folder, "wb") as target_file:
            target_file.write(file_data)

        return upload_folder
    except Exception as e:
        print(f"Error saving file: {e}")
        return None


def get_businesses_by_category(category_id):
    businesses = Business.query.filter_by(category_id=category_id).all()
    return [business.to_dict() for business in businesses]


def save_image_from_url_(url, prefix):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            upload_folder = os.path.join(os.getcwd(), "app", "static", "uploads")
            os.makedirs(upload_folder, exist_ok=True)

            filename = f"{prefix}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{secure_filename(url.split('/')[-1])}"
            file_path = os.path.join(upload_folder, filename)

            with open(file_path, "wb") as file:
                file.write(response.content)
            return filename
        else:
            return None
    except Exception as e:
        print(f"Error downloading image: {e}")
        return None


def save_image_from_url(url, prefix):
    response = requests.get(url)
    if response.status_code == 200:

        upload_folder = os.path.join(os.getcwd(), "app", "static", "uploads")
        os.makedirs(upload_folder, exist_ok=True)

        filename = secure_filename(url.split("/")[-1])
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{prefix}_{timestamp}_{filename}"
        file_path = os.path.join(upload_folder, filename)

        with open(file_path, "wb") as file:
            file.write(response.content)
        return filename
    return None
