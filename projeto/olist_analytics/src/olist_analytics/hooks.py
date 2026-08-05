"""Hooks do projeto — vitrine curta (Encontro 2, ~20 min), não seção longa.

Dois hooks, cada um com um argumento de negócio direto:

- RelatorioExecucaoHook: "onde meu pipeline gasta tempo" (e, por extensão,
  dinheiro de processamento).
- QualidadeDadosHook: "dado ruim não chega no relatório da diretoria" — barra
  a execução quando a tabela analítica viola uma regra mínima.

Registrados em settings.py.
"""

from __future__ import annotations

import logging
import time

from kedro.framework.hooks import hook_impl
from kedro.pipeline.node import Node

logger = logging.getLogger(__name__)

NOME_TABELA_ANALITICA = "tabela_analitica"
MINIMO_LINHAS_TABELA_ANALITICA = 100


class RelatorioExecucaoHook:
    """Cronometra cada nó e imprime um resumo ao final da execução."""

    def __init__(self) -> None:
        self._inicio: dict[str, float] = {}
        self._duracoes: dict[str, float] = {}

    @hook_impl
    def before_node_run(self, node: Node) -> None:
        self._inicio[node.name] = time.perf_counter()

    @hook_impl
    def after_node_run(self, node: Node) -> None:
        duracao = time.perf_counter() - self._inicio.get(node.name, time.perf_counter())
        self._duracoes[node.name] = duracao

    @hook_impl
    def after_pipeline_run(self) -> None:
        if not self._duracoes:
            return

        mais_lento = max(self._duracoes, key=self._duracoes.get)
        largura_nome = max(len(nome) for nome in self._duracoes)

        print("\n" + "=" * (largura_nome + 20))
        print("RELATÓRIO DE EXECUÇÃO — tempo por nó")
        print("=" * (largura_nome + 20))
        for nome, duracao in sorted(self._duracoes.items(), key=lambda item: -item[1]):
            marcador = "  <-- mais lento" if nome == mais_lento else ""
            print(f"{nome:<{largura_nome}}  {duracao:6.2f}s{marcador}")
        print("=" * (largura_nome + 20) + "\n")

        self._inicio.clear()
        self._duracoes.clear()


class QualidadeDadosHook:
    """Valida a tabela analítica assim que ela é carregada e barra a execução
    se alguma regra mínima de qualidade for violada.

    Demo ao vivo (roteiros/aula.md, bloco de Hooks): editar `periodo.inicio` e
    `periodo.fim` em conf/base/parameters.yml para o mesmo dia (testado:
    "2018-08-31" nos dois campos → 0 linhas) e rodar `kedro run` — a regra de
    volume mínimo dispara e a pipeline para antes de gerar relatório. Uma
    semana inteira (ex. 25 a 31/08) NÃO é suficiente — ainda dá ~223 linhas,
    acima do mínimo. Restaurar os valores originais depois da demo.
    """

    @hook_impl
    def after_dataset_loaded(self, dataset_name: str, data, node: Node) -> None:
        if dataset_name != NOME_TABELA_ANALITICA:
            return

        erros = []

        if data["review_ruim"].isna().any():
            n_nulos = int(data["review_ruim"].isna().sum())
            erros.append(f"coluna alvo 'review_ruim' tem {n_nulos} valor(es) nulo(s)")

        prazos_negativos = data["prazo_entrega_dias"] < 0
        if prazos_negativos.any():
            erros.append(
                f"{int(prazos_negativos.sum())} pedido(s) com prazo de entrega negativo"
            )

        if len(data) < MINIMO_LINHAS_TABELA_ANALITICA:
            erros.append(
                f"apenas {len(data)} linha(s) na tabela analítica "
                f"(mínimo esperado: {MINIMO_LINHAS_TABELA_ANALITICA})"
            )

        if erros:
            mensagem = "Qualidade de dados reprovada em '{}':\n  - {}".format(
                dataset_name, "\n  - ".join(erros)
            )
            logger.error(mensagem)
            raise ValueError(mensagem)

        logger.info("Qualidade de dados OK em '%s' (%d linhas)", dataset_name, len(data))
