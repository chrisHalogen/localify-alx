from flask import Blueprint, request, url_for, redirect, render_template, jsonify
from .models import User, Business, Category
from . import db, bcrypt
from flask_login import login_user, logout_user, login_required, current_user
from .utils import user_exists, create_user, save_image_from_url
from datetime import datetime
import os
from werkzeug.utils import secure_filename
import re
import csv


accounts = Blueprint("accounts", __name__)


# User Registration Page
@accounts.route("/register", methods=["GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("accounts.listings"))
    return render_template("account/register.html")


# User Login Page
@accounts.route("/login", methods=["GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("accounts.listings"))
    return render_template("account/login.html")


# Logout Route
@accounts.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("general.home"))


# User Creation Logic
@accounts.route("/create-new-user", methods=["POST"])
def create_new_user():
    data = request.get_json()
    username = data["username"]
    email = data["email"]
    password = data["password"]

    if user_exists(username, email):
        return jsonify(status="error", message="Username or email already exists."), 409

    create_user(username, email, password)
    return jsonify(status="success", message="User registered successfully."), 201


# User Login Logic
@accounts.route("/log-user-in", methods=["POST"])
def log_user_in():
    data = request.get_json()
    user_input = data["user_input"]
    password = data["password"]

    user = User.query.filter(
        (User.email == user_input) | (User.username == user_input)
    ).first()

    if user and bcrypt.check_password_hash(user.password, password):
        login_user(user)
        return jsonify(status="success", message="Logged in successfully."), 200

    return jsonify(status="error", message="Invalid username/email or password."), 401


# Listings Dashboard Page
@accounts.route("/listings")
@login_required
def listings():
    data = {"active": 5, "tab": 1}
    data["businesses"] = Business.query.filter_by(user_id=current_user.id).all()
    return render_template("account/listings.html", data=data)


# Render Listings Create Page
@accounts.route("/listings/create")
@login_required
def create_new_listing():
    data = {"active": 5, "tab": 1}
    data["categories"] = Category.query.all()
    return render_template("account/create-new.html", data=data)


# Render Profile Page
@accounts.route("/profile")
@login_required
def profile():
    data = {"active": 5, "tab": 2}
    data["user"] = current_user
    return render_template("account/profile.html", data=data)


# Logic to create new business
@accounts.route("/listings/create-new-business", methods=["POST"])
@login_required
def create_new_business():
    data = {"active": 5, "tab": 1}
    data = request.form
    name = data.get("name")
    address = data.get("address")
    city = data.get("city")
    state = data.get("state")
    zip_code = data.get("zip_code")
    phone = data.get("phone")
    website = data.get("website")
    category_id = data.get("category")
    description = data.get("description")
    logo = request.files.get("logo")
    cover_photo = request.files.get("cover_photo")

    if not all([name, address, city, state, zip_code, phone, category_id]):
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "All fields except description are required.",
                }
            ),
            400,
        )

    if int(category_id) == 0:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Invalid Category Selected.",
                }
            ),
            400,
        )

    try:
        upload_folder = os.path.join(os.getcwd(), "app", "static", "uploads")
        os.makedirs(upload_folder, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        if logo:
            logo_filename = (
                f"{current_user.id}_logo_{timestamp}_{secure_filename(logo.filename)}"
            )
            logo.save(os.path.join(upload_folder, logo_filename))
        else:
            logo_filename = None

        if cover_photo:
            cover_photo_filename = f"{current_user.id}_cover_{timestamp}_{secure_filename(cover_photo.filename)}"
            cover_photo.save(os.path.join(upload_folder, cover_photo_filename))
        else:
            cover_photo_filename = None

        business = Business(
            user_id=current_user.id,
            category_id=category_id,
            name=name,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            phone_number=phone,
            website=website,
            logo=logo_filename,
            cover_photo=cover_photo_filename,
            description=description,
        )
        db.session.add(business)
        db.session.commit()

        return jsonify(status="success", message="Business created successfully"), 201

    except Exception as e:
        return jsonify(status="error", message=str(e)), 500


# Logic to Delete Business
@login_required
@accounts.route("/delete-business", methods=["DELETE"])
def delete_business():
    data = request.get_json()
    business_id = data.get("id")

    if not business_id:
        return jsonify(status="error", message="Business ID is required"), 400

    business = Business.query.get(business_id)

    if not business:
        return jsonify(status="error", message="Business not found"), 404

    if business.user_id != current_user.id:
        return (
            jsonify(
                status="error",
                message="You do not have permission to delete this business",
            ),
            403,
        )

    try:
        db.session.delete(business)
        db.session.commit()

        return jsonify(status="success", message="Business deleted successfully"), 204

    except Exception as e:
        db.session.rollback()
        return (
            jsonify(
                status="error", message="An error occurred while deleting the business"
            ),
            500,
        )


# Listings edit page
@accounts.route("/listings/edit/<int:pk>")
@login_required
def edit_listing(pk):
    data = {"active": 5, "tab": 1}
    data["business"] = Business.query.get(pk)
    data["categories"] = Category.query.all()
    return render_template("account/edit.html", data=data)


# Logic to Update Business
@accounts.route("/edit-business/<int:business_id>", methods=["PUT"])
@login_required
def edit_business(business_id):
    data = request.form
    business = Business.query.get(business_id)

    if not business:
        return jsonify({"status": "error", "message": "Business not found"}), 404

    if business.user_id != current_user.id:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "You do not have permission to edit this business",
                }
            ),
            403,
        )

    try:
        business.name = data.get("name", business.name)
        business.address = data.get("address", business.address)
        business.city = data.get("city", business.city)
        business.state = data.get("state", business.state)
        business.zip_code = data.get("zip_code", business.zip_code)
        business.phone_number = data.get("phone_number", business.phone_number)
        business.website = data.get("website", business.website)
        business.category_id = data.get("category_id", business.category_id)
        business.description = data.get("description", business.description)

        logo = request.files.get("logo")
        cover_photo = request.files.get("cover_photo")

        if logo:
            logo_filename = f"{business_id}_logo_{datetime.now().strftime('%Y%m%d%H%M%S')}.{logo.filename.split('.')[-1]}"
            logo.save(os.path.join("static/uploads", logo_filename))
            business.logo = logo_filename

        if cover_photo:
            cover_photo_filename = f"{business_id}_cover_photo_{datetime.now().strftime('%Y%m%d%H%M%S')}.{cover_photo.filename.split('.')[-1]}"
            cover_photo.save(os.path.join("static/uploads", cover_photo_filename))
            business.cover_photo = cover_photo_filename

        db.session.commit()
        return (
            jsonify({"status": "success", "message": "Business updated successfully"}),
            200,
        )
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


# Render Profile edit page
@accounts.route("/profile/edit/")
@login_required
def edit_profile():
    data = {"active": 5, "tab": 2}
    data["user"] = current_user
    return render_template("account/edit-profile.html", data=data)


# Logic to edit profile
@accounts.route("/edit-profile", methods=["PUT"])
@login_required
def edit_user_profile():
    data = request.json

    if data["user_id"] != current_user.id:
        return jsonify({"error": "Unauthorized access"}), 403

    username = data["username"].strip()
    email = data["email"].strip()
    is_business = data["is_business"]

    if (
        not username
        or not email
        or not re.match(r"^[a-zA-Z]{4,}$", username)
        or not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email)
    ):
        return jsonify({"error": "Invalid input data"}), 400

    existing_user = (
        User.query.filter((User.username == username) | (User.email == email))
        .filter(User.id != current_user.id)
        .first()
    )
    if existing_user:
        return jsonify({"error": "Username or email already taken"}), 409

    current_user.username = username
    current_user.email = email
    current_user.is_business = is_business

    db.session.commit()

    return jsonify({"message": "Profile updated successfully"}), 200


# Get user paginated data for the listings on the dashboard
@accounts.route("/get-user-paginated-data", methods=["GET"])
@login_required
def get_user_paginated_data():
    page = request.args.get("page", 1, type=int)
    per_page = 6
    pagination = Business.query.filter_by(user_id=current_user.id).paginate(
        page=page, per_page=per_page, error_out=False
    )

    data = {
        "businesses": [business.to_dict() for business in pagination.items],
        "total_pages": pagination.pages,
        "current_page": pagination.page,
    }

    return jsonify(data)


# Render Bulk upload page
@accounts.route("/bulk-upload")
@login_required
def bulk_upload():
    data = {"active": 5, "tab": 3}
    return render_template("account/bulk-upload.html", data=data)


# Logic to upload csv and create businesses
@accounts.route("/upload-csv", methods=["POST"])
def upload_csv():

    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if not file.filename.endswith(".csv"):
        return jsonify({"error": "File is not a CSV"}), 400

    if file and file.filename.endswith(".csv"):
        upload_folder_csv = os.path.join(os.getcwd(), "app", "static", "uploads", "csv")
        os.makedirs(upload_folder_csv, exist_ok=True)

        upload_folder = os.path.join(os.getcwd(), "app", "static", "uploads")
        os.makedirs(upload_folder, exist_ok=True)

        user_id = current_user.id
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        new_filename = f"{user_id}_{timestamp}_{filename}"
        file_path = os.path.join(upload_folder_csv, new_filename)
        file.save(file_path)

        logs = []
        with open(file_path, newline="") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                print("Iteration")

                required_fields = [
                    "category_id",
                    "name",
                    "description",
                    "address",
                    "city",
                    "state",
                    "zip_code",
                    "phone_number",
                    "website",
                    "logo",
                    "cover_photo",
                ]
                for field in required_fields:
                    if field not in row or not row[field]:
                        logs.append(
                            f"Row {reader.line_num}: Missing or empty field {field}."
                        )
                        break
                else:

                    logo_filename = save_image_from_url(row["logo"], "logo")
                    cover_photo_filename = save_image_from_url(
                        row["cover_photo"], "cover"
                    )

                    if logo_filename and cover_photo_filename:

                        business = Business(
                            user_id=user_id,
                            category_id=row["category_id"],
                            name=row["name"],
                            description=row["description"],
                            address=row["address"],
                            city=row["city"],
                            state=row["state"],
                            zip_code=row["zip_code"],
                            phone_number=row["phone_number"],
                            website=row["website"],
                            logo=logo_filename,
                            cover_photo=cover_photo_filename,
                        )
                        db.session.add(business)
                        db.session.commit()
                        logs.append(
                            f"Row {reader.line_num}: Business '{row['name']}' created successfully."
                        )
                    else:
                        logs.append(f"Row {reader.line_num}: Failed to save images.")

        return jsonify({"logs": logs})

    return jsonify({"error": "Invalid file format"}), 400


# View to see previous uploads
@accounts.route("/previous-uploads", methods=["GET"])
def previous_uploads():
    data = {"active": 5, "tab": 3}
    user_id = current_user.id

    csv_files = []

    upload_folder_csv = os.path.join(os.getcwd(), "app", "static", "uploads", "csv")
    os.makedirs(upload_folder_csv, exist_ok=True)

    for filename in os.listdir(upload_folder_csv):
        if filename.startswith(f"{user_id}_") and filename.endswith(".csv"):
            match = re.match(rf"{user_id}_(\d{{14}})_(.+\.csv)", filename)
            if match:
                timestamp = match.group(1)
                original_filename = match.group(2)
                dt = datetime.strptime(timestamp, "%Y%m%d%H%M%S")
                csv_files.append(
                    {
                        "original_filename": original_filename,
                        "datetime": dt.strftime("%Y-%m-%d %H:%M:%S"),
                        "filename": filename,
                    }
                )

    data["csv_files"] = csv_files

    return render_template("account/previous-uploads.html", data=data)
