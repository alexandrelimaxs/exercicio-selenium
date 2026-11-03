# Exercício Selenium — Automation Exercise

Testes end-to-end com **Selenium + pytest** para as funcionalidades de **login com e-mail incorreto**
(Test Case 3) e **registro de usuário** (Test Case 1) do site
<https://automationexercise.com/>.

## Stack

- Python 3.12
- Selenium 4 (Selenium Manager baixa o driver automaticamente)
- pytest + pytest-html
- Padrão **Page Object Model**

## Estrutura

```text
.
├── conftest.py                     # fixtures, driver, relatório e screenshot em falha
├── pytest.ini                      # configuração e markers (login / registro)
├── requirements.txt
├── data/
│   └── casos_login.csv             # 6 entradas parametrizadas de login
├── pages/
│   ├── base_page.py
│   ├── home_page.py
│   ├── login_page.py
│   ├── signup_page.py
│   └── account_page.py
├── tests/
│   ├── test_login_incorreto.py     # Test Case 3
│   └── test_registro_usuario.py    # Test Case 1
├── utils/
│   ├── api.py                      # setup/teardown da conta de apoio
│   └── dados.py                    # geração de e-mail único e massa de dados
└── reports/                        # relatório HTML e screenshots (gerados)
```

## Como executar

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
```

Opções úteis:

| Comando | Descrição |
|---|---|
| `pytest` | Executa tudo em modo headless |
| `HEADLESS=0 pytest` | Executa com o navegador visível |
| `pytest -m login` | Somente os testes de login |
| `pytest -m registro` | Somente os testes de cadastro |
| `pytest -k L3` | Um caso específico de login |

O relatório HTML é gerado em `reports/relatorio.html`; em caso de falha, um screenshot é salvo em
`reports/screenshots/`.

## Casos de teste

### Login (Test Case 3)

| ID | Entrada | Classe / limite | Esperado |
|---|---|---|---|
| L1 | e-mail válido não cadastrado + senha errada | classe válida | `Your email or password is incorrect!` |
| L2 | e-mail cadastrado + senha errada | classe válida | `Your email or password is incorrect!` |
| L3 | `semarroba.example.com` | inválido (sem `@`) | validação nativa bloqueia |
| L4 | `semdominio@` | inválido (sem domínio) | validação nativa bloqueia |
| L5 | e-mail vazio | limite inferior | validação nativa bloqueia |
| L6 | senha vazia | limite inferior | validação nativa bloqueia |

### Registro (Test Case 1)

| ID | Cenário | Técnica |
|---|---|---|
| R1 | fluxo completo: cadastro → conta criada → login → exclusão | fluxo principal |
| R2 | nome com 1 caractere | valor limite inferior |
| R3 | e-mail já existente | classe inválida |
| R4 | campos obrigatórios vazios | valor limite inferior (0) |

## Resultados

Execução local em 02/11/2026:

```text
collected 10 items
tests/test_login_incorreto.py ....... 6 passed
tests/test_registro_usuario.py ...... 4 passed

10 passed in 151.51s
```

A suíte foi executada duas vezes seguidas após o ajuste de bloqueio de anúncios, com o mesmo
resultado (10 passed).

## Decisões técnicas

- **Isolamento:** cada teste abre e fecha um navegador próprio, pois `/login` redireciona para `/`
  quando já existe sessão autenticada.
- **Dados únicos:** e-mails são gerados com timestamp para evitar colisão entre execuções.
- **Conta de apoio:** o caso L2 cria e remove uma conta via API pública do site apenas como
  *setup/teardown*; o comportamento validado continua sendo o da interface.
- **Anúncios:** o site exibe anúncios que podem cobrir o formulário e interceptar cliques. A suíte
  bloqueia os domínios de anúncio no Chrome, remove iframes de anúncio antes das interações e usa
  clique via JavaScript como fallback. O clique em “Continue” também pode abrir o *Google
  vignette*; o `AccountPage` contorna isso navegando explicitamente para a home.
- **Limpeza:** o fluxo de cadastro exclui a conta ao final e ainda faz uma limpeza defensiva via API
  caso o teste falhe no meio.

## Exercício 2

O material de apoio da avaliação da plataforma GenIA-E2ETest é mantido apenas localmente e não é
versionado neste repositório.

> ⚠️ A API Key citada no arquivo local `exercicio-selenium-2.md` está exposta em texto puro e foi
> mantida **fora do repositório** (ver `.gitignore`). Revogue-a após a atividade.
