"""Page Object do formulário de cadastro (ENTER ACCOUNT INFORMATION)."""

from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class SignupPage(BasePage):
    # O texto no DOM é title case; o CSS é que o exibe em maiúsculas.
    TITULO_CONTA = (
        By.XPATH,
        "//h2[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
        "'abcdefghijklmnopqrstuvwxyz'), 'enter account information')]",
    )
    TITULO_ENDERECO = (
        By.XPATH,
        "//h2[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
        "'abcdefghijklmnopqrstuvwxyz'), 'address information')]",
    )

    TITULO_MR = (By.CSS_SELECTOR, "#id_gender1")
    TITULO_MRS = (By.CSS_SELECTOR, "#id_gender2")
    NOME = (By.CSS_SELECTOR, "#name")
    EMAIL = (By.CSS_SELECTOR, "#email")
    SENHA = (By.CSS_SELECTOR, "#password")
    DIA = (By.CSS_SELECTOR, "#days")
    MES = (By.CSS_SELECTOR, "#months")
    ANO = (By.CSS_SELECTOR, "#years")
    NEWSLETTER = (By.CSS_SELECTOR, "#newsletter")
    OFERTAS = (By.CSS_SELECTOR, "#optin")

    PRIMEIRO_NOME = (By.CSS_SELECTOR, "#first_name")
    SOBRENOME = (By.CSS_SELECTOR, "#last_name")
    EMPRESA = (By.CSS_SELECTOR, "#company")
    ENDERECO = (By.CSS_SELECTOR, "#address1")
    ENDERECO2 = (By.CSS_SELECTOR, "#address2")
    PAIS = (By.CSS_SELECTOR, "#country")
    ESTADO = (By.CSS_SELECTOR, "#state")
    CIDADE = (By.CSS_SELECTOR, "#city")
    CEP = (By.CSS_SELECTOR, "#zipcode")
    CELULAR = (By.CSS_SELECTOR, "#mobile_number")

    BOTAO_CRIAR_CONTA = (By.CSS_SELECTOR, "button[data-qa='create-account']")

    def formulario_visivel(self) -> bool:
        return self.visivel(self.TITULO_CONTA)

    def preencher_dados_conta(
        self,
        senha: str,
        titulo: str = "Mr",
        dia: str = "10",
        mes: str = "5",
        ano: str = "1990",
        newsletter: bool = True,
        ofertas: bool = True,
    ) -> "SignupPage":
        self.clicar(self.TITULO_MR if titulo == "Mr" else self.TITULO_MRS)
        self.digitar(self.SENHA, senha)
        Select(self.encontrar(self.DIA)).select_by_value(dia)
        Select(self.encontrar(self.MES)).select_by_value(mes)
        Select(self.encontrar(self.ANO)).select_by_value(ano)
        if newsletter:
            self.clicar(self.NEWSLETTER)
        if ofertas:
            self.clicar(self.OFERTAS)
        return self

    def preencher_endereco(
        self,
        primeiro_nome: str,
        sobrenome: str,
        empresa: str,
        endereco: str,
        endereco2: str,
        pais: str,
        estado: str,
        cidade: str,
        cep: str,
        celular: str,
    ) -> "SignupPage":
        self.digitar(self.PRIMEIRO_NOME, primeiro_nome)
        self.digitar(self.SOBRENOME, sobrenome)
        self.digitar(self.EMPRESA, empresa)
        self.digitar(self.ENDERECO, endereco)
        self.digitar(self.ENDERECO2, endereco2)
        Select(self.encontrar(self.PAIS)).select_by_value(pais)
        self.digitar(self.ESTADO, estado)
        self.digitar(self.CIDADE, cidade)
        self.digitar(self.CEP, cep)
        self.digitar(self.CELULAR, celular)
        return self

    def criar_conta(self):
        from pages.account_page import AccountPage

        self.clicar(self.BOTAO_CRIAR_CONTA)
        return AccountPage(self.driver)

    def validacao_senha(self) -> str:
        return self.driver.execute_script(
            "return document.querySelector('#password').validationMessage;"
        ) or ""
