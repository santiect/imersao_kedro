# Imersão Kedro

Material de uma aula remota de **3 horas** sobre Kedro, para alunos de MBA em
Business Analytics. 100% demonstração — os alunos não instalam nem codificam
nada.

> **Dataset:** Brazilian E-Commerce Public Dataset by Olist (Kaggle),
> **CC BY-NC-SA 4.0**. Nenhum arquivo de dado está neste repositório — ver
> [por quê](#licença-e-dados) mais abaixo.

---

## Para quem vai dar a aula

1. **Ambiente** — siga [`ambiente/setup.md`](ambiente/setup.md). Resumo:
   ```bash
   uv venv .venv --python 3.12
   uv pip install --python .venv/bin/python -r ambiente/requirements.txt
   source .venv/bin/activate
   ```
2. **Dados** — baixe o dataset manualmente (requer conta Kaggle), seguindo
   [`dados/README.md`](dados/README.md), e gere a amostra local:
   ```bash
   python dados/preparar_amostra.py
   ```
3. **Validar tudo antes da aula:**
   ```bash
   cd projeto/olist_analytics
   kedro run        # deve terminar em menos de 1 min
   kedro viz run    # abre o grafo em localhost:4141
   ```
4. **O roteiro da aula** está em [`roteiros/aula.md`](roteiros/aula.md) — é o
   documento que você segue numa segunda tela. O protocolo pra quando algo
   quebra ao vivo está em [`roteiros/plano-b.md`](roteiros/plano-b.md).
5. **Os slides** estão em [`slides/aula.md`](slides/aula.md) (Marp). Para
   exportar em PDF (requer Node.js — `node --version` pra conferir):
   ```bash
   npx @marp-team/marp-cli slides/aula.md --pdf --allow-local-files --theme-set slides/tema/imersao.css
   ```
   Gera `slides/aula.pdf`.
6. **O cheatsheet do aluno** (`material-aluno/cheatsheet.md`) não é slide —
   é documento de 1 página A4, exportado com `md-to-pdf` (Marp não pagina
   documento fluido, só corta):
   ```bash
   npx md-to-pdf material-aluno/cheatsheet.md \
     --pdf-options '{"format":"A4","margin":{"top":"10mm","bottom":"10mm","left":"12mm","right":"12mm"},"printBackground":true}' \
     --css "body{font-family:sans-serif;font-size:10.5px;line-height:1.3;color:#1a1a2e} h1{font-size:19px;margin:0 0 2px} h2{font-size:13px;margin:9px 0 3px;color:#0f172a} table{width:100%;border-collapse:collapse;font-size:9.5px;margin:4px 0} th,td{border:1px solid #cbd5e1;padding:2px 6px;text-align:left} th{background:#f1f5f9} code{background:#f1f5f9;padding:1px 4px;border-radius:3px;font-size:0.9em} pre{background:#f1f5f9;padding:6px;border-radius:6px;font-size:9px;margin:4px 0} em{color:#334155} ul{margin:3px 0;padding-left:18px} li{margin:1px 0}"
   ```
   Gera `material-aluno/cheatsheet.pdf` — testado, cabe numa página só.

Antes de ensaiar, leia [`PLANO.md`](PLANO.md) inteiro — é o desenho completo
da aula (agenda, narrativa, riscos, checklist de pré-produção em §9).

### Publicar o Kedro-Viz (opcional)

O build é local — sem workflow, sem secrets do Kaggle. Você builda na sua
máquina (onde o dado já está) e publica via GitHub Pages servindo a pasta
`docs/` da branch `main`.

1. Ative uma vez: Settings → Pages → Source = "Deploy from a branch" →
   branch `main`, pasta `/docs`.
2. Sempre que quiser atualizar o grafo publicado:
   ```bash
   bash scripts/publicar_viz.sh
   ```
   Isso roda `kedro viz build` e copia o resultado pra `docs/`.
3. **Antes de commitar**, confira se o build não embutiu prévia de linhas
   dos datasets (licença CC BY-NC-SA do Olist — ver `PLANO.md` §3.0):
   ```bash
   grep -rl '"preview": [^n]' docs/api/nodes/ || echo "ok, nenhum preview embutido"
   ```
4. `git add docs && git commit && git push` — o Pages atualiza sozinho em
   ~1 min.

O link publicado é o principal entregável pós-aula: os alunos exploram o
grafo do projeto sem instalar nada.

---

## Para quem assistiu a aula

Bem-vindo(a) de volta. Aqui você encontra:

- **[`material-aluno/cheatsheet.md`](material-aluno/cheatsheet.md)** — os
  comandos e conceitos essenciais, em 1 página.
- **[`material-aluno/glossario.md`](material-aluno/glossario.md)** — os
  termos usados na aula, explicados em linguagem de negócio.
- **[`material-aluno/leituras.md`](material-aluno/leituras.md)** — para onde
  ir se quiser se aprofundar.
- **O grafo interativo do projeto (Kedro-Viz)** — link compartilhado no chat
  da aula.
- **Todo o código do projeto de demonstração** — em
  [`projeto/olist_analytics/`](projeto/olist_analytics/).

---

## Para quem chegou aqui por curiosidade

Este repositório é material didático de uma imersão em Kedro — não é uma
aplicação em produção. Contém:

- `antes/` — um script de análise "ruim" de propósito, usado para instalar o
  problema que o Kedro resolve.
- `projeto/olist_analytics/` — um projeto Kedro 1.5 completo e funcional, com
  5 pipelines, catálogo de dados em 7 camadas, parâmetros de negócio e hooks
  de qualidade de dados.
- `slides/`, `roteiros/`, `material-aluno/` — o material da aula em si.

O desenho completo (narrativa, decisões de arquitetura, riscos) está em
[`PLANO.md`](PLANO.md).

## Licença e dados

O dataset usado é o **Brazilian E-Commerce Public Dataset by Olist**
(Kaggle), sob licença **CC BY-NC-SA 4.0**. *Usar* o dataset numa aula é uso
legítimo do que ele foi publicado para fazer; *redistribuir* dados ou
derivados exigiria atender às condições da licença (atribuição, uso não
comercial, mesma licença) — por isso a política deste repositório é **nunca
versionar nenhum arquivo de dado**, nem bruto, nem amostra, nem saída de
relatório. Detalhes em [`PLANO.md` §3.0](PLANO.md).

Atribuição: *Brazilian E-Commerce Public Dataset by Olist (Kaggle),
CC BY-NC-SA 4.0.*

O código deste repositório (slides, roteiros, projeto Kedro de exemplo) é
material didático — sem licença de reuso declarada além do uso educacional
pretendido.
