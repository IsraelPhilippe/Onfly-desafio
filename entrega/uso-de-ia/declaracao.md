# Declaração de uso de inteligência artificial

## Ferramenta e modelo

- **Ferramenta:** ChatGPT, da OpenAI.
- **Modelo:** GPT-6.
- **Modalidade de uso:** tutoria interativa e revisão técnica durante a resolução do desafio Onfly Report.
- **Registro:** [`sessao.md`](sessao.md), um log consolidado de prompts e respostas desta conversa; não é exportação integral automática do histórico do produto.

## O que a IA fez

- Explicou o enunciado, a estrutura das pastas, os arquivos Python e o fluxo entre CLI, repositories, models e services.
- Ajudou a interpretar os cinco testes que inicialmente falhavam e a localizar as funções relacionadas às regras de câmbio, noites, status e ranking.
- Forneceu explicações e exemplos de `Decimal`, `date`/`timedelta`, `sorted`, `lambda`, `key`, tuplas, dicionários, list comprehension, `assert`, pytest, Ruff, exceções e códigos de saída.
- Orientou a identificação do limite artificial de 200 registros e sugeriu cenários adicionais de regressão e de fronteira.
- Sugeriu trechos de correção e modelos de testes automatizados, que foram discutidos e aplicados pelo candidato.
- Ajudou a revisar o repositório GitHub e a estruturar este resumo de entrega, a declaração e o log consolidado.

## O que o candidato fez

- Preparou e ativou o ambiente virtual, instalou as dependências e executou os comandos em seu computador usando PowerShell.
- Inspecionou o código, apresentou hipóteses, identificou causas de erros, participou do raciocínio e propôs parte das correções antes de implementá-las.
- Aplicou e salvou as modificações nos cinco arquivos Python relacionados aos defeitos.
- Criou os arquivos de testes adicionais com orientação da IA e executou os testes individualmente e em conjunto.
- Executou o CLI nos arquivos de dados, conferiu o JSON da amostra oficial e validou os códigos de saída para argumentos ou caminhos inválidos.
- Executou o Ruff, corrigiu um ajuste de organização do teste e publicou as alterações no repositório GitHub.
- Ficou responsável por revisar e incluir os documentos finais de entrega no repositório e fornecer o link no formulário do processo seletivo.

## Critério de transparência

O trabalho foi realizado em colaboração com a IA. A declaração não atribui ao candidato autoria exclusiva de todos os trechos sugeridos pelo assistente nem apresenta verificações locais como uma execução de CI. O registro de sessão resume fielmente a interação acessível nesta conversa, mas não pretende ser uma transcrição literal e integral.
