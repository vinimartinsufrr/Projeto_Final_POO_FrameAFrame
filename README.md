🎬 Sistema de Locadora de Vídeos

✨ Introdução

Bem-vindo ao nosso Sistema de Locadora de Vídeos! Este projeto foi desenvolvido com base nos conceitos de Programação Orientada a Objetos (POO) e tem como objetivo oferecer uma maneira eficiente de gerenciar o aluguel de filmes. Com ele, os usuários podem visualizar e reservar filmes, enquanto os administradores têm controle sobre clientes, locações e estoque de filmes.

🔍 Funcionalidades Principais

👤 Gerenciamento de Usuários

Cadastro de novos usuários com nome, CPF, telefone e e-mail.

Edição e exclusão de cadastros de clientes.

Consulta de clientes ativos e histórico de locações.

🎬 Gerenciamento de Filmes

Cadastro de filmes com título, gênero, ano de lançamento, diretor e quantidade disponível.

Edição e remoção de registros de filmes.

Consulta de filmes disponíveis e alugados.

✅ Controle de Locações

Realização de novas locações associando um cliente a um ou mais filmes.

Cálculo automático do valor do aluguel com base na categoria do filme e tempo de locação.

Registro de datas de locação e devolução.

Controle de devoluções com cálculo de multas por atraso.

📝 Relatórios e Consultas

Visualização de locações em andamento e clientes com pendências.

Histórico de locações por cliente e por filme.

📚 Regras de Negócio

Cadastro de Clientes: Cada cliente deve ter um CPF único. Não é possível alugar sem cadastro.

Cadastro de Filmes: O título do filme deve ser único e o estoque deve ser controlado.

Locação de Filmes: Um cliente pode alugar até 5 filmes simultaneamente. O valor do aluguel é cobrado por dia.

Devolução e Multas: Multa diária de R$ 1,00 por atraso. Após a devolução, o filme volta ao estoque.

🎨 Tecnologias Utilizadas

Linguagem: Python

Framework para Interface: Streamlit

Banco de Dados: SQLite (ou outra opção a ser definida)

✨ Como Executar o Projeto

Clone este repositório:

git clone https://github.com/seu-usuario/seu-repositorio.git

Instale as dependências necessárias:

pip install -r requirements.txt

Execute o sistema:

streamlit run app.py

✨ Contribuição

Se você deseja contribuir para este projeto, fique à vontade para enviar pull requests ou abrir issues relatando bugs ou sugerindo melhorias.

👤 Equipe

Nome do Integrante 1

Nome do Integrante 2

Nome do Integrante 3

Feito com ❤️ pela equipe!
