"""Testes do Test Case 1: registrar usuário."""

from __future__ import annotations

import pytest

from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.signup_page import SignupPage
from utils import dados
from utils.api import excluir_conta

pytestmark = pytest.mark.registro


def test_registrar_usuario_fluxo_completo(driver):
    info = dados.dados_cadastro("Usuario E2E", dados.email_unico("registro"))
    try:
        home = HomePage(driver).abrir_home()
        assert home.home_visivel(), "A home nao ficou visivel"

        login = home.ir_para_login()
        assert login.texto(LoginPage.TITULO_SIGNUP) == "New User Signup!"

        login.iniciar_cadastro(info["nome"], info["email"])
        signup = SignupPage(driver)
        assert signup.formulario_visivel(), "O formulario de cadastro nao abriu"

        signup.preencher_dados_conta(
            senha=info["senha"],
            titulo=info["titulo"],
            dia=info["dia"],
            mes=info["mes"],
            ano=info["ano"],
        )
        signup.preencher_endereco(
            primeiro_nome=info["primeiro_nome"],
            sobrenome=info["sobrenome"],
            empresa=info["empresa"],
            endereco=info["endereco"],
            endereco2=info["endereco2"],
            pais=info["pais"],
            estado=info["estado"],
            cidade=info["cidade"],
            cep=info["cep"],
            celular=info["celular"],
        )

        conta = signup.criar_conta()
        assert conta.conta_criada() == "ACCOUNT CREATED!"

        conta.continuar()
        assert conta.nome_logado() == info["nome"], "Usuario nao aparece logado"

        conta.excluir_conta()
        assert conta.conta_deletada() == "ACCOUNT DELETED!"
        conta.continuar_apos_exclusao()
    finally:
        # Limpeza defensiva: remove a conta caso o fluxo tenha falhado no meio.
        excluir_conta(info["email"], info["senha"])


def test_cadastro_nome_um_caractere_limite_inferior(driver):
    """Valor limite inferior do nome: 1 caractere e aceito pelo site."""
    email = dados.email_unico("nome_limite")

    home = HomePage(driver).abrir_home()
    login = home.ir_para_login()
    login.iniciar_cadastro("A", email)

    signup = SignupPage(driver)
    assert signup.formulario_visivel(), "Nome com 1 caractere deveria ser aceito"


def test_cadastro_email_duplicado(driver, usuario_cadastrado):
    home = HomePage(driver).abrir_home()
    login = home.ir_para_login()
    login.iniciar_cadastro("Outro Nome", usuario_cadastrado["email"])

    assert login.mensagem_erro_signup() == "Email Address already exist!"
    assert "/signup" in driver.current_url


def test_cadastro_campos_obrigatorios_vazios(driver):
    """Valor limite inferior dos campos obrigatorios: 0 caractere."""
    email = dados.email_unico("campos_vazios")

    home = HomePage(driver).abrir_home()
    login = home.ir_para_login()
    login.iniciar_cadastro("Teste Vazio", email)

    signup = SignupPage(driver)
    assert signup.formulario_visivel()

    signup.clicar(SignupPage.BOTAO_CRIAR_CONTA)

    assert signup.validacao_senha() != "", "Senha vazia deveria ser barrada"
    assert "/signup" in driver.current_url
