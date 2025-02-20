# models/filme.py

class Filme:
    def __init__(self, id_filme, titulo, genero, descricao, data_lancamento, preco, faixa_etaria, avaliacao, estoque):
        self.id_filme = id_filme
        self.titulo = titulo
        self.genero = genero
        self.descricao = descricao
        self.data_lancamento = data_lancamento
        self.preco = preco
        self.faixa_etaria = faixa_etaria
        self.avaliacao = avaliacao
        self.estoque = estoque  # Número de cópias disponíveis

    def verificar_disponibilidade(self):
        """Verifica se o filme está disponível para locação."""
        return self.estoque > 0

    def alugar(self):
        """Reduz o estoque ao alugar um filme, se disponível."""
        if self.verificar_disponibilidade():
            self.estoque -= 1
            return True
        return False

    def devolver(self):
        """Aumenta o estoque ao devolver um filme."""
        self.estoque += 1

    def __str__(self):
        return f"{self.titulo} ({self.data_lancamento}) - {self.genero} | Estoque: {self.estoque} | Avaliação: {self.avaliacao}/10"
