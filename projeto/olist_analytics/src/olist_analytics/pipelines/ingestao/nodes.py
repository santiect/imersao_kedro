"""Nós de ingestão: cada tabela bruta vira uma tabela limpa e tipada.

Um nó por tabela de origem, de propósito — é o que faz o grafo no Kedro-Viz
ficar ramificado em vez de uma linha reta.
"""

from __future__ import annotations

import logging

import pandas as pd

logger = logging.getLogger(__name__)

COLUNAS_DATA_PEDIDOS = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]


def limpar_pedidos(pedidos: pd.DataFrame) -> pd.DataFrame:
    """Tipa as datas do ciclo de vida do pedido."""
    pedidos = pedidos.copy()
    for coluna in COLUNAS_DATA_PEDIDOS:
        pedidos[coluna] = pd.to_datetime(pedidos[coluna])
    return pedidos


def filtrar_pedidos_por_periodo(pedidos_limpos: pd.DataFrame, params: dict) -> pd.DataFrame:
    """Recorta os pedidos para o período de análise definido em parameters.yml.

    Esta é a demonstração central de "config fora do código": mudar o período
    da análise é editar uma data em YAML, não caçar um valor no meio do script.
    """
    inicio = pd.Timestamp(params["periodo"]["inicio"])
    fim = pd.Timestamp(params["periodo"]["fim"])
    filtrados = pedidos_limpos[
        pedidos_limpos["order_purchase_timestamp"].between(inicio, fim)
    ].copy()
    logger.info(
        "Período %s a %s: %d de %d pedidos",
        inicio.date(),
        fim.date(),
        len(filtrados),
        len(pedidos_limpos),
    )
    return filtrados


def limpar_itens(itens: pd.DataFrame) -> pd.DataFrame:
    """Tipa a data limite de envio de cada item."""
    itens = itens.copy()
    itens["shipping_limit_date"] = pd.to_datetime(itens["shipping_limit_date"])
    return itens


def agregar_pagamentos(pagamentos: pd.DataFrame) -> pd.DataFrame:
    """Consolida os pagamentos por pedido: valor total e nº de formas usadas.

    Um pedido pode ter mais de uma linha de pagamento (ex.: cartão + boleto).
    """
    return (
        pagamentos.groupby("order_id")
        .agg(
            valor_pago=("payment_value", "sum"),
            formas_pagamento=("payment_type", "nunique"),
        )
        .reset_index()
    )


def limpar_avaliacoes(avaliacoes: pd.DataFrame) -> pd.DataFrame:
    """Mantém a avaliação mais recente por pedido, quando há mais de uma."""
    avaliacoes = avaliacoes.copy()
    avaliacoes["review_creation_date"] = pd.to_datetime(avaliacoes["review_creation_date"])
    avaliacoes = avaliacoes.sort_values("review_creation_date").drop_duplicates(
        "order_id", keep="last"
    )
    return avaliacoes[["order_id", "review_score", "review_creation_date"]]


def limpar_clientes(clientes: pd.DataFrame) -> pd.DataFrame:
    """Mantém a localização do cliente."""
    return clientes[
        ["customer_id", "customer_unique_id", "customer_city", "customer_state"]
    ].copy()


def traduzir_categorias(produtos: pd.DataFrame, traducao_categorias: pd.DataFrame) -> pd.DataFrame:
    """Junta o produto com a tradução da categoria (PT -> EN).

    Categorias sem tradução mantêm o nome original em português — é melhor
    mostrar a categoria em PT do que perder a linha inteira.
    """
    produtos = produtos.merge(traducao_categorias, on="product_category_name", how="left")
    produtos["product_category_name_english"] = produtos[
        "product_category_name_english"
    ].fillna(produtos["product_category_name"])
    return produtos[["product_id", "product_category_name_english"]].rename(
        columns={"product_category_name_english": "categoria"}
    )


def limpar_vendedores(vendedores: pd.DataFrame) -> pd.DataFrame:
    """Mantém a localização do vendedor."""
    return vendedores[["seller_id", "seller_city", "seller_state"]].copy()
