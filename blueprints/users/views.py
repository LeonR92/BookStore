from flask import Blueprint, abort, redirect, render_template, request, jsonify, session, url_for
from core.di import create_mfa_service, create_user_service

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

        user_service = create_user_service(write_db=write_db,read_db=read_db)
        user_service.create_user(**data)
        return redirect(url_for('users.login'))



@users.route("/get_users")
def get_user():
     with get_write_db() as write_db, get_read_db() as read_db:
        user_service = create_user_service(write_db=write_db, read_db=read_db)
        users = user_service.get_all_users()
        return jsonify([{k: v for k, v in user.__dict__.items() if not k.startswith("_")} for user in users])

@users.route("/show_qr_code/<int:user_id>")
def show_qrcode(user_id: int):
    """Display QR code for MFA setup for both new and existing users"""
    with get_write_db() as write_db, get_read_db() as read_db:
        user_service = create_user_service(write_db=write_db, read_db=read_db)
        
        user = user_service.get_user_by_id(user_id)
        if not user:
            abort(404)
            
        name = f"{user.last_name} {user.first_name}"
        mfa_service = create_mfa_service(write_db=write_db, read_db=read_db)
        qr_data = mfa_service.create_qrcode_totp(name=name, user_id=user_id)
        
        return render_template(
            'users_qrcode.html',
            qr_code=qr_data['qr_code_base64'],
            user_id=user_id,
            name=name
        )


@users.route("/mfa_input")
def mfa_input():
    user_id = session.get("user_id") 
    return render_template("users_otp_input.html", user_id = user_id)
