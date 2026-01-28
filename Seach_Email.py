from flask import Flask, request, render_template_string

app = Flask(__name__)

                                                           # Exemplo de "banco de dados" fictício
cadastros = {
    "teste@email.com": ["Amazon", "Netflix", "Spotify"],
    "joao@gmail.com": ["Facebook", "Instagram"]
}

                                                                 #Página inicial
@app.route("/")
def index():
    return render_template_string(open("index.html").read())

                                                                    #Consulta
@app.route("/consulta", methods=["POST"])
def consulta():
    email = request.form["email"]
    sites = cadastros.get(email, [])
    if sites:
        return f"<h3>O e-mail {email} está cadastrado em:</h3><ul>" + "".join(f"<li>{s}</li>" for s in sites) + "</ul>"
    else:
        return f"<h3>O e-mail {email} não foi encontrado em nenhum site do banco.</h3>"

if __name__ == "__main__":
    app.run(debug=True)
