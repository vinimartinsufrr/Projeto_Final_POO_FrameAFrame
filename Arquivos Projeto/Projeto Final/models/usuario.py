# models/usuario.py
import re


class Usuario:
    def __init__(self, nome: str, cpf: str, telefone: str, email: str, senha: str, administrador: bool = False):
        """Inicializa um usuário com suas informações pessoais e valida os dados."""
        if not self.validar_nome(nome):
            raise ValueError("Nome deve ter pelo menos 3 caracteres.")
        if not self.validar_cpf(cpf):
            raise ValueError(
                "CPF inválido. Deve conter exatamente 11 dígitos numéricos.")
        if not self.validar_telefone(telefone):
            raise ValueError(
                "Telefone inválido. O formato correto é (11) 91111-1111.")
        if not self.validar_senha(senha):
            raise ValueError("A senha deve ter pelo menos 4 caracteres.")

        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.email = email
        self.senha = senha
        self.administrador = administrador
        self.filmes_alugados = []  # Lista de filmes alugados pelo usuário

    @staticmethod
    def validar_nome(nome):
        """Verifica se o nome tem pelo menos 3 caracteres."""
        if len(nome) < 3:
            raise ValueError("O nome deve ter pelo menos 3 caracteres.")
        return True

    @staticmethod
    def validar_cpf(cpf):
        """Verifica se o CPF tem exatamente 11 dígitos numéricos."""
        if not re.fullmatch(r"\d{11}", cpf):
            raise ValueError(
                "CPF inválido. Deve conter exatamente 11 dígitos numéricos.")
        return True

    @staticmethod
    def validar_telefone(telefone):
        """Verifica se o telefone está no formato correto: (XX) 9XXXX-XXXX"""
        if not re.fullmatch(r"\(\d{2}\) 9\d{4}-\d{4}", telefone):
            raise ValueError(
                "O telefone deve estar no formato (XX) 9XXXX-XXXX.")
        return True

    @staticmethod
    def validar_senha(senha: str):
        """Verifica se a senha tem pelo menos 4 caracteres."""
        if len(senha) < 4:
            raise ValueError("A senha deve ter pelo menos 4 caracteres.")
        return True

    def eh_administrador(self) -> bool:
        """Verifica se o usuário é administrador."""
        return self.administrador

    def __str__(self):
        tipo = "Administrador" if self.administrador else "Cliente"
        return f"{self.nome} ({tipo}) - Email: {self.email}"
