# Cenário adicional

`missing_test.py` verifica um pedido de R$ 80,00 sem premium, sem cupom e com entrega normal. O resultado esperado é desconto zero, frete de R$ 20,00 e total de R$ 100,00.

Esse cenário exercita as quatro saídas falsas não percorridas pela suíte inicial. Está fora de `tests` e não segue o padrão `test_*.py`, por isso não é coletado na execução padrão.

Execute os três testes sem modificar arquivos:

```bash
python -m coverage erase
python -m coverage run --branch -m pytest -q tests demo_solution/missing_test.py
python -m coverage report -m
```

Veja o [README do projeto](../README.md) para a descrição das regras, instalação, métricas e limitações.
