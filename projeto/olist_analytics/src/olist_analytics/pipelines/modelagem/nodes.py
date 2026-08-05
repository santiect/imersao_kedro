"""Nós de modelagem: feature -> model_input -> models -> reporting.

Modelo simples de propósito (Random Forest sobre 5 variáveis numéricas) — o
objetivo da demo não é acurácia, é mostrar o ciclo split -> treino ->
avaliação dentro da estrutura de pipelines do Kedro.
"""

from __future__ import annotations

import logging

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split

logger = logging.getLogger(__name__)

COLUNAS_FEATURES = [
    "prazo_entrega_dias",
    "atraso_dias",
    "frete_percentual",
    "n_itens",
    "valor_itens",
]
COLUNA_ALVO = "review_ruim"


def dividir_treino_teste(
    tabela_analitica: pd.DataFrame, params: dict
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Separa treino e teste, de forma estratificada pelo alvo."""
    dados = tabela_analitica.dropna(subset=COLUNAS_FEATURES + [COLUNA_ALVO])

    treino, teste = train_test_split(
        dados[COLUNAS_FEATURES + [COLUNA_ALVO]],
        test_size=params["modelo"]["proporcao_teste"],
        random_state=params["modelo"]["semente"],
        stratify=dados[COLUNA_ALVO],
    )
    logger.info("Treino: %d linhas | Teste: %d linhas", len(treino), len(teste))
    return treino, teste


def treinar_modelo(dados_treino: pd.DataFrame, params: dict) -> RandomForestClassifier:
    """Treina um Random Forest para prever review_ruim."""
    X = dados_treino[COLUNAS_FEATURES]
    y = dados_treino[COLUNA_ALVO]

    modelo = RandomForestClassifier(
        n_estimators=params["modelo"]["n_estimadores"],
        random_state=params["modelo"]["semente"],
    )
    modelo.fit(X, y)
    return modelo


def avaliar_modelo(modelo: RandomForestClassifier, dados_teste: pd.DataFrame) -> dict:
    """Métricas do modelo sobre o conjunto de teste."""
    X = dados_teste[COLUNAS_FEATURES]
    y = dados_teste[COLUNA_ALVO]
    y_previsto = modelo.predict(X)

    metricas = {
        "acuracia": round(accuracy_score(y, y_previsto), 4),
        "precisao": round(precision_score(y, y_previsto, zero_division=0), 4),
        "revocacao": round(recall_score(y, y_previsto, zero_division=0), 4),
        "f1": round(f1_score(y, y_previsto, zero_division=0), 4),
        "linhas_teste": len(dados_teste),
    }
    logger.info("Métricas do modelo: %s", metricas)
    return metricas


def calcular_importancia_features(
    modelo: RandomForestClassifier, dados_treino: pd.DataFrame
) -> pd.DataFrame:
    """Quais variáveis mais pesam na previsão — o argumento de negócio do modelo."""
    return pd.DataFrame(
        {
            "variavel": COLUNAS_FEATURES,
            "importancia": modelo.feature_importances_.round(4),
        }
    ).sort_values("importancia", ascending=False)
