# Coverage.py Seminar

Demonstração de cobertura de código com **coverage.py**, preparada para uma apresentação de aproximadamente 10 minutos na disciplina Engenharia de Software II.

Dois testes passam e executam 100% das linhas do checkout. A medição com branches revela quatro caminhos ausentes. Um único teste adicional completa esses caminhos e leva a cobertura a 100%.

## Objetivo

Praticar testes automatizados com pytest, comparar cobertura de linhas e de branches, interpretar os relatórios textual e HTML e demonstrar um limite de cobertura com `fail-under`, como em integração contínua (CI).

O projeto é propositalmente pequeno. Depois da instalação, a demonstração funciona localmente, sem rede, banco de dados, Docker ou variáveis de ambiente.

## Regra de negócio

A função `calcular_checkout` calcula os descontos e o custo de entrega de um pedido.

| Regra | Comportamento |
|---|---|
| Subtotal menor ou igual a zero | Lança `ValueError` com mensagem explicativa |
| Cliente premium | 5% de desconto sobre o subtotal original |
| Cupom `SAVE10` | Mais 10% sobre o subtotal original |
| Outro cupom ou nenhum cupom | Não acrescenta desconto |
| Premium com `SAVE10` | Desconto acumulado de 15% |
| Frete normal | R$ 20,00 |
| Subtotal após desconto maior ou igual a R$ 200,00 | Frete normal grátis |
| Entrega expressa | Acrescenta R$ 15,00 ao frete, inclusive quando o frete normal é grátis |
| Total | Subtotal com desconto + frete final |

Para manter o exemplo legível, os valores usam `float` e `round(..., 2)`. O desconto é arredondado antes de calcular o subtotal com desconto; este é arredondado antes de verificar o frete grátis. O retorno também arredonda subtotal, frete e total. É uma simplificação didática, com valores previsíveis nos cenários apresentados.

No cenário inicial: R$ 300,00, cliente premium, cupom `SAVE10` e entrega expressa resultam em R$ 45,00 de desconto, R$ 255,00 após desconto, R$ 15,00 de frete e **R$ 270,00 de total**.

## Estrutura do projeto

```text
coverage_py_demo/
├── README.md
├── pyproject.toml
├── .gitignore
├── src/
│   └── coverage_demo/
│       ├── __init__.py
│       └── checkout.py
├── tests/
│   └── test_checkout.py
└── demo_solution/
    ├── README.md
    └── missing_test.py
```

- `src/coverage_demo/checkout.py`: regras de negócio e a dataclass imutável `ResultadoCheckout`.
- `tests/test_checkout.py`: os dois testes iniciais, incluindo a validação do subtotal.
- `demo_solution/missing_test.py`: o teste reservado para a segunda parte da apresentação.
- `pyproject.toml`: instalação editável, dependências de desenvolvimento e configuração de coleta e cobertura.
- `.gitignore`: mantém ambiente virtual, relatórios e arquivos temporários fora do Git.

O pytest procura somente em `tests`, com o padrão `test_*.py`. Assim, a solução não entra na execução normal. O coverage mede todo o pacote `coverage_demo`; não há exclusões artificiais nem ativação de branches por padrão.

## Pré-requisitos

- Python **3.11 ou superior**, com `pip` e suporte a `venv`.
- Terminal e navegador para visualizar o HTML.
- Git, se desejar versionar ou publicar o projeto.

Verifique a instalação:

```bash
python --version
python -m pip --version
```

Em Linux/macOS, use `python3 --version` se esse for o nome do executável. Os comandos abaixo devem ser executados **na pasta que contém este README e o `pyproject.toml`**:

```bash
cd coverage_py_demo
```

Se você clonou o repositório com outro nome, entre na pasta criada pelo clone.

## Criação do ambiente virtual

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Caso a política do PowerShell bloqueie a ativação, use o Prompt de Comando conforme abaixo ou execute diretamente `.venv\Scripts\python.exe -m pytest` e `.venv\Scripts\python.exe -m coverage` com os argumentos das próximas etapas.

### Windows Prompt de Comando

```bat
python -m venv .venv
.venv\Scripts\activate.bat
```

### Linux e macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Instalação

Com o ambiente virtual ativado:

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

A instalação editável permite alterar os arquivos sem reinstalar o pacote. O extra `dev` instala pytest e coverage.py. Faça essa preparação antes da aula: somente a instalação precisa baixar dependências.

Dentro do ambiente ativado, `python` aponta para o Python desse ambiente. Se `pytest` ou `coverage` não forem encontrados, use `python -m pytest` e `python -m coverage` respectivamente.

## Execução dos testes

```bash
pytest -q
```

São **dois testes aprovados** na suíte inicial. A validação foi feita em Linux com **Python 3.14.7, pytest 9.1.1 e coverage.py 7.16.2**. Saída observada:

```text
..                                                                       [100%]
2 passed in 0.00s
```

O tempo varia entre execuções. As instruções incluem Windows e macOS, mas a validação realizada foi em Linux.

## Primeira medição: cobertura de linhas

```bash
coverage erase
coverage run -m pytest
coverage report -m
```

`erase` apaga a medição anterior. `run -m pytest` executa a suíte sob medição. `report -m` exibe os resultados e as linhas ausentes, se houver.

Resultado medido:

```text
Name                            Stmts   Miss  Cover   Missing
-------------------------------------------------------------
src/coverage_demo/__init__.py       0      0   100%
src/coverage_demo/checkout.py      19      0   100%
-------------------------------------------------------------
TOTAL                              19      0   100%
```

`Stmts` indica instruções executáveis consideradas pela ferramenta, `Miss` as não executadas e `Cover` o percentual de cobertura. Todas as linhas consideradas foram visitadas. Isso ainda não informa se cada decisão foi exercitada nos dois sentidos.

## Cobertura de branches

```bash
coverage erase
coverage run --branch -m pytest
coverage report -m
```

Limpe os dados ao alternar os modos de medição. Resultado medido:

```text
Name                            Stmts   Miss Branch BrPart  Cover   Missing
---------------------------------------------------------------------------
src/coverage_demo/__init__.py       0      0      0      0   100%
src/coverage_demo/checkout.py      19      0     10      4    86%   26->28, 28->31, 34->36, 36->39
---------------------------------------------------------------------------
TOTAL                              19      0     10      4    86%
```

Um **branch** é uma saída possível de uma decisão. Neste exemplo, cada `if` pode seguir o caminho verdadeiro (executar seu corpo) ou falso (pular seu corpo).

A validação de subtotal já tem os dois caminhos: lançar a exceção e continuar com um pedido válido. As outras quatro decisões só foram executadas com resultado verdadeiro. O subtotal inválido encerra a função antes de alcançá-las, portanto não cobre seus caminhos falsos.

| Coluna | Interpretação nesta medição |
|---|---|
| `Miss = 0` | Nenhuma linha executável ficou sem execução |
| `Branch = 10` | Cinco decisões, com duas saídas cada |
| `BrPart = 4` | Quatro branches parcialmente cobertos: a decisão foi visitada, mas uma saída ficou sem execução |
| `Missing` | Setas indicam transições entre linhas ainda não percorridas |
| `Cover = 86%` | Percentual combinado de linhas e saídas de decisões |

Por exemplo, `26->28` indica que falta sair do `if cliente_premium` diretamente para a decisão do cupom, sem aplicar o desconto premium. Os números de linha podem mudar se o arquivo for editado.

**Os 86% não são o percentual exclusivo de branches.** Foram cobertas 19 de 19 instruções e 6 de 10 saídas: `(19 + 6) / (19 + 10)`, aproximadamente 86%. A cobertura exclusiva das saídas é **60%**. O relatório com `--branch` combina as duas métricas na coluna `Cover`.

## Relatório HTML

Após a medição com branches:

```bash
coverage html
```

Abra `htmlcov/index.html` manualmente no navegador ou use o comando do seu sistema:

### Windows PowerShell ou Prompt de Comando

```powershell
start htmlcov\index.html
```

### macOS

```bash
open htmlcov/index.html
```

### Linux

```bash
xdg-open htmlcov/index.html
```

Não é necessário iniciar um servidor web. `coverage html` usa a última medição salva; ele não executa os testes novamente.

### O que observar no relatório HTML

Abra o módulo `checkout.py` a partir do índice. Observe a indicação de linhas executadas, linhas ausentes e branches parciais. Inicialmente não há linhas ausentes, mas as quatro decisões apresentam saídas faltantes. As anotações ao lado das decisões ajudam a identificar essas transições.

Depois de adicionar o teste e gerar novamente o HTML, recarregue a página: os branches parciais desaparecem. A aparência e as cores podem variar conforme a versão ou o tema da ferramenta.

## Demonstração do problema

A suíte inicial foi construída deliberadamente para mostrar que **todos os testes podem passar sem que todos os caminhos lógicos tenham sido exercitados**.

Um teste verifica a exceção para subtotal zero; o outro ativa premium, cupom, frete grátis e entrega expressa ao mesmo tempo. Isso visita todas as linhas, mas deixa sem verificação um pedido comum que não ativa nenhuma dessas condições. Não há contradição: passar significa que as asserções dos cenários executados foram satisfeitas.

Mesmo 100% de branches não garante todas as combinações de decisões, valores de fronteira ou boas asserções. Por exemplo, a suíte didática não verifica especificamente o limite exato de R$ 200,00 após descontos nem um cupom desconhecido. A métrica orienta a investigação; ela não substitui a análise dos requisitos.

## Adicionando o teste faltante

1. Abra `demo_solution/missing_test.py`.
2. Copie somente a função `test_cliente_comum_sem_cupom_e_entrega_normal` abaixo.
3. Cole ao final de `tests/test_checkout.py`, fora das outras funções. Os imports necessários já existem.
4. Salve o arquivo.
5. Execute novamente os testes e a medição.

```python
def test_cliente_comum_sem_cupom_e_entrega_normal():
    resultado = calcular_checkout(
        subtotal=80.0,
        cliente_premium=False,
        cupom=None,
        entrega_expressa=False,
    )

    assert resultado == ResultadoCheckout(
        subtotal=80.0,
        desconto=0.0,
        subtotal_com_desconto=80.0,
        frete=20.0,
        total=100.0,
    )
```

Esse pedido percorre as quatro saídas falsas ausentes e verifica todos os campos do resultado.

```bash
pytest -q
coverage erase
coverage run --branch -m pytest
coverage report -m
coverage html
```

Agora são **três testes aprovados**. Resultado medido:

```text
Name                            Stmts   Miss Branch BrPart  Cover   Missing
---------------------------------------------------------------------------
src/coverage_demo/__init__.py       0      0      0      0   100%
src/coverage_demo/checkout.py      19      0     10      0   100%
---------------------------------------------------------------------------
TOTAL                              19      0     10      0   100%
```

Reabra ou atualize o HTML para mostrar a diferença.

## Comparação antes e depois

Resultados reais para `checkout.py`, no ambiente descrito acima:

| Situação | Testes aprovados | Cobertura de linhas | Saídas de branches cobertas | `Cover` com `--branch` | `BrPart` |
|---|---:|---:|---:|---:|---:|
| Suíte inicial | 2 | 100% (19/19) | 60% (6/10) | 86% | 4 |
| Após novo teste | 3 | 100% (19/19) | 100% (10/10) | 100% | 0 |

A contagem de instruções pode variar conforme as versões de Python e coverage. Os valores acima são da execução efetivamente validada; o contraste pedagógico é executar todas as linhas e deixar quatro saídas sem execução na suíte inicial.

## Uso de fail-under

Depois de medir **com branches**, execute:

```bash
coverage report --fail-under=100
```

| Estado dos dados de cobertura | Resultado observado | Código de saída |
|---|---|---:|
| Suíte inicial com branches | 86%, abaixo do limite; comando falha | 2 |
| Suíte com o novo teste e nova medição com branches | 100%; comando passa | 0 |

A falha inicial é esperada e faz parte da demonstração. O limite se aplica ao total combinado mostrado no relatório. Se os dados forem de uma execução somente com linhas, a suíte inicial já passará nesse limite; por isso use `coverage run --branch` antes.

Para consultar o código de saída imediatamente após o comando:

- Bash (Linux/macOS): `echo $?`
- PowerShell: `echo $LASTEXITCODE`
- Prompt de Comando: `echo %ERRORLEVEL%`

Em CI, um status diferente de zero pode reprovar a etapa e impedir que uma redução de cobertura passe despercebida. O limite de 100% foi escolhido para este exemplo pequeno; não garante que os testes detectem todos os defeitos.

## Roteiro de demonstração em 10 minutos

Prepare o ambiente e abra o código antes da aula. Comece com apenas os dois testes iniciais.

| Tempo | Ação |
|---|---|
| 0 a 1 min | Explicar as cinco decisões do checkout e o pedido de R$ 300,00 |
| 1 a 2 min | Executar `pytest -q`: dois testes passam |
| 2 a 4 min | Medir sem `--branch` e mostrar os 100% de linhas |
| 4 a 6 min | Medir com `--branch`, mostrar 86%, quatro branches parciais e abrir HTML; executar o `fail-under=100` que falha |
| 6 a 8 min | Copiar o teste do pedido comum de R$ 80,00 e salvar |
| 8 a 9 min | Executar a suíte e a medição com branches novamente; mostrar 100% e atualizar HTML |
| 9 a 10 min | Repetir `fail-under=100`, agora com sucesso, e discutir os limites da métrica |

### Preparar uma nova apresentação

Remova **somente a função que você acrescentou** ao final de `tests/test_checkout.py` e salve. Preserve os dois testes iniciais. Depois:

```bash
pytest -q
coverage erase
coverage run --branch -m pytest
coverage report -m
coverage html
```

Confirme dois testes, 86% na coluna `Cover` e quatro branches parciais no ambiente de referência. Isso também substitui o relatório HTML da execução final pelo inicial.

## Repositório Git e publicação

O nome de apresentação é **Coverage.py Seminar**. Use `Coverage.py-Seminar` como nome do repositório remoto, sem espaços. O projeto está preparado como repositório Git independente na pasta `coverage_py_demo`, com branch `main`, commit inicial e arquivos gerados ignorados.

Para conferir o estado local:

```bash
git status
git log -1 --oneline
```

Para publicar, crie um repositório remoto vazio chamado `Coverage.py-Seminar`, sem adicionar README, licença ou `.gitignore` pelo serviço. Substitua `SEU_USUARIO` pelo seu usuário nos comandos abaixo:

```bash
git remote add origin https://github.com/SEU_USUARIO/Coverage.py-Seminar.git
git push -u origin main
```

A publicação requer sua conta e autenticação no serviço. O projeto entregue não configura um remoto fictício e não publica nada automaticamente.

## Mensagem final

**Alta cobertura de linhas não significa, sozinha, que todos os comportamentos do sistema foram testados.**

Coverage é um indicador de execução, não uma garantia da qualidade das asserções. Nesta demonstração, um teste adicional torna visíveis comportamentos que a primeira métrica não revelava; a análise dos requisitos continua necessária mesmo após atingir 100%.
