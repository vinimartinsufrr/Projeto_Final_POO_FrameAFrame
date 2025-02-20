# models/locacao.py

from datetime import datetime, timedelta
from models.filme import Filme  # Importando a classe Filme
from models.usuario import Usuario  # Importando a classe Usuario


class Locacao:
    MULTA_DIARIA = 1.00  # Multa de R$1,00 por dia de atraso
    LIMITE_FILMES = 5  # Máximo de filmes que um usuário pode alugar ao mesmo tempo

    def __init__(self, usuario: Usuario, filme: Filme, dias_aluguel: int):
        """Inicializa uma locação associada a um usuário e um filme."""
        self.usuario = usuario  # Corrigido para seguir convenção de variáveis
        self.filme = filme
        self.data_locacao = datetime.now()
        self.data_devolucao_prevista = self.data_locacao + timedelta(days=dias_aluguel)
        self.data_devolucao_real = None
        self.valor_total = filme.preco * dias_aluguel
        self.multa = 0.0

    def realizar_locacao(self) -> bool:
        """Tenta alugar um filme verificando a disponibilidade e o limite do usuário."""
        if len(self.usuario.filmes_alugados) >= self.LIMITE_FILMES:
            return False  # Usuário atingiu o limite de locações

        if self.filme.verificar_disponibilidade():
            self.filme.alugar()
            self.usuario.filmes_alugados.append(self)  # Registra a locação no usuário
            return True
        return False

    def devolver_filme(self):
        """Processa a devolução do filme, remove dos alugados e calcula multa se houver atraso."""
        self.data_devolucao_real = datetime.now()
        atraso = (self.data_devolucao_real - self.data_devolucao_prevista).days

        if atraso > 0:
            self.multa = atraso * self.MULTA_DIARIA

        self.filme.devolver()  # Atualiza o estoque do filme
        self.usuario.filmes_alugados.remove(self)  # Remove a locação ativa do usuário

    def __str__(self):
        status = "Em andamento" if not self.data_devolucao_real else "Finalizada"
        return f"Locação de '{self.filme.titulo}' para {self.usuario.nome} | Status: {status}"
