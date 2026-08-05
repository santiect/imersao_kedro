# Ambiente — guia de instalação

Para o instrutor. Alvo: ambiente pronto e validado **até 3 dias antes** do
primeiro encontro (ver checklist em [PLANO.md](../PLANO.md) §10).

## Requisitos

- Python **3.10 a 3.14** (faixa suportada pelo Kedro 1.5). Este projeto foi
  validado com **3.12**.
- Acesso à internet para instalar pacotes.

## Passo a passo

### Linux / macOS

Se você tem Python 3.12 disponível:

```bash
cd imersao_kedro
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r ambiente/requirements.txt
```

Se **não** tem Python 3.12 instalado no sistema, use
[`uv`](https://docs.astral.sh/uv/) — ele baixa o interpretador sozinho, sem
precisar de `sudo` nem de pacotes do sistema operacional:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh   # se ainda não tiver uv
cd imersao_kedro
uv venv .venv --python 3.12
uv pip install --python .venv/bin/python -r ambiente/requirements.txt
source .venv/bin/activate
```

### Windows (PowerShell)

```powershell
cd imersao_kedro
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r ambiente/requirements.txt
```

Sem Python 3.12 instalado, o caminho equivalente com `uv`:

```powershell
irm https://astral.sh/uv/install.ps1 | iex
uv venv .venv --python 3.12
uv pip install --python .venv\Scripts\python.exe -r ambiente\requirements.txt
.venv\Scripts\Activate.ps1
```

## Validação

Com o ambiente ativado:

```bash
kedro info
```

Deve mostrar:

```
v1.5.0
Installed plugins:
kedro_mlflow: 2.0.3
kedro_viz: 12.4.0
```

Se as versões vierem diferentes, **não prossiga** sem revisar
`ambiente/requirements.txt` contra `PLANO.md` §2 — a API do Kedro muda entre
versões e o material foi escrito para 1.5.0 especificamente.

## Problemas comuns

**Python fora da faixa 3.10–3.14**
O `pip install` falha na resolução de dependências do `kedro`. Instale uma
versão suportada (o caminho `uv venv --python 3.12` acima resolve sem exigir
instalação manual de um Python novo).

**Falha ao compilar `pyarrow`**
Geralmente falta de wheel pré-compilada para sua plataforma/arquitetura. Em
Linux, verificar se está numa distro/arquitetura incomum (ex.: ARM em
container antigo). Solução mais rápida: usar `uv`, que resolve wheels de forma
mais robusta que `pip` puro.

**`externally-managed-environment` (Debian/Ubuntu recentes)**
O `pip install` no Python do sistema recusa instalar pacotes fora de um
ambiente virtual (PEP 668). **Sempre** use um venv (`python3 -m venv .venv` ou
`uv venv`) — nunca `--break-system-packages`.

**Porta 4141 ocupada (Kedro-Viz)**
`kedro viz run` usa a porta 4141 por padrão. Se estiver ocupada:
```bash
kedro viz run --port 4142
```

**Telemetria do Kedro**
Na primeira execução, o Kedro pede consentimento para telemetria anônima. Para
não interromper a demo ao vivo, decida com antecedência:
```bash
# desativar
echo "consent: false" > .telemetry
```

**`kedro ipython` reclama que não acha o executável `ipython`**
Sintoma: `FileNotFoundError: [Errno 2] No such file or directory: 'ipython'`.
`kedro ipython` chama o binário `ipython` via subprocesso — se você invocar o
`kedro` pelo caminho completo (`.venv/bin/kedro ...`) sem ativar o ambiente, o
`.venv/bin` não está no `PATH` e a chamada falha. Sempre **ative o venv**
(`source .venv/bin/activate`) antes de rodar `kedro ipython` ao vivo.
