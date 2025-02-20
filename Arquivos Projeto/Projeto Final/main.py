import streamlit as st
from data.database import criar_banco, consultar_usuario, cadastrar_usuario, tornar_administrador
from models.usuario import Usuario

# Criando o banco de dados ao iniciar
criar_banco()

st.title("🎬 Locadora FrameAFrame")

# Tela de Login/Cadastro
st.sidebar.header("🔑 Acesso")

opcao = st.sidebar.radio("Escolha uma opção:", ["Login", "Cadastrar"])

if "usuario_logado" not in st.session_state:
    st.session_state["usuario_logado"] = None

if opcao == "Login":
    email = st.sidebar.text_input("E-mail")
    senha = st.sidebar.text_input("Senha", type="password")

    if st.sidebar.button("Entrar"):
        usuario_logado = consultar_usuario(email, senha)
        if usuario_logado:
            st.session_state["usuario_logado"] = usuario_logado
            st.sidebar.success(f"✅ Bem-vindo, {usuario_logado.nome}!")
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
            else:
                st.sidebar.error("❌ Este e-mail ou CPF já está cadastrado.")
        except ValueError as e:
            st.sidebar.error(f"Erro no cadastro: {e}")

# Exibição de informações pós-login
usuario_logado = st.session_state["usuario_logado"]

if usuario_logado:
    st.subheader(f"👋 Olá, {usuario_logado.nome}!")

    if usuario_logado.eh_administrador():
        st.write("🔧 Você tem acesso às funções administrativas.")
        st.write("📌 Aqui você pode gerenciar filmes e usuários.")
        st.subheader("👑 Gestão de Usuários")

        email_promo = st.text_input("E-mail do usuário para tornar administrador")
        if st.button("Promover a Administrador"):
            if tornar_administrador(email_promo):
                st.success(f"✅ O usuário {email_promo} agora é administrador!")
            else:
                st.error("❌ Usuário não encontrado.")

    else:
        st.write("🎥 Explore nosso catálogo de filmes e faça locações!")

else:
    st.write("🔒 Faça login para acessar o sistema.")
