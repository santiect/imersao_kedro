# Comandos — referência rápida do dia da aula

> Isto é só a sequência de comandos, para consulta rápida enquanto você fala.
> Para o que dizer, perguntas prováveis e o plano B, use
> [`roteiros/aula.md`](aula.md) — este arquivo não substitui aquele.

---

## Antes de ligar a câmera

```bash
cd ~/imersao_kedro
source .venv/bin/activate
cd projeto/olist_analytics

git diff conf/base/parameters.yml conf/base/catalog.yml   # tem que vir vazio
kedro run > /dev/null 2>&1 && echo "pronto pra aula"
```

---

## [0:10–0:35] O problema

```bash
cd ~/imersao_kedro/antes
python analise_olist.py    # falha de propósito — FileNotFoundError
```

*(sem mais comandos neste bloco — o resto é ler o código na tela)*

---

## [0:50–1:15] Anatomia + Data Catalog

```bash
cd ~/imersao_kedro/projeto/olist_analytics
ls
cat conf/base/catalog.yml
kedro catalog describe-datasets
```

**Editar `conf/base/catalog.yml` ao vivo** — bloco `receita_mensal`:
```yaml
# de:
  type: pandas.CSVDataset
  filepath: data/08_reporting/receita_mensal.csv
# para:
  type: pandas.ExcelDataset
  filepath: data/08_reporting/receita_mensal.xlsx
```

```bash
rm -f data/08_reporting/receita_mensal.csv
kedro run --pipeline=relatorio
ls data/08_reporting/ | grep receita
```

**Reverter:**
```bash
git checkout -- conf/base/catalog.yml
rm -f data/08_reporting/receita_mensal.xlsx
kedro run --pipeline=relatorio
```

**`kedro ipython` (2 min):**
```bash
kedro ipython
```
```python
catalog.load("tabela_analitica").head()
exit
```

**Extra opcional (só se sobrar tempo, não orçado):**
```bash
kedro jupyter notebook
```
*(abrir `notebooks/explorar_catalogo.ipynb`, rodar, mostrar tabela + gráfico)*
```bash
# ao terminar, sempre limpar output antes de fechar:
jupyter nbconvert --clear-output --inplace notebooks/explorar_catalogo.ipynb
```

---

## [1:25–1:55] Nodes/Pipelines + Parameters

```bash
kedro run --pipeline=features
kedro run --from-nodes=calcular_receita_mensal
kedro run --to-nodes=limpar_pedidos
```

```bash
cat conf/base/parameters.yml
kedro run --pipeline=relatorio
cat data/08_reporting/review_por_estado.csv | head -6
```

**Editar `conf/base/parameters.yml` ao vivo:**
```yaml
analise:
  nota_corte_review_ruim: 2   # → 3
```

```bash
kedro run --pipeline=relatorio
cat data/08_reporting/review_por_estado.csv | head -6
```

**Reverter:**
```bash
git checkout -- conf/base/parameters.yml
```

---

## [1:55–2:25] Kedro-Viz

```bash
kedro viz run --autoreload
```
*(fica rodando — navegar em `http://127.0.0.1:4141`)*

Ordem no navegador: grafo geral → camadas coloridas → clicar num nó de
`reporting` e subir linhagem → painel de metadados → ramo `modelagem` →
abrir `metricas_modelo.json`.

**Autoreload:** editar docstring de `calcular_prazo_entrega` em
`src/olist_analytics/pipelines/features/nodes.py`, salvar, atualizar o painel
no navegador. Desfazer a edição depois.

**Build estático** (outro terminal):
```bash
cd ~/imersao_kedro/projeto/olist_analytics
kedro viz build
```

---

## [2:35–2:50] Hooks

**Editar `conf/base/parameters.yml` ao vivo:**
```yaml
periodo:
  inicio: "2018-08-31"
  fim: "2018-08-31"
```

```bash
kedro run
# falha de propósito:
# ValueError: Qualidade de dados reprovada em 'tabela_analitica':
#   - apenas 0 linha(s) na tabela analítica (mínimo esperado: 100)
```

**Reverter imediatamente:**
```bash
git checkout -- conf/base/parameters.yml
kedro run > /dev/null 2>&1 && echo "voltou ao normal"
```

---

## Depois que os alunos saírem

```bash
cd ~/imersao_kedro/projeto/olist_analytics
git status
git diff conf/base/parameters.yml conf/base/catalog.yml   # tem que vir vazio
```

Se algo ficou pendurado:
```bash
git checkout -- conf/base/parameters.yml conf/base/catalog.yml
rm -f info.log .coverage data/08_reporting/receita_mensal.xlsx
rm -rf .pytest_cache .viz mlruns
```
