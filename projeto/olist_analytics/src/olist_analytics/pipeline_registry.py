"""Project pipelines."""
from __future__ import annotations

from kedro.pipeline import Pipeline

from olist_analytics.pipelines import features, ingestao, integracao, modelagem, relatorio


def register_pipelines() -> dict[str, Pipeline]:
    """Register the project's pipelines.

    Cada pipeline é importada explicitamente (em vez de descoberta automática
    via ``find_pipelines``) para deixar claro, na leitura do arquivo, quais
    etapas compõem o projeto e em que ordem elas aparecem no grafo.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """
    pipelines = {
        "ingestao": ingestao.create_pipeline(),
        "integracao": integracao.create_pipeline(),
        "features": features.create_pipeline(),
        "modelagem": modelagem.create_pipeline(),
        "relatorio": relatorio.create_pipeline(),
    }
    pipelines["__default__"] = sum(pipelines.values())
    return pipelines
