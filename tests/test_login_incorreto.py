"""Testes do Test Case 3: login com e-mail e senha incorretos."""

from __future__ import annotations

import pytest

from pages.home_page import HomePage
from pages.login_page import LoginPage

pytestmark = pytest.mark.login


def test_login_com_credenciais_incorretas(driver, caso_login, usuario_cadastrado):
    home = HomePage(driver).abrir_home()
    assert home.home_visivel(), "A home nao ficou visivel"

    login = home.ir_para_login()
    assert login.texto(LoginPage.TITULO_LOGIN) == "Login to your account"

    login.fazer_login(caso_login["email"], caso_login["senha"])

    if caso_login["tipo"] == "servidor":
        # Classe valida: formato de e-mail aceito, porem credenciais nao conferem.
        assert (
            login.mensagem_erro_login()
            == "Your email or password is incorrect!"
        ), caso_login["descricao"]

    elif caso_login["tipo"] == "email_invalido":
        # Classe invalida: o navegador barra o envio antes de chegar ao servidor.
        assert login.email_valido() is False, caso_login["descricao"]
        assert "Please" in login.validacao_email(), caso_login["descricao"]
        assert login.mensagem_erro_login(timeout=2) == "", (
            "O servidor nao deveria receber e-mail com formato invalido"
        )

    elif caso_login["tipo"] == "senha_vazia":
        # Valor limite inferior da senha: 0 caractere.
        assert login.email_valido() is True
        assert login.validacao_senha() != "", "Senha vazia deveria ser barrada"
        assert login.mensagem_erro_login(timeout=2) == ""

    else:  # pragma: no cover - proteção contra erro de digitação no CSV
        pytest.fail(f"Tipo de caso desconhecido: {caso_login['tipo']}")
