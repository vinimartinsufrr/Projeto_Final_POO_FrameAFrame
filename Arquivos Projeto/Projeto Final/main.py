import streamlit as st
from data.database import criar_banco, consultar_usuario, cadastrar_usuario, tornar_administrador
from models.usuario import Usuario

# Criar o banco de dados ao iniciar
criar_banco()

st.title("🎬 Locadora FrameAFrame")

# Verifica se o usuário está logado
if "usuario_logado" not in st.session_state:
    st.session_state["usuario_logado"] = None

usuario_logado = st.session_state["usuario_logado"]

if usuario_logado:
    # 🔹 Menu Principal (Aparece apenas para usuários logados)
    menu_opcao = st.selectbox(
        "📌 Escolha uma opção:",
        ["Meus Dados", "Minhas Locações", "Sair"]
    )

    if menu_opcao == "Meus Dados":
        st.subheader("👤 Meus Dados")
        st.write(f"**Nome:** {usuario_logado.nome}")
        st.write(f"**E-mail:** {usuario_logado.email}")
        st.write(f"**CPF:** {usuario_logado.cpf}")
        st.write(f"**Telefone:** {usuario_logado.telefone}")
        st.write(f"**Tipo de Conta:** {'Administrador' if usuario_logado.eh_administrador() else 'Cliente'}")

    elif menu_opcao == "Minhas Locações":
        st.subheader("🎥 Minhas Locações")
        if usuario_logado.filmes_alugados:
            for locacao in usuario_logado.filmes_alugados:
                st.write(f"📽️ {locacao.filme.titulo} - Devolução: {locacao.data_devolucao_prevista.strftime('%d/%m/%Y')}")
        else:
            st.write("📭 Você não possui locações ativas.")

    elif menu_opcao == "Sair":
        st.session_state["usuario_logado"] = None
        st.success("👋 Você saiu do sistema.")
        st.rerun()  # Recarrega a página

else:
    # 🔹 Tela de Login/Cadastro (Aparece somente para usuários deslogados)
    st.sidebar.header("🔑 Acesso")
    opcao = st.sidebar.radio("Escolha uma opção:", ["Login", "Cadastrar"])

    if opcao == "Login":
        email = st.sidebar.text_input("E-mail")
        senha = st.sidebar.text_input("Senha", type="password")

        if st.sidebar.button("Entrar"):
            usuario_logado = consultar_usuario(email, senha)
            if usuario_logado:
                st.session_state["usuario_logado"] = usuario_logado
                st.sidebar.success(f"✅ Bem-vindo, {usuario_logado.nome}!")
                st.rerun()  # Recarrega a página para mostrar o menu
            else:
                st.sidebar.error("❌ Usuário ou senha incorretos.")

    elif opcao == "Cadastrar":
        nome = st.sidebar.text_input("Nome")
        cpf = st.sidebar.text_input("CPF (somente números)")
        telefone = st.sidebar.text_input("Telefone (formato (XX) 9XXXX-XXXX)")
        email = st.sidebar.text_input("E-mail")
        senha = st.sidebar.text_input("Senha", type="password")

        if st.sidebar.button("Criar Conta"):
            try:
                novo_usuario = Usuario(nome, cpf, telefone, email, senha)
                if cadastrar_usuario(novo_usuario.nome, novo_usuario.cpf, novo_usuario.telefone, novo_usuario.email, novo_usuario.senha, novo_usuario.administrador):
                    st.session_state["usuario_logado"] = novo_usuario
                    st.sidebar.success("✅ Cadastro realizado com sucesso! Você já está logado.")
                    st.rerun()  # Recarrega a página para mostrar o menu
                else:
                    st.sidebar.error("❌ Este e-mail ou CPF já está cadastrado.")
            except ValueError as e:
                st.sidebar.error(f"Erro no cadastro: {e}")

