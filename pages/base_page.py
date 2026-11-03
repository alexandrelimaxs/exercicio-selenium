"""Classe base para os Page Objects."""

from __future__ import annotations

import os

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = os.getenv("BASE_URL", "https://automationexercise.com")

# O site exibe anúncios que às vezes cobrem o formulário e interceptam o clique.
JS_REMOVER_ANUNCIOS = """
const seletores = [
  'iframe[src*="googlesyndication"]',
  'iframe[src*="googleads"]',
  'iframe[src*="doubleclick"]',
  'iframe[id^="aswift"]',
  'iframe[name^="aswift"]',
  'ins.adsbygoogle',
];
seletores.forEach((seletor) =>
  document.querySelectorAll(seletor).forEach((elemento) => elemento.remove())
);
"""


class BasePage:
    def __init__(self, driver: WebDriver, timeout: int = 15) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def abrir(self, caminho: str = "") -> None:
        self.driver.get(f"{BASE_URL}{caminho}")

    def encontrar(self, localizador: tuple[str, str]):
        return self.wait.until(EC.visibility_of_element_located(localizador))

    def _remover_anuncios(self) -> None:
        try:
            self.driver.execute_script(JS_REMOVER_ANUNCIOS)
        except WebDriverException:
            pass

    def clicar(self, localizador: tuple[str, str]):
        elemento = self.wait.until(EC.presence_of_element_located(localizador))
        self._remover_anuncios()
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", elemento
        )
        try:
            self.wait.until(EC.element_to_be_clickable(localizador)).click()
        except (ElementClickInterceptedException, WebDriverException):
            # Fallback para quando um anúncio cobre o elemento.
            self._remover_anuncios()
            self.driver.execute_script("arguments[0].click();", elemento)

    def digitar(self, localizador: tuple[str, str], texto: str) -> None:
        self._remover_anuncios()
        campo = self.encontrar(localizador)
        campo.clear()
        campo.send_keys(texto)

    def texto(self, localizador: tuple[str, str]) -> str:
        return self.encontrar(localizador).text.strip()

    def visivel(self, localizador: tuple[str, str], timeout: int = 10) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(localizador)
            )
            return True
        except TimeoutException:
            return False
