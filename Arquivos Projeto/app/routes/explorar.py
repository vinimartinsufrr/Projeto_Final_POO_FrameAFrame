from flask import Blueprint, render_template
from flask_login import login_required
from app.models import Filme

explorar_bp = Blueprint("explorar", __name__)

@explorar_bp.route("/explorar")
@login_required
def explorar_filmes():
    filmes = Filme.query.all()
    filmes_disponiveis = [filme for filme in filmes if filme.quantidade_disponivel > 0]
    filmes_indisponiveis = [filme for filme in filmes if filme.quantidade_disponivel == 0]

    return render_template("explorar.html", filmes_disponiveis=filmes_disponiveis, filmes_indisponiveis=filmes_indisponiveis)