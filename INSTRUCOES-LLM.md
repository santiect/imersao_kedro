# Instruções de construção — Imersão Kedro

> **Para o agente/LLM que vai executar.** Este documento é a especificação de
> build. O desenho e as justificativas estão em [PLANO.md](PLANO.md) — leia-o
> por inteiro antes de começar. Este arquivo diz **o que produzir**, em que
> ordem, e com quais critérios de aceite.
>
> **Revisão 2026-08-04:** a aula é **1 encontro único de 3h**, não mais 2
> encontros de 3h. `roteiros/` e `slides/` têm **um arquivo cada**, não um por
> encontro. O projeto Kedro em si não muda de escopo — só o roteiro e os slides.

---

## 0. Antes de qualquer coisa

1. Leia `PLANO.md` inteiro e `CLAUDE.md`.
2. **Confirme as versões dos pacotes** consultando o PyPI. O `PLANO.md` foi
   escrito em agosto/2026 com Kedro 1.5.0, kedro-viz 12.4.0,
   kedro-datasets 9.5.0. Se houver versão maior disponível, **pergunte ao
   usuário** antes de trocar — não atualize por conta própria.
3. **Nunca escreva código Kedro de memória.** A API mudou muito entre 0.18,
   0.19 e 1.0. Consulte `https://docs.kedro.org/en/stable/` para qualquer
   assinatura de que não tenha certeza absoluta. A lista de armadilhas está em
   `PLANO.md` §2.1.
4. Todo texto entregue é em **português do Brasil**. Nomes de variáveis,
   funções, nós e datasets também.

---

## 1. Ordem de execução

Construa nesta ordem. Cada etapa depende da anterior estar validada.

| # | Etapa | Produz | Bloqueante? |
|---|---|---|---|
| 1 | Ambiente | `ambiente/requirements.txt`, `ambiente/setup.md` | sim |
| 2 | Dados | `dados/README.md`, `dados/preparar_amostra.py` | sim |
| 3 | Script "antes" | `antes/analise_olist.py`, `antes/README.md` | sim |
| 4 | Projeto Kedro | `projeto/olist_analytics/` completo | sim |
| 5 | Hooks | dentro do projeto | não |
| 6 | Roteiros de demo | `roteiros/*.md` | não |
| 7 | Slides | `slides/*.md` + tema | não |
| 8 | Material do aluno | `material-aluno/*.md` | não |
| 9 | Publicação do Viz | `.github/workflows/publicar-viz.yml` | não |
| 10 | README raiz | `README.md` | não |

**Ponto de parada obrigatório:** ao terminar a etapa 4, rode a pipeline de
verdade e reporte o resultado ao usuário antes de seguir. Se não for possível
rodar (dataset ausente), diga isso explicitamente — não afirme que funciona.

---

## 2. Etapa 1 — Ambiente

**`ambiente/requirements.txt`**
- Versões fixadas com `==` para `kedro`, `kedro-viz`, `kedro-datasets`,
  `kedro-mlflow`.
- `kedro-datasets` com os extras necessários para CSV, Parquet e Excel via pandas.
- `scikit-learn`, `pandas`, `pyarrow`, `matplotlib` fixados.
- Comentário no topo indicando a data da verificação das versões.

**`ambiente/setup.md`**
- Passo a passo com `python3.12 -m venv`, ativação em Linux/macOS **e** Windows.
- Comando de validação final: `kedro info` mostrando a versão esperada.
- Seção "problemas comuns" com pelo menos: Python fora da faixa 3.10–3.14,
  falha de compilação de `pyarrow`, e porta 4141 ocupada (Kedro-Viz).

---

## 3. Etapa 2 — Dados

> Leia `PLANO.md` §3.0 antes desta etapa. A política é: **nenhum dado é
> versionado, em hipótese alguma** — nem bruto, nem amostra, nem saída de
> `reporting`. Os alunos não executam nada, logo não precisam dos arquivos.

**`dados/README.md`**
- Origem: Kaggle `olistbr/brazilian-ecommerce`.
- Licença **CC BY-NC-SA 4.0** declarada, com o texto de atribuição padrão.
- Explicar a distinção **usar × redistribuir** (§3.0) em dois parágrafos: por
  que dar aula com o dataset é tranquilo e por que o repositório não guarda dado.
- Instruções manuais de download (o download exige conta Kaggle — não tente
  automatizar com credenciais).
- Lista das 9 tabelas com uma linha de descrição cada, marcando
  `olist_geolocation_dataset.csv` como descartada.
- Instrução de rodar `preparar_amostra.py` em seguida.
- Aviso de que a licença deve ser reconferida no bloco "License" da página do
  Kaggle antes da produção final.

**`dados/preparar_amostra.py`**
- Script Python puro (sem Kedro), executável direto.
- Lê de `dados/raw/`, escreve em `projeto/olist_analytics/data/01_raw/`.
- Filtra pedidos de 2017-01-01 a 2018-08-31 e propaga o filtro às tabelas
  filhas por `order_id`.
- **Descarta `olist_geolocation_dataset.csv`** por completo.
- Imprime um relatório: linhas antes/depois e tamanho final em MB por arquivo.
- Alvo: total ≤ 25 MB.
- Falha com mensagem clara e acionável se `dados/raw/` estiver vazio.
- Cabeçalho do script deixando explícito: a amostra é local, para as demos, e
  **não deve ser distribuída**.

**`.gitignore`** — crie na raiz cobrindo as pastas de dados **por inteiro**:

```gitignore
dados/raw/
projeto/olist_analytics/data/
*.csv
*.parquet
*.xlsx
```

O bloqueio por extensão é uma segunda barreira contra commit acidental. Se
algum CSV precisar ser versionado (nenhum deve), a exceção é explícita e
consciente. Depois de criar, valide: `git ls-files | grep -iE '\.(csv|parquet|xlsx)$'`
tem de vir vazio.

---

## 4. Etapa 3 — O script "antes"

`antes/analise_olist.py` é **material didático**. Ele precisa ser ruim de forma
*realista* e *legível* — não uma caricatura. Alvo: 150–200 linhas.

Requisitos obrigatórios — cada um mapeia a uma dor do `PLANO.md` §1.2:

| Defeito | Dor | Como implementar |
|---|---|---|
| Caminho absoluto hardcoded | #1 | `C:/Users/everton/Downloads/olist/...` no topo, em 9 linhas de `pd.read_csv` |
| Constantes mágicas espalhadas | #2 | O ano `2017`, o corte de nota `2` e a proporção `0.25` aparecem em **4 lugares diferentes** do arquivo |
| Tudo em sequência, sem função | #3 | Nenhuma `def`. Para chegar ao modelo, tudo acima reprocessa |
| Origem do número final ilegível | #4 | `taxa_ruim` calculada na linha ~170 a partir de `df_final_v2`, que veio de `df3`, que veio de `df2` |

Complementos que aumentam o realismo:
- Nomes: `df`, `df2`, `df3`, `df_final`, `df_final_v2`.
- Um bloco comentado com `# descomentar pra rodar o modelo`.
- Um `# TODO: arrumar isso depois` datado de dois anos atrás.
- Salva `resultado.xlsx` na raiz de onde for executado.
- **Deve rodar e falhar** com `FileNotFoundError` na máquina do instrutor —
  esse é o primeiro momento da aula.

`antes/README.md`: lista numerada dos defeitos, cada um apontando a linha e
dizendo qual recurso do Kedro resolve. Este arquivo é a cola do instrutor
durante o bloco de abertura.

---

## 5. Etapa 4 — Projeto Kedro

Gere com o CLI real, não à mão:

```bash
kedro new --name=olist_analytics --tools=log,test,data --example=n
```

Depois implemente conforme `PLANO.md` §5. Requisitos de aceite:

- **Catálogo** (`conf/base/catalog.yml`)
  - Todos os datasets declaram `metadata.kedro-viz.layer` com uma das 7 camadas.
  - `raw` em CSV; `intermediate` e `primary` em Parquet (isso permite a demo
    "trocar o formato mexendo só no YAML").
  - Pelo menos um dataset com `versioned: true` — use um de `reporting`.
  - Comentários em português explicando as seções, já que o arquivo vai para a tela.
- **Pipelines** — as 5 de `PLANO.md` §5.2, cada uma em seu diretório sob
  `src/olist_analytics/pipelines/`.
  - Importar `Node` e `Pipeline` de `kedro.pipeline`. Nunca de `modular_pipeline`.
  - `pipeline_registry.py` expõe as 5 nomeadas **e** `__default__`.
  - Nós são funções puras, tipadas, com docstring de uma linha em português.
  - Nenhum `print` dentro de nó — usar `logging.getLogger(__name__)`.
- **Parâmetros** — exatamente as chaves de `PLANO.md` §5.4, com comentário de
  negócio em cada uma.
- **Saídas de `reporting`** — pelo menos: receita mensal, ranking de categorias,
  taxa de review ruim por estado, e as métricas do modelo. Formatos legíveis
  (Excel ou CSV), porque vão ser abertos na tela.
- **Testes** — `pytest` cobrindo os 4 nós de `features`. Poucos e rápidos; eles
  existem para o slide de testes, não para cobertura.

**Critério de aceite da etapa:** `kedro run` completa sem erro em < 60s a partir
da amostra, e `kedro viz run` renderiza o grafo com as camadas coloridas.

---

## 6. Etapa 5 — Hooks

Em `src/olist_analytics/hooks.py`, registrados em `settings.py`.

1. **`RelatorioExecucaoHook`** — mede a duração de cada nó
   (`before_node_run` / `after_node_run`) e imprime uma tabela ordenada em
   `after_pipeline_run`. Saída formatada para ser lida na tela: alinhada, com
   o nó mais lento destacado.
2. **`QualidadeDadosHook`** — em `after_dataset_loaded`, quando o dataset for a
   tabela analítica, valida:
   - coluna alvo sem nulos;
   - prazo de entrega não negativo;
   - contagem de linhas acima de um mínimo.
   Ao violar, levanta exceção com mensagem em português explicando **qual regra
   quebrou e em quantas linhas**.

Documente em `roteiros/aula.md` o passo exato para provocar a falha ao vivo
(qual parâmetro alterar, para qual valor).

---

## 7. Etapa 6 — Roteiro

**Um arquivo único**, `roteiros/aula.md` — a aula agora é uma sessão só de 3h
(ver `PLANO.md` §6). Estrutura obrigatória por bloco:

```markdown
## [HH:MM–HH:MM] Título do bloco  ·  (duração)

**Objetivo do bloco:** uma frase.
**Slides:** 14–19
**Tela:** terminal | VS Code | navegador | slides

### Comandos
```bash
# comentário do que vai acontecer
comando exato
```

### O que falar
- Enquanto o comando roda: ...
- Ao aparecer X, apontar para: ...

### Perguntas prováveis
- **"..."** → resposta curta

### Se der errado
Cortar para o vídeo `backup/nome.mp4` e continuar em ...
```

Regras:
- Os comandos precisam ser **copiáveis e exatos**, na ordem de execução.
- Nenhum bloco de terminal com mais de ~7 minutos sem retorno a slide.
- Marcar explicitamente os momentos de troca de tela compartilhada.
- A soma dos blocos não pode passar de **160 min de conteúdo** (a sessão é de
  180 min com 2 pausas de 10 min). Inclua a **válvula de segurança de tempo**
  de `PLANO.md` §6 como uma seção própria no topo do roteiro, para o instrutor
  decidir cortes em tempo real sem improvisar.

**`roteiros/plano-b.md`** — protocolo de falha: árvore de decisão de 1 página
("demo falhou → tentar 1× → cortar para vídeo → seguir"), lista dos vídeos de
backup a gravar, e o checklist pré-aula de `PLANO.md` §9.

---

## 8. Etapa 7 — Slides

Marp, **um único arquivo** `slides/aula.md`, seguindo o storyboard de
`PLANO.md` §7 (~36 slides, sessão única).

- Front-matter Marp com `theme`, `paginate: true`, `size: 16:9`.
- Tema próprio em `slides/tema/imersao.css`: fonte grande (corpo ≥ 24px),
  alto contraste, tema claro — o Meet comprime muito.
- Slides de demo são marcadores visuais claros (fundo contrastante, uma palavra:
  **DEMO**) — servem para o instrutor saber que vai trocar de tela.
- Máximo 5 linhas de texto por slide. Sem parágrafo corrido.
- Todo slide conceitual fecha com **uma frase de impacto de negócio**.
- Diagramas em Mermaid quando possível (versionável); caso contrário, descreva
  o diagrama em comentário e deixe um placeholder — **não gere imagem falsa**.
- O slide-âncora das 4 dores tem uma variante por dor resolvida (a dor resolvida
  aparece riscada/apagada). São 5 variantes do mesmo slide ao todo.
- **Créditos do dataset** no encerramento (pode dividir espaço com o slide de
  recursos): *"Brazilian E-Commerce Public Dataset by Olist (Kaggle),
  CC BY-NC-SA 4.0."*
- Marque no próprio slide (rodapé ou canto) os blocos cortáveis descritos na
  válvula de segurança de tempo de `PLANO.md` §6, para o instrutor identificar
  rápido durante a aula.

Comando de export documentado no README:
```bash
npx @marp-team/marp-cli slides/aula.md --pdf --allow-local-files --theme-set slides/tema/imersao.css
```

---

## 9. Etapa 8 — Material do aluno

- **`cheatsheet.md`** — cabe em 1 página A4 impressa. Comandos essenciais do
  CLI, estrutura de pastas anotada, as 7 camadas, e o vocabulário mínimo.
- **`glossario.md`** — ~20 termos (nó, pipeline, catálogo, DAG, linhagem,
  camada, hook, parâmetro, ambiente, dataset versionado...). Cada verbete em
  **linguagem de negócio**, não de engenharia. Uma a três frases.
- **`leituras.md`** — documentação oficial, curso oficial gratuito, comunidade
  Slack, repositório de exemplos. **Verifique cada URL antes de incluir**; não
  liste link que você não confirmou.

---

## 10. Etapa 9 — Publicação do Viz

`.github/workflows/publicar-viz.yml`: instala as dependências, roda `kedro run`,
`kedro viz build`, e publica em GitHub Pages.

⚠️ **Não habilite o workflow nem faça push por conta própria.** Deixe-o no repo
e documente no README como o usuário o ativa. Publicar é ação externa e cabe ao
usuário decidir.

⚠️ **Dado no HTML publicado.** O build do Kedro-Viz pode embutir prévia das
primeiras linhas dos datasets. Isso seria redistribuição de obra derivada e
contraria a política de §3.0. Antes de documentar o fluxo:

1. Verifique na documentação do Kedro-Viz 12.4 se existe opção de desabilitar o
   preview (à época deste texto, datasets aceitam `metadata.kedro-viz.preview`
   e há flag de CLI para desligar a exibição — **confirme a sintaxe atual**).
2. Aplique a desativação no catálogo e/ou no comando de build.
3. Documente no README o passo manual de conferência: buscar por dados no
   diretório gerado antes de publicar.

Se não houver forma confiável de desabilitar, **não documente a publicação
como recomendada** — reporte o achado ao usuário e proponha alternativa
(capturas de tela do Viz no lugar do site interativo).

O workflow também **não deve** fazer commit de nenhum artefato de dados de volta
ao repositório.

---

## 11. Etapa 10 — README raiz

Porta de entrada para três públicos, nesta ordem:

1. **Instrutor** — como preparar tudo, em 5 passos, com os comandos.
2. **Aluno** — o que é a imersão, link do Viz publicado, onde estão os PDFs.
3. **Curioso que caiu no repo** — o que é este material, licença, atribuição do dataset.

Inclua a agenda resumida da aula (3h, sessão única) e a nota de licença do Olist.

---

## 12. Regras invioláveis

1. **Zero Jupyter Notebook.** Nenhum `.ipynb`, nenhuma menção como ferramenta
   recomendada. Exploração interativa é `kedro ipython`. A pasta `notebooks/`
   gerada pelo `kedro new` deve ser removida.
2. **Nenhuma API removida no Kedro 1.x.** Consulte `PLANO.md` §2.1 e valide
   contra a documentação oficial.
3. **Não invente números.** Estatísticas do dataset (nº de pedidos, % de nulos)
   só entram nos slides depois de calculadas de verdade sobre a amostra. Se
   ainda não foram calculadas, deixe `{{CALCULAR}}` e liste as pendências no
   final do trabalho.
4. **Não invente URLs.** Verifique antes de citar.
5. **Não faça commit, push, nem publique nada** sem o usuário pedir.
6. **Não baixe o dataset.** Exige conta Kaggle; a obtenção é manual e do usuário.
6a. **Nenhum arquivo de dado entra no repositório** — bruto, amostra, saída de
    `reporting` ou prévia embutida em HTML. Ver `PLANO.md` §3.0. Ao terminar
    qualquer etapa, confirme com
    `git ls-files | grep -iE '\.(csv|parquet|xlsx)$'` (deve vir vazio).
6b. **Atribuição do dataset obrigatória** em três lugares: o slide de créditos,
    `README.md` e `material-aluno/leituras.md`. Texto:
    *"Brazilian E-Commerce Public Dataset by Olist (Kaggle), CC BY-NC-SA 4.0."*
7. Se uma instrução daqui conflitar com o que a documentação oficial do Kedro
   1.5 diz, **a documentação vence** — e avise o usuário sobre o conflito.

---

## 13. Relatório final esperado

Ao concluir, entregue:

- Lista do que foi criado, por etapa.
- Resultado real de `kedro run` e `kedro viz run` (saída, tempo). Se não rodou,
  diga que não rodou e por quê.
- Lista de todos os `{{CALCULAR}}` pendentes.
- Divergências encontradas entre este documento e a documentação oficial.
- O que ficou fora do escopo e por quê.
