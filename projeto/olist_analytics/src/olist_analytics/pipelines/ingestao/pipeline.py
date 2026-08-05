"""Pipeline de ingestão: 8 tabelas brutas -> 8 tabelas intermediárias."""

from __future__ import annotations

from kedro.pipeline import Pipeline, node

from . import nodes


def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline(
        [
            node(
                func=nodes.limpar_pedidos,
                inputs="olist_pedidos_raw",
                outputs="pedidos_limpos",
                name="limpar_pedidos",
            ),
            node(
                func=nodes.filtrar_pedidos_por_periodo,
                inputs=["pedidos_limpos", "parameters"],
                outputs="pedidos_filtrados",
                name="filtrar_pedidos_por_periodo",
            ),
            node(
                func=nodes.limpar_itens,
                inputs="olist_itens_raw",
                outputs="itens_limpos",
                name="limpar_itens",
            ),
            node(
                func=nodes.agregar_pagamentos,
                inputs="olist_pagamentos_raw",
                outputs="pagamentos_agregados",
                name="agregar_pagamentos",
            ),
            node(
                func=nodes.limpar_avaliacoes,
                inputs="olist_avaliacoes_raw",
                outputs="avaliacoes_limpas",
                name="limpar_avaliacoes",
            ),
            node(
                func=nodes.limpar_clientes,
                inputs="olist_clientes_raw",
                outputs="clientes_limpos",
                name="limpar_clientes",
            ),
            node(
                func=nodes.traduzir_categorias,
                inputs=["olist_produtos_raw", "olist_traducao_categorias_raw"],
                outputs="produtos_traduzidos",
                name="traduzir_categorias",
            ),
            node(
                func=nodes.limpar_vendedores,
                inputs="olist_vendedores_raw",
                outputs="vendedores_limpos",
                name="limpar_vendedores",
            ),
        ]
    )
