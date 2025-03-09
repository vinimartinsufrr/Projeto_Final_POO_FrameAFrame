from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Cliente

clientes_bp = Blueprint("clientes", __name__)

@clientes_bp.route("/clientes", methods=["GET", "POST"])
@login_required
def listar_clientes():
    if not current_user.is_admin:
        flash("Acesso negado! Apenas administradores podem acessar esta página.", "danger")
        return redirect(url_for("home.index"))

    if request.method == "POST":
        nome = request.form["nome"]
        cpf = request.form["cpf"]
        telefone = request.form["telefone"]
        email = request.form["email"]

        novo_cliente = Cliente(nome=nome, cpf=cpf, telefone=telefone, email=email)
        db.session.add(novo_cliente)
        db.session.commit()
        flash("Cliente cadastrado com sucesso!", "success")
        return redirect(url_for("clientes.listar_clientes"))

    clientes = Cliente.query.all()
    return render_template("clientes.html", clientes=clientes)
