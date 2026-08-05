# Plano B — protocolo de falha ao vivo

Uma página. Print isso ou deixe aberto numa aba fixa durante a aula.

## Árvore de decisão

```
Demo falhou na tela?
│
├─ É a primeira vez que falha nesta aula?
│  ├─ SIM → tente 1x corrigir ao vivo (30s no máximo, cronometrado)
│  │        funcionou? → continue normalmente
│  │        não funcionou? → vá para "Cortar para vídeo" abaixo
│  │
│  └─ NÃO (já tentou corrigir antes) → vá direto para "Cortar para vídeo"
│
└─ É uma falha ESPERADA (script antes/, hook de qualidade)?
   → não é falha, é a demo funcionando. Siga o roteiro normalmente.
```

## Cortar para vídeo

1. Diga em voz alta, sem se desculpar longamente: *"vou usar a gravação que
   preparei pra esse passo, pra gente não perder tempo"*.
2. Abra a aba B (preparada com os vídeos already carregados).
3. Toque o vídeo correspondente ao bloco (ver tabela abaixo).
4. Ao terminar o vídeo, volte para a aba A e siga o roteiro a partir do
   próximo comando — não tente retomar o comando que falhou.

## Vídeos de backup a gravar (antes da aula)

Grave cada um em 2–5 min, com narração, exatamente como sairia ao vivo.
Salve em `roteiros/backup/<nome>.mp4` (pasta local, fora do git — vídeo é
pesado e não precisa ser versionado).

| Bloco | Arquivo | O que grava |
|---|---|---|
| O problema | `backup/01-script-falha.mp4` | Rodar `antes/analise_olist.py` e o erro aparecer |
| Data Catalog | `backup/02-catalog-formato.mp4` | Troca CSV→Excel no `catalog.yml` + `kedro run --pipeline=relatorio` |
| Nodes/Pipelines | `backup/03-from-nodes.mp4` | `kedro run --from-nodes=calcular_receita_mensal` |
| Parameters | `backup/04-parametros.mp4` | Editar `nota_corte_review_ruim` e comparar `review_por_estado.csv` |
| Kedro-Viz | `backup/05-viz-linhagem.mp4` | Abrir o grafo, colorir por camada, subir linhagem até o raw — **o mais importante de gravar bem** |
| Kedro-Viz autoreload | `backup/06-viz-autoreload.mp4` | Editar docstring, salvar, ver atualizar no navegador |
| Hooks | `backup/07-hook-qualidade.mp4` | Período de 1 dia só + `kedro run` falhando com a mensagem do hook |

## Regras gerais

- **Nunca** tente depurar um erro ao vivo por mais de 30 segundos. A plateia
  não ganha nada vendo você resolver um traceback.
- **Nunca** peça desculpas repetidas — uma frase e seguir em frente.
- Se **duas** demos seguidas falharem, é sinal de que o ambiente está com
  problema (não a sorte) — pule direto para os slides do bloco seguinte e
  volte para as demos só se sobrar tempo no fim.
- Depois da aula, **sempre** rode o checklist de encerramento do
  `roteiros/aula.md` para garantir que nenhuma edição ao vivo (parameters.yml,
  catalog.yml) ficou pendurada pro próximo ensaio.
