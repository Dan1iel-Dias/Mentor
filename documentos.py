from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

def buscar_documentos_aluno(nome_aluno, usuario, senha):
    caminho_driver = r"C:\Users\daniel.santos\Desktop\automaçaopx\chromedriver-win64\chromedriver-win64\chromedriver.exe"

    options = Options()
    # options.add_argument("--headless")  # descomente para rodar em modo invisível
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

        # Acessa via F2 e nome do aluno
        ActionChains(driver).send_keys(Keys.F2).perform()
        time.sleep(2)

        campo_nome = wait.until(EC.presence_of_element_located((By.ID, "opcaoAtalhoCampoNome")))
        campo_nome.clear()
        campo_nome.send_keys(nome_aluno)
        time.sleep(1)
        campo_nome.send_keys(Keys.ENTER)
        time.sleep(2)

        # Abas "Cadastro" e "Documentos"
        link_cadastro = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Cadastro')]")))
        link_cadastro.click()
        time.sleep(2)

        aba_documentos = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Documentos') and contains(@onclick, 'trocaAba')]")))
        aba_documentos.click()
        time.sleep(2)

        # Coleta dados
        cpf_input = wait.until(EC.presence_of_element_located((By.ID, "cpfMascara")))
        cpf_valor = cpf_input.get_attribute("value").strip()

        rg_input = wait.until(EC.presence_of_element_located((By.ID, "nroRG")))
        rg_valor = rg_input.get_attribute("value").strip()

        print(f"✅ Dados coletados para {nome_aluno}:")
        print(f"🪪 CPF/Passaporte: {cpf_valor}")
        print(f"🪪 RG/RNM: {rg_valor}")

        return {
            "nome": nome_aluno,
            "cpf": cpf_valor,
            "rg": rg_valor
        }

    except Exception as e:
        print("⚠️ Erro durante automação:", e)
        return None

    finally:
        driver.quit()
