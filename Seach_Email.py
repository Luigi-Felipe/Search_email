from flask import Flask, request, render_template_string

app = Flask(__name__)

                                  # Simulação de banco de dados (Dicionário)
CADASTROS = {
    "teste@email.com": ["Amazon", "Netflix", "Spotify"]
}
                                    # Template HTML centralizado com lógica Jinja segura
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
        ul { margin: 10px 0 0 20px; padding: 0; }
    </style>
</head>
<body>
    <div class="card">
        <h2>Consulta de E-mail</h2>
        <p>Verifique em quais plataformas seu e-mail está cadastrado:</p>
        <form action="/consulta" method="POST">
            <input type="email" name="email" value="{{ email_pesquisado or '' }}" placeholder="seu@email.com" required>
            <button type="submit">Consultar</button>
        </form>

        {% if searched %}
            <div class="result {% if sites %}found{% else %}not-found{% endif %}">
                {% if sites %}
                    <strong>{{ email_pesquisado }}</strong> encontrado em:
                    <ul>
                        {% for site in sites %}
                            <li>{{ site }}</li>
                        {% endfor %}
                    </ul>
                {% else %}
                    O e-mail <strong>{{ email_pesquisado }}</strong> não consta na nossa base.
                {% endif %}
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_LAYOUT, searched=False)

@app.route("/consulta", methods=["POST"])
def consulta():
    email_bruto = request.form.get("email", "").strip().lower()
    sites = CADASTROS.get(email_bruto, [])
    
    return render_template_string(
        HTML_LAYOUT, 
        searched=True,
        email_pesquisado=email_bruto, 
        sites=sites
    )

if __name__ == "__main__":
    app.run(debug=True)