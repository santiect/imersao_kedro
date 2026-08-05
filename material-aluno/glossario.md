# Glossário — Imersão Kedro

Vocabulário explicado em linguagem de negócio, não de engenharia. Pensado
para quem assistiu à aula e quer relembrar um termo sem reabrir o vídeo.

**Camada de dados**
Um estágio na jornada do dado, do bruto até o pronto para consumo — como um
estoque que passa por recebimento, triagem e expedição. Cada camada tem um
propósito claro, e dado de uma camada nunca se mistura com dado de outra.

**Catálogo de dados (Data Catalog)**
O "índice" do projeto: um arquivo que lista todo dado usado, dizendo onde
está e em que formato. Substitui a prática de deixar caminhos de arquivo
espalhados dentro do código.

**DAG (grafo sem ciclos)**
A forma de um pipeline: uma sequência de etapas que nunca volta pra trás.
Garante que não existe uma etapa que depende de si mesma — o processo sempre
tem começo, meio e fim definidos.

**Dataset**
Qualquer fonte ou destino de dado que o projeto usa — uma planilha, uma
tabela de banco, um arquivo na nuvem. No Kedro, cada um tem um nome e uma
entrada no catálogo.

**Dataset versionado**
Uma configuração em que cada execução salva uma cópia nova, com data e hora,
sem apagar a anterior. Permite comparar "o relatório de hoje" com "o
relatório de terça passada" sem perder nenhum dos dois.

**Framework**
Uma estrutura de trabalho pronta que organiza como o código deve ser escrito,
para que times diferentes produzam projetos parecidos entre si — como um
formulário padrão, em vez de cada um escrever do seu jeito.

**Governança de dados**
A capacidade de responder, com confiança, perguntas como "de onde veio esse
número" e "quem pode ver esse dado". Um projeto bem estruturado tem
governança embutida na própria organização do código.

**Hook**
Um ponto de checagem automática dentro da execução — como um controle de
qualidade numa linha de produção, que barra o produto antes de ele sair da
fábrica com defeito.

**Kedro-Viz**
A ferramenta que desenha o pipeline como um mapa visual e clicável — permite
ver todo o caminho do dado, da fonte ao relatório, sem ler uma linha de
código.

**Linhagem de dados (data lineage)**
O rastro completo de um número: de qual fonte ele veio, por quais
transformações passou, até chegar no relatório final. É a resposta direta
para "de onde veio esse número".

**Node (nó)**
Uma etapa isolada de processamento — por exemplo, "calcular o prazo de
entrega". Cada nó faz uma coisa só, o que facilita testar, reaproveitar e
substituir sem afetar o resto.

**Notebook**
Um formato de documento interativo (ex.: Jupyter) que mistura código,
resultado e texto na mesma tela. Ótimo para explorar uma ideia; frágil para
sustentar um processo que precisa rodar sempre do mesmo jeito — por isso esta
imersão não usa notebook.

**Open source (código aberto)**
Software cujo código é público e pode ser usado, inspecionado e modificado
por qualquer pessoa. O Kedro é mantido por uma fundação (Linux Foundation),
não por uma única empresa.

**Parâmetro**
Um número ou critério de negócio (ex.: "nota mínima para considerar um
cliente insatisfeito") guardado num arquivo de configuração, não dentro do
código. Trocar um parâmetro não exige entender ou editar a lógica do
programa.

**Pipeline**
Uma sequência de nós encadeados que, juntos, transformam dado bruto em
resultado final. É possível ter vários pipelines no mesmo projeto, cada um
com um propósito.

**Pipeline modular / nomeado**
Um pipeline menor, com um nome próprio, que pode ser executado sozinho —
por exemplo, rodar só a parte de "relatório" sem refazer a parte de
"modelagem".

**Reprodutibilidade**
A garantia de que o mesmo processo, rodado de novo, chega no mesmo resultado
— ou, se o dado mudou, chega num resultado diferente de forma rastreável, não
por acaso.

**REPL (terminal interativo)**
Uma forma de rodar comandos um de cada vez e ver o resultado na hora, sem
salvar num arquivo — o `kedro ipython` usado na imersão é isso, e não deve
ser confundido com notebook.

**Runner / execução**
O ato de efetivamente rodar um pipeline. O Kedro decide sozinho a ordem
correta de execução dos nós, a partir de quem depende de quem.

**Versionamento (de código)**
A prática de guardar o histórico de mudanças de um projeto (normalmente via
Git), permitindo voltar a qualquer versão anterior e ver exatamente o que
mudou e quando.
