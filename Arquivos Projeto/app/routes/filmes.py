from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Filme
from flask_login import login_required

filmes_bp = Blueprint("filmes", __name__)

@filmes_bp.route("/filmes", methods=["GET", "POST"])
@login_required
def cadastrar_filmes():
    if request.method == "POST":
        titulo = request.form.get("titulo")
        genero = request.form.get("genero")
        ano = request.form.get("ano")
        diretor = request.form.get("diretor")
        quantidade = request.form.get("quantidade_disponivel")
        descricao = request.form.get("descricao")
        preco = request.form.get("preco")
        imagem_url = request.form.get("imagem_url")

        # Validação dos campos obrigatórios
        if not titulo or not genero or not ano or not diretor or not quantidade or not descricao or not imagem_url or not preco:
            flash("Por favor, preencha todos os campos obrigatórios.", category="filme_cadastro")
            return redirect(url_for("filmes.cadastrar_filmes"))

        try:
            ano = int(ano)
            quantidade = int(quantidade)
            preco = float(preco)
        except ValueError:
            flash("Certifique-se de que os campos de ano, quantidade e preço são válidos.", category="filme_cadastro")
            return redirect(url_for("filmes.cadastrar_filmes"))

        novo_filme = Filme(
            titulo=titulo,
            genero=genero,
            ano=ano,
            diretor=diretor,
            quantidade_disponivel=quantidade,
            descricao=descricao,
            preco=preco,
            imagem_url=imagem_url,
        )

        # Adiciona o filme no banco de dados
        db.session.add(novo_filme)
        db.session.commit()

        flash("Filme cadastrado com sucesso!", category="filme_cadastro")
        return redirect(url_for("filmes.cadastrar_filmes"))

    filmes = Filme.query.all()
    return render_template("filmes_admin.html", filmes=filmes)

# Rota para gerenciar filmes
@filmes_bp.route("/gerenciar_filmes", methods=["GET", "POST"])
@login_required
def gerenciar_filmes():
    filmes = Filme.query.all()

    if request.method == "POST":
        if "adicionar_exemplares" in request.form:
            filme_id = request.form["filme_id"]
            quantidade = int(request.form["quantidade"])
            filme = Filme.query.get(filme_id)
            if filme:
                filme.quantidade_disponivel += quantidade
                db.session.commit()
                flash(f"Adicionados {quantidade} exemplares ao filme '{filme.titulo}'", category="sucesso")
            else:
                flash("Filme não encontrado.", category="erro")
        elif "remover_filme" in request.form:
            filme_id = request.form["filme_id"]
            filme = Filme.query.get(filme_id)
            if filme:
                db.session.delete(filme)
                db.session.commit()
                flash(f"Filme '{filme.titulo}' removido com sucesso.", category="sucesso")
            else:
                flash("Filme não encontrado.", category="erro")
        return redirect(url_for("filmes.gerenciar_filmes"))

    return render_template("gerenciar_filmes.html", filmes=filmes)
