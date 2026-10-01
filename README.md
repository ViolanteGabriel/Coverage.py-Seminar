# Coverage.py: cobertura de linhas e branches

Projeto didático da disciplina **Engenharia de Software II**, desenvolvido por **João Pedro Viana Araldi, Gabriel Machado Violante e Isaac Reyes Alves de Abreu**.

O exemplo implementa o checkout de uma loja virtual e mostra como testes aprovados podem executar todas as linhas sem exercitar todas as saídas das decisões. A suíte inicial tem dois testes e 100% de cobertura de linhas. Ao medir branches, aparecem quatro saídas ausentes. Um terceiro teste completa essas saídas.

## A ferramenta

[coverage.py](https://coverage.readthedocs.io/) mede o código Python executado durante uma execução. Neste projeto, o [pytest](https://docs.pytest.org/) executa os testes e verifica as asserções; o coverage.py coleta dados e produz relatórios no terminal e em HTML.

- **Cobertura de linhas:** quais instruções executáveis foram visitadas.
- **Cobertura de branches:** quais saídas das decisões foram percorridas, como os caminhos verdadeiro e falso de um `if`.
- **Relatório HTML:** permite consultar o código e localizar linhas ausentes e decisões parcialmente cobertas.
- **`fail-under`:** retorna um código de falha quando a cobertura total fica abaixo de um limite, permitindo usar a métrica em integração contínua.

Quando a medição usa `--branch`, a coluna `Cover` combina instruções e saídas de decisões. Ela não representa somente a porcentagem de branches. Consulte a [documentação de branches](https://coverage.readthedocs.io/en/7.16.2/branch.html) e a [referência do relatório](https://coverage.readthedocs.io/en/7.16.2/commands/cmd_report.html).

## Regra de negócio

A função `calcular_checkout` retorna uma `ResultadoCheckout` imutável, com subtotal, desconto, subtotal após desconto, frete e total.

| Condição | Resultado |
|---|---|
| Subtotal menor ou igual a zero | Lança `ValueError` |
| Cliente premium | Desconto de 5% sobre o subtotal original |
| Cupom `SAVE10` | Desconto adicional de 10% sobre o subtotal original |
| Outro cupom ou nenhum cupom | Sem desconto de cupom |
| Premium com `SAVE10` | Desconto acumulado de 15% |
| Entrega normal | Frete de R$ 20,00 |
| Subtotal após descontos ≥ R$ 200,00 | Frete normal grátis |
| Entrega expressa | Acrescenta R$ 15,00, mesmo com frete normal grátis |
| Total | Subtotal após descontos + frete |

Os valores usam `float` e arredondamento para duas casas decimais por simplicidade didática. O desconto e o subtotal após descontos são arredondados antes da decisão de frete grátis. Para uma aplicação financeira real, a representação monetária e a política de arredondamento precisam ser definidas com maior rigor.

## Estrutura

```text
.
├── README.md
├── Coverage.py - Apresentação EDSII (1).pptx
├── pyproject.toml
├── src/coverage_demo/
│   ├── __init__.py
│   └── checkout.py
├── tests/test_checkout.py
└── demo_solution/
    ├── README.md
    └── missing_test.py
```

`tests/test_checkout.py` contém a suíte inicial. `demo_solution/missing_test.py` contém o terceiro cenário para comparação. O pytest coleta apenas arquivos `test_*.py` em `tests`, portanto esse cenário adicional não entra na execução padrão. A configuração de coverage em `pyproject.toml` mede somente o pacote `coverage_demo`; os testes não entram no percentual. Branches são ativados explicitamente pelo comando.

## Instalação

Requer **Python 3.11 ou superior**. Na raiz do repositório, crie e ative um ambiente virtual:

```bash
# Linux/macOS
python3 -m venv .venv
source .venv/bin/activate
```

```powershell
# Windows PowerShell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Se a ativação no PowerShell estiver bloqueada, execute diretamente `.venv\Scripts\python.exe` no lugar de `python` nos comandos seguintes.

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
```

O extra `dev` instala pytest e coverage.py. Após instalar as dependências, a execução é local e não exige rede, banco de dados ou serviços externos.

## Medição e resultados

Cobertura somente de linhas:

```bash
python -m coverage erase
python -m coverage run -m pytest -q
python -m coverage report -m
```

Cobertura com branches:

```bash
python -m coverage erase
python -m coverage run --branch -m pytest -q
python -m coverage report -m
python -m coverage html
```

Abra `htmlcov/index.html` no navegador e selecione `checkout.py`. `coverage html` usa os dados já coletados; não executa testes novamente. A limpeza evita misturar medições de linhas e branches.

| Cenário | Testes | Linhas cobertas | Saídas cobertas | `Cover` com branches | `BrPart` |
|---|---:|---:|---:|---:|---:|
| Suíte inicial | 2 | 19/19 (100%) | 6/10 (60%) | 86% | 4 |
| Com cenário adicional | 3 | 19/19 (100%) | 10/10 (100%) | 100% | 0 |

A suíte inicial verifica subtotal zero e um pedido de R$ 300,00 com premium, `SAVE10` e entrega expressa. O pedido recebe R$ 45,00 de desconto, fica com R$ 255,00 após desconto e paga R$ 15,00 de frete: **total de R$ 270,00**.

A decisão de subtotal inválido tem suas duas saídas exercitadas. As outras quatro decisões só têm a saída verdadeira executada. O relatório aponta `26->28`, `28->31`, `34->36` e `36->39`: transições que pulam os corpos dos respectivos `if`. Os números mudam se o código for editado.

Na medição inicial, `Stmts = 19`, `Miss = 0`, `Branch = 10` e `BrPart = 4`. O percentual combinado é `(19 + 6) / (19 + 10) ≈ 86%`. `BrPart` conta saídas faltantes em decisões parcialmente cobertas; neste exemplo, há uma em cada uma das quatro decisões.

Para reproduzir o cenário completo **sem alterar a suíte inicial**, inclua explicitamente o arquivo adicional:

```bash
python -m coverage erase
python -m coverage run --branch -m pytest -q tests demo_solution/missing_test.py
python -m coverage report -m
python -m coverage html
python -m coverage report --fail-under=100
```

O cenário adicional verifica um pedido de R$ 80,00, sem premium, sem cupom e com entrega normal. O desconto é zero, o frete é R$ 20,00 e o **total é R$ 100,00**. Ele percorre as quatro saídas falsas ausentes e compara todos os campos retornados.

Os valores da tabela foram reproduzidos em Linux com Python 3.14.7, pytest 9.1.1 e coverage.py 7.16.2. Contagens podem variar entre versões; o comportamento demonstrado é a diferença entre visitar todas as linhas e exercitar todas as saídas das decisões.

## Limite de cobertura

Após uma medição com branches:

```bash
python -m coverage report --fail-under=100
```

Com a suíte inicial, o comando encontra 86% e retorna **2**. Com os três testes, encontra 100% e retorna **0**. Esse status pode reprovar uma etapa de CI. O projeto demonstra o comando, mas não inclui um pipeline configurado.

## Conclusão

Cobertura revela execução, não prova ausência de defeitos nem qualidade das asserções. Mesmo com 100% de branches, ainda faltam combinações e valores de fronteira, como o limite exato de R$ 200,00 após descontos, subtotal negativo e cupom desconhecido. A análise dos requisitos deve orientar os testes além da métrica.
