---
title: Kedro — Cheatsheet
---

# Kedro — Cheatsheet da Imersão

*Brazilian E-Commerce Public Dataset by Olist (Kaggle), CC BY-NC-SA 4.0*

## Os 4 conceitos

| Conceito | O que é | Resolve |
|---|---|---|
| **Catálogo** (`catalog.yml`) | mapa de nome → dataset (arquivo, formato, local) | não precisar de caminho fixo no código |
| **Nó** (`node`) | uma função Python, com nome, entrada e saída | uma unidade de trabalho testável e reaproveitável |
| **Pipeline** | nós encadeados em grafo | rodar só a parte que interessa, sem reprocessar tudo |
| **Parâmetros** (`parameters.yml`) | decisões de negócio fora do código | mudar um critério sem editar função |

## Estrutura de um projeto

```
conf/base/catalog.yml       # onde estão os dados
conf/base/parameters.yml    # decisões de negócio
conf/local/                 # credenciais — nunca vai pro git
data/01_raw .. 08_reporting # dado por camada
src/<pacote>/pipelines/     # um subpasta por pipeline nomeado
```

## As 7 camadas de dados

| # | Camada | Conteúdo típico |
|---|---|---|
| 1 | `raw` | dado bruto, como chegou |
| 2 | `intermediate` | limpo e tipado |
| 3 | `primary` | a tabela-verdade do negócio |
| 4 | `feature` | variáveis derivadas |
| 5 | `model_input` | treino / teste |
| 6 | `models` | modelo treinado |
| 7 | `reporting` | saída para consumo humano |

## Comandos essenciais

| Comando | O que faz |
|---|---|
| `kedro run` | roda o pipeline completo |
| `kedro run --pipeline=<nome>` | roda só um pipeline nomeado |
| `kedro run --from-nodes=<nó>` | roda a partir de um nó (input precisa estar persistido) |
| `kedro run --to-nodes=<nó>` | roda só até um nó |
| `kedro viz run` | abre o grafo visual do projeto |
| `kedro viz run --autoreload` | grafo se atualiza ao salvar o código |
| `kedro viz build` | gera site estático do grafo |
| `kedro catalog describe-datasets` | lista os datasets do catálogo |
| `kedro ipython` | REPL de terminal com `catalog`, `context`, `session` carregados — a ferramenta **principal** de exploração |
| `kedro jupyter notebook` | abre notebook com o mesmo `catalog` carregado — uso **opcional**, só para tabela formatada/gráfico |

## Vocabulário mínimo

- **DAG** — grafo sem ciclos; é a forma do pipeline
- **Linhagem** — o caminho de um dado, da fonte até o relatório
- **Hook** — código que roda automaticamente em pontos da execução (ex.: validar dado antes de salvar)
- **Dataset versionado** — cada execução grava uma cópia nova, sem sobrescrever a anterior
