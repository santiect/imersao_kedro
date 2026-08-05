# Imersão Kedro — Blueprint do Material

> Documento de projeto. Define **o que** será construído e **por quê**, antes de
> qualquer linha de código ou slide. As instruções de execução estão em
> [INSTRUCOES-LLM.md](INSTRUCOES-LLM.md).
>
> **Revisão 2026-08-04:** o formato mudou de 2 encontros de 3h para **1
> encontro único de 3h (no máximo)**. Este documento reflete só a versão
> atual. A estrutura do projeto Kedro (`projeto/olist_analytics/`) não muda —
> só a profundidade e o ritmo da demonstração.

---

## 1. Contexto e restrições

| Item | Definição |
|---|---|
| Público | Alunos de MBA em Business Analytics |
| Perfil técnico | Heterogêneo. Assume-se familiaridade com Excel/SQL/BI e noção de Python. **Não** se assume prática de engenharia de software |
| Formato | Aula remota via Google Meet, **100% demonstração** — alunos apenas assistem |
| Carga | **1 encontro, 3h no máximo** |
| Idioma | Português do Brasil (material e código) |
| Proibido | Jupyter Notebook em qualquer momento. Exploração interativa, quando necessária, usa `kedro ipython` (REPL de terminal) |
| Objetivo pedagógico | Que o aluno saia sabendo **o que é**, **para que serve**, **quando vale a pena** e **como é o dia a dia** de um projeto Kedro — não que saiba escrever um |

### 1.1 Princípio de design da imersão

O aluno é passivo por 3 horas, e 3 horas é pouco tempo para o tanto de
conceito que o Kedro carrega. As regras que governam todas as decisões
abaixo:

1. **Dor antes de solução.** Nenhum recurso do Kedro é apresentado antes de o
   aluno ter visto o problema que ele resolve, rodando e falhando na tela.
2. **Ciclo curto.** Nenhum bloco de terminal passa de ~7 minutos sem voltar
   para um slide de "por que isso importa".
3. **Valor de negócio explícito.** Todo conceito técnico é fechado com uma
   frase de impacto gerencial (custo, risco, governança, tempo de onboarding).
4. **Uma sessão, uma prioridade.** Em 3h só cabe **uma** coisa de verdade: a
   espinha dorsal das 4 dores (§1.2). Tudo que não sustenta essa espinha é
   panorama de 1 slide ou é cortado — nunca um bloco dedicado. Ver §1.3.

### 1.2 A espinha dorsal: 4 dores → 4 respostas

Esta é a estrutura narrativa que sustenta a aula inteira. Todo o material
serve a ela — é o que **não** pode ser cortado quando o tempo apertar.

| # | Dor demonstrada no script "antes" | Resposta do Kedro |
|---|---|---|
| 1 | Caminho de arquivo quebrado; ninguém sabe de onde vem o dado | **Data Catalog** |
| 2 | Mudar o período de análise exige caçar o número em 4 lugares | **Parameters** |
| 3 | Para rodar só uma parte, é preciso reprocessar tudo | **Nodes, Pipelines, `--from-nodes`** |
| 4 | "Esse número no relatório veio de onde?" — ninguém sabe responder | **Kedro-Viz (linhagem)** |

O slide de fechamento do bloco "o problema" apresenta as 4 dores numeradas.
Cada resposta, ao longo da aula, retoma visualmente o número — é o fio que dá
a sensação de unidade numa aula com muito conteúdo técnico em pouco tempo.

### 1.3 O que foi cortado ao ir de 6h para 3h

Registro deliberado, para não perder de vista o que ficou de fora e por quê —
e para poder recolocar se um dia a carga voltar a crescer.

| Cortado / reduzido | De (2×3h) | Para (1×3h) | Critério |
|---|---|---|---|
| `kedro-mlflow` / rastreio de experimentos | Demo dedicada + painel | 1 bullet num slide de "próximos passos" | Não sustenta nenhuma das 4 dores; é evolução, não fundamento |
| Produção (Docker/Airflow/Databricks) | Bloco de 15–20 min | 1 slide panorama | A plateia de MBA precisa saber que existe, não como configurar |
| Modo dev / depuração de nó | Bloco dedicado de 20 min | Uma menção de 2 min dentro do bloco do Catálogo (`kedro ipython`) | Interessa a quem vai codar; a plateia não vai |
| Hooks | Vitrine de 20 min (2 hooks explicados a fundo) | Vitrine de ~15 min, só a demonstração — sem aprofundar a API de hooks | O "dado ruim barra a pipeline" é forte e rápido de mostrar; a mecânica interna não precisa ser ensinada |
| Modelagem preditiva | Bloco dedicado (split, treino, avaliação, importância) | Aparece como saída do pipeline dentro do bloco do Kedro-Viz, sem walkthrough de código | O pipeline `modelagem` continua existindo e rodando — só não vira um bloco de aula em si |
| Retomada entre encontros | 15 min de abertura do Enc. 2 | Eliminado (não há segundo encontro) | — |

O projeto Kedro (`projeto/olist_analytics/`) **mantém os 5 pipelines**
(`ingestao`, `integracao`, `features`, `relatorio`, `modelagem`) e os 2 hooks
já implementados — nada no código precisa mudar. O corte é só de **tempo de
demonstração e de slide**, não de escopo técnico do projeto.

---

## 2. Stack e versões

Verificado em **agosto/2026**. Versões **fixadas** — tutorial desatualizado é o
maior risco técnico de uma aula ao vivo.

| Pacote | Versão | Observação |
|---|---|---|
| Python | 3.12 | Kedro 1.5 suporta 3.10–3.14; 3.12 é o meio-termo estável |
| `kedro` | 1.5.0 | |
| `kedro-viz` | 12.4.0 | |
| `kedro-datasets` | 9.5.0 | instalar com extras `[pandas-csvdataset,pandas-parquetdataset,pandas-exceldataset]` |
| `kedro-mlflow` | 2.0.3 | instalado, mas com hook **desativado por padrão** — ver §2.1.1. Vira 1 bullet de panorama, não demo |
| `scikit-learn`, `pandas`, `pyarrow`, `matplotlib` | livres | fixar no lock |

### 2.1 Diferenças de API do Kedro 1.x que o material DEVE respeitar

Erros comuns de quem aprendeu em tutorial de 0.18/0.19:

- `KedroDataCatalog` → **`DataCatalog`** (a experimental virou a padrão).
- `kedro.pipeline.modular_pipeline` **não existe mais**; tudo vem de
  `kedro.pipeline`. Importar `Node` e `Pipeline` diretamente de `kedro.pipeline`.
- Argumento `pipe=` de `Pipeline(...)` → **`nodes=`**.
- `extra_params` → **`runtime_params`** (sessão, contexto e hooks).
- `session_id` → **`run_id`** em runners e hooks.
- CLI: `--namespace` → **`--namespaces`** (aceita lista separada por vírgula).
- `kedro catalog create` **foi removido**.
- `kedro catalog list` **foi removido** — usar `kedro catalog describe-datasets`
  (confirmado rodando o CLI em 2026-08-04; `kedro catalog --help` lista os
  subcomandos atuais: `describe-datasets`, `list-patterns`, `resolve-patterns`).
- Métodos removidos do catálogo: `_get_dataset()`, `add_all()`, `add_feed_dict()`,
  `list()`, `shallow_copy()`. Usar `catalog.get()` e `catalog.filter()`.
- Classes de dataset terminam em `Dataset`, nunca `DataSet`.

### 2.1.1 Armadilha real encontrada na construção: `kedro-mlflow` quebra `kedro run`

Confirmado em 2026-08-04 ao rodar o projeto de verdade: com MLflow 3.x, o
backend de arquivo (`./mlruns`, o padrão) é **recusado** ("filesystem tracking
backend is in maintenance mode"). Como `kedro-mlflow` se auto-registra como
hook assim que instalado, isso quebra **qualquer** `kedro run` — mesmo sem
nenhum node tocando em MLflow. Resolvido com
`DISABLE_HOOKS_FOR_PLUGINS = ("kedro_mlflow",)` em `settings.py` (o nome usado
é o `project_name` do pacote — **underscore**, não o nome do PyPI com hífen).
Com a sessão única, `kedro-mlflow` vira só uma linha de panorama no slide de
fechamento — nenhuma demo ao vivo depende dele, então esse hook permanece
desativado o tempo todo.

### 2.2 Recursos que NÃO devem entrar

- **Experiment tracking nativo do Kedro-Viz** — depreciado na 11.0, removido na
  12.0. Se citado, é como panorama (`kedro-mlflow`), nunca como demo.
- **`ConfigLoader` / `TemplatedConfigLoader`** — removidos. O padrão é
  `OmegaConfigLoader`.
- Qualquer coisa que dependa de `kedro.extras.datasets`.

---

## 3. Dataset e case

**Olist — E-commerce Brasileiro** (Kaggle, `olistbr/brazilian-ecommerce`).
~100 mil pedidos reais, 2016–2018, 9 CSVs relacionais.

### 3.0 Licença e política de dados

O dataset é **CC BY-NC-SA 4.0**. Três obrigações: atribuição (**BY**), uso não
comercial (**NC**), e derivados distribuídos sob a mesma licença (**SA**).

A distinção que governa este repositório:

| Ato | Situação |
|---|---|
| **Usar** os dados na aula (abrir na tela, rodar pipeline, mostrar gráfico) | Uso, não redistribuição. É o uso para o qual o dataset foi publicado. Risco baixo |
| **Distribuir** amostra ou derivado num repositório público | Obra derivada. BY, NC e SA valem integralmente. É aqui que mora o problema |

**Decisão de projeto: nenhum dado é versionado. Em hipótese alguma.**

Isso é possível porque os alunos não executam nada — eles não precisam dos
arquivos. O que levam para casa é slide, código e o Kedro-Viz estático. Sem dado
no repositório, não há obra derivada distribuída, e a licença deixa de ser uma
restrição operacional.

Consequências práticas:

- `dados/raw/` e `projeto/olist_analytics/data/` ficam **inteiros** no
  `.gitignore`. Inclusive as saídas de `reporting`, que são derivadas.
- O `preparar_amostra.py` roda **só na máquina do instrutor**, antes da aula,
  para alimentar as demos.
- **Atribuição obrigatória** em três lugares: um slide de créditos, o
  `README.md` e `material-aluno/leituras.md`. Texto padrão:
  *"Brazilian E-Commerce Public Dataset by Olist (Kaggle), CC BY-NC-SA 4.0."*
- Antes de publicar o Kedro-Viz estático, **verificar se o build embute prévia
  de linhas dos datasets**. Se embutir, desabilitar o preview — HTML publicado
  com amostra de dados é redistribuição pela porta dos fundos. (Verificado em
  2026-08-04: o build padrão do Kedro-Viz 12.4 **não** embute prévia de linhas,
  só estatísticas agregadas — linhas, colunas, tamanho do arquivo. Reconferir
  se a versão mudar.)
- Sobre o **NC** num MBA pago: zona genuinamente cinzenta, e a Creative Commons
  trata a avaliação como caso a caso, dependente do uso e não de quem usa.
  Ensinar com dataset público não é explorá-lo comercialmente. Se a instituição
  tiver política própria sobre material de terceiros, ela prevalece — e nesse
  caso o plano B é **Online Retail II** (UCI, CC BY 4.0), ver §9.
- A licença acima deve ser **conferida no bloco "License" da página do Kaggle**
  antes da produção final. Não foi possível verificá-la automaticamente (a
  página é renderizada por JavaScript).

### 3.0.1 A amostra

Gerada localmente por `dados/preparar_amostra.py`: recorte de 2017-01-01 a
2018-08-31, sem `geolocation`. Existe para que `kedro run` termine em segundos
ao vivo — não para ser distribuída.

**Nota de calibração (medida em 2026-08-04):** o dataset Olist concentra quase
todos os pedidos em 2017–2018 (apenas 329 de ~99 mil são de 2016), então o
recorte de período reduz pouco o volume — a amostra final fica em ~60 MB, não
nos ~20 MB estimados originalmente. Isso não afeta o repositório (a amostra
nunca é commitada) nem a demo ao vivo (`kedro run` completo mediu 19–23s do
zero). Se quiser reduzir mais, a alavanca certa é amostragem aleatória de
pedidos, não o corte de data.

### 3.1 Pergunta de negócio do case

> **"O que faz um cliente do marketplace dar nota baixa?"**

Numa sessão só, a parte **descritiva** (receita, categorias, prazo de entrega,
taxa de review ruim por estado) recebe o tempo de demonstração. A parte
**preditiva** (o pipeline `modelagem`) aparece como fechamento — o instrutor
mostra que o mesmo pipeline vai até um modelo e suas métricas, dentro do
bloco do Kedro-Viz, sem parar para explicar hiperparâmetro por hiperparâmetro.

Números reais já calculados sobre a amostra completa (ver
`projeto/olist_analytics/data/08_reporting/` após um `kedro run`), prontos
para os slides:

- 80.423 pedidos entregues na tabela analítica
- Modelo: acurácia 0,888 / F1 0,39 — `frete_percentual` e `atraso_dias` são as
  variáveis mais importantes (bom gancho de negócio: "atraso e frete caro
  pesam mais que o valor da compra")

### 3.2 Sujeira útil já presente no dataset

Cada uma vira um momento de demonstração — não são defeitos, são material didático.

| Sujeira | Uso pedagógico |
|---|---|
| Datas como string em todas as tabelas | Justifica a camada `intermediate` |
| `order_delivered_customer_date` nula em pedidos cancelados/em trânsito | Justifica tratamento explícito e um hook de qualidade |
| ~3% dos pedidos sem review | Justifica decisão de negócio documentada em `parameters.yml` |
| Categorias de produto em português, com tabela de tradução separada | Justifica join e a camada `primary` |
| Outliers de frete e de prazo | Justifica parâmetros de corte configuráveis |
| `geolocation` com duplicatas em massa | Justifica descartar a tabela — e discutir custo de processamento |

---

## 4. Arquitetura do repositório

```
imersao_kedro/
├── CLAUDE.md                     # regras para agentes que editarem este repo
├── README.md                     # porta de entrada: o que é, como usar
├── PLANO.md                      # este documento
├── INSTRUCOES-LLM.md             # spec de construção
│
├── dados/
│   ├── README.md                 # como obter o dataset no Kaggle (manual)
│   ├── raw/                      # .gitignore INTEIRO — nunca versionado
│   └── preparar_amostra.py       # roda só na máquina do instrutor
│
├── antes/                        # o "pecado original" — script monolítico
│   ├── analise_olist.py
│   └── README.md                 # o que está errado aqui, e por quê
│
├── projeto/
│   └── olist_analytics/          # projeto Kedro 1.5 completo
│
├── slides/
│   ├── aula.md                   # Marp — sessão única
│   ├── tema/imersao.css
│   └── assets/
│
├── roteiros/
│   ├── aula.md                   # roteiro de demo, minuto a minuto
│   └── plano-b.md                # protocolo de falha ao vivo
│
├── material-aluno/
│   ├── cheatsheet.md             # 1 página, exporta PDF
│   ├── glossario.md              # 20 termos, linguagem de negócio
│   └── leituras.md               # para onde ir depois
│
├── ambiente/
│   ├── requirements.txt          # versões fixadas
│   └── setup.md                  # instalação (para o instrutor)
│
└── .github/workflows/
    └── publicar-viz.yml          # kedro viz build → GitHub Pages
```

### 4.1 Decisões de arquitetura e justificativa

| Decisão | Motivo |
|---|---|
| `antes/` e `projeto/` coexistem no mesmo repo | A comparação lado a lado **é** a aula. Precisam ser abertos simultaneamente no VS Code |
| Slides em **Marp** (Markdown), um arquivo único | Versionado no git, diff legível, exporta PDF e HTML por CLI, sem depender de PowerPoint. Um arquivo só porque agora há um encontro só |
| Roteiro de demo **separado** dos slides | O instrutor lê o roteiro numa segunda tela; os slides vão para o Meet |
| `kedro viz build` publicado no GitHub Pages | Entregável pós-aula que o aluno explora **sem instalar nada**. É o item de maior valor percebido para esse público. Publicar só após checar o preview de dados (§3.0) |
| **Nenhum dado versionado** — nem bruto, nem amostra, nem saída de `reporting` | Resolve a licença CC BY-NC-SA na raiz (§3.0), mantém o repo leve, e o script gerador vira demonstração de reprodutibilidade |
| Sem branches/tags por etapa | Alunos não codificam. Etapas viram **seções do roteiro**, não estados do git |
| Projeto Kedro mantém os 5 pipelines mesmo com menos tempo de demo | O corte de §1.3 é de tempo de aula, não de arquitetura — um material mais completo custa pouco a mais para construir e sobra para quem quiser se aprofundar depois |

---

## 5. Projeto Kedro — desenho detalhado

Nome do pacote: `olist_analytics`.
Criado com `kedro new --tools=log,test,data --example=n`.

### 5.1 Camadas de dados

Convenção oficial Kedro, declarada em `metadata.kedro-viz.layer` no catálogo —
é o que colore o grafo no Kedro-Viz e sustenta o argumento de governança.

| Camada | Conteúdo |
|---|---|
| `raw` | 8 CSVs Olist, imutáveis |
| `intermediate` | Cada tabela limpa e tipada, 1:1 com a origem |
| `primary` | `pedidos_enriquecidos` — a tabela-verdade do negócio |
| `feature` | Variáveis derivadas (prazo, atraso, frete %, nº de itens) |
| `model_input` | Treino e teste separados |
| `models` | Modelo serializado |
| `reporting` | Saídas para consumo humano |

### 5.2 Pipelines

Cinco pipelines nomeados. O registry expõe também o `__default__` compondo todos.

| Pipeline | Camadas | Nós (aprox.) | Papel na sessão única |
|---|---|---|---|
| `ingestao` | raw → intermediate | 8 (um por tabela) | Base do bloco de Catálogo e do bloco de Pipelines |
| `integracao` | intermediate → primary | 1 join central | Mencionado ao passar pelo grafo no Kedro-Viz |
| `features` | primary → feature | 4 | Base do bloco de Nodes/Pipelines (dor #3) |
| `relatorio` | feature → reporting | 3 | Fecha o bloco de Catálogo/Parameters com números na tela |
| `modelagem` | feature → model_input → models → reporting | 4 | Aparece só como saída no bloco do Kedro-Viz — sem walkthrough dedicado |

**Por que 8 nós de ingestão e não 1:** o DAG precisa ser visualmente ramificado.
Um grafo em linha reta destrói o efeito do Kedro-Viz, que é o clímax da aula.
A ramificação também torna `--from-nodes` uma demonstração óbvia.

### 5.3 Nós de `features` (os que sustentam o case)

- `calcular_prazo_entrega` — dias entre compra e entrega
- `calcular_atraso` — entrega real vs. estimada (dias, positivo = atrasado)
- `calcular_peso_frete` — frete como % do valor do pedido
- `montar_tabela_analitica` — consolida + cria o alvo `review_ruim` (nota ≤ 2)

### 5.4 Parâmetros expostos em `parameters.yml`

Escolhidos por serem **decisões de negócio**, não hiperparâmetros técnicos —
isso é o que faz a demo conversar com a plateia de MBA.

```yaml
periodo:
  inicio: "2017-01-01"
  fim: "2018-08-31"
analise:
  nota_corte_review_ruim: 2      # o que conta como "cliente insatisfeito"
  frete_percentual_maximo: 0.5   # corte de outlier
  incluir_pedidos_cancelados: false
modelo:
  proporcao_teste: 0.25
  semente: 42
  n_estimadores: 200
```

**Demo de alto impacto:** rodar a mesma pipeline com `nota_corte_review_ruim`
2 e depois 3, sem tocar em uma linha de código, e mostrar o relatório mudando.
Esta é a demo mais eficiente em tempo×impacto de toda a aula — cabe em ~5 min.

### 5.5 Hooks (vitrine — ~15 min, não seção)

Dois hooks, ambos já implementados em `hooks.py`. Na sessão única, só
**demonstrados**, sem aprofundar a API de hooks em si:

1. **`RelatorioExecucaoHook`** — cronometra cada nó e imprime uma tabela ao
   final de **todo** `kedro run`. Não precisa de tempo dedicado: já aparece
   sozinho em qualquer demo de pipeline anterior — o instrutor só aponta na
   primeira vez que surgir na tela.
2. **`QualidadeDadosHook`** — em `after_dataset_loaded`, valida a tabela
   analítica e **interrompe a execução** ao violar uma regra mínima. Esta é a
   única parte que ganha tempo dedicado (~10 min): o instrutor edita
   `periodo.inicio` e `periodo.fim` em `parameters.yml` para o mesmo dia
   (testado: `"2018-08-31"` nos dois campos → 0 linhas — uma semana inteira
   **não** é suficiente, ainda dá ~223 linhas), roda, e a pipeline para com uma
   mensagem clara. Mensagem de negócio: *"dado ruim não chega no relatório da
   diretoria"*.

### 5.6 Kedro-Viz — o clímax

Sequência de demonstração, nesta ordem — bloco mais longo da aula (~30 min):

1. `kedro viz run` — o grafo completo aparece.
2. Colorir por camada — mostra a arquitetura que os slides descreveram.
3. Clicar num nó de `reporting` e subir a linhagem até o CSV bruto —
   **este é o momento de maior impacto da aula inteira**.
4. Painel de parâmetros e metadados do nó.
5. Apontar o ramo `modelagem` do grafo e abrir `metricas_modelo.json` — é
   aqui que a parte preditiva do case aparece, sem bloco dedicado.
6. `kedro viz run --autoreload` — instrutor edita um nó no VS Code, salva, e o
   grafo se atualiza sozinho na tela.
7. `kedro viz build` — vira site estático; mostrar a URL do GitHub Pages que os
   alunos vão levar para casa.

---

## 6. Agenda — Encontro único: "De um script frágil a um mapa navegável"

3h = 180 min. Duas pausas de 10 min → 160 min de conteúdo.

| Tempo | Bloco | Formato | Dor / entregável |
|---|---|---|---|
| 0:00–0:10 | Abertura, combinados, enquete de aquecimento | Slide | — |
| 0:10–0:35 | **O problema.** Rodar `antes/analise_olist.py`, falhar, e percorrer as 4 dores | Demo | `antes/` |
| 0:35–0:50 | O que é Kedro: definição, origem, posicionamento no stack, o que **não** é | Slide | — |
| 0:50–1:15 | Anatomia do projeto + **Data Catalog** (dor #1): `kedro new`, trocar CSV→Parquet só em YAML, `versioned: true`, menção rápida a `kedro ipython` | Demo | `projeto/` |
| 1:15–1:25 | **Pausa** | | |
| 1:25–1:55 | **Nodes/Pipelines** (dor #3) + **Parameters** (dor #2): decompor o script, `--from-nodes`/`--to-nodes`/`--pipeline`, dois cenários de negócio via `parameters.yml` | Demo | |
| 1:55–2:25 | **Kedro-Viz** (dor #4) — o clímax: grafo, camadas, linhagem clicável, ramo de modelagem, `--autoreload`, `viz build` | Demo | |
| 2:25–2:35 | **Pausa** | | |
| 2:35–2:50 | **Hooks**: qualidade de dados barrando a pipeline ao vivo (relatório de execução já apareceu sozinho nos blocos anteriores) | Demo | |
| 2:50–3:00 | Produção e valor (panorama de 1 slide), argumento de handoff/onboarding, créditos do dataset, entrega do material, encerramento | Slide | |

**Ponto de não-retorno:** o bloco 0:10–0:35 é o mais importante da aula. Sem a
dor instalada, todo o resto vira abstração — e como não há segundo encontro
para recuperar o fio, esse bloco precisa estar redondo. Ensaiar duas vezes,
cronometrado.

**Válvula de segurança de tempo:** se a aula atrasar, corte nesta ordem (do
menos ao mais crítico): (1) slide de produção/panorama → 1 frase falada, sem
slide; (2) demo de `--autoreload` no Kedro-Viz → menção verbal; (3) segundo
cenário de parâmetros → mostrar só um; nunca corte o bloco "o problema" nem o
bloco do Kedro-Viz.

---

## 7. Slides — storyboard

Marp, 16:9, **um arquivo único** (`slides/aula.md`). Alvo: **~36 slides**.
Regra de densidade: um slide, uma ideia; no máximo 5 linhas de texto; código
em slide só quando for o objeto da explicação (o resto é demo ao vivo).

1. Capa
2. Combinados (gravação, chat, 2 pausas, duração 3h)
3. Enquete: "já perdeu uma análise por não achar a versão certa do dado?"
4. Agenda do dia (visão única, blocos e pausas marcados)
5–6. O ciclo de vida real de uma análise (do pedido do gestor ao esquecimento)
7. **[DEMO]** marcador de tela — rodar o script bagunçado
8–11. As 4 dores, uma por slide, com o trecho de código culpado
12. **Slide-âncora:** as 4 dores numeradas (retomado 4x ao longo da aula)
13. O que é Kedro — definição em uma frase
14. Origem e governança (QuantumBlack/McKinsey → Linux Foundation)
15. Onde encaixa: Kedro × notebook × dbt × Airflow × MLflow × Databricks (1 slide compacto, não aprofundar)
16. O que Kedro **não** é
17. Os 4 conceitos que sustentam tudo (Catálogo, Nó, Pipeline, Config)
18. **[DEMO]** anatomia do projeto
19. Camadas de dados — paralelo com Medallion/Lakehouse
20. **[DEMO]** Data Catalog (formato, versionamento, `kedro ipython`)
21. Antes/depois: `read_csv` hardcoded × YAML
22. Recap: dor #1 resolvida
23. **[DEMO]** decompondo o script em nós + execução seletiva
24. Recap: dor #3 resolvida
25. **[DEMO]** dois cenários de negócio via `parameters.yml`
26. Recap: dor #2 resolvida
27. **[DEMO]** Kedro-Viz — bloco longo (grafo, camadas, linhagem, ramo de modelagem, autoreload, build)
28. Linhagem de dados — "de onde veio esse número?" antes/depois
29. Recap: dor #4 resolvida
30. Entregável: o Viz estático que vocês levam
31. **[DEMO]** qualidade de dados barrando a pipeline
32. Panorama de produção (Docker/Airflow/Databricks) + próximo passo (`kedro-mlflow`) — 1 slide só, sem aprofundar
33. O argumento econômico: onboarding, handoff, continuidade
34. Quando Kedro **não** vale a pena
35. Créditos do dataset + recursos para continuar
36. Encerramento + entrega do material

---

## 8. Riscos e mitigações

| Risco | Probabilidade | Mitigação |
|---|---|---|
| Demo quebra ao vivo | Alta | **Vídeo gravado de cada demo** (2–5 min) pronto para cortar. Ver `roteiros/plano-b.md` |
| Aula atrasar e faltar tempo para o Kedro-Viz | Alta (regime de 3h é apertado) | Válvula de segurança de tempo definida em §6 — corte planejado, não improvisado |
| Ambiente do instrutor se atualiza e quebra a API | Média | Versões fixadas em `requirements.txt` + ambiente virtual dedicado, criado e congelado com antecedência |
| Queda de atenção numa sessão de 3h contínuas | Alta | 2 pausas fixas, enquete por bloco, ciclos de ≤7 min de terminal |
| Fonte pequena no compartilhamento do Meet | Alta | Editor e terminal a ≥18pt, tema claro, zoom do Viz ajustado. Checklist pré-aula |
| Dado do Olist vazar para o repositório público (commit acidental, saída de `reporting`, preview no Viz) | Média | `.gitignore` cobrindo as pastas de dados **inteiras**; conferência do build do Viz antes de publicar. Ver §3.0 |
| Licença NC do Olist barrada pela instituição | Baixa | Plano B: **Online Retail II** (UCI, CC BY 4.0). Case vira segmentação RFM; a arquitetura de camadas e pipelines se mantém, muda só `ingestao` |
| Perguntas de "e comparado com X?" | Alta | Slide 15 antecipa. Ter respostas curtas prontas para dbt, Airflow, Databricks Workflows — sem se alongar |
| Aluno pede o material durante a aula | Certa | Link do repo + Viz estático no chat, já no primeiro slide |

---

## 9. Checklist de pré-produção

**Até 7 dias antes**
- [ ] Dataset baixado e amostra gerada
- [ ] Projeto Kedro rodando ponta a ponta com as versões fixadas
- [ ] Slide único exportado em PDF e HTML

**Até 3 dias antes**
- [ ] Vídeos de backup de todas as demos gravados
- [ ] `git status` limpo — **nenhum arquivo de dado rastreado** (`git ls-files | grep -i csv` deve vir vazio)
- [ ] Build do Viz inspecionado: sem prévia de linhas dos datasets embutida
- [ ] `kedro viz build` publicado no GitHub Pages, URL testada em aba anônima
- [ ] Slide de créditos do dataset presente
- [ ] Ensaio cronometrado do bloco "o problema" (0:10–0:35) — é o único bloco que não tem segunda chance numa sessão de 3h
- [ ] Ensaio cronometrado da aula inteira, ao menos uma vez, com as duas pausas reais

**No dia**
- [ ] Ambiente virtual ativo e validado com um `kedro run` completo
- [ ] Fontes ampliadas, tema claro, notificações desligadas
- [ ] Gravação do Meet ativada e anunciada
- [ ] Roteiro aberto na segunda tela, com a válvula de segurança de tempo (§6) grifada
- [ ] Vídeos de backup abertos em abas prontas

---

## 10. Definição de pronto

O material está pronto quando:

1. `kedro run` executa a pipeline completa sem erro, em menos de 60 segundos,
   partindo da amostra de dados.
2. `kedro viz run` renderiza o grafo com as 7 camadas coloridas.
3. O arquivo Marp único exporta para PDF sem erro.
4. Um leitor que só tenha o `README.md` consegue reproduzir o ambiente.
5. Cada bloco do roteiro tem os comandos exatos, na ordem, com o texto do que
   falar enquanto o comando roda, e soma no máximo 160 min de conteúdo +
   20 min de pausas.
6. Nenhum trecho de código usa API removida no Kedro 1.x (ver §2.1).
