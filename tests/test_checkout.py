import pytest

from coverage_demo.checkout import ResultadoCheckout, calcular_checkout


def test_subtotal_invalido():
    with pytest.raises(ValueError, match="O subtotal deve ser maior que zero"):
        calcular_checkout(subtotal=0)


def test_premium_com_cupom_e_entrega_expressa():
    resultado = calcular_checkout(
        subtotal=300.0,
        cliente_premium=True,
        cupom="SAVE10",
        entrega_expressa=True,
    )

    assert resultado == ResultadoCheckout(
        subtotal=300.0,
        desconto=45.0,
        subtotal_com_desconto=255.0,
        frete=15.0,
        total=270.0,
    )
