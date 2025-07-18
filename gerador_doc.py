from docx import Document
import os
from datetime import datetime
import locale

def gerar_comprovante(dados, nome_aluno, modelo_nome, documentos_extra=None, fase=None):
    modelo_formatado = modelo_nome.strip().lower().replace(" ", "_") + ".docx"
    caminho_modelo = os.path.join("templates_arquivos", modelo_formatado)

    if not os.path.exists(caminho_modelo):
        raise FileNotFoundError(f"❌ Modelo não encontrado: {modelo_formatado}")

    doc = Document(caminho_modelo)

    # Define locale para pt_BR para data por extenso
    try:
        locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')
    except:
        try:
            locale.setlocale(locale.LC_TIME, 'pt_BR')
        except:
            locale.setlocale(locale.LC_TIME, '')  # Fallback para o sistema

    data_hoje_formatada = datetime.today().strftime("%d de %B de %Y")

    # Define o horário conforme a fase
    horario = ""
    if fase == "ECI":
        horario = "08:00 às 11:30"
    elif fase == "EPT":
        horario = "14:10 às 17:50"


    resultados_texto = ""
    for f in dados["fases"]:
        resultados_texto += f"• Período: {f['periodo_letivo']} | Fase: {f['fase']} | Situação: {f['situacao_resultado']}\n"

    for p in doc.paragraphs:
        if "{{nome}}" in p.text:
            p.text = p.text.replace("{{nome}}", nome_aluno)
        if "{{curso}}" in p.text:
            p.text = p.text.replace("{{curso}}", dados.get("curso", ""))
        if "{{resultados}}" in p.text:
            p.text = p.text.replace("{{resultados}}", resultados_texto.strip())
        if "{{data}}" in p.text:
            p.text = p.text.replace("{{data}}", datetime.today().strftime("%d/%m/%Y"))
        if "{{data_hoje}}" in p.text:
            p.text = p.text.replace("{{data_hoje}}", data_hoje_formatada)
        if "{{horario}}" in p.text:
            p.text = p.text.replace("{{horario}}", horario)

        if documentos_extra:
            if "{{cpf}}" in p.text:
                p.text = p.text.replace("{{cpf}}", documentos_extra.get("cpf", ""))
            if "{{rg}}" in p.text:
                p.text = p.text.replace("{{rg}}", documentos_extra.get("rg", ""))

    nome_arquivo = f"comprovante_{nome_aluno.replace(' ', '_').lower()}_{datetime.now().strftime('%Y%m%d%H%M%S')}.docx"
    caminho_saida = os.path.join("comprovantes", nome_arquivo)
    os.makedirs("comprovantes", exist_ok=True)
    doc.save(caminho_saida)

    return caminho_saida
