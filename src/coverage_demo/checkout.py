"""Regras simples de descontos e entrega de uma loja virtual."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ResultadoCheckout:
    subtotal: float
    desconto: float
    subtotal_com_desconto: float
    frete: float
    total: float


def calcular_checkout(
    subtotal: float,
    cliente_premium: bool = False,
    cupom: str | None = None,
    entrega_expressa: bool = False,
) -> ResultadoCheckout:
    """Calcule descontos acumulados sobre o subtotal e o frete final."""
    if subtotal <= 0:
        raise ValueError("O subtotal deve ser maior que zero.")

    percentual_desconto = 0.0
    if cliente_premium:
        percentual_desconto += 0.05
    if cupom == "SAVE10":
        percentual_desconto += 0.10

    desconto = round(subtotal * percentual_desconto, 2)
    subtotal_com_desconto = round(subtotal - desconto, 2)
    frete = 20.0
    if subtotal_com_desconto >= 200:
        frete = 0.0
    if entrega_expressa:
        frete += 15.0

    return ResultadoCheckout(
        subtotal=round(subtotal, 2),
        desconto=desconto,
        subtotal_com_desconto=subtotal_com_desconto,
        frete=round(frete, 2),
        total=round(subtotal_com_desconto + frete, 2),
    )
