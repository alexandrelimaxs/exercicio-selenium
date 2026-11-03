"""Page Object da tela de Login / Signup."""

from __future__ import annotations

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage


class LoginPage(BasePage):
    TITULO_LOGIN = (By.CSS_SELECTOR, ".login-form h2")
    TITULO_SIGNUP = (By.CSS_SELECTOR, ".signup-form h2")
    MENSAGEM_ERRO_LOGIN = (By.CSS_SELECTOR, ".login-form p")
    MENSAGEM_ERRO_SIGNUP = (By.CSS_SELECTOR, ".signup-form p")

    EMAIL_LOGIN = (By.CSS_SELECTOR, "input[data-qa='login-email']")
    SENHA_LOGIN = (By.CSS_SELECTOR, "input[data-qa='login-password']")
    BOTAO_LOGIN = (By.CSS_SELECTOR, "button[data-qa='login-button']")

    NOME_SIGNUP = (By.CSS_SELECTOR, "input[data-qa='signup-name']")
    EMAIL_SIGNUP = (By.CSS_SELECTOR, "input[data-qa='signup-email']")
    BOTAO_SIGNUP = (By.CSS_SELECTOR, "button[data-qa='signup-button']")

    # Expressões usadas para inspecionar a validação nativa do HTML5.
    JS_EMAIL_VALIDO = (
        "return document.querySelector(\"input[data-qa='login-email']\").checkValidity();"
    )
    JS_VALIDACAO_EMAIL = (
        "return document.querySelector(\"input[data-qa='login-email']\").validationMessage;"
    )
    JS_VALIDACAO_SENHA = (
        "return document.querySelector(\"input[data-qa='login-password']\").validationMessage;"
    )

    def fazer_login(self, email: str, senha: str) -> "LoginPage":
        if email:
            self.digitar(self.EMAIL_LOGIN, email)
        else:
            self.encontrar(self.EMAIL_LOGIN).clear()
        if senha:
            self.digitar(self.SENHA_LOGIN, senha)
        else:
            self.encontrar(self.SENHA_LOGIN).clear()
        self.clicar(self.BOTAO_LOGIN)
        return self

    def iniciar_cadastro(self, nome: str, email: str) -> "LoginPage":
        self.digitar(self.NOME_SIGNUP, nome)
        self.digitar(self.EMAIL_SIGNUP, email)
        self.clicar(self.BOTAO_SIGNUP)
        return self

    def mensagem_erro_login(self, timeout: int = 8) -> str:
        return self._mensagem(self.MENSAGEM_ERRO_LOGIN, timeout)

    def mensagem_erro_signup(self, timeout: int = 8) -> str:
        return self._mensagem(self.MENSAGEM_ERRO_SIGNUP, timeout)

    def _mensagem(self, localizador: tuple[str, str], timeout: int) -> str:
        try:
            elemento = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(localizador)
            )
            return elemento.text.strip()
        except TimeoutException:
            return ""

    def email_valido(self) -> bool:
        self.encontrar(self.EMAIL_LOGIN)
        return bool(self.driver.execute_script(self.JS_EMAIL_VALIDO))

    def validacao_email(self) -> str:
        self.encontrar(self.EMAIL_LOGIN)
        return self.driver.execute_script(self.JS_VALIDACAO_EMAIL) or ""

    def validacao_senha(self) -> str:
        self.encontrar(self.SENHA_LOGIN)
        return self.driver.execute_script(self.JS_VALIDACAO_SENHA) or ""
