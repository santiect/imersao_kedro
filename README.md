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
   exportar em PDF:
   ```bash
   npx @marp-team/marp-cli slides/aula.md --pdf --allow-local-files --theme-set slides/tema/imersao.css
   ```

Antes de ensaiar, leia [`PLANO.md`](PLANO.md) inteiro — é o desenho completo
da aula (agenda, narrativa, riscos, checklist de pré-produção em §9).

### Publicar o Kedro-Viz (opcional)

Existe um workflow pronto (`.github/workflows/publicar-viz.yml`) que gera e
publica o grafo interativo no GitHub Pages. Ele **não roda sozinho** — para
ativar:

1. Vá em Settings → Pages e habilite GitHub Pages para o repositório.
2. Vá em Settings → Secrets and variables → Actions e cadastre
   `KAGGLE_USERNAME` e `KAGGLE_KEY` (sua chave de API do Kaggle, gerada em
   kaggle.com/settings).
3. Vá na aba Actions → "Publicar Kedro-Viz" → "Run workflow".

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
