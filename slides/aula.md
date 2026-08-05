---
marp: true
theme: imersao
paginate: true
size: 16:9
footer: 'Imersão Kedro · MBA Business Analytics'
---

<!-- _class: capa -->

# Kedro na prática
## De um script frágil a um mapa navegável

Estruturando projetos de dados que sobrevivem ao time que os escreveu

---

# Combinados

- Sessão de **3h**, gravada — o link fica disponível depois
- Pergunte a qualquer momento, pelo chat — não precisa esperar
- 2 pausas de 10 min, já marcadas na agenda
- Vocês **não vão codar** — é 100% demonstração

<p class="impacto">Ao final, vocês saem sabendo o que é, pra que serve, e quando vale a pena — não como escrever um.</p>

---

# Antes de começar

**Enquete:** quantos aqui já perderam uma análise porque não sabiam qual era
a versão certa da planilha ou do dado?

*(respondam no chat ou na enquete do Meet)*

---

# Agenda de hoje

1. O problema — 25 min
2. O que é Kedro — 15 min
3. Anatomia do projeto + Catálogo — 25 min
4. **Pausa** — 10 min
5. Nós, Pipelines e Parâmetros — 30 min
6. Kedro-Viz — 30 min
7. **Pausa** — 10 min
8. Hooks + Encerramento — 25 min

---

# Uma análise comum

- O Ricardo, da diretoria, pediu um número pra reunião de terça
- Alguém do time abriu um notebook, escreveu um script, mandou o Excel
- Funcionou. A reunião aconteceu.
- Três meses depois, alguém precisa do mesmo número — atualizado

<p class="impacto">A pergunta que decide se um time de dados escala: dá pra refazer isso sem a pessoa que escreveu?</p>

---

<!-- _class: demo -->

<p class="rotulo">DEMO</p>

# Rodando o script real

```bash
cd antes
python analise_olist.py
```

*(trocar para o terminal)*

---

# Dor #1 — o caminho quebrado

```python
PASTA = "C:/Users/everton/Downloads/olist/"
```

- Funcionou na máquina de quem escreveu
- Na sua, `FileNotFoundError`
- Reproduzir a análise = editar código

---

# Dor #2 — regras de negócio espalhadas

O ano da análise, o corte de frete, o que conta como "cliente insatisfeito"
— cada um **repetido em pelo menos 4 lugares** do arquivo.

- Mudar um critério = caçar linha por linha
- Fácil esquecer um lugar
- Ninguém documenta *por que* aquele número foi escolhido

---

# Dor #3 — tudo em sequência

```python
# descomentar pra rodar o modelo
# df_modelo = df_final2.dropna(...)
```

- Nenhuma função no arquivo inteiro
- Pra rodar só uma parte, roda tudo de novo
- Quem escreveu sabia do problema — não teve tempo de resolver

---

# Dor #4 — de onde veio esse número?

```
taxa_ruim  ←  df_final_v2  ←  df_final2  ←  df_final  ←  df3  ←  df.merge(df2, ...)
```

- O número que vai pro slide da diretoria
- Vem de uma cadeia de nomes genéricos
- Ninguém responde "de onde veio" sem ler o arquivo inteiro de trás pra frente

---

<!-- _class: ancora -->

# As 4 dores de hoje

1. Caminho de arquivo quebrado
2. Regras de negócio espalhadas
3. Tudo em sequência, nada seletivo
4. Origem do número ilegível

*Vamos voltar aqui a cada uma resolvida.*

---

# O que é Kedro

> Um framework Python de código aberto para **estruturar** projetos de dados

Não processa dado sozinho — organiza como seu código:
- acessa dado
- se divide em etapas
- se configura

---

# De onde vem

- 2019 — criado pela QuantumBlack (McKinsey) como ferramenta interna
- Jan/2022 — doado à **Linux Foundation** (LF AI & Data)
- Hoje: comunidade aberta, não depende de um fornecedor só

<p class="impacto">Não é aposta em fornecedor — é padrão aberto, mantido por uma fundação.</p>

---

# Onde o Kedro se encaixa

| Ferramenta | Papel |
|---|---|
| **Kedro** | organiza o código Python entre as etapas |
| dbt | transformação em SQL, dentro do warehouse |
| Airflow | agenda e executa em produção |
| MLflow | rastreia experimentos de modelo |

*Não competem — cada um cuida de uma parte.*

---

# O que Kedro não é

- Não é banco de dados
- Não é ferramenta de BI
- Não substitui a análise em si — organiza o código que a prepara

---

# Os 4 conceitos que sustentam tudo

| Conceito | Resolve |
|---|---|
| **Catálogo** | dor #1 — onde está o dado |
| **Nó + Pipeline** | dor #3 — execução seletiva |
| **Configuração** | dor #2 — regras fora do código |
| **Kedro-Viz** | dor #4 — de onde veio o número |

---

<!-- _class: demo -->

<p class="rotulo">DEMO</p>

# Anatomia de um projeto Kedro

```bash
cd projeto/olist_analytics
ls
```

`conf/` · `src/olist_analytics/` · `data/`

---

# Camadas de dados

```
01_raw → 02_intermediate → 03_primary → 04_feature
       → 05_model_input → 06_models → 08_reporting
```

- Convenção do Kedro — mesma lógica do Medallion/Lakehouse
- Dado bruto nunca se mistura com dado tratado

<p class="impacto">Qualquer pessoa nova no time sabe onde procurar, sem perguntar.</p>

---

<!-- _class: demo -->

<p class="rotulo">DEMO</p>

# O Data Catalog

```bash
cat conf/base/catalog.yml
kedro catalog describe-datasets
```

Trocar formato de saída — CSV → Excel — editando só o YAML

---

# Antes e depois

```python
# antes — 8 linhas assim, caminho fixo
df = pd.read_csv("C:/Users/.../orders.csv")
```

```yaml
# depois — um nome, um lugar, um formato
olist_pedidos_raw:
  type: pandas.CSVDataset
  filepath: data/01_raw/olist_orders_dataset.csv
```

<p class="impacto">O node nem sabe de onde o dado vem — só usa o nome.</p>

---

<!-- _class: ancora -->

# Dor #1 — resolvida

<p class="dor-resolvida">1. Caminho de arquivo quebrado</p>

2. Regras de negócio espalhadas
3. Tudo em sequência, nada seletivo
4. Origem do número ilegível

---

<!-- _class: pausa -->

# Pausa — 10 min

---

<!-- _class: demo -->

<p class="rotulo">DEMO</p>

# Decompondo o script em nós

```bash
kedro run --pipeline=features
kedro run --from-nodes=calcular_receita_mensal
```

Cada função: uma entrada, uma saída, um nome

---

# Execução seletiva

- `--pipeline=<nome>` roda só um grupo de etapas
- `--from-nodes=<nó>` roda a partir dali — sem reprocessar o que já existe
- `--to-nodes=<nó>` roda só até ali

<p class="impacto">O bloco comentado "descomentar pra rodar o modelo" do script antigo — isso resolve aquilo.</p>

---

<!-- _class: ancora -->

# Dor #3 — resolvida

<p class="dor-resolvida">1. Caminho de arquivo quebrado</p>

2. Regras de negócio espalhadas
<p class="dor-resolvida">3. Tudo em sequência, nada seletivo</p>

4. Origem do número ilegível

---

<!-- _class: demo -->

<p class="rotulo">DEMO</p>

# Um critério de negócio, dois cenários

```yaml
analise:
  nota_corte_review_ruim: 2   # → 3
```

```bash
kedro run --pipeline=relatorio
```

*Mudar uma linha, recalcular o relatório inteiro.*

---

# Configuração fora do código

- Toda decisão de negócio vive em `parameters.yml`
- Nunca hardcoded dentro de uma função
- Mudar de cenário = editar YAML, não caçar constante

<p class="impacto">O critério de "cliente insatisfeito" fica documentado, versionado, e visível pra qualquer pessoa do time.</p>

---

<!-- _class: ancora -->

# Dor #2 — resolvida

<p class="dor-resolvida">1. Caminho de arquivo quebrado</p>
<p class="dor-resolvida">2. Regras de negócio espalhadas</p>
<p class="dor-resolvida">3. Tudo em sequência, nada seletivo</p>

4. Origem do número ilegível

---

<!-- _class: demo -->

<p class="rotulo">DEMO</p>

# Kedro-Viz

```bash
kedro viz run --autoreload
```

O grafo completo — das 8 tabelas brutas até o modelo

---

# Linhagem de dados

Clicar num número do relatório e **subir até a fonte** — literalmente
clicando, camada por camada.

<p class="impacto">"De onde veio esse número?" deixa de ser uma investigação e vira um clique.</p>

---

<!-- _class: ancora -->

# Dor #4 — resolvida

<p class="dor-resolvida">1. Caminho de arquivo quebrado</p>
<p class="dor-resolvida">2. Regras de negócio espalhadas</p>
<p class="dor-resolvida">3. Tudo em sequência, nada seletivo</p>
<p class="dor-resolvida">4. Origem do número ilegível</p>

**As 4 dores do início, resolvidas.**

---

# O que vocês levam

```bash
kedro viz build
```

Um site estático — o mesmo grafo que vimos agora — publicado, sem precisar
instalar nada pra explorar depois da aula.

---

<!-- _class: demo -->

<p class="rotulo">DEMO</p>

# Quando o dado vem ruim

```yaml
periodo:
  inicio: "2018-08-31"
  fim: "2018-08-31"
```

```bash
kedro run
```

---

# Hooks

- Já apareceu a aula inteira: uma tabela de tempo por nó, depois de cada `kedro run`
- Isso é um **hook** — código que roda automaticamente em pontos da execução
- Agora: um hook que **impede** um relatório vazio de ser gerado

<p class="impacto">Dado ruim não chega no relatório da diretoria — sem precisar lembrar de validar manualmente.</p>

---

# Em produção

- Container **Docker** empacota o projeto
- **Airflow** (ou similar) agenda a execução
- **MLflow** registra experimentos de modelo

*Não muda a estrutura que vocês viram hoje — só onde ela roda.*

---

# O argumento econômico

- Pessoa nova entende a estrutura em horas, não em dias lendo 200 linhas
- Se quem escreveu sai da empresa, o projeto continua legível
- Erro de dado é pego antes de virar decisão errada

<p class="impacto">O ganho não é técnico — é de continuidade do time.</p>

---

# Quando não vale a pena

- Exploração rápida, de uma pessoa só, que não vai durar
- Protótipo descartável

*O Kedro compensa quando o projeto vai durar e/ou ser compartilhado.*

---

# Créditos e recursos

Dataset: *Brazilian E-Commerce Public Dataset by Olist (Kaggle),
CC BY-NC-SA 4.0*

- Documentação oficial: docs.kedro.org
- Repositório desta imersão: (link no chat)
- Kedro-Viz publicado: (link no chat)

---

<!-- _class: capa -->

# Obrigado

Perguntas? O chat está aberto.

Material completo e link do Kedro-Viz publicado: ver chat.
