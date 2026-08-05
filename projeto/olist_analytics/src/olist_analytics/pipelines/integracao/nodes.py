"""Nó de integração: as 8 tabelas intermediárias viram a tabela-verdade do negócio."""

from __future__ import annotations

import logging

import pandas as pd

logger = logging.getLogger(__name__)


def montar_pedidos_enriquecidos(
    pedidos_filtrados: pd.DataFrame,
    itens_limpos: pd.DataFrame,
    pagamentos_agregados: pd.DataFrame,
    avaliacoes_limpas: pd.DataFrame,
    clientes_limpos: pd.DataFrame,
    produtos_traduzidos: pd.DataFrame,
    vendedores_limpos: pd.DataFrame,
) -> pd.DataFrame:
    """Consolida um pedido por linha, juntando as 7 tabelas de entrada.

    Simplificação assumida: quando um pedido tem mais de um item, produto e
    vendedor vêm do primeiro item — o pedido em si permanece no grão de
    negócio (1 linha = 1 pedido), que é o que o caso de uso precisa.
    """
    itens_por_pedido = (
        itens_limpos.sort_values("order_item_id")
        .groupby("order_id")
        .agg(
            valor_itens=("price", "sum"),
            frete_total=("freight_value", "sum"),
            n_itens=("order_item_id", "count"),
            product_id=("product_id", "first"),
            seller_id=("seller_id", "first"),
        )
        .reset_index()
    )

    base = pedidos_filtrados.merge(itens_por_pedido, on="order_id", how="inner")
    base = base.merge(produtos_traduzidos, on="product_id", how="left")
    base = base.merge(vendedores_limpos, on="seller_id", how="left")
    base = base.merge(clientes_limpos, on="customer_id", how="left")
    base = base.merge(pagamentos_agregados, on="order_id", how="left")
    base = base.merge(
        avaliacoes_limpas[["order_id", "review_score"]], on="order_id", how="left"
    )

    logger.info(
        "pedidos_enriquecidos: %d pedidos, %d colunas", len(base), base.shape[1]
    )
    return base
