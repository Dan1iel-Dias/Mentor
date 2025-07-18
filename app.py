from flask import Flask, render_template, request, send_file
from mentor import obter_situacao_resultado_com_login
from gerador_doc import gerar_comprovante
from documentos import buscar_documentos_aluno  # ← nova importação
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    erro = None
    caminho_arquivo = None

    if request.method == "POST":
        nome = request.form.get("nome")
        fase = request.form.get("fase")  # novo input select "fase"
        modelo_input = request.form.get("modelo", "")
        modelo_formatado = modelo_input.strip().lower().replace(" ", "_") + ".docx"

        usuario = "daniel.santos@pedreira.org"
        senha = "5673D15d@"

        dados = obter_situacao_resultado_com_login(nome, usuario, senha, fase)  # <-- passa fase
        documentos = buscar_documentos_aluno(nome, usuario, senha)  # busca documentos extras
        fase = request.form.get("fase")  # Novo campo do <select>


        if dados and "fases" in dados:
            resultado = dados
            try:
                caminho_arquivo = gerar_comprovante(
                    dados,
                    nome,
                    modelo_input,
                    documentos_extra=documentos,
                    fase=fase 
                )
            except FileNotFoundError:
                erro = f"❌ Modelo '{modelo_formatado}' não encontrado em templates_arquivos."
        else:
            erro = "❌ Erro na automação ou aluno não encontrado."

    return render_template("index.html", resultado=resultado, erro=erro, caminho_arquivo=caminho_arquivo)

@app.route("/download")
def download():
    arquivo = request.args.get("arquivo")
    if not arquivo or not os.path.isfile(arquivo):
        return "Arquivo não encontrado.", 404
    return send_file(arquivo, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
