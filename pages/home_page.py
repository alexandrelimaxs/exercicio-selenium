"""Page Object da home do Automation Exercise."""

from __future__ import annotations

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class HomePage(BasePage):
    LOGO = (By.CSS_SELECTOR, "#header .logo img")
    LINK_SIGNUP_LOGIN = (By.CSS_SELECTOR, "a[href='/login']")
    TITULO_FEATURES = (By.CSS_SELECTOR, ".features_items h2.title")

    def abrir_home(self) -> "HomePage":
        self.abrir("/")
        self.encontrar(self.LOGO)
        return self

    def home_visivel(self) -> bool:
        return self.visivel(self.LOGO)

    def ir_para_login(self):
        from pages.login_page import LoginPage

        self.clicar(self.LINK_SIGNUP_LOGIN)
        return LoginPage(self.driver)
