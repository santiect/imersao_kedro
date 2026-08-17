# Roteiro — Imersão Kedro (sessão única, 3h)

> Este é o documento que você segue durante a aula, numa segunda tela. Os
> slides (`slides/aula.md`) vão para o Meet. Todos os comandos abaixo foram
> **testados de verdade** nesta máquina em 2026-08-05 — não são exemplos
> genéricos.
>
> Setup de tela: 2 abas de terminal.
> - **Aba A** (principal): todos os comandos deste roteiro.
> - **Aba B** (reserva): fica parada, pronta para abrir um vídeo de backup se
>   uma demo travar (ver `roteiros/plano-b.md`).

---

## Antes de ligar a câmera

```bash
cd ~/imersao_kedro
source .venv/bin/activate
cd projeto/olist_analytics
kedro run > /dev/null 2>&1 && echo "pipeline OK, pronto pra aula"
```

Confirme que `conf/base/parameters.yml` está nos valores originais (período
2017-01-01 a 2018-08-31) — se você ensaiou o bloco de Hooks antes, pode ter
ficado com o período estreito. `git diff conf/base/parameters.yml` deve vir
vazio (o repo do instrutor não deveria ter esse arquivo modificado).

---

## Válvula de segurança de tempo

Se a aula atrasar, corte **nesta ordem** (do menos ao mais crítico). Nunca
corte o bloco "O problema" nem o bloco do Kedro-Viz — são os dois que
carregam a aula.

1. Slide de produção/panorama (2:50) → vira 1 frase falada, sem exibir o slide.
2. Demo de `--autoreload` no Kedro-Viz → menção verbal ("isso aqui atualiza
   sozinho quando eu edito o código, não vou fazer ao vivo por tempo").
3. Segundo cenário de parâmetros (nota_corte 3) → mostra só o primeiro (nota 2).

---

## [0:00–0:10] Abertura · (10 min)

**Objetivo:** combinar as regras da sessão e aquecer a plateia.
**Slides:** 1–4
**Tela:** slides

### O que falar
- Se apresentar, agradecer a presença.
- Avisar que a sessão é gravada.
- Regras: câmera opcional, perguntas pelo chat a qualquer momento (não precisa
  esperar), 2 pausas de 10 min já marcadas na agenda.
- Enquete de aquecimento (slide 3): "quantos aqui já perderam uma análise
  porque não sabiam qual era a versão certa da planilha/dado?" — deixar
  a plateia responder no chat ou por enquete do Meet, comentar 2-3 respostas.
- Mostrar a agenda (slide 4) e dizer: "hoje é sobre o Kedro resolver 4
  problemas específicos — vou nomear os 4 já no início, e vamos voltar a eles
  a aula inteira".

### Perguntas prováveis
- **"Vamos instalar o Kedro?"** → Não, a sessão é 100% demonstração; o link do
  repositório fica disponível pra quem quiser reproduzir depois.

---

## [0:10–0:35] O problema · (25 min)

**Objetivo:** instalar a dor antes de qualquer solução. Bloco mais importante
da aula — sem segunda chance.
**Slides:** 5–12
**Tela:** slides → terminal/VS Code → slides

### Comandos
```bash
# a partir de ~/imersao_kedro (não dentro de projeto/)
cd ~/imersao_kedro/antes
cat analise_olist.py | head -20     # ou abrir no editor, fonte >= 18pt
python analise_olist.py
```
Isso **falha de propósito** com:
```
FileNotFoundError: [Errno 2] No such file or directory: 'C:/Users/everton/Downloads/olist/olist_orders_dataset.csv'
```

### O que falar
- Slides 5–6: contextualizar — "o Ricardo, da diretoria, pediu a taxa de
  clientes insatisfeitos — nota de review ≤ 2 — pra reunião de terça. Alguém
  do time fez isso." Abrir o arquivo
  `analise_olist.py` na tela (VS Code, fonte grande).
- Rodar o comando acima. Deixar o erro aparecer sem cortar.
- **Dor #1 (linha 14):** "isso funcionou na máquina de quem escreveu.
  Aqui, não funciona — porque o caminho do arquivo tá dentro do código."
- Rolar até as linhas 27, 43, 56–57, 76–78: **Dor #2** — "o ano da análise,
  o corte de frete, a definição de 'cliente insatisfeito'... estão espalhados
  em pelo menos 4 lugares diferentes. Mudar um critério de negócio significa
  caçar linha por linha."
- Rolar até o bloco comentado (linhas 82–92) e o comentário da linha 121:
  **Dor #3** — "pra rodar só a parte do modelo, é preciso rodar o arquivo
  inteiro de novo. Quem escreveu isso sabia do problema e não teve tempo de
  resolver."
- Rolar até as linhas 94–112: **Dor #4** — "esse número aqui, que vai pro
  slide da diretoria, vem de `df_final_v2`, que vem de `df_final2`, que vem
  de `df_final`... Pergunta simples: de onde veio esse número? Ninguém
  responde sem ler o arquivo inteiro de trás pra frente. Olha o comentário da
  linha 110 — nem quem escreveu tinha certeza."
- Slide 12 (âncora): mostrar as 4 dores numeradas, juntas. "Essas 4 coisas vão
  aparecer de novo a aula inteira — cada vez que resolvermos uma, eu volto
  nesse slide."

### Perguntas prováveis
- **"Isso é exagero, ninguém escreve código assim"** → "Esse código roda de
  verdade com os dados reais do Olist — testei antes da aula. E se você já
  trabalhou com dado, provavelmente já viu pior."
- **"Por que não usar um notebook Jupyter?"** → A crítica não é ao notebook em
  si, é a **isso aqui ser o projeto inteiro**: tudo em sequência, sem
  estrutura, dentro de células — os mesmos 4 problemas, só escondidos. Um
  notebook pequeno, que só olha um catálogo já estruturado, é outra
  conversa — tem um lá no projeto, mostro mais adiante.

### Se der errado
O comando é *desenhado* para falhar — não há "der errado" aqui, a única forma
de quebrar a demo é o arquivo `analise_olist.py` não existir ou o Python não
estar no PATH. Se isso acontecer, pule para o slide 8 (screenshot do erro,
guardado em `roteiros/plano-b.md`) e siga narrando por cima do slide.

**Opcional, só se sobrar tempo:** corrigir a linha 14 para o caminho local
(`dados/raw/`) e rodar de novo, mostrando que "funciona, mas continua frágil e
opaco". Os números que aparecem (ano 2017 apenas) **não devem ser citados
depois** — o projeto Kedro usa um período diferente (2017–2018) e os números
não batem. Se fizer esse extra, não gaste mais que 3 min nele.

---

## [0:35–0:50] O que é Kedro · (15 min)

**Objetivo:** dar nome e contexto ao que resolve as 4 dores, sem entrar em código.
**Slides:** 13–17
**Tela:** slides

### O que falar
- Slide 13: "Kedro é um framework Python de código aberto para estruturar
  projetos de dados — ele não processa dado nenhum sozinho, ele organiza
  **como seu código acessa dado, se divide em etapas, e se configura**."
- Slide 14: origem — nasceu na QuantumBlack (McKinsey), hoje é projeto da
  Linux Foundation. Não é ferramenta de um fornecedor só.
- Slide 15: posicionamento — Kedro não compete com dbt (que é SQL/warehouse),
  nem com Airflow (que agenda e executa em produção), nem com MLflow (que
  rastreia experimentos). Kedro organiza o **código Python** que fica entre
  esses mundos. Não aprofundar — 1 slide, seguir.
- Slide 16: o que Kedro **não é** — não é banco de dados, não é ferramenta de
  BI, não substitui a análise em si.
- Slide 17: os 4 conceitos que sustentam tudo — Catálogo (onde tá o dado),
  Nó (uma função), Pipeline (nós encadeados), Configuração (parâmetros fora
  do código). "Esses 4 conceitos resolvem as 4 dores que vimos. Vamos ver um
  de cada vez, com o projeto rodando de verdade."

### Perguntas prováveis
- **"Isso substitui o Excel/Power BI?"** → Não — Kedro organiza o código que
  *prepara* o dado; o BI continua consumindo o resultado.
- **"Precisa saber Python avançado?"** → O suficiente pra escrever uma função.
  A curva é mais sobre organização do que sobre sintaxe.

---

## [0:50–1:15] Anatomia do projeto + Data Catalog (dor #1) · (25 min)

**Objetivo:** mostrar a estrutura de um projeto real e resolver a dor #1 ao vivo.
**Slides:** 18–22
**Tela:** terminal/VS Code → slides

### Comandos
```bash
cd ~/imersao_kedro/projeto/olist_analytics
code .                      # se for usar VS Code
ls
```
Abrir e comentar rapidamente: `conf/`, `src/olist_analytics/`, `data/`
(as 8 subpastas numeradas — 01_raw até 08_reporting).

```bash
# o catálogo — abrir conf/base/catalog.yml no editor, rolar devagar
```
Apontar: comentário do topo, os 8 datasets `raw` em CSV, os `intermediate`
em Parquet, o `metadata.kedro-viz.layer` em cada um.

```bash
kedro catalog describe-datasets
```

**Demo do "trocar formato só no YAML"** — editar `conf/base/catalog.yml` ao
vivo, no bloco `receita_mensal`:
```yaml
# de:
receita_mensal:
  type: pandas.CSVDataset
  filepath: data/08_reporting/receita_mensal.csv
# para:
receita_mensal:
  type: pandas.ExcelDataset
  filepath: data/08_reporting/receita_mensal.xlsx
```
```bash
rm -f data/08_reporting/receita_mensal.csv
kedro run --pipeline=relatorio
ls data/08_reporting/ | grep receita
# abrir o .xlsx gerado, mostrar que abre no Excel
```
**Depois da demo, reverta** (Ctrl+Z no editor ou `git checkout -- conf/base/catalog.yml`)
para deixar o projeto limpo para o resto da aula:
```bash
git checkout -- conf/base/catalog.yml
rm -f data/08_reporting/receita_mensal.xlsx
kedro run --pipeline=relatorio
```

**Demo rápida de `kedro ipython`** (2 min, sem aprofundar em modo dev):
```bash
kedro ipython
```
```python
catalog.load("tabela_analitica").head()
exit
```

**Extra opcional, só se sobrar tempo** (não é orçado nos 25 min do bloco —
nunca atrasar o próximo bloco por causa disso):
```bash
kedro jupyter notebook
```
Abrir `notebooks/explorar_catalogo.ipynb`, rodar as células, mostrar a tabela
formatada e o gráfico de receita mensal. **Depois de mostrar, fechar sem
salvar** (ou rodar `jupyter nbconvert --clear-output --inplace
notebooks/explorar_catalogo.ipynb` antes de sair) — o notebook não pode ficar
com output no repositório.

### O que falar
- "Isso aqui substitui as 8 linhas de `pd.read_csv` com caminho fixo que
  vimos há pouco. Cada dataset tem um nome, um lugar, um formato — declarados
  em um arquivo só, que qualquer pessoa do time lê sem abrir o código."
- Ao trocar CSV → Excel: "Eu não toquei em nenhuma linha de código Python.
  Troquei duas linhas de configuração e o node que gera esse relatório nem
  sabe que mudou de formato."
- No `kedro ipython`: "e se eu quiser só espiar um dado, sem escrever um
  script? Uso isso — é um terminal Python com o catálogo já carregado."
- *(se fizer o extra do notebook)*: "e se eu quiser ver isso mais visual, com
  gráfico? O mesmo catálogo funciona dentro de um notebook também — a
  diferença é que aqui ele não guarda nenhuma lógica do projeto, só olha o
  que já existe. O risco que vimos no início da aula era usar notebook como
  o projeto inteiro, não usar notebook."
- Slide 19 (camadas): "Essa numeração de pastas — 01 a 08 — é convenção do
  Kedro. É o mesmo princípio do Medallion/Lakehouse que muita empresa já usa:
  dado bruto nunca se mistura com dado tratado."
- Slide 21 (antes/depois): comparar lado a lado o trecho do `analise_olist.py`
  com o `catalog.yml`.
- Slide 22 (recap): voltar ao slide-âncora, riscar a dor #1.

### Perguntas prováveis
- **"E se o dado tiver senha, tipo banco de dados?"** → Aponta pra
  `conf/local/credentials.yml`, que fica fora do git.
- **"Kedro guarda o dado?"** → Não, ele só aponta pra onde o dado está —
  disco local, S3, banco, etc.

### Se der errado
Se `kedro run --pipeline=relatorio` falhar após a edição do YAML (erro de
indentação é o mais provável), mostrar o erro é parte da demo: "vejam como o
erro aponta exatamente pro YAML, não pro código Python — é aí que mexi."
Corrigir a indentação ao vivo (geralmente rápido) ou, se travar, `git checkout
-- conf/base/catalog.yml` e seguir.

---

## [1:15–1:25] PAUSA · (10 min)

Avisar retomada, deixar slide de pausa com o tempo restante em contagem, se o
Meet permitir. Aproveitar para checar o chat.

---

## [1:25–1:55] Nodes/Pipelines (dor #3) + Parameters (dor #2) · (30 min)

**Objetivo:** mostrar execução seletiva e configuração fora do código.
**Slides:** 23–26
**Tela:** VS Code → terminal → slides

### Comandos — Nodes e Pipelines
```bash
# abrir no editor:
# src/olist_analytics/pipelines/features/nodes.py
# src/olist_analytics/pipelines/features/pipeline.py
```
Apontar: cada função é pura (entrada → saída, sem efeito colateral), docstring
de uma linha, sem `print`. O `pipeline.py` só liga os nomes.

```bash
kedro run --pipeline=features
```
```bash
# rodar só o relatório, sem reprocessar nada anterior:
kedro run --from-nodes=calcular_receita_mensal
```
```bash
# rodar só até um ponto específico:
kedro run --to-nodes=limpar_pedidos
```

### O que falar
- "Cada uma dessas funções faz uma coisa só, e tem nome. `pipeline.py` é só a
  lista de quem alimenta quem — o Kedro monta o grafo de execução sozinho a
  partir disso."
- Ao rodar `--from-nodes=calcular_receita_mensal`: "reparem: 1 tarefa só.
  Não recalculei nada anterior — o Kedro sabe que a tabela analítica já
  existe em disco e só roda o relatório. Lembra do bloco comentado no script
  antigo, `descomentar pra rodar o modelo`? Isso aqui resolve aquilo."
- Slide 24 (recap): riscar dor #3.

### Comandos — Parameters
```bash
cat conf/base/parameters.yml
```
Apontar a seção `analise.nota_corte_review_ruim: 2`.

```bash
kedro run --pipeline=relatorio
cat data/08_reporting/review_por_estado.csv | head -6
```

Editar `conf/base/parameters.yml` ao vivo: `nota_corte_review_ruim: 2` → `3`.

```bash
kedro run --pipeline=relatorio
cat data/08_reporting/review_por_estado.csv | head -6
```

**Reverter depois da demo:**
```bash
git checkout -- conf/base/parameters.yml
```

### O que falar
- "Mudei UMA linha — o que conta como 'cliente insatisfeito' — e o relatório
  inteiro recalculou com o novo critério. No script antigo isso era procurar
  o número em 4 lugares e torcer pra não esquecer nenhum."
- Slide 26 (recap): riscar dor #2.

### Perguntas prováveis
- **"Isso equivale a um parâmetro de função?"** → Sim, mas centralizado — todo
  node que precisa desse número lê do mesmo lugar, nunca duplica o valor.
- **"E se eu quiser um ambiente de teste com parâmetros diferentes?"** →
  Mencionar rapidamente `conf/local/` vs `conf/base/` sem se alongar.

### Se der errado
Se a edição do YAML quebrar a indentação, o erro do Kedro aponta a linha —
corrigir ao vivo é rápido. Se travar, `git checkout -- conf/base/parameters.yml`
e seguir com os números da primeira rodada (nota 2), citando o segundo cenário
só verbalmente.

---

## [1:55–2:25] Kedro-Viz (dor #4) — o clímax · (30 min)

**Objetivo:** o momento de maior impacto visual da aula.
**Slides:** 27–30
**Tela:** terminal → navegador → slides

### Comandos
```bash
kedro viz run --autoreload
```
Abre em `http://127.0.0.1:4141`. Deixar esse terminal rodando — ele é
bloqueante; use a Aba B só se precisar editar código durante o autoreload
(ou abra um terceiro terminal).

### O que falar, na ordem
1. **Tour geral do grafo:** "esse é o pipeline inteiro, todas as 5 etapas,
   desde os 8 CSVs até o modelo."
2. **Camadas coloridas:** apontar a legenda (raw, intermediate, primary,
   feature, model_input, models, reporting). "É a mesma numeração de pastas
   que vimos há pouco — aqui ela vira cor."
3. **O momento alto da aula:** clicar num dataset da camada `reporting`
   (ex.: `review_por_estado`) e usar o botão de expandir linhagem até
   chegar nos CSVs brutos. "Essa é a resposta pra dor #4 — 'de onde veio esse
   número' — literalmente clicando."
4. **Painel de metadados:** clicar num nó, mostrar código-fonte e
   inputs/outputs no painel lateral.
5. **Ramo de modelagem:** apontar o ramo que vai até `modelo_review_ruim` e
   `metricas_modelo` — abrir o painel desse dataset e mostrar as métricas reais
   (acurácia 0,888, F1 0,39) e, se houver tempo, `importancia_features`
   (frete e atraso pesam mais que o valor da compra — bom gancho de negócio).
   **Sem explicar hiperparâmetro nenhum** — é só "o mesmo pipeline chega até
   aqui".
6. **Autoreload:** no editor, abrir
   `src/olist_analytics/pipelines/features/nodes.py`, mudar a docstring de
   `calcular_prazo_entrega` (ex.: acrescentar uma palavra), salvar, voltar pro
   navegador e clicar de novo no nó — o texto atualizado aparece sem reiniciar
   nada. Desfazer a edição depois (Ctrl+Z + salvar).
7. **Build estático**, em outro terminal:
   ```bash
   kedro viz build
   ```
   "Isso gera um site — o mesmo que vocês estão vendo agora — que eu publico
   e vocês acessam depois da aula, sem instalar nada."

### Perguntas prováveis
- **"Isso atualiza sozinho em produção?"** → O `--autoreload` é só para
  desenvolvimento local; em produção o grafo é gerado a partir do código
  publicado.
- **"Dá pra exportar isso como imagem/PDF?"** → Sim, o Kedro-Viz tem opção de
  exportar PNG do grafo.
- **"88% de acurácia é bom?"** (se alguém perguntar ao ver `metricas_modelo.json`)
  → **Não caia na armadilha de confirmar que é bom.** Só 12,6% dos pedidos têm
  review ruim — um modelo preguiçoso que sempre chuta "não é ruim" já acertaria
  uns 87% sem aprender nada. 88,8% é só um pouco melhor que isso.
  O número que importa aqui é a **revocação: 28%** — de todo cliente que
  realmente ficou insatisfeito, o modelo só identificou 28%, deixou passar 72%.
  **F1 (0,39)** resume isso — combina precisão (63%, "quando o modelo grita
  'ruim', acerta 63% das vezes") com essa revocação baixa, e por isso sai
  puxado pra baixo. Frase pronta: *"O modelo acerta muito no geral porque a
  maioria dos pedidos é normal — o que interessa pro negócio é que ele só
  pega 1 em cada 4 clientes insatisfeitos. É ponto de partida, não produto
  pronto."* Não se alongar mais que isso — é uma resposta de 30s, não um
  bloco novo.

### Se der errado
Se o servidor não subir (porta ocupada), `kedro viz run --port 4142`. Se o
navegador travar, cortar para o vídeo de backup gravado deste bloco — é o mais
importante ter backup, porque é o clímax da aula.

---

## [2:25–2:35] PAUSA · (10 min)

---

## [2:35–2:50] Hooks · (15 min)

**Objetivo:** mostrar governança automática — dado ruim não passa.
**Slides:** 31
**Tela:** terminal → VS Code → terminal

### O que falar (abertura, sem comando)
- "Vocês repararam que depois de cada `kedro run`, apareceu uma tabelinha de
  tempo por node? Isso é automático — um hook que já roda desde o começo da
  aula, sem eu ter feito nada de especial. Serve pra saber onde o pipeline
  gasta tempo (e, em produção, dinheiro de processamento)."
- "Agora vou mostrar outro hook, que **impede** um relatório ruim de ser
  gerado."

### Comandos
Editar `conf/base/parameters.yml` ao vivo:
```yaml
periodo:
  inicio: "2018-08-31"
  fim: "2018-08-31"
```
```bash
kedro run
```

Isso **falha de propósito** com:
```
ValueError: Qualidade de dados reprovada em 'tabela_analitica':
  - apenas 0 linha(s) na tabela analítica (mínimo esperado: 100)
```

**Reverter imediatamente depois:**
```bash
git checkout -- conf/base/parameters.yml
kedro run > /dev/null 2>&1 && echo "voltou ao normal"
```

### O que falar
- "Restringi o período pra um único dia — praticamente não sobra pedido
  nenhum. O pipeline **parou sozinho**, antes de gerar um relatório vazio ou
  enganoso, com uma mensagem clara do que faltou."
- "Isso é um hook — um pedaço de código que roda automaticamente em pontos
  específicos da execução. Não preciso lembrar de validar manualmente toda
  vez; a regra está no projeto."
- Mensagem de negócio: "dado ruim não chega no relatório da diretoria."

### Perguntas prováveis
- **"Isso substitui teste de dados tipo Great Expectations?"** → É mais
  simples — dá pra crescer pra ferramentas dedicadas, mas o princípio
  (validar antes de entregar) é o mesmo.

### Se der errado
Se por algum motivo o hook não disparar (regra de negócio foi alterada por
engano antes da aula), o erro esperado não aparece — nesse caso, siga direto
com a explicação verbal da tabela de tempo por node (que já apareceu em todo
`kedro run` anterior) e pule a quebra proposital.

---

## [2:50–3:00] Produção, valor e encerramento · (10 min)

**Objetivo:** fechar com o argumento de negócio e entregar o material.
**Slides:** 32–36
**Tela:** slides

### O que falar
- Slide 32 (panorama, rápido): "em produção, esse projeto roda dentro de um
  container Docker, agendado por uma ferramenta como Airflow, e pode registrar
  experimentos com o MLflow. Não vou entrar em como configurar isso — só
  saibam que existe e que o Kedro se encaixa nesse ecossistema sem mudar a
  estrutura que vocês viram hoje."
- Slide 33 (argumento econômico): "o ganho real não é técnico, é de time.
  Uma pessoa nova entra no projeto e entende a estrutura em horas, não em
  dias lendo um script de 200 linhas. Se quem escreveu sai da empresa, o
  projeto continua legível."
- Slide 34 (quando não vale a pena): projeto de exploração de 1 pessoa, muito
  curto, não precisa dessa estrutura — o Kedro compensa quando o projeto vai
  durar e/ou ser compartilhado.
- Slide 35: créditos do dataset (*"Brazilian E-Commerce Public Dataset by
  Olist (Kaggle), CC BY-NC-SA 4.0"*) + recursos pra continuar.
- Slide 36: agradecer, avisar que o link do repositório e do Kedro-Viz
  publicado vão para o chat, abrir pra últimas perguntas.

### Perguntas prováveis
- **"Onde acho o material depois?"** → link do repositório + Kedro-Viz
  publicado, já deixados no chat desde o início.
- **"Tem certificado?"** → conforme política da instituição, fora do escopo
  deste roteiro.

---

## Checklist de encerramento (depois que os alunos saírem)

```bash
cd ~/imersao_kedro/projeto/olist_analytics
git status                      # não deve haver alterações não commitadas relevantes
git diff conf/base/parameters.yml conf/base/catalog.yml   # deve vir vazio
```

Se algum arquivo ficou modificado por uma demo que não foi revertida:
```bash
git checkout -- conf/base/parameters.yml conf/base/catalog.yml
```
