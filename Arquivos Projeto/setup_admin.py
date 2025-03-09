from app import create_app, db
from app.models import Usuario

app = create_app()

with app.app_context():
    admin_email = "admin@locadora.com"

    if not Usuario.query.filter_by(email=admin_email).first():
        admin = Usuario(nome="Admin", email=admin_email, is_admin=True)
        admin.set_password("admin123")  # 🔹 Define a senha do admin
        db.session.add(admin)
        db.session.commit()
        print("✅ Conta de administrador criada com sucesso!")
    else:
        print("⚠️ Conta de administrador já existe.")
