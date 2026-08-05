"""
Analise de satisfacao dos clientes - Olist
Pediu o Ricardo (diretoria) pra reuniao de terca

# TODO arrumar isso depois - 2024-08-10
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# caminho dos dados - baixei do kaggle semana passada
PASTA = "C:/Users/everton/Downloads/olist/"

df = pd.read_csv(PASTA + "olist_orders_dataset.csv")
df2 = pd.read_csv(PASTA + "olist_order_items_dataset.csv")
pagamentos = pd.read_csv(PASTA + "olist_order_payments_dataset.csv")
reviews = pd.read_csv(PASTA + "olist_order_reviews_dataset.csv")
clientes = pd.read_csv(PASTA + "olist_customers_dataset.csv")
produtos = pd.read_csv(PASTA + "olist_products_dataset.csv")
vendedores = pd.read_csv(PASTA + "olist_sellers_dataset.csv")
traducao = pd.read_csv(PASTA + "product_category_name_translation.csv")

# só 2017 pra não ficar pesado (ver com o Ricardo se quer 2018 tb)
df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
df = df[df["order_purchase_timestamp"].dt.year == 2017]

df["order_delivered_customer_date"] = pd.to_datetime(df["order_delivered_customer_date"])
df["order_estimated_delivery_date"] = pd.to_datetime(df["order_estimated_delivery_date"])
df["prazo_entrega"] = (df["order_delivered_customer_date"] - df["order_purchase_timestamp"]).dt.days
df["atraso"] = (df["order_delivered_customer_date"] - df["order_estimated_delivery_date"]).dt.days

# junta com item, cliente etc
df3 = df.merge(df2, on="order_id", how="left")
df3 = df3.merge(clientes, on="customer_id", how="left")
df3 = df3.merge(produtos, on="product_id", how="left")
df3 = df3.merge(vendedores, on="seller_id", how="left")
df3 = df3.merge(traducao, on="product_category_name", how="left")

# frete em % do preço - > 50% já é estranho, corta fora
df3["frete_pct"] = df3["freight_value"] / df3["price"]
df3 = df3[df3["frete_pct"] <= 0.5]

# review por pedido (pega o mais recente se tiver mais de um)
reviews["review_creation_date"] = pd.to_datetime(reviews["review_creation_date"])
reviews_ult = reviews.sort_values("review_creation_date").drop_duplicates("order_id", keep="last")

df_final = df3.merge(reviews_ult[["order_id", "review_score"]], on="order_id", how="left")
df_final = df_final.merge(
    pagamentos.groupby("order_id")["payment_value"].sum().reset_index(),
    on="order_id",
    how="left",
)

# nota <= 2 é cliente insatisfeito (combinado com o Ricardo em algum email)
df_final["review_ruim"] = df_final["review_score"] <= 2

# --- receita mensal ---
df_final["mes"] = df_final["order_purchase_timestamp"].dt.to_period("M")
receita_mensal = df_final.groupby("mes")["payment_value"].sum()
print("Receita mensal:")
print(receita_mensal)

# --- top categorias ---
top_categorias = (
    df_final.groupby("product_category_name_english")["price"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)
print("\nTop 10 categorias:")
print(top_categorias)

# --- taxa de review ruim por estado ---
# (tirei os pedidos cancelados manualmente olhando o excel, deve ter uns 200)
df_final2 = df_final[df_final["order_status"] != "canceled"]
taxa_por_estado = df_final2.groupby("customer_state")["review_ruim"].mean().sort_values(ascending=False)
print("\nTaxa de review ruim por estado:")
print(taxa_por_estado)

# ============================================================
# modelo preditivo - comecei mas não terminei, ver com o Bruno
# descomentar pra rodar o modelo
# ============================================================
# df_modelo = df_final2.dropna(subset=["review_ruim", "prazo_entrega", "frete_pct"])
# X = df_modelo[["prazo_entrega", "frete_pct", "atraso"]]
# y = df_modelo["review_ruim"]
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
# modelo = LogisticRegression()
# modelo.fit(X_train, y_train)
# print("Acurácia:", modelo.score(X_test, y_test))

# --- junta tudo pra mandar pro Ricardo ---
# essa parte ficou grande, cuidado pra não rodar 2x sem reiniciar o kernel
resumo_estado = taxa_por_estado.reset_index()
resumo_estado.columns = ["estado", "taxa_review_ruim"]

resumo_categoria = top_categorias.reset_index()
resumo_categoria.columns = ["categoria", "receita_total"]

df_final_v2 = df_final2.copy()
df_final_v2["ano_mes"] = df_final_v2["order_purchase_timestamp"].dt.to_period("M").astype(str)

# taxa geral pra colocar no slide
# (o Ricardo só quer um número, não precisa quebrar por nada)
taxa_ruim = df_final_v2["review_ruim"].mean()
print(f"\nTaxa geral de review ruim: {taxa_ruim:.2%}")

# essa conta bate com o painel? confirmar com o BI antes de mandar
ticket_medio = df_final_v2.groupby("order_id")["payment_value"].first().mean()
print(f"Ticket médio: R$ {ticket_medio:.2f}")

with pd.ExcelWriter("resultado.xlsx") as writer:
    receita_mensal.to_frame("receita").to_excel(writer, sheet_name="receita_mensal")
    resumo_categoria.to_excel(writer, sheet_name="top_categorias", index=False)
    resumo_estado.to_excel(writer, sheet_name="review_por_estado", index=False)

print("\npronto, salvou resultado.xlsx na pasta")

# nota pra próxima vez: separar isso em pedaços, tá difícil de mexer
# ver se dá pra rodar só a parte do modelo sem rodar tudo de novo (demora)
