from flask import Blueprint, jsonify
from .seed_data import categories, restaurants
from .models import Category, User, Business
from werkzeug.utils import secure_filename
from datetime import datetime
from . import db
import os
import random
import shutil

seed_bp = Blueprint("seed_bp", __name__)

LOGO_FOLDER = "/home/chris/Downloads/logos"
COVER_PHOTO_FOLDER = "/home/chris/Downloads/photos"


# Seed Categories
@seed_bp.route("/seed-categories", methods=["GET"])
def seed_categories():
    try:
        for category_data in categories:
            category = Category(
                name=category_data["name"], description=category_data.get("description")
            )
            db.session.add(category)
        db.session.commit()
        return jsonify({"message": "Categories seeded successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@seed_bp.route("/import-businesses", methods=["GET"])
def import_businesses():
    # Fetch all users and get a list of their IDs
    users = User.query.all()
    user_ids = [user.id for user in users]

    # Fetch the list of logos and cover photos
    logos = os.listdir(LOGO_FOLDER)
    cover_photos = os.listdir(COVER_PHOTO_FOLDER)

    upload_folder = os.path.join(os.getcwd(), "app", "static", "uploads")
    os.makedirs(upload_folder, exist_ok=True)

    try:
        # Process each business entry in the imported data
        for data in restaurants:
            # Select a random user ID
            user_id = random.choice(user_ids)

            # Select a random logo and cover photo
            logo_filename = secure_filename(random.choice(logos))
            cover_photo_filename = secure_filename(random.choice(cover_photos))

            # Generate unique filenames
            logo_filename_unique = f"{user_id}_logo_{datetime.now().strftime('%Y%m%d%H%M%S')}_{logo_filename}"
            cover_photo_filename_unique = f"{user_id}_cover_{datetime.now().strftime('%Y%m%d%H%M%S')}_{cover_photo_filename}"

            # Copy logo and cover photo to static/uploads
            shutil.copy(
                os.path.join(LOGO_FOLDER, logo_filename),
                os.path.join(upload_folder, logo_filename_unique),
            )
            shutil.copy(
                os.path.join(COVER_PHOTO_FOLDER, cover_photo_filename),
                os.path.join(upload_folder, cover_photo_filename_unique),
            )

            # Create a new Business entry
            new_business = Business(
                user_id=user_id,
                category_id=1,
                name=data["name"],
                description=data.get("description"),
                address=data.get("address"),
                city=data.get("city"),
                state=data.get("state"),
                zip_code=data.get("zip_code"),
                phone_number=data.get("phone_number"),
                website=data.get("website"),
                logo=logo_filename_unique,
                cover_photo=cover_photo_filename_unique,
            )
            db.session.add(new_business)

        # Commit all changes to the database
        db.session.commit()

        return jsonify({"message": "Businesses imported successfully!"}), 201

    except Exception as e:
        return jsonify({"message": "An Error Occured!", "error": e}), 400
