"""Nós de feature engineering: primary -> feature.

As quatro variáveis calculadas aqui (prazo, atraso, % de frete, e o alvo
review_ruim) são exatamente as que sustentam o case da imersão: "o que faz um
cliente do marketplace dar nota baixa?".
"""

from __future__ import annotations

import logging

import pandas as pd

logger = logging.getLogger(__name__)


def calcular_prazo_entrega(pedidos_enriquecidos: pd.DataFrame) -> pd.DataFrame:
    """Dias entre a compra e a entrega ao cliente."""
    df = pedidos_enriquecidos.copy()
    df["prazo_entrega_dias"] = (
        df["order_delivered_customer_date"] - df["order_purchase_timestamp"]
    ).dt.days
    return df


def calcular_atraso(df: pd.DataFrame) -> pd.DataFrame:
    """Dias de atraso: entrega real menos estimada. Negativo = entregue antes."""
    df = df.copy()
    df["atraso_dias"] = (
        df["order_delivered_customer_date"] - df["order_estimated_delivery_date"]
    ).dt.days
    return df


def calcular_peso_frete(df: pd.DataFrame, params: dict) -> pd.DataFrame:
    """Frete como percentual do valor dos itens; descarta outliers acima do corte."""
    df = df.copy()
    df["frete_percentual"] = df["frete_total"] / df["valor_itens"]

    corte = params["analise"]["frete_percentual_maximo"]
    antes = len(df)
    df = df[df["frete_percentual"] <= corte].copy()
    logger.info(
        "Corte de frete (%.0f%%): %d de %d pedidos mantidos", corte * 100, len(df), antes
    )
    return df


def montar_tabela_analitica(df: pd.DataFrame, params: dict) -> pd.DataFrame:
    """Fecha a tabela analítica: aplica regras de negócio e cria o alvo.

    Regras aplicadas, todas configuráveis em parameters.yml (nunca no código):
    - inclui ou não pedidos cancelados;
    - considera apenas pedidos entregues (a satisfação pós-entrega não faz
      sentido para um pedido que não chegou);
    - define o corte de nota que caracteriza "cliente insatisfeito".
    """
    df = df.copy()

    if not params["analise"]["incluir_pedidos_cancelados"]:
        df = df[df["order_status"] != "canceled"]

    df = df[df["order_status"] == "delivered"]
    df = df.dropna(subset=["review_score"])

    corte_nota = params["analise"]["nota_corte_review_ruim"]
    df["review_ruim"] = (df["review_score"] <= corte_nota).astype(int)

    colunas = [
        "order_id",
        "customer_state",
        "categoria",
        "order_purchase_timestamp",
        "prazo_entrega_dias",
        "atraso_dias",
        "frete_percentual",
        "n_itens",
        "valor_itens",
        "valor_pago",
        "review_score",
        "review_ruim",
    ]
    tabela = df[colunas].copy()
    logger.info(
        "tabela_analitica: %d pedidos, taxa de review ruim = %.1f%%",
        len(tabela),
        tabela["review_ruim"].mean() * 100,
    )
    return tabela
