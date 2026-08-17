# CLAUDE.md

Orientações para agentes que trabalharem neste repositório.

## O que é este repositório

Material didático de uma **imersão em Kedro**: **1 encontro único de 3h (no
máximo)**, aula remota via Google Meet, para alunos de **MBA em Business
Analytics**.

Não é uma aplicação. É material de ensino. O "produto" são slides, roteiros de
demonstração e um projeto Kedro exemplar que existe **para ser mostrado numa
tela compartilhada**.

Dois documentos governam o trabalho:

- **[PLANO.md](PLANO.md)** — o desenho: público, narrativa, agenda, arquitetura,
  storyboard dos slides. Leia antes de propor qualquer mudança estrutural.
- **[INSTRUCOES-LLM.md](INSTRUCOES-LLM.md)** — a especificação de construção:
  ordem das etapas, requisitos e critérios de aceite de cada artefato.

## Restrições que não se negociam

1. **Os alunos não codificam.** Tudo é demonstração. Não crie exercícios,
   TODOs para o aluno preencher, ou material que pressuponha ambiente instalado
   na máquina deles.
2. **`kedro ipython` é a ferramenta principal de exploração interativa —
   notebook é secundário e opcional.** A crítica ao notebook nesta aula nunca
   foi "notebook é proibido"; é "não construa o projeto inteiro dentro de um
   notebook" (é exatamente o defeito do script em `antes/`, só que em células).
   Uma vez que catálogo, nós, pipelines e parâmetros já existem, um notebook
   que só *lê* o catálogo para visualizar (tabela formatada, gráfico) não tem
   esse problema — não guarda lógica, não precisa ser reproduzido.
   Consequência prática: existe **um único notebook**,
   `projeto/olist_analytics/notebooks/explorar_catalogo.ipynb`, e ele:
   - nunca é commitado com output executado (a saída de `catalog.load()` é
     dado real do Olist — ver regra de licença abaixo). Antes de qualquer
     commit: `jupyter nbconvert --clear-output --inplace
     notebooks/explorar_catalogo.ipynb`.
   - nunca duplica lógica de node — só chama `%load_ext kedro.ipython` e lê
     datasets já prontos.
   - não é mencionado aos alunos como recomendação de fluxo de trabalho — é
     uma curiosidade opcional dentro do bloco do Data Catalog, citada só se
     sobrar tempo.
3. **Português do Brasil em tudo** — texto, comentários, nomes de funções, nós,
   datasets e parâmetros.
4. **Público de negócio, não de engenharia.** Todo conceito técnico fecha com
   uma frase de impacto gerencial. Jargão sem tradução é defeito.
5. **Versões fixadas.** Ver `ambiente/requirements.txt`. Não atualize pacote sem
   perguntar ao usuário.

## Kedro 1.x — armadilhas de API

Este projeto usa **Kedro 1.5**. A maior parte dos tutoriais na web é 0.18/0.19 e
**não roda**. Nunca escreva código Kedro de memória; confirme em
`https://docs.kedro.org/en/stable/`.

Mudanças que mais causam erro:

| Antigo (0.19) | Atual (1.x) |
|---|---|
| `KedroDataCatalog` | `DataCatalog` |
| `kedro.pipeline.modular_pipeline` | tudo em `kedro.pipeline` |
| `Pipeline(pipe=...)` | `Pipeline(nodes=...)` |
| `extra_params` | `runtime_params` |
| `session_id` | `run_id` |
| `--namespace` | `--namespaces` |
| `catalog.list()`, `add_all()`, `add_feed_dict()` | `catalog.filter()`, `catalog.get()` |
| `kedro catalog create` | removido |
| `kedro catalog list` | removido — usar `kedro catalog describe-datasets` |
| `...DataSet` | `...Dataset` |
| `ConfigLoader`, `TemplatedConfigLoader` | `OmegaConfigLoader` |

**Removido do Kedro-Viz 12:** experiment tracking nativo. O caminho atual é o
plugin `kedro-mlflow`.

**`--from-nodes` só funciona se o(s) input(s) do nó estiverem persistidos no
catálogo.** Nós intermediários de `features` (`pedidos_com_prazo`,
`pedidos_com_atraso`, `pedidos_com_frete`) são `MemoryDataset` de propósito —
não sobrevivem entre execuções de `kedro run`. `--from-nodes=<nó que consome
MemoryDataset>` falha com `Pipeline input(s) {...} not found`. Exemplos que
funcionam: `--from-nodes=montar_pedidos_enriquecidos`,
`--from-nodes=calcular_receita_mensal`, `--from-nodes=dividir_treino_teste` —
todos consomem datasets persistidos (Parquet).

**`kedro-mlflow` quebra `kedro run` se ficar com o hook ativo por padrão.**
A partir do MLflow 3.x, o backend de arquivo (`./mlruns`) é recusado por
padrão ("filesystem tracking backend is in maintenance mode"). Como
`kedro-mlflow` se auto-registra via entry point assim que instalado, isso
derruba **qualquer** `kedro run`, mesmo sem nenhum node usando MLflow.
Solução aplicada neste projeto: `DISABLE_HOOKS_FOR_PLUGINS = ("kedro_mlflow",)`
em `settings.py` (nome do pacote com **underscore**, não hífen — é o
`project_name` reportado por `importlib.metadata`, não o nome do PyPI). O
plugin fica desativado o tempo todo na sessão única — vira 1 bullet de
panorama, nunca uma demo ao vivo (ver `PLANO.md` §1.3).

## Estrutura

```
antes/          script monolítico "ruim" — material didático da abertura
projeto/        o projeto Kedro exemplar (olist_analytics)
slides/         Marp, arquivo único (aula.md) — sessão de 3h
roteiros/       script de demo minuto a minuto, para o instrutor
material-aluno/ cheatsheet, glossário, leituras
dados/          instruções de download + gerador da amostra
ambiente/       requirements fixados + guia de instalação
```

## Comandos

```bash
# ambiente
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r ambiente/requirements.txt

# projeto (a partir de projeto/olist_analytics/)
kedro run
kedro run --pipeline=relatorio
kedro run --from-nodes=calcular_receita_mensal   # só funciona com input persistido — ver nota abaixo
kedro viz run
kedro viz run --autoreload
kedro catalog describe-datasets   # "kedro catalog list" não existe mais no 1.x
kedro ipython
kedro jupyter notebook   # opcional/secundário — abre notebooks/explorar_catalogo.ipynb
jupyter nbconvert --clear-output --inplace notebooks/explorar_catalogo.ipynb   # rodar SEMPRE antes de commitar

# slides
npx @marp-team/marp-cli slides/aula.md --pdf --allow-local-files --theme-set slides/tema/imersao.css
```

## Convenções

- **Nós** são funções puras, tipadas, com docstring de uma linha. Sem `print` —
  use `logging.getLogger(__name__)`.
- **Números de negócio** (cortes, períodos, proporções) vivem em
  `parameters.yml`, nunca no código. Isso é um dos 4 argumentos centrais da
  aula (dor #2, ver `PLANO.md` §1.2).
- **Todo dataset do catálogo declara sua camada** em
  `metadata.kedro-viz.layer` — é o que colore o grafo e sustenta a narrativa de
  governança.
- **Comentários em YAML são material de aula**, não ruído: `catalog.yml` e
  `parameters.yml` vão ser projetados na tela e lidos em voz alta.
- **Slides**: máx. 5 linhas de texto, uma ideia por slide, corpo ≥ 24px, tema
  claro (o Meet comprime muito).

## Cuidados

- **Não invente estatísticas do dataset.** Números que forem para o slide
  precisam ter sido calculados sobre a amostra real. Use `{{CALCULAR}}` como
  marcador e reporte as pendências.
- **Não invente URLs.** Verifique antes de citar.
- **Não baixe o dataset** — exige conta Kaggle, a obtenção é manual do usuário.
- **Não faça commit, push, nem publique o Kedro-Viz** sem o usuário pedir.
- Se `INSTRUCOES-LLM.md` conflitar com a documentação oficial do Kedro 1.5, a
  documentação vence — e avise o usuário.

## Dados e licença — regra dura

O dataset Olist é **CC BY-NC-SA 4.0**. *Usar* em aula é tranquilo; *redistribuir*
derivados é que traz obrigações. Como os alunos não executam nada, a política é:

> **Nenhum arquivo de dado entra neste repositório.** Nem bruto, nem amostra,
> nem saída de `reporting`, nem prévia embutida em HTML publicado.

- `dados/raw/` e `projeto/olist_analytics/data/` estão inteiros no `.gitignore`,
  com bloqueio adicional por extensão (`*.csv`, `*.parquet`, `*.xlsx`).
- Verificação, sempre que mexer em algo relacionado:
  ```bash
  git ls-files | grep -iE '\.(csv|parquet|xlsx)$'
  ```
  Tem de vir vazio.
- `dados/preparar_amostra.py` roda **só na máquina do instrutor**, antes da aula.
- **Atribuição obrigatória** no `README.md`, em `material-aluno/leituras.md` e
  num slide de créditos:
  *"Brazilian E-Commerce Public Dataset by Olist (Kaggle), CC BY-NC-SA 4.0."*
- Antes de publicar o Kedro-Viz estático, confirmar que o build **não embute
  prévia de linhas** dos datasets.

Racional completo em [PLANO.md §3.0](PLANO.md).
