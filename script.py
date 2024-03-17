import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Automation:
    def __init__(self, login_sptfy, senha_sptfy, buscar_cantor, log_function=None):
        self.login_sptfy = login_sptfy
        self.senha_sptfy = senha_sptfy
        self.buscar_cantor = buscar_cantor
        self.log_function = log_function

    def log(self, message, tag=None):
        if self.log_function:
            self.log_function(message, tag)

    def run(self):
        with webdriver.Chrome() as driver:
            self.driver = driver
            try:
                self.driver.get("https://open.spotify.com/intl-pt")
                self.entrando_pag_login()
                self.fazendo_login()
                self.buscando_cantor()
                self.clicando_no_cantor()
                self.pagina_do_cantor()
                self.log("Automação concluída com sucesso.")
            except Exception as e:
                self.log(f"Erro durante a automação: {str(e)}", "error")

    def entrando_pag_login(self):
        self.log("Entrando na página de login...")
        botao_entrar = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@data-testid='login-button']"))
        )
        botao_entrar.click()

    def fazendo_login(self):
        self.log("Fazendo login...")
        campo_email = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='login-username']"))
        )
        campo_senha = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='login-password']"))
        )
        botao_entrar = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@data-testid='login-button']"))
        )

        campo_email.clear()
        self.digite_como_uma_pessoa(self.login_sptfy, campo_email)

        campo_senha.clear()
        self.digite_como_uma_pessoa(self.senha_sptfy, campo_senha)

        botao_entrar.click()

    def buscando_cantor(self):
        self.log(f"Buscando o cantor {self.buscar_cantor}...")
        botao_buscar = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[@href='/search']"))
        )
        botao_buscar.click()

        caixa_de_busca = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@data-testid='search-input']"))
        )
        self.digite_como_uma_pessoa(self.buscar_cantor, caixa_de_busca)

    def clicando_no_cantor(self):
        self.log(f"Clicando no cantor {self.buscar_cantor}...")
        clicando_cantor = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@data-testid='herocard-click-handler']"))
        )
        clicando_cantor.click()

    def pagina_do_cantor(self):
        self.log(f"Acessando página do cantor {self.buscar_cantor}...")
        xpath = '//span[text()="Mostrar tudo"]'
        elemento_mostrar_tudo = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        self.log("Abrindo discografia")
        try:
            elemento_mostrar_tudo.click()
        except Exception as e:
            self.log(f"Erro ao acessar a página do cantor: {str(e)}", "error")

    @staticmethod
    def digite_como_uma_pessoa(frase, campo_input_unico):
        print("Digitando...")
        for letra in frase:
            campo_input_unico.send_keys(letra)
            time.sleep(random.randint(1, 5) / 30)
