# Imports necessários
import sqlalchemy as sa
from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from ..extensions import db, login_manager
from ..models.users import User
from flask_login import  login_required

user_bp = Blueprint("user", __name__, url_prefix="/user") #Criando uma Blueprint(Agrupamnento de rotas)

# Carregando os dados do usuário
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# Rota login
@user_bp.route("/login", methods=["GET", "POST"]) # Métodos da requisição aceites nessa rota
def login():
    if request.method == "POST": # Caso for post ele pega os valores email e password no formulário html
        email = request.form["email"]
        password = request.form["password"]

        user = db.session.scalar(
            sa.select(User).where(User.email == email) # Procura um usuário pelo email
        )

        if user is None or not check_password_hash(
            user.password_hash,
            password # Caso não encontrar o User ou password estiver incorreto ele retorna um erro
        ):
            return "Email ou password inválidos", 404

        login_user(user) # Caso encontrar o User e o password estiver correto o usuário vai estar logado e redirecionado para a página home

        return redirect(url_for("inicio"))

    return render_template("login.html") # Caso contrário para a página login

@user_bp.route("/register", methods=["GET", "POST"]) # Rota para fazer o login
def register():
    if request.method == "POST": # A mesma lógica que o login
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        user = db.session.scalar( # Procura o usuário pelo email
            sa.select(User).where(User.email == email)
        )
        
        if user:# Caso encontrado retorna essa mensagem
            return "Usuário já está catrado"
        

        user = User(name = name, email = email, password_hash = generate_password_hash(password))# Caso estiver tudo certo registra no banco de dados
        db.session.add(user)
        db.session.commit()

        return redirect(url_for("user.login")) # retorna para o login
    return render_template("register.html")

@user_bp.route("/logout")# rota para fazer o logout
@login_required
def logout():
    logout_user()
    return redirect(url_for("user.login"))