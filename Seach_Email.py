from flask import Flask, request, render_template_string

app = Flask(__name__)

                                                           #  "banco de dados" f
cadastros = {
    "teste@email.com": ["Amazon", "Netflix", "Spotify"],
    "joao@gmail.com": ["Facebook", "Instagram"]
}

                                                                 #Página inicial
@app.route("/")
def index():
    return render_template_string(open("index.html").re
@app.route("/consulta", methods=["POST"])
def consulta():
    email = request.form["email"]
    sites = cadastros.get(email, [])
    if sites

from flask import Flask, request, render_template_string, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "segredo_super_secreto"                                    #  usar flash messages

#                                                                       # "Banco de dados"
cadastros = {
    "teste@email.com": ["Amazon", "Netflix", "Spotify"],
    "joao@gmail.com": ["Facebook", "Instagram"]
}

                                                                         # Bootstrap
base_template = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Sistema de Cadastros</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css">
</head>
<body class="container mt-4">
    <h1 class="mb-4">Sistema de Cadastros</h1>
    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <div class="alert alert-info">
          {{ messages[0] }}
        </div>
      {% endif %}
    {% endwith %}
    {{ content|safe }}
    <hr>
    <a href="{{ url_for('index') }}" class="btn btn-secondary">Página inicial</a>
</body>
</html>
"""

                                                                           # Página inicial
@app.route("/")
def index():
    content = """
    <form action="/consulta" method="POST" class="mb-3">
        <label for="email">Consultar e-mail:</label>
        <input type="email" name="email" required class="form-control mb-2">
        <button type="submit" class="btn btn-primary">Consultar</button>
    </form>
    <a href="/listar" class="btn btn-info">Listar todos os cadastros</a>
    <a href="/novo" class="btn btn-success">Cadastrar novo e-mail</a>
    """
    return render_template_string(base_template, content=content)

                                                                             # Consulta
@app.route("/consulta", methods=["POST"])
def consulta():
    email = request.form["email"].strip().lower()
    sites = cadastros.get(email, [])
    if sites:
        content = f"<h3>O e-mail <b>{email}</b> está cadastrado em:</h3><ul>" + "".join(f"<li>{s}</li>" for s in sites) + "</ul>"
    else:
        content = f"<h3>O e-mail <b>{email}</b> não foi encontrado em nenhum site do banco.</h3>"
    return render_template_string(base_template, content=content)

                                                                               # Listar todos
@app.route("/listar")
def listar():
    content = "<h3>Todos os cadastros:</h3><ul>"
    for email, sites in cadastros.items():
        content += f"<li><b>{email}</b>: {', '.join(sites)}</li>"
    content += "</ul>"
    return render_template_string(base_template, content=content)

                                                                              # Novo cadastro
@app.route("/novo", methods=["GET", "POST"])
def novo():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        site = request.form["site"].strip()
        if not email or not site:
            flash("Preencha todos os campos!")
        else:
            cadastros.setdefault(email, []).append(site)
            flash(f"Cadastro atualizado: {email} → {site}")
            return redirect(url_for("index"))
    content = """
    <form method="POST">
        <label for="email">E-mail:</label>
        <input type="email" name="email" required class="form-control mb-2">
        <label for="site">Site:</label>
        <input type="text" name="site" required class="form-control mb-2">
        <button type="submit" class="btn btn-success">Cadastrar</button>
    </form>
    """
    return render_template_string(base_template, content=content)

                                                  # Remover cadastro
@app.route("/remover", methods=["POST"])
def remover():
    email = request.form["email"].strip().lower()
    if email in cadastros:
        cadastros.pop(email)
        flash(f"E-mail {email} removido com sucesso!")
    else:
        flash(f"E-mail {email} não encontrado.")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True) 
