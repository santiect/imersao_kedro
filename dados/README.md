# Dados — Brazilian E-Commerce Public Dataset by Olist

## Sobre a licença, antes de tudo

Este dataset é distribuído sob **CC BY-NC-SA 4.0**: atribuição obrigatória
(**BY**), uso não comercial (**NC**), compartilhamento pela mesma licença de
qualquer derivado que seja distribuído (**SA**).

Duas coisas são bem diferentes perante essa licença:

- **Usar os dados numa aula** — abrir na tela, rodar um pipeline, mostrar um
  gráfico — é uso, não redistribuição. É exatamente o uso para o qual um
  dataset público de Kaggle existe.
- **Publicar os dados (ou uma amostra deles) num repositório** é distribuir
  uma obra derivada, e aí as três letras da licença valem por inteiro.

Por isso a regra deste projeto é simples: **nenhum arquivo de dado é
versionado, em hipótese alguma.** `dados/raw/` e as pastas de dados do projeto
Kedro estão no `.gitignore`, com bloqueio duplo (por pasta e por extensão).
Os alunos não executam nada — eles não precisam dos arquivos, só do que é
gerado *a partir* deles na tela do instrutor. Detalhes em
[PLANO.md §3.0](../PLANO.md).

**Atribuição usada em todo o material:**
> Brazilian E-Commerce Public Dataset by Olist (Kaggle), CC BY-NC-SA 4.0.

⚠️ Confira a licença atual no bloco "License" da própria página do Kaggle antes
da produção final do material — este texto foi escrito a partir do
conhecimento prévio do autor, não de leitura automatizada da página.

## Como baixar

1. Acesse `https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce`
   (requer conta Kaggle logada).
2. Clique em **Download** — baixa um único `.zip` com os 9 CSVs.
3. Descompacte **todos os arquivos soltos**, sem subpastas, dentro de:
   ```
   dados/raw/
   ```

## Tabelas do dataset

| Arquivo | Conteúdo | Uso no projeto |
|---|---|---|
| `olist_orders_dataset.csv` | Pedidos, com as datas do ciclo de entrega | tabela central |
| `olist_order_items_dataset.csv` | Itens de cada pedido, preço e frete | usado |
| `olist_order_payments_dataset.csv` | Forma e parcelamento de pagamento | usado |
| `olist_order_reviews_dataset.csv` | Nota (1–5) e comentário do cliente | usado — é a base do alvo do modelo |
| `olist_customers_dataset.csv` | Cliente, cidade, estado | usado |
| `olist_products_dataset.csv` | Produto, categoria, dimensões | usado |
| `olist_sellers_dataset.csv` | Vendedor e localização | usado |
| `product_category_name_translation.csv` | Categoria de produto, português → inglês | usado |
| `olist_geolocation_dataset.csv` | CEP → latitude/longitude | **descartado** — ~1 milhão de linhas, mais da metade do peso do dataset, e não entra no case. A própria decisão de excluí-lo é um bom momento de aula sobre escopo |

## Depois de baixar

Rode o script que gera a amostra usada nas demos:

```bash
python dados/preparar_amostra.py
```

Ele lê de `dados/raw/`, filtra o período de 2017-01-01 a 2018-08-31, descarta
`geolocation`, e escreve o resultado em
`projeto/olist_analytics/data/01_raw/`. Essa amostra existe **só na sua
máquina** — nunca é commitada.
