# olist_analytics

Projeto Kedro de demonstração da **Imersão Kedro** (2 encontros de 3h, MBA em
Business Analytics). Caso de negócio: *o que faz um cliente do marketplace
Olist dar nota baixa?*

Contexto completo em [`../../PLANO.md`](../../PLANO.md). Este README cobre só
o "como rodar".

## Instalar

A partir da raiz do repositório (não daqui):

```bash
source ../../.venv/bin/activate   # ver ../../ambiente/setup.md
```

## Dados

Este projeto não traz dados — nem brutos, nem amostra (ver
[`PLANO.md` §3.0](../../PLANO.md)). Antes de rodar:

```bash
# a partir da raiz do repositório
python dados/preparar_amostra.py
```

## Rodar o pipeline completo

```bash
kedro run
```

Rodar só um pipeline nomeado:

```bash
kedro run --pipeline=relatorio
```

Rodar a partir de um nó específico (útil depois de mexer só na modelagem):

```bash
kedro run --from-nodes=dividir_treino_teste
```

## Ver o grafo (Kedro-Viz)

```bash
kedro viz run
kedro viz run --autoreload   # o grafo se atualiza ao salvar um node
kedro viz build              # gera site estático em build/
```

## Explorar interativamente

A ferramenta principal é o REPL de terminal do Kedro:

```bash
kedro ipython
```

Carrega `catalog`, `context`, `session` e `pipelines` no escopo. Exemplo:
```python
catalog.load("tabela_analitica").head()
```

### Notebook (opcional, só para visualização)

Existe um único notebook, `notebooks/explorar_catalogo.ipynb`, para quando
tabela formatada ou gráfico inline ajudam mais que o terminal — não guarda
nenhuma lógica de pipeline, só lê o catálogo.

```bash
kedro jupyter notebook
```

⚠️ **Nunca commitar esse notebook com output executado** — a saída de
`catalog.load()` é dado real do Olist (ver `PLANO.md` §3.0 sobre a licença).
Antes de qualquer commit:
```bash
jupyter nbconvert --clear-output --inplace notebooks/explorar_catalogo.ipynb
```

## Testes

```bash
pytest
```

## Estrutura

| Camada | Pasta | Conteúdo |
|---|---|---|
| raw | `data/01_raw/` | os 8 CSVs do Olist |
| intermediate | `data/02_intermediate/` | uma tabela limpa por tabela de origem |
| primary | `data/03_primary/` | `pedidos_enriquecidos` — a tabela-verdade |
| feature | `data/04_feature/` | `tabela_analitica` — com o alvo `review_ruim` |
| model_input | `data/05_model_input/` | treino e teste |
| models | `data/06_models/` | modelo treinado (pickle) |
| reporting | `data/08_reporting/` | saídas para consumo humano |

Pipelines em `src/olist_analytics/pipelines/`: `ingestao`, `integracao`,
`features`, `relatorio`, `modelagem`. Cada um em seu diretório com `nodes.py`
e `pipeline.py`.

## Parâmetros

Toda decisão de negócio (período de análise, corte de nota, corte de frete,
proporção de teste) vive em `conf/base/parameters.yml` — nunca no código. É a
demonstração central da imersão: comparar dois cenários é editar uma linha de
YAML, não caçar uma constante espalhada pelo código.

## Hooks

`src/olist_analytics/hooks.py`: um relatório de tempo por nó, e uma validação
de qualidade de dados que barra a execução se a tabela analítica vier
inconsistente. Ver `PLANO.md` §5.5 para a demo de falha proposital.

`kedro-mlflow` está instalado mas com o hook **desativado por padrão**
(`DISABLE_HOOKS_FOR_PLUGINS` em `settings.py`) — ver o comentário lá para o
porquê. É reativado só para a demo pontual de rastreio de experimentos.
