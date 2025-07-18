from flask import Flask, render_template, request
from mentor import obter_situacao_resultado_com_login

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    erro = None

    if request.method == "POST":
        nome = request.form.get("nome")
        usuario = "daniel.santos@pedreira.org"
        senha = "5673D15d@"

        dados = obter_situacao_resultado_com_login(nome, usuario, senha)

        if dados and isinstance(dados, dict) and "fases" in dados:
            resultado = dados
        else:
            erro = "❌ Erro na automação ou aluno não encontrado."

    return render_template("index.html", resultado=resultado, erro=erro)

if __name__ == "__main__":
    app.run(debug=True)
