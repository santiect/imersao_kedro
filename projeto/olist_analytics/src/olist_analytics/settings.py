"""Project settings. There is no need to edit this file unless you want to change values
from the Kedro defaults. For further information, including these default values, see
https://docs.kedro.org/en/stable/configure/configuration_basics/#configuration"""

# Instantiated project hooks.
# Hooks are executed in a Last-In-First-Out (LIFO) order.
from olist_analytics.hooks import MetricaModeloHook, QualidadeDadosHook, RelatorioExecucaoHook

HOOKS = (RelatorioExecucaoHook(), QualidadeDadosHook(), MetricaModeloHook())

# Installed plugins for which to disable hook auto-registration.
#
# kedro-mlflow se auto-registra e, com o MLflow 3.x, tenta inicializar um
# tracking client de arquivo (./mlruns) que o MLflow recusa por padrão desde a
# versão 3 (backend de arquivo em modo de manutenção — ver
# https://mlflow.org/docs/latest/self-hosting/migrate-from-file-store).
# Isso quebraria TODO `kedro run`, mesmo sem nenhum node usando MLflow.
#
# Como o kedro-mlflow entra na imersão só como panorama de ~5 min (Encontro 2,
# menção rápida — ver PLANO.md e roteiros/encontro-02.md), o hook fica
# desativado por padrão. Para a demo pontual de MLflow, reative manualmente
# (comente a linha abaixo) com um mlflow.yml configurado — ver
# roteiros/encontro-02.md para o passo a passo isolado.
DISABLE_HOOKS_FOR_PLUGINS = ("kedro_mlflow",)

# Class that manages the KedroSession.
# from kedro.framework.session import KedroSession
# SESSION_CLASS = KedroSession

# Class that manages storing KedroSession data.
# from kedro.framework.session.store import BaseSessionStore
# SESSION_STORE_CLASS = BaseSessionStore
# Keyword arguments to pass to the `SESSION_STORE_CLASS` constructor.
# SESSION_STORE_ARGS = {
#     "path": "./sessions"
# }

# Directory that holds configuration.
# CONF_SOURCE = "conf"

# Class that manages how configuration is loaded.
# from kedro.config import OmegaConfigLoader

# CONFIG_LOADER_CLASS = OmegaConfigLoader

# Keyword arguments to pass to the `CONFIG_LOADER_CLASS` constructor.
CONFIG_LOADER_ARGS = {
    "base_env": "base",
    "default_run_env": "local",
    # "config_patterns": {
    #     "spark" : ["spark*/"],
    #     "parameters": ["parameters*", "parameters*/**", "**/parameters*"],
    # }
}

# Class that manages Kedro's library components.
# from kedro.framework.context import KedroContext
# CONTEXT_CLASS = KedroContext

# Class that manages the Data Catalog.
# from kedro.io import DataCatalog
# DATA_CATALOG_CLASS = DataCatalog
