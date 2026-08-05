"""Testes dos 4 nós de features — cobertura mínima, para a demo de testes.

Existem para o slide "testes automatizados" do Encontro 2 (5 min, menção), não
para cobertura exaustiva.
"""

from __future__ import annotations

import pandas as pd
import pytest

from olist_analytics.pipelines.features.nodes import (
    calcular_atraso,
    calcular_peso_frete,
    calcular_prazo_entrega,
    montar_tabela_analitica,
)


@pytest.fixture
def pedidos_enriquecidos() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "order_id": ["p1", "p2", "p3"],
            "order_status": ["delivered", "delivered", "canceled"],
            "customer_state": ["SP", "RJ", "SP"],
            "categoria": ["moveis", "eletronicos", "moveis"],
            "order_purchase_timestamp": pd.to_datetime(
                ["2017-03-01", "2017-03-05", "2017-03-10"]
            ),
            "order_delivered_customer_date": pd.to_datetime(
                ["2017-03-10", "2017-03-20", pd.NaT]
            ),
            "order_estimated_delivery_date": pd.to_datetime(
                ["2017-03-15", "2017-03-12", "2017-03-25"]
            ),
            "valor_itens": [100.0, 200.0, 50.0],
            "frete_total": [10.0, 150.0, 5.0],
            "n_itens": [1, 2, 1],
            "valor_pago": [110.0, 350.0, 55.0],
            "review_score": [5, 1, 3],
        }
    )


def test_calcular_prazo_entrega(pedidos_enriquecidos):
    resultado = calcular_prazo_entrega(pedidos_enriquecidos)
    assert resultado.loc[0, "prazo_entrega_dias"] == 9
    assert resultado.loc[1, "prazo_entrega_dias"] == 15


def test_calcular_atraso(pedidos_enriquecidos):
    com_prazo = calcular_prazo_entrega(pedidos_enriquecidos)
    resultado = calcular_atraso(com_prazo)
    assert resultado.loc[0, "atraso_dias"] == -5  # entregue antes do estimado
    assert resultado.loc[1, "atraso_dias"] == 8  # entregue depois do estimado


def test_calcular_peso_frete_remove_outlier(pedidos_enriquecidos):
    params = {"analise": {"frete_percentual_maximo": 0.5}}
    resultado = calcular_peso_frete(pedidos_enriquecidos, params)
    # pedido p2 tem frete de 150 sobre 200 de item = 75% > 50%, deve sair
    assert "p2" not in resultado["order_id"].values
    assert "p1" in resultado["order_id"].values


def test_montar_tabela_analitica_aplica_regras_de_negocio(pedidos_enriquecidos):
    params = {
        "analise": {
            "nota_corte_review_ruim": 2,
            "incluir_pedidos_cancelados": False,
            "frete_percentual_maximo": 1.0,
        }
    }
    encadeado = calcular_peso_frete(
        calcular_atraso(calcular_prazo_entrega(pedidos_enriquecidos)), params
    )
    resultado = montar_tabela_analitica(encadeado, params)

    # p3 é cancelado -> fora; sobra p1 (nota 5) e p2 (nota 1)
    assert set(resultado["order_id"]) == {"p1", "p2"}
    assert resultado.set_index("order_id").loc["p1", "review_ruim"] == 0
    assert resultado.set_index("order_id").loc["p2", "review_ruim"] == 1
