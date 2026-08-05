"""Pipeline de integração: junta as tabelas intermediárias na tabela primária."""

from __future__ import annotations

from kedro.pipeline import Pipeline, node

from . import nodes


def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline(
        [
            node(
                func=nodes.montar_pedidos_enriquecidos,
                inputs=[
                    "pedidos_filtrados",
                    "itens_limpos",
                    "pagamentos_agregados",
                    "avaliacoes_limpas",
                    "clientes_limpos",
                    "produtos_traduzidos",
                    "vendedores_limpos",
                ],
                outputs="pedidos_enriquecidos",
                name="montar_pedidos_enriquecidos",
            ),
        ]
    )
