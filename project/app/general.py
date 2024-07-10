from flask import Blueprint, render_template, request, jsonify
from .models import Category, Business

# from .utils import get_businesses_by_category
from sqlalchemy import or_

general = Blueprint("general", __name__)


@general.route("/")
def home():
    data = {"active": 1}
    data["categories"] = Category.query.all()
    return render_template("guest/home.html", data=data)


@general.route("/about")
def about():
    data = {"active": 2}
    return render_template("guest/about.html", data=data)


@general.route("/categories")
def categories():
    data = {"active": 3}
    data["categories"] = Category.query.all()
    return render_template("guest/categories.html", data=data)


@general.route("/categories/<int:cat_id>")
def categories_details(cat_id):
    data = {"active": 3}
    data["category"] = Category.query.get(cat_id)
    return render_template("guest/categories-list.html", data=data)


@general.route("/business-profile/<int:business_id>")
def business_details(business_id):
    data = {"active": 3}
    data["business"] = Business.query.get(business_id)
    return render_template("guest/business-profile.html", data=data)


@general.route("/contact")
def contact():
    data = {"active": 4}
    return render_template("guest/contact.html", data=data)


@general.route("/load-businesses-by-category", methods=["GET"])
def get_user_paginated_data():
    page = request.args.get("page", 1, type=int)
    category_id = int(request.args.get("category_id"))
    per_page = 6
    pagination = Business.query.filter_by(category_id=category_id).paginate(
        page=page, per_page=per_page, error_out=False
    )

    data = {
        "businesses": [business.to_dict() for business in pagination.items],
        "total_pages": pagination.pages,
        "current_page": pagination.page,
    }

    return jsonify(data)


@general.route("/load-businesses-on-home-page", methods=["GET"])
def load_business_by_search():
    page = request.args.get("page", 1, type=int)
    search_term = request.args.get("search_term", "")
    category = request.args.get("category", type=int)
    address = request.args.get("address", "")
    city = request.args.get("city", "")
    state = request.args.get("state", "")
    per_page = 6

    query = Business.query.filter_by()

    if search_term:
        query = query.filter(
            or_(
                Business.name.ilike(f"%{search_term}%"),
                Business.description.ilike(f"%{search_term}%"),
            )
        )
    if category:
        query = query.filter_by(category_id=category)
    if address:
        query = query.filter(Business.address.ilike(f"%{address}%"))
    if city:
        query = query.filter(Business.city.ilike(f"%{city}%"))
    if state:
        query = query.filter(Business.state.ilike(f"%{state}%"))

    per_page = 6
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    data = {
        "businesses": [business.to_dict() for business in pagination.items],
        "total_pages": pagination.pages,
        "current_page": pagination.page,
    }

    return jsonify(data)
