from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
# 🔹 Importamos Cliente para armazenar CPF e telefone
from app.models import Usuario, Cliente
from app import db

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]
        user = Usuario.query.filter_by(email=email).first()

        if user and user.check_password(senha):
            login_user(user)
            flash("Login bem-sucedido!", "success")
            return redirect(url_for("home.index"))
        else:
            flash("Credenciais inválidas.", "danger")

    return render_template("login.html")


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("Você saiu da conta.", "info")
    return redirect(url_for("auth.login"))


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]
        cpf = request.form["cpf"]
        telefone = request.form["telefone"]

        # 🔹 Validações no backend
        if len(nome) < 4:
            flash("O nome deve ter pelo menos 4 caracteres.", "danger")
            return redirect(url_for("auth.register"))

        if not cpf.isdigit() or len(cpf) != 11:
            flash("CPF inválido! Deve conter exatamente 11 números.", "danger")
            return redirect(url_for("auth.register"))

        if not telefone.isdigit() or len(telefone) != 11:
            flash(
                "Número de telefone inválido! Deve conter exatamente 11 números.", "danger")
            return redirect(url_for("auth.register"))

        if not email.endswith(".com"):
            flash("E-mail inválido! O endereço deve terminar com '.com'.", "danger")
            return redirect(url_for("auth.register"))

        if len(senha) < 4:
            flash("A senha deve ter pelo menos 4 caracteres.", "danger")
            return redirect(url_for("auth.register"))

        # Verifica se o e-mail já está cadastrado
        if Usuario.query.filter_by(email=email).first():
            flash("E-mail já cadastrado!", "danger")
            return redirect(url_for("auth.register"))

        # Verifica se o CPF já está cadastrado
        if Cliente.query.filter_by(cpf=cpf).first():
            flash("CPF já cadastrado!", "danger")
            return redirect(url_for("auth.register"))

        # 🔹 Criando o usuário e cliente
        novo_usuario = Usuario(nome=nome, email=email, is_admin=False)
        novo_usuario.set_password(senha)
        db.session.add(novo_usuario)
        db.session.commit()

        # Criar entrada na tabela Cliente
        novo_cliente = Cliente(usuario_id=novo_usuario.id,
                               cpf=cpf, telefone=telefone)
        db.session.add(novo_cliente)
        db.session.commit()

        flash("Conta criada com sucesso! Faça login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")
