"""Pipeline de modelagem: split -> treino -> avaliação -> importância."""

from __future__ import annotations

from kedro.pipeline import Pipeline, node

from . import nodes


def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline(
        [
            node(
                func=nodes.dividir_treino_teste,
                inputs=["tabela_analitica", "parameters"],
                outputs=["dados_treino", "dados_teste"],
                name="dividir_treino_teste",
            ),
            node(
                func=nodes.treinar_modelo,
                inputs=["dados_treino", "parameters"],
                outputs="modelo_review_ruim",
                name="treinar_modelo",
            ),
            node(
                func=nodes.avaliar_modelo,
                inputs=["modelo_review_ruim", "dados_teste"],
                outputs="metricas_modelo",
                name="avaliar_modelo",
            ),
            node(
                func=nodes.calcular_importancia_features,
                inputs=["modelo_review_ruim", "dados_treino"],
                outputs="importancia_features",
                name="calcular_importancia_features",
            ),
        ]
    )
