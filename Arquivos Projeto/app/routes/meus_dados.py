from flask import Blueprint, render_template
from flask_login import login_required, current_user

meus_dados_bp = Blueprint("meus_dados", __name__)

@meus_dados_bp.route("/meus_dados")
@login_required
def visualizar_dados():
    return render_template("meus_dados.html", usuario=current_user)
