from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

def obter_situacao_resultado_com_login(nome_aluno, usuario, senha, fase):
    caminho_driver = r"C:\Users\daniel.santos\Desktop\automaçaopx\chromedriver-win64\chromedriver-win64\chromedriver.exe"

    options = Options()
    # options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(caminho_driver), options=options)
    wait = WebDriverWait(driver, 15)

    try:
        driver.get("https://mentorweb.pedreira.org/ceap/inicial.do?pcaes=0f595d7f836bd3dc4a7b90184b310a25")
        time.sleep(2)

        # Login
        campo_login = wait.until(EC.element_to_be_clickable((By.ID, "j_username")))
        campo_login.clear()
        campo_login.send_keys(usuario)
        campo_senha = wait.until(EC.element_to_be_clickable((By.ID, "senha")))
        campo_senha.clear()
        campo_senha.send_keys(senha)
        campo_senha.send_keys(Keys.ENTER)
        time.sleep(3)

        # Escolhe o módulo conforme a fase
        if fase == "ECI":
            link_colegio = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'moduloID=33')]")))
            link_colegio.click()
        elif fase == "EPT":
            link_tecnico = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'moduloID=65')]")))
            link_tecnico.click()
        else:
            print(f"⚠️ Fase '{fase}' inválida. Continuando sem troca de módulo.")

        # F2 > Busca nome aluno
        ActionChains(driver).send_keys(Keys.F2).perform()
        time.sleep(2)
        campo_nome = wait.until(EC.presence_of_element_located((By.ID, "opcaoAtalhoCampoNome")))
        campo_nome.clear()
        campo_nome.send_keys(nome_aluno)
        time.sleep(1)
        campo_nome.send_keys(Keys.ENTER)
        time.sleep(2)

        # Clica em "Períodos de matrícula"
        link_periodo = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Períodos de matrícula')]")))
        link_periodo.click()
        time.sleep(2)

        # Coleta matrículas
        wait.until(EC.presence_of_all_elements_located((By.XPATH, "//tr[contains(@onclick, 'matriculaturma.do')]")))
        linhas = driver.find_elements(By.XPATH, "//tr[contains(@onclick, 'matriculaturma.do')]")
        matriculas = []
        for linha in linhas:
            periodo = linha.find_element(By.XPATH, "./td[1]").text.strip()
            onclick = linha.get_attribute("onclick")
            if "redirect('" in onclick:
                url = onclick.split("redirect('")[1].split("'")[0]
                matriculas.append((periodo, url))

        if not matriculas:
            print("⚠️ Nenhuma matrícula encontrada.")
            return None

        # Vai para a matrícula mais recente
        matriculas.sort(key=lambda x: x[0], reverse=True)
        driver.get("https://mentorweb.pedreira.org" + matriculas[0][1])
        time.sleep(2)

        # Coleta o nome do curso
        try:
            elemento_curso = wait.until(EC.presence_of_element_located((
                By.XPATH,
                "//td[contains(text(), 'Curso')]/following-sibling::td[1]/a"
            )))
            nome_curso = elemento_curso.text.strip()
        except:
            nome_curso = "CURSO NÃO ENCONTRADO"


        # Vai para "Resultado nas fases"
        link_resultado = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//a[contains(@onclick, 'ingressoresultadofaseman.do')]")
        ))
        url_resultado = link_resultado.get_attribute("onclick").split("redirect('")[1].split("'")[0]
        driver.get("https://mentorweb.pedreira.org" + url_resultado)
        time.sleep(2)

        # Coleta fases
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.delimitador")))
        linhas_fase = driver.find_elements(By.CSS_SELECTOR, "table.delimitador tbody tr")

        dados_resultado = []

        for linha in linhas_fase:
            try:
                select_periodo = Select(linha.find_element(By.CSS_SELECTOR, "select[name^='resultadoFase'][name$='periodoLetivoAux']"))
                periodo_texto = select_periodo.first_selected_option.text.strip()

                input_fase = linha.find_element(By.CSS_SELECTOR, "input[name^='resultadoFase'][name$='faseAux']")
                fase_valor = input_fase.get_attribute("value").strip()

                select_situacao = Select(linha.find_element(By.CSS_SELECTOR, "select[name^='resultadoFase'][name$='situacaoResultadoAux']"))
                situacao_texto = select_situacao.first_selected_option.text.strip()

                dados_resultado.append({
                    "periodo_letivo": periodo_texto,
                    "fase": fase_valor,
                    "situacao_resultado": situacao_texto
                })
            except:
                continue

        return {
            "curso": nome_curso,
            "fases": dados_resultado
        }

    except Exception as e:
        print("⚠️ Erro durante automação:", e)
        return None

    finally:
        driver.quit()



def main():
    nome_aluno = "Daniel dias tome dos santos"
    usuario = "daniel.santos@pedreira.org"
    senha = "5673D15d@"

    print(f"\n🔍 Consultando aluno: {nome_aluno}")
    dados = obter_situacao_resultado_com_login(nome_aluno, usuario, senha)

    if dados and "fases" in dados:
        print(f"\n📄 Curso: {dados['curso']}")
        for item in dados['fases']:
            print(f"  • Período: {item['periodo_letivo']} | Fase: {item['fase']} | Situação: {item['situacao_resultado']}")
    else:
        print(f"\n⚠️ Nenhum dado retornado para {nome_aluno}.")


if __name__ == "__main__":
    main()
