# BASIC scanner e parser

## Como rodar

para rodar o scanner e o parser, basta rodar  o arquivo `main.py`  como um módulo, passando como parâmetros o caminho para o arquivo de tokens e de entrada.

```shell
python -m src.main --token-file <caminho para o arquivo de tokens> --input-file <caminho para o arquivo de entrada>
```

Temos um arquivo de exemplo de entrada e de token, na pasta `examples`. Para rodar este exemplo, basta executar o comando abaixo:

```shell
python -m src.main --token-file ./examples/example1/tokens.txt --input-file examples/example1/input.txt
```

Ou se preferir, basta utilizar o comando Make:

```shell
make example1
```

Ao rodar o programa, ele irá parsear o arquivo de tokens e o arquivo de entrada, converter os tokens em automatos, unificar estes  automatos e gerar um scanner para o conteúdo da entrada. Em seguida, o programa instanciará o Parser utilizando o scanner gerado na etapa anterior e converterá os tokens em uma AST (Abstract Syntax Tree). Está árvore será impressa na saída padrão. Se desejar, você pode fazer *pipe* desta saída para um arquivo, para melhorar a visualização:

```shell
make example1 > ./ast.txt
```

Caso o programa possua algum erro (léxico ou sintático), estes erros são armazenados pelo scanner e pelo parser, e impressos no final da execução do programa.

## Especificação do arquivo de tokens

O arquivo de tokens é composto de blocos de três linhas, separados por uma linha em branco, no seguinte formato:

```txt
REGEX1
TYPE1
PRIORITY1

REGEX2
TYPE2
PRIORITY2
```

A primeira linha é a regex do token, a segunda o seu tipo e a terceira a prioridade. A prioridade deve ser, obrigatoriamente, `HIGH`, `MEDIUM` ou `LOW`. Aconselhamos utilizar apenas `HIGH` para tokens de palavras reservadas e `LOW` para demais palavras: a prioridade `MEDIUM` foi criada mais como uma garantia futura do que de fato por necessidade.

## Especificação do arquivo de entrada

O arquivo de entrada deve ser um programa na linguagem BASIC, e cada linha deve ter, **obrigatoriamente** um número como primeiro token. Exemplo de programa em BASIC:

```BASIC
10 PRINT "HELLO WORLD"
20 LET A = 10
30 PRINT
```

