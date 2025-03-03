from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Filme, Locacao

relatorios_estoque_bp = Blueprint("relatorios_estoque", __name__)

@relatorios_estoque_bp.route("/relatorios/estoque")
@login_required
def listar_estoque():
    if not current_user.is_admin:
        return "Você não tem permissão para acessar esta página.", 403

    filmes = Filme.query.all()
    estoque_info = []

    for filme in filmes:
        alugados = Locacao.query.filter_by(filme_id=filme.id, finalizada=False).count()
        estoque_info.append({
            "id": filme.id,
            "titulo": filme.titulo,
            "quantidade_total": filme.quantidade_disponivel + alugados,
            "quantidade_alugada": alugados,
            "quantidade_disponivel": filme.quantidade_disponivel
        })

    return render_template("relatorios_estoque.html", estoque=estoque_info)
