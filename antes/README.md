# `analise_olist.py` — o pecado original

Este é o material do **primeiro bloco de demonstração** da imersão (Encontro 1,
0:15–0:50 — o bloco mais importante das 6 horas, segundo `PLANO.md`). É um
script realista, do tipo que existe em produção em qualquer empresa: feito sob
pressão, funcional, e impossível de manter.

**Não conserte este script.** Ele existe exatamente como está — inclusive o
comentário datado e o `# TODO` de dois anos atrás são intencionais.

## Como demonstrar

1. Rode direto, sem alterar nada:
   ```bash
   python antes/analise_olist.py
   ```
   Ele **vai falhar** com `FileNotFoundError` — o caminho da linha 14 é da
   máquina de quem escreveu o script, não da sua. Esse é o primeiro momento da
   aula: "rodou na máquina de quem fez, na sua não roda".

2. Corrija a `PASTA` na linha 14 para apontar para a amostra local
   (`dados/raw/` ou a saída de `preparar_amostra.py`) e rode de novo — agora
   funciona e imprime os números. Use isso para mostrar que o problema **não é
   o código estar errado**, é ele ser frágil e opaco.

## Os quatro defeitos — e o que cada um custa

Cada linha abaixo é uma das "4 dores" que estruturam a imersão inteira
(`PLANO.md` §1.2). Volte a este mapeamento sempre que introduzir o recurso
correspondente do Kedro.

### 1 — Caminho hardcoded (linha 14, usado nas linhas 16–23)

```python
PASTA = "C:/Users/everton/Downloads/olist/"
```

Custa: o script só roda na máquina de quem escreveu. Ninguém mais reproduz a
análise sem editar código. **Resolvido por:** Data Catalog (Encontro 1, bloco 5).

### 2 — Constantes de negócio espalhadas (linhas 27, 43, 56/57, 76–78, 89, 106)

O ano da análise (`2017`), o corte de frete (`0.5`), a nota que define
insatisfação (`<= 2`) e a proporção de teste (`0.25`, no bloco comentado)
aparecem soltos pelo arquivo, sem um lugar único. Mudar "vamos olhar 2018
também" exige caçar e editar em vários pontos — e é fácil esquecer um.
**Resolvido por:** `parameters.yml` (Encontro 2, bloco 3).

### 3 — Tudo em sequência, nada em função (o arquivo inteiro)

Não há uma única `def`. Para rodar só a parte do modelo (linhas 86–92,
comentadas), é preciso rodar tudo acima de novo — o comentário da linha 121
confirma que quem escreveu sabia disso e não teve tempo de resolver.
**Resolvido por:** Nodes e Pipelines, com execução seletiva via
`--from-nodes` (Encontro 2, bloco 2).

### 4 — Origem do número final ilegível (linhas 94–108)

`taxa_ruim`, o número que vai para o slide da diretoria, vem de
`df_final_v2`, que veio de `df_final2`, que veio de `df_final`, que veio de
`df3`, que veio de `df.merge(df2, ...)`. Não há como responder "de onde veio
esse número" sem ler o arquivo inteiro de trás para frente — e o comentário da
linha 110 mostra que nem quem escreveu tinha certeza. **Resolvido por:**
Kedro-Viz e a linhagem de dados (Encontro 2, bloco 4).

## Bônus — sinais de um script em sofrimento

Úteis para apontar rapidamente durante a demo, sem parar muito tempo em cada um:

- Nomes de variável (`df`, `df2`, `df3`, `df_final`, `df_final_v2`) que não
  dizem o que contêm.
- Bloco de modelo comentado com instrução manual (`# descomentar pra rodar`) —
  sintoma de que rodar tudo de novo é caro demais para deixar ligado.
- Decisão de negócio registrada em comentário e não em configuração:
  *"tirei os pedidos cancelados manualmente olhando o excel, deve ter uns 200"*
  (linha 76) — um número aproximado, sem validação, decidindo o que entra ou
  não no relatório da diretoria.
- Saída (`resultado.xlsx`) escrita na pasta corrente, sem controle de versão —
  rodar duas vezes sobrescreve sem aviso.

## Números reais (para reaproveitar nos slides)

Calculados sobre a amostra 2017 completa, para conferência:

- Taxa geral de review ruim: **14,68%**
- Ticket médio: **R$ 178,54**

Se os slides usarem números deste script, confirme que batem com os do
projeto Kedro final — as regras de negócio (período, corte de frete, corte de
nota) precisam ser as mesmas dos dois lados.
