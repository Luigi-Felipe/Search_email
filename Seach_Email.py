from flask import Flask, request, render_template_string, escape

app = Flask(__name__)

                                                                               # Simulação de banco de dados (Dicionário)
                                                                               # Dica: Em produção, use um banco como SQLite ou PostgreSQL
CADASTROS = {
    "teste@email.com": ["Amazon", "Netflix", "Spotify"],
    "joao@gmail.com": ["Facebook", "Instagram"]
}

                                                           # Template HTML centralizado para manter a interface consistente
HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Verificador de Contas</title>
    <style>
        body { font-family: sans-serif; max-width: 500px; margin: 50px auto; line-height: 1.6; }
        .card { border: 1px solid #ddd; padding: 20px; border-radius: 8px; box-shadow: 2px 2px 10px #eee; }
        input[type="email"] { width: 70%; padding: 8px; margin-bottom: 10px; }
        button { padding: 8px 15px; cursor: pointer; background-color: #007bff; color: white; border: none; border-radius: 4px; }
        .result { margin-top: 20px; padding: 15px; border-radius: 4px; }
        .found { background-color: #d4edda; color: #155724; }
        .not-found { background-color: #f8d7da; color: #721c24; }
    </style>
</head>
<body>
    <div class="card">
        <h2>Consulta de E-mail</h2>
        <p>Verifique em quais plataformas seu e-mail está cadastrado:</p>
        <form action="/consulta" method="POST">
            <input type="email" name="email" placeholder="seu@email.com" required>
            <button type="submit">Consultar</button>
        </form>

        {% if resultado %}
            <div class="result {{ classe_css }}">
                {{ resultado | safe }}
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_LAYOUT)

@app.route("/consulta", methods=["POST"])
def consulta():
                                                        # 1. Proteção contra XSS: usando escape() para limpar a entrada do usuário
    email_bruto = request.form.get("email", "").strip().lower()
    email_seguro = escape(email_bruto)
    
    sites = CADASTROS.get(email_bruto, [])
    
    if sites:
        lista_html = "".join(f"<li>{s}</li>" for s in sites)
        resultado = f"<strong>{email_seguro}</strong> encontrado em: <ul>{lista_html}</ul>"
        classe_css = "found"
    else:
        resultado = f"O e-mail <strong>{email_seguro}</strong> não consta na nossa base."
        classe_css = "not-found"

    return render_template_string(HTML_LAYOUT, resultado=resultado, classe_css=classe_css)

if __name__ == "__main__":
    app.run(debug=True)