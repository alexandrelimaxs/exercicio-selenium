"""Geração de dados únicos para os testes."""

from __future__ import annotations

import time


def email_unico(prefixo: str = "usuario") -> str:
    """Gera um e-mail único para evitar colisão com contas já existentes."""
    return f"{prefixo}_{int(time.time() * 1000)}@example.com"


def dados_cadastro(nome: str, email: str) -> dict[str, str]:
    """Dados completos usados no formulário de cadastro (Test Case 1)."""
    return {
        "nome": nome,
        "email": email,
        "senha": "Senha@123",
        "titulo": "Mr",
        "dia": "10",
        "mes": "5",
        "ano": "1990",
        "primeiro_nome": nome,
        "sobrenome": "Teste E2E",
        "empresa": "Qualidade de Software",
        "endereco": "Rua dos Testes, 100",
        "endereco2": "Apto 42",
        "pais": "India",
        "estado": "RJ",
        "cidade": "Niteroi",
        "cep": "24000000",
        "celular": "21999999999",
    }
