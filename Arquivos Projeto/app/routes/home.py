from flask import Blueprint, redirect, url_for
from flask_login import current_user

home_bp = Blueprint("home", __name__)

@home_bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("explorar.explorar_filmes"))  # Se logado, vai para explorar filmes
    return redirect(url_for("auth.login"))  
