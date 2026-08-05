"""Gera a amostra de dados usada nas demos da imersão.

Roda SÓ na máquina do instrutor, antes da aula. A saída nunca é commitada —
ver dados/README.md e PLANO.md secao 3.0 sobre a licenca CC BY-NC-SA 4.0 do
dataset Olist: usar em aula esta ok, redistribuir no repositorio nao.

Uso:
    python dados/preparar_amostra.py

Le de dados/raw/ (os 9 CSVs baixados do Kaggle) e escreve em
projeto/olist_analytics/data/01_raw/ uma versao filtrada para o periodo de
2017-01-01 a 2018-08-31, sem a tabela de geolocation.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent
ORIGEM = RAIZ / "raw"
DESTINO = RAIZ.parent / "projeto" / "olist_analytics" / "data" / "01_raw"

INICIO_PERIODO = "2017-01-01"
FIM_PERIODO = "2018-08-31"

ARQUIVO_ORDERS = "olist_orders_dataset.csv"
ARQUIVO_ITEMS = "olist_order_items_dataset.csv"
ARQUIVO_PAYMENTS = "olist_order_payments_dataset.csv"
ARQUIVO_REVIEWS = "olist_order_reviews_dataset.csv"
ARQUIVO_CUSTOMERS = "olist_customers_dataset.csv"
ARQUIVO_PRODUCTS = "olist_products_dataset.csv"
ARQUIVO_SELLERS = "olist_sellers_dataset.csv"
ARQUIVO_TRADUCAO = "product_category_name_translation.csv"
ARQUIVO_GEOLOCATION = "olist_geolocation_dataset.csv"  # descartado de propósito


def verificar_origem() -> None:
    if not ORIGEM.exists() or not any(ORIGEM.glob("*.csv")):
        sys.exit(
            "\nNenhum CSV encontrado em dados/raw/.\n"
            "Baixe o dataset do Kaggle e descompacte os arquivos ali antes de "
            "rodar este script. Instruções em dados/README.md.\n"
        )
    esperados = {
        ARQUIVO_ORDERS, ARQUIVO_ITEMS, ARQUIVO_PAYMENTS, ARQUIVO_REVIEWS,
        ARQUIVO_CUSTOMERS, ARQUIVO_PRODUCTS, ARQUIVO_SELLERS, ARQUIVO_TRADUCAO,
    }
    faltando = esperados - {p.name for p in ORIGEM.glob("*.csv")}
    if faltando:
        sys.exit(
            f"\nArquivo(s) ausente(s) em dados/raw/: {', '.join(sorted(faltando))}\n"
            "Confira se o .zip do Kaggle foi descompactado por completo.\n"
        )


def tamanho_mb(caminho: Path) -> float:
    return caminho.stat().st_size / (1024 * 1024)


def relatorio(nome: str, linhas_antes: int, linhas_depois: int, caminho: Path) -> None:
    print(
        f"  {nome:<45} {linhas_antes:>8} -> {linhas_depois:>8} linhas   "
        f"({tamanho_mb(caminho):6.2f} MB)"
    )


def main() -> None:
    verificar_origem()
    DESTINO.mkdir(parents=True, exist_ok=True)

    print(f"Periodo do recorte: {INICIO_PERIODO} a {FIM_PERIODO}\n")
    print("Gerando amostra...")

    orders = pd.read_csv(ORIGEM / ARQUIVO_ORDERS, parse_dates=["order_purchase_timestamp"])
    linhas_orders_antes = len(orders)

    inicio = pd.Timestamp(INICIO_PERIODO)
    fim = pd.Timestamp(FIM_PERIODO)
    mascara_periodo = orders["order_purchase_timestamp"].between(inicio, fim)
    orders = orders[mascara_periodo].copy()

    ids_pedidos = set(orders["order_id"])
    ids_clientes = set(orders["customer_id"])

    items = pd.read_csv(ORIGEM / ARQUIVO_ITEMS)
    linhas_items_antes = len(items)
    items = items[items["order_id"].isin(ids_pedidos)].copy()
    ids_produtos = set(items["product_id"])
    ids_vendedores = set(items["seller_id"])

    payments = pd.read_csv(ORIGEM / ARQUIVO_PAYMENTS)
    linhas_payments_antes = len(payments)
    payments = payments[payments["order_id"].isin(ids_pedidos)].copy()

    reviews = pd.read_csv(ORIGEM / ARQUIVO_REVIEWS)
    linhas_reviews_antes = len(reviews)
    reviews = reviews[reviews["order_id"].isin(ids_pedidos)].copy()

    customers = pd.read_csv(ORIGEM / ARQUIVO_CUSTOMERS)
    linhas_customers_antes = len(customers)
    customers = customers[customers["customer_id"].isin(ids_clientes)].copy()

    products = pd.read_csv(ORIGEM / ARQUIVO_PRODUCTS)
    linhas_products_antes = len(products)
    products = products[products["product_id"].isin(ids_produtos)].copy()

    sellers = pd.read_csv(ORIGEM / ARQUIVO_SELLERS)
    linhas_sellers_antes = len(sellers)
    sellers = sellers[sellers["seller_id"].isin(ids_vendedores)].copy()

    traducao = pd.read_csv(ORIGEM / ARQUIVO_TRADUCAO)  # tabela pequena, mantida inteira

    saidas = [
        (ARQUIVO_ORDERS, orders, linhas_orders_antes),
        (ARQUIVO_ITEMS, items, linhas_items_antes),
        (ARQUIVO_PAYMENTS, payments, linhas_payments_antes),
        (ARQUIVO_REVIEWS, reviews, linhas_reviews_antes),
        (ARQUIVO_CUSTOMERS, customers, linhas_customers_antes),
        (ARQUIVO_PRODUCTS, products, linhas_products_antes),
        (ARQUIVO_SELLERS, sellers, linhas_sellers_antes),
        (ARQUIVO_TRADUCAO, traducao, len(traducao)),
    ]

    total_mb = 0.0
    for nome, df, linhas_antes in saidas:
        caminho = DESTINO / nome
        df.to_csv(caminho, index=False)
        relatorio(nome, linhas_antes, len(df), caminho)
        total_mb += tamanho_mb(caminho)

    print(f"\n  {ARQUIVO_GEOLOCATION:<45} descartado (nao entra no case)")
    print(f"\nTotal da amostra: {total_mb:.2f} MB em {DESTINO}")
    print(
        "\nLembrete: esta amostra e para uso local nas demos. Nunca commitar "
        "(ver .gitignore e PLANO.md secao 3.0)."
    )


if __name__ == "__main__":
    main()
