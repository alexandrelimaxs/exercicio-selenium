"""Apoio de setup/teardown via API pública do Automation Exercise.

Usada apenas para preparar e limpar dados de teste (usuário cadastrado),
nunca para validar o comportamento em si — a validação é sempre pela UI.
"""

from __future__ import annotations

import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen

API_BASE = "https://automationexercise.com/api"


def _requisicao(metodo: str, caminho: str, dados: dict[str, str]) -> dict:
    corpo = urlencode(dados).encode("utf-8")
    requisicao = Request(f"{API_BASE}/{caminho}", data=corpo, method=metodo)
    requisicao.add_header("Content-Type", "application/x-www-form-urlencoded")
    requisicao.add_header("Accept", "application/json")
    # O Cloudflare do site rejeita o User-Agent padrão do urllib com HTTP 403.
    requisicao.add_header(
        "User-Agent",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36",
    )
    with urlopen(requisicao, timeout=30) as resposta:
        return json.loads(resposta.read().decode("utf-8"))


def criar_conta(email: str, senha: str, nome: str = "Usuario Cadastrado") -> dict:
    """Cria uma conta de apoio para o caso de senha incorreta."""
    return _requisicao(
        "POST",
        "createAccount",
        {
            "name": nome,
            "email": email,
            "password": senha,
            "title": "Mr",
            "birth_date": "10",
            "birth_month": "5",
            "birth_year": "1990",
            "firstname": nome,
            "lastname": "Teste",
            "company": "Qualidade de Software",
            "address1": "Rua dos Testes, 100",
            "address2": "Apto 42",
            "country": "India",
            "zipcode": "24000000",
            "state": "RJ",
            "city": "Niteroi",
            "mobile_number": "21999999999",
        },
    )


def excluir_conta(email: str, senha: str) -> dict:
    """Remove a conta de apoio ao final da sessão de testes."""
    return _requisicao("DELETE", "deleteAccount", {"email": email, "password": senha})
