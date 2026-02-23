from flask import Flask, render_template, request, redirect, url_for, session
import os
import secrets

# Gerando uma secret_key se não existir uma
secret_key = secrets.token_hex(32)

# 1 Criando a aplicação Flask
app = Flask(__name__)

# 2 Definindo a secret_key
# Pega da variável de ambiente se existir, senão usa uma chave gerada
app.secret_key = os.environ.get("MINHA_CHAVE", secret_key)

# Usuário fixo para estudo (simulando um banco de dados)
USUARIOS_CORRETO = {
    "admin": "123"
}

# Rota Principal


@app.route("/")
def home():
    # Verifica se o usuário está logado
    if "usuario" in session:
        return render_template("home.html", usuario=session["usuario"])
    else:
        return redirect(url_for("login"))

# Rota de Login


@app.route("/login", methods=["GET", "POST"])
def login():
    erro = None

    # Se o Formulario for enviado (post)
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]

        # Verifica se o usuário e senha estão corretos
        if usuario in USUARIOS_CORRETO and USUARIOS_CORRETO[usuario] == senha:
            session["usuario"] = usuario  # Armazena o usuário na sessão
            return redirect(url_for("home"))
        else:
            erro = "Usuário ou senha incorretos. Tente novamente."

    # Se for GET, apenas mostra a página
    return render_template("login.html", error=erro)

# Rota de Logout


@app.route("/logout")
def logout():
    session.pop("usuario", None)  # Remove o usuário da sessão
    return redirect(url_for("login"))


# Rodar aplicação
if __name__ == "__main__":
    # Usando 0.0.0.0 para ser acessível na rede local ou IP fixo se necessário
    app.run(host="0.0.0.0", port=8080, debug=True)
