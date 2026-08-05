"""Nós de relatório: feature -> reporting (a parte descritiva do case)."""

from __future__ import annotations

import pandas as pd


def calcular_receita_mensal(tabela_analitica: pd.DataFrame) -> pd.DataFrame:
    """Receita paga, somada por mês de compra."""
    df = tabela_analitica.copy()
    df["mes"] = df["order_purchase_timestamp"].dt.to_period("M").astype(str)
    return (
        df.groupby("mes")["valor_pago"]
        .sum()
        .round(2)
        .reset_index()
        .rename(columns={"valor_pago": "receita_total"})
        .sort_values("mes")
    )


def calcular_top_categorias(tabela_analitica: pd.DataFrame, params: dict) -> pd.DataFrame:
    """As N categorias de produto com maior receita em itens."""
    n = params.get("relatorio", {}).get("top_n_categorias", 10)
    return (
        tabela_analitica.groupby("categoria")["valor_itens"]
        .sum()
        .round(2)
        .sort_values(ascending=False)
        .head(n)
        .reset_index()
        .rename(columns={"valor_itens": "receita_itens"})
    )


def calcular_taxa_review_por_estado(tabela_analitica: pd.DataFrame) -> pd.DataFrame:
    """Percentual de pedidos com review ruim, por estado do cliente."""
    return (
        tabela_analitica.groupby("customer_state")
        .agg(taxa_review_ruim=("review_ruim", "mean"), n_pedidos=("order_id", "count"))
        .assign(taxa_review_ruim=lambda d: (d["taxa_review_ruim"] * 100).round(1))
        .sort_values("taxa_review_ruim", ascending=False)
        .reset_index()
    )
