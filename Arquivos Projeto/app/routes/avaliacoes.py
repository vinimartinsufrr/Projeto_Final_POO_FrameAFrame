from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Filme, Avaliacao

avaliacoes_bp = Blueprint('avaliacoes', __name__)

# Rota para mostrar a página de detalhes do filme e permitir avaliação
@avaliacoes_bp.route("/filmes/<int:filme_id>", methods=["GET", "POST"])
@login_required
def detalhes_filme(filme_id):
    filme = Filme.query.get_or_404(filme_id)

    if request.method == "POST":
        nota = request.form['nota']
        descricao = request.form['descricao']

        # Validação da nota
        if not (0 <= float(nota) <= 5):
            flash("A nota deve ser entre 0 e 5", "danger")
            return redirect(url_for('avaliacoes.detalhes_filme', filme_id=filme_id))

        # Criando uma nova avaliação
        nova_avaliacao = Avaliacao(
            nota=nota, descricao=descricao, filme_id=filme.id, usuario_id=current_user.id
        )
        db.session.add(nova_avaliacao)
        db.session.commit()
        flash("Avaliação enviada com sucesso!", "success")

        # Após salvar a avaliação, redireciona para evitar reenvio
        return redirect(url_for('avaliacoes.detalhes_filme', filme_id=filme.id))

    # Carregando as avaliações ao fazer o GET
    avaliacoes = Avaliacao.query.filter_by(filme_id=filme.id).all()

    return render_template('detalhes_filme.html', filme=filme, avaliacoes=avaliacoes)
