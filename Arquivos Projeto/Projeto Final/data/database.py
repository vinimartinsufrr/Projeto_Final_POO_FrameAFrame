import sqlite3
from models.usuario import Usuario


def criar_banco():
    conexao = sqlite3.connect("data/locadora.db")
    cursor = conexao.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cpf TEXT UNIQUE NOT NULL,
        telefone TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL,
        administrador INTEGER DEFAULT 0
    )""")

    # Verifica se já existe um administrador
    cursor.execute("SELECT * FROM usuarios WHERE administrador = 1")
    admin_existe = cursor.fetchone()

    if not admin_existe:
        # Insere um administrador padrão se não existir
        cursor.execute("INSERT INTO usuarios (nome, cpf, telefone, email, senha, administrador) VALUES (?, ?, ?, ?, ?, ?)",
                       ("Admin", "12345678901", "(11) 91111-1111", "admin@locadora.com", "1234", 1))
        conexao.commit()

    conexao.close()

def tornar_administrador(email):
    """
    Torna um usuário administrador com base no email.
    """
    conexao = sqlite3.connect("data/locadora.db")
    cursor = conexao.cursor()

    # Verifica se o usuário existe
    cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
    usuario = cursor.fetchone()

    if usuario:
        # Atualiza o usuário para administrador
        cursor.execute("UPDATE usuarios SET administrador = 1 WHERE email = ?", (email,))
        conexao.commit()
        conexao.close()
        return True  # Retorna True se a promoção foi bem-sucedida
    else:
        conexao.close()
        return False  # Retorna False se o usuário não existir


def cadastrar_usuario(nome, cpf, telefone, email, senha, administrador=False):
    """Cadastra um novo usuário no banco de dados."""
    conexao = sqlite3.connect("data/locadora.db")
    cursor = conexao.cursor()

    try:
        cursor.execute(
            "INSERT INTO usuarios (nome, cpf, telefone, email, senha, administrador) VALUES (?, ?, ?, ?, ?, ?)",
            (nome, cpf, telefone, email, senha, int(administrador)),
        )
        conexao.commit()
        conexao.close()
        return True  # Cadastro realizado com sucesso
    except sqlite3.IntegrityError:
        conexao.close()
        return False  # E-mail ou CPF já cadastrados


def consultar_usuario(email, senha):
    """Busca um usuário no banco de dados pelo e-mail e senha e retorna um objeto Usuario."""
    conexao = sqlite3.connect("data/locadora.db")
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT nome, cpf, telefone, email, senha, administrador FROM usuarios WHERE email = ? AND senha = ?",
        (email, senha),
    )
    usuario_db = cursor.fetchone()
    conexao.close()

    if usuario_db:
        nome, cpf, telefone, email, senha, administrador = usuario_db
        return Usuario(nome, cpf, telefone, email, senha, administrador=bool(administrador))

    return None  # Retorna None se não encontrar o usuário
