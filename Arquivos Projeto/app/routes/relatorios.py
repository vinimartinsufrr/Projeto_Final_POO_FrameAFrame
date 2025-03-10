from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Usuario, Locacao, Filme

relatorios_bp = Blueprint("relatorios", __name__)


@relatorios_bp.route("/relatorios")
@login_required
def hub():
    """Exibe o hub de gerenciamento"""
    if current_user.is_admin:
        return render_template("relatorios_hub.html")
    else:
        return "Você não tem permissão para acessar esta página.", 403


@relatorios_bp.route("/relatorios/clientes")
@login_required
def listar_clientes():
    """Lista todos os clientes registrados"""
    if current_user.is_admin:
        usuarios = Usuario.query.all()
        return render_template("relatorios_clientes.html", usuarios=usuarios)
    else:
        return "Você não tem permissão para acessar esta página.", 403


@relatorios_bp.route("/relatorios/locacoes")
@login_required
def listar_locacoes():
    """Lista todas as locações realizadas"""
    if current_user.is_admin:
        locacoes = Locacao.query.all()
        relatorios = {}

        for locacao in locacoes:
            cliente = Usuario.query.get(locacao.cliente_id)
            filmes = Filme.query.filter(Filme.id == locacao.filme_id).all()

            if locacao.id not in relatorios:
                # Inicializa a locação com o primeiro filme
                relatorios[locacao.id] = {
                    "id": locacao.id,
                    "cliente_nome": cliente.nome,
                    "filmes": [filme.titulo for filme in filmes],
                    "valor_total": locacao.valor_total,
                    "forma_pagamento": locacao.forma_pagamento,
                    "data_retirada": locacao.data_locacao,
                    "data_devolucao": locacao.data_devolucao_prevista,
                    "finalizada": locacao.finalizada,
                }
            else:
                # Se a locação já estiver no dicionário, apenas adiciona o filme e soma o valor
                relatorios[locacao.id]["filmes"].extend([filme.titulo for filme in filmes])
                relatorios[locacao.id]["valor_total"] += locacao.valor_total  

        # Convertendo o dicionário para lista
        relatorios_list = list(relatorios.values())
        return render_template("relatorios_locacoes.html", relatorios=relatorios_list)
    else:
        return "Você não tem permissão para acessar esta página.", 403

@relatorios_bp.route("/relatorios/finalizar/<int:locacao_id>", methods=["POST"])
@login_required
def finalizar_locacao(locacao_id):
    """Finaliza a locação, altera o status e incrementa o estoque do filme"""
    if not current_user.is_admin:
        flash("Você não tem permissão para realizar essa ação.", "danger")
        return redirect(url_for("relatorios.listar_locacoes"))

    locacao = Locacao.query.get_or_404(locacao_id)

    if locacao.finalizada:
        flash("Essa locação já foi finalizada.", "warning")
    else:
        
        locacao.finalizada = True

        
        filme = Filme.query.get(locacao.filme_id)
        if filme:
            filme.quantidade_disponivel += 1  # Incrementa o estoque

        db.session.commit()
        flash("Locação finalizada com sucesso!", "success")

    return redirect(url_for("relatorios.listar_locacoes"))
