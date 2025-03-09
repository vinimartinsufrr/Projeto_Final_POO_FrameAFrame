from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Locacao, Filme, Cliente
from datetime import datetime, timedelta

locacoes_bp = Blueprint("locacoes", __name__)

@locacoes_bp.route("/locacoes", methods=["GET", "POST"])
@login_required
def locar_filmes():
    if request.method == "POST":
        filmes_ids = request.form.getlist("filmes")
        forma_pagamento = request.form["forma_pagamento"]
        data_retirada = request.form["data_retirada"]
        dias_locacao = int(request.form["dias_locacao"])

        # Verificando se todos os campos foram preenchidos
        if not filmes_ids or not forma_pagamento or not data_retirada or not dias_locacao:
            flash("Por favor, preencha todos os campos obrigatórios.", "danger")
            return redirect(url_for("locacoes.locar_filmes"))

        data_retirada = datetime.strptime(data_retirada, "%Y-%m-%d").date()

        # Calculando a data de devolução
        data_devolucao_prevista = calcular_data_devolucao(data_retirada, dias_locacao)

        # Calculando o valor total
        valor_total = sum(
            Filme.query.get(filme_id).preco * dias_locacao for filme_id in filmes_ids
        )

        for filme_id in filmes_ids:
            filme = Filme.query.get(filme_id)
            if filme and filme.quantidade_disponivel > 0:
                nova_locacao = Locacao(
                    cliente_id=current_user.id,
                    filme_id=filme.id,
                    data_locacao=data_retirada,
                    data_devolucao_prevista=data_devolucao_prevista,
                    preco_diario=filme.preco,
                    forma_pagamento=forma_pagamento,
                    valor_total=valor_total,
                    finalizada=False,  # Locação começa como pendente
                )
                db.session.add(nova_locacao)
                filme.quantidade_disponivel -= 1  # Reduz o estoque
            else:
                flash(f"Filme '{filme.titulo}' não disponível.", "danger")

        db.session.commit()
        flash("Filmes alugados com sucesso!", "success")
        return redirect(url_for("locacoes.listar_locacoes"))

    filmes_disponiveis = Filme.query.filter(Filme.quantidade_disponivel > 0).all()  # Filtrando apenas filmes disponíveis
    return render_template("locacoes.html", filmes=filmes_disponiveis)


@locacoes_bp.route("/locacoes")
@login_required
def listar_locacoes():
    if current_user.is_admin:
        locacoes = Locacao.query.all()
    else:
        locacoes = Locacao.query.filter_by(cliente_id=current_user.id).all()

    return render_template("locacoes.html", locacoes=locacoes)


def calcular_data_devolucao(data_locacao, dias_locacao):
    data_devolucao = data_locacao + timedelta(days=dias_locacao)
    if data_devolucao.weekday() == 5:
        data_devolucao += timedelta(days=2)
    elif data_devolucao.weekday() == 6:
        data_devolucao += timedelta(days=1)
    return data_devolucao
