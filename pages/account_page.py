"""Page Object das telas de conta criada / excluída e do cabeçalho logado."""

from __future__ import annotations

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BASE_URL, BasePage


class AccountPage(BasePage):
    CONTA_CRIADA = (By.CSS_SELECTOR, "h2[data-qa='account-created']")
    CONTA_DELETADA = (By.CSS_SELECTOR, "h2[data-qa='account-deleted']")
    BOTAO_CONTINUAR = (By.CSS_SELECTOR, "a[data-qa='continue-button']")
    LOGADO_COMO = (By.CSS_SELECTOR, "#header li a b")
    LINK_DELETAR_CONTA = (By.CSS_SELECTOR, "a[href='/delete_account']")
    LOGO = (By.CSS_SELECTOR, "#header .logo img")

    def conta_criada(self) -> str:
        return self.texto(self.CONTA_CRIADA)

    def conta_deletada(self) -> str:
        return self.texto(self.CONTA_DELETADA)

    def nome_logado(self) -> str:
        return self.texto(self.LOGADO_COMO)

    def continuar(self) -> "AccountPage":
        """Clica em Continue e contorna o Google vignette, que às vezes bloqueia a navegação."""
        self.clicar(self.BOTAO_CONTINUAR)
        try:
            WebDriverWait(self.driver, 6).until(
                EC.presence_of_element_located(self.LOGADO_COMO)
            )
        except TimeoutException:
            self.driver.get(BASE_URL)
            self.wait.until(EC.presence_of_element_located(self.LOGADO_COMO))
        return self

    def continuar_apos_exclusao(self) -> "AccountPage":
        self.clicar(self.BOTAO_CONTINUAR)
        try:
            WebDriverWait(self.driver, 6).until(
                EC.presence_of_element_located(self.LOGO)
            )
        except TimeoutException:
            self.driver.get(BASE_URL)
            self.wait.until(EC.presence_of_element_located(self.LOGO))
        return self

    def excluir_conta(self) -> "AccountPage":
        self.clicar(self.LINK_DELETAR_CONTA)
        self.encontrar(self.CONTA_DELETADA)
        return self
