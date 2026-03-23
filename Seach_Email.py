from flask import Flask, request, render_template, render_template_string, Markup

app = Flask(__name__)

                                   #Simulação de banco de dados
CADASTROS = {
    "teste@email.com": ["Amazon", "Netflix", "Spotify"],
    "joao@gmail.com": ["Facebook", "Instagram"]
}

@app.route("/")
def index():
                                 # Em produção, use render_template('index.html') com arquivos na pasta /templates
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return render_template_string(f.read())
    except FileNotFoundError:
        return "Arquivo index.html não encontrado.", 404

@app.route("/consulta", methods=["POST"])
def consulta():
    email = request.form.get("email", "").strip().lower()
    
    if not email:
        return "<h3>Por favor, insira um e-mail válido.</h3>", 400

    sites = CADASTROS.get(email)

    if sites:
                                    # Usamos uma lista para construir o HTML e evitamos concatenação direta de strings do usuário
        lista_sites = "".join(f"<li>{Markup.escape(s)}</li>" for s in sites)
        return (
            f"<h3>O e-mail <strong>{Markup.escape(email)}</strong> está cadastrado em:</h3>"
            f"<ul>{lista_sites}</ul>"
            f'<br><a href="/">Voltar</a>'
        )
    
    return (
        f"<h3>O e-mail {Markup.escape(email)} não foi encontrado.</h3>"
        f'<br><a href="/">Voltar</a>'
    )

if __name__ == "__main__":
    app.run(debug=True)