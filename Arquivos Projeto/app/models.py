from app import db  # 🔹 Importamos `db` da app para evitar problemas de múltiplas instâncias
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta


class Usuario(db.Model, UserMixin):
    """Tabela de usuários - Inclui tanto clientes quanto administradores."""
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(256), nullable=False)
    # Define se o usuário é administrador
    is_admin = db.Column(db.Boolean, default=False)

    # 🔹 Relação 1:1 com Cliente
    cliente = db.relationship(
        "Cliente", back_populates="usuario", uselist=False)

    def set_password(self, senha):
        """Gera o hash da senha e armazena."""
        self.senha_hash = generate_password_hash(senha)

    def check_password(self, senha):
        """Verifica se a senha inserida corresponde ao hash armazenado."""
        return check_password_hash(self.senha_hash, senha)


class Cliente(db.Model):
    """Tabela de clientes - Está vinculada a um usuário da tabela `Usuario`."""
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey(
        "usuario.id"), nullable=False, unique=True)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    telefone = db.Column(db.String(20))

    # 🔹 Relação 1:1 com Usuario
    usuario = db.relationship("Usuario", back_populates="cliente")
    # 🔹 Um cliente pode ter várias locações
    locacoes = db.relationship("Locacao", backref="cliente", lazy="dynamic")


class Filme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), unique=True, nullable=False)
    genero = db.Column(db.String(50), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    diretor = db.Column(db.String(100))
    quantidade_disponivel = db.Column(db.Integer, nullable=False)
    descricao = db.Column(db.Text, nullable=True)  # 🔹 Adicionamos descrição
    preco = db.Column(db.Float, nullable=False)  # 🔹 Adicionamos preço
    imagem_url = db.Column(db.String(255), nullable=True)  # 🔹 Link da imagem

    def __repr__(self):
        return f"<Filme {self.titulo} ({self.ano})>"


class Locacao(db.Model):
    """Tabela de locações realizadas pelos clientes."""
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey(
        "cliente.id"), nullable=False)
    filme_id = db.Column(db.Integer, db.ForeignKey("filme.id"), nullable=False)
    data_locacao = db.Column(db.Date, nullable=False)
    data_devolucao_prevista = db.Column(db.Date, nullable=False)
    data_devolucao_real = db.Column(db.Date, nullable=True)
    valor_total = db.Column(db.Float, nullable=False)
    multa = db.Column(db.Float, default=0.0)
    forma_pagamento = db.Column(db.String(50), nullable=False)
    retirada_feita = db.Column(db.Boolean, default=False)
    preco_diario = db.Column(db.Float, nullable=False)
    # 🚀 Adicionamos o campo de status
    finalizada = db.Column(db.Boolean, default=False)

    filme = db.relationship("Filme", backref="locacoes")

    def __init__(self, cliente_id, filme_id, data_locacao, preco_diario, forma_pagamento, data_devolucao_prevista, valor_total=None, finalizada=False):
        self.cliente_id = cliente_id
        self.filme_id = filme_id
        self.data_locacao = data_locacao
        self.preco_diario = preco_diario
        self.forma_pagamento = forma_pagamento
        self.data_devolucao_prevista = data_devolucao_prevista
        self.valor_total = valor_total if valor_total else preco_diario
        self.finalizada = finalizada  # ✅ Agora o modelo reconhece esse campo!

    def calcular_data_devolucao(self, data_locacao, dias_locacao):
        data_devolucao = data_locacao + timedelta(days=dias_locacao)
        if data_devolucao.weekday() == 5:
            data_devolucao += timedelta(days=2)
        elif data_devolucao.weekday() == 6:
            data_devolucao += timedelta(days=1)
        return data_devolucao
