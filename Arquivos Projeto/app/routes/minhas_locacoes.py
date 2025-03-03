from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Locacao, Filme

minhas_locacoes_bp = Blueprint("minhas_locacoes", __name__)

@minhas_locacoes_bp.route("/minhas_locacoes")
@login_required
def visualizar_locações():
    locacoes = Locacao.query.filter_by(cliente_id=current_user.id).all()

    # Formatar os dados corretamente para exibição no HTML
    locacoes_formatadas = []
    for locacao in locacoes:
        filmes = Filme.query.filter(Filme.id == locacao.filme_id).all()

        locacoes_formatadas.append({
            "id": locacao.id,
            "filmes": [filme.titulo for filme in filmes],
            "data_locacao": locacao.data_locacao,
            "data_devolucao_prevista": locacao.data_devolucao_prevista,
            "valor_total": locacao.valor_total,
            "finalizada": locacao.finalizada
        })

    return render_template("minhas_locacoes.html", locacoes=locacoes_formatadas)
