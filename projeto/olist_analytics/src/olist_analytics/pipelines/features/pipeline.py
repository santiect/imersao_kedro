"""Pipeline de features: encadeia as 4 variáveis do case."""

from __future__ import annotations

from kedro.pipeline import Pipeline, node

from . import nodes


def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline(
        [
            node(
                func=nodes.calcular_prazo_entrega,
                inputs="pedidos_enriquecidos",
                outputs="pedidos_com_prazo",
                name="calcular_prazo_entrega",
            ),
            node(
                func=nodes.calcular_atraso,
                inputs="pedidos_com_prazo",
                outputs="pedidos_com_atraso",
                name="calcular_atraso",
            ),
            node(
                func=nodes.calcular_peso_frete,
                inputs=["pedidos_com_atraso", "parameters"],
                outputs="pedidos_com_frete",
                name="calcular_peso_frete",
            ),
            node(
                func=nodes.montar_tabela_analitica,
                inputs=["pedidos_com_frete", "parameters"],
                outputs="tabela_analitica",
                name="montar_tabela_analitica",
            ),
        ]
    )
