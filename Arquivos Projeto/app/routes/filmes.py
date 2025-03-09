from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.models import Filme, Avaliacao
from flask_login import login_required

filmes_bp = Blueprint("filmes", __name__)


@filmes_bp.route("/filmes", methods=["GET", "POST"])
@login_required
def listar_filmes():
    if request.method == "POST":
        titulo = request.form["titulo"]
        genero = request.form["genero"]
        ano = int(request.form["ano"])
        diretor = request.form["diretor"]
        quantidade = int(request.form["quantidade_disponivel"])
        descricao = request.form["descricao"]
        preco = float(request.form["preco"])
        imagem_url = request.form["imagem_url"]

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
        db.session.add(novo_filme)
        db.session.commit()

        return redirect(url_for("filmes.listar_filmes"))

    filmes = Filme.query.all()
    return render_template("filmes_admin.html", filmes=filmes)


