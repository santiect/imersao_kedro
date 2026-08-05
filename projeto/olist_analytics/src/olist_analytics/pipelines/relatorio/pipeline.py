"""Pipeline de relatório: as 3 saídas descritivas do Encontro 1."""

from __future__ import annotations

from kedro.pipeline import Pipeline, node

from . import nodes


def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline(
        [
            node(
                func=nodes.calcular_receita_mensal,
                inputs="tabela_analitica",
                outputs="receita_mensal",
                name="calcular_receita_mensal",
            ),
            node(
                func=nodes.calcular_top_categorias,
                inputs=["tabela_analitica", "parameters"],
                outputs="top_categorias",
                name="calcular_top_categorias",
            ),
            node(
                func=nodes.calcular_taxa_review_por_estado,
                inputs="tabela_analitica",
                outputs="review_por_estado",
                name="calcular_taxa_review_por_estado",
            ),
        ]
    )
