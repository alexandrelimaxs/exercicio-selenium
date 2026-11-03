"""Fixtures compartilhadas da suíte de testes."""

from __future__ import annotations

import csv
import os
import time
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from utils.api import criar_conta, excluir_conta

RAIZ = Path(__file__).resolve().parent
RELATORIOS = RAIZ / "reports"
BASE_URL = os.getenv("BASE_URL", "https://automationexercise.com")

# Conta de apoio criada via API para o caso "e-mail cadastrado + senha incorreta".
EMAIL_CADASTRADO = f"genia_cadastrado_{int(time.time())}@example.com"
SENHA_CADASTRADA = "Senha@123"
NOME_CADASTRADO = "Usuario Cadastrado"


def carregar_casos_login() -> list[dict[str, str]]:
    """Lê o CSV e resolve os placeholders usados nos dados dinâmicos."""
    carimbo = str(int(time.time() * 1000))
    caminho = RAIZ / "data" / "casos_login.csv"
    with caminho.open(encoding="utf-8") as arquivo:
        casos = []
        for linha in csv.DictReader(arquivo):
            casos.append(
                {
                    **linha,
                    "email": linha["email"]
                    .replace("${EMAIL_CADASTRADO}", EMAIL_CADASTRADO)
                    .replace("${STAMP}", carimbo),
                }
            )
    return casos


def pytest_generate_tests(metafunc) -> None:
    if "caso_login" in metafunc.fixturenames:
        casos = carregar_casos_login()
        metafunc.parametrize("caso_login", casos, ids=[caso["id"] for caso in casos])


@pytest.fixture(scope="session")
def base_url() -> str:
    return BASE_URL


@pytest.fixture(scope="session")
def usuario_cadastrado() -> dict[str, str]:
    resposta = criar_conta(EMAIL_CADASTRADO, SENHA_CADASTRADA, NOME_CADASTRADO)
    if resposta.get("responseCode") != 201:
        pytest.fail(f"Falha ao criar usuario de apoio: {resposta}")
    yield {
        "email": EMAIL_CADASTRADO,
        "senha": SENHA_CADASTRADA,
        "nome": NOME_CADASTRADO,
    }
    excluir_conta(EMAIL_CADASTRADO, SENHA_CADASTRADA)


@pytest.fixture
def driver():
    opcoes = Options()
    if os.getenv("HEADLESS", "1") != "0":
        opcoes.add_argument("--headless=new")
    opcoes.add_argument("--window-size=1400,1000")
    opcoes.add_argument("--disable-notifications")
    # Bloqueia os domínios de anúncio que cobrem o formulário durante os testes.
    opcoes.add_argument(
        "--host-resolver-rules="
        "MAP pagead2.googlesyndication.com 127.0.0.1,"
        "MAP googleads.g.doubleclick.net 127.0.0.1,"
        "MAP tpc.googlesyndication.com 127.0.0.1,"
        "MAP securepubads.g.doubleclick.net 127.0.0.1,"
        "MAP adservice.google.com 127.0.0.1,"
        "MAP www.googletagservices.com 127.0.0.1"
    )
    navegador = webdriver.Chrome(options=opcoes)
    navegador.set_window_size(1400, 1000)
    yield navegador
    navegador.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    resultado = yield
    relatorio = resultado.get_result()
    setattr(item, f"rep_{relatorio.when}", relatorio)


@pytest.fixture(autouse=True)
def capturar_tela_em_falha(request, driver):
    yield
    relatorio = getattr(request.node, "rep_call", None)
    if relatorio is not None and relatorio.failed:
        pasta = RELATORIOS / "screenshots"
        pasta.mkdir(parents=True, exist_ok=True)
        nome = request.node.name.replace("[", "_").replace("]", "").replace("/", "_")
        driver.save_screenshot(str(pasta / f"{nome}.png"))
