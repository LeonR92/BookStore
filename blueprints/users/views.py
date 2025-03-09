from flask import Blueprint, redirect, render_template, request, jsonify, url_for
from blueprints.users.credentials_repository import CredentialsRepository
from blueprints.users.crendentials_service import CredentialsService
from blueprints.users.user_repository import UserRepository
from blueprints.users.user_service import UserService
from core.database import get_read_db,get_write_db


users = Blueprint(
    "users",
    __name__,
    template_folder="templates",  
    static_folder="static" ,
    url_prefix="/users"       
)


@users.route("/login")
def login():
    return render_template("users_login.html")

@users.route("/register")
def register_user():
    return render_template("users_register.html")

@users.route("/users", methods=["POST"])
def create_user():
    """Create a new user."""
    data = request.form.to_dict()
    with get_write_db() as write_db, get_read_db() as read_db:
        user_repo = UserRepository(write_db,read_db)
        user_service = UserService(user_repo)
        user = user_service.create_user(**data)
        print(user)
    return redirect(url_for('users.login'))

@users.route("/create_credentials", methods=["POST"])
def create_credentials():
    """Create a new user with email and hashed password."""
    data = request.json

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400
    try:
        with get_write_db() as write_db, get_read_db() as read_db:
            cred_repo = CredentialsRepository(write_db, read_db)
            cred_service = CredentialsService(cred_repo)
            credentials = cred_service.create_credentials(email=email, password=password)

        return jsonify({"id": credentials.id, "email": credentials.email}), 201 

    except Exception as e:
        return jsonify({"error": str(e)}), 400  
    

