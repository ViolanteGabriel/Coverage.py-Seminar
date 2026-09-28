from coverage_demo.checkout import ResultadoCheckout, calcular_checkout


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
