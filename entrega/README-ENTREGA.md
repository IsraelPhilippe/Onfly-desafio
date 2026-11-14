# Entrega técnica — Onfly Report

## 1. Objetivo e resultado

O desafio consistiu em corrigir um CLI Python que consolida reservas de hotéis em um relatório JSON, preservando o contrato de execução, as regras de negócio e os arquivos fornecidos pela Onfly.

**Resultado registrado na execução local:** os cinco testes fornecidos e quatro testes adicionais passaram juntos (`9 passed`); a amostra oficial gerou os resultados esperados; o arquivo principal teve suas 300 reservas processadas; e `python -m ruff check src tests` retornou `All checks passed!`.

Esses resultados foram obtidos e informados pelo candidato em seu ambiente local Windows/PowerShell. Não são apresentados como execução de CI no GitHub.

## 2. Defeitos corrigidos e respectivas causas-raiz

| Arquivo | Defeito identificado | Causa-raiz (uma frase) | Correção aplicada |
|---|---|---|---|
| `src/onfly_report/services/currency_converter.py` | Conversão para BRL produzia valores incorretos. | A implementação dividia o valor pela taxa de câmbio e convertia `Decimal` em `float`, contrariando a regra de conversão e comprometendo a precisão. | Passou a utilizar `return amount * rate`, preservando `Decimal`. |
| `src/onfly_report/services/stay_calculator.py` | Reservas na virada do mês podiam gerar noites negativas. | O cálculo subtraía apenas os números dos dias (`checkout.day - checkin.day`), ignorando mês e ano. | Passou a utilizar `(checkout - checkin).days * rooms`. |
| `src/onfly_report/services/status_policy.py` | Reservas `NO_SHOW` eram incluídas nos valores e noites. | A condição `status != "CANCELLED"` considerava faturável qualquer reserva não cancelada. | Passou a utilizar `status == "CONFIRMED"`. |
| `src/onfly_report/services/report_builder.py` | O ranking exibia hotéis de menor faturamento primeiro. | A ordenação crescente usava o montante positivo como primeiro critério, invertendo a prioridade exigida pelo relatório. | A chave passou a ser `(-item[1]["amount"], item[0])`: valor decrescente e ID crescente em caso de empate. |
| `src/onfly_report/repositories/csv_reservation_repository.py` | O relatório principal processava somente 200 das 300 reservas. | Um `if len(rows) == 200: break` interrompia antecipadamente a leitura do CSV. | Removeu-se o limite artificial, permitindo ler todas as linhas. |

Nenhum teste original nem os arquivos `data/reservas_hoteis.csv` e `data/taxas_cambio.csv` foram alterados.

## 3. Como o problema foi investigado

1. **Leitura do contrato:** estudo do `README.md`, do formato JSON, das regras de status, noites, câmbio, agregação e ordenação, além da estrutura das pastas `src/`, `tests/`, `data/` e `entrega/`.
2. **Reprodução dos defeitos:** execução inicial de `python -m pytest -q`, que resultou em **5 falhas**. As diferenças observadas incluíam conversão monetária de `118.45` versus `642.00`, noites `-28` versus `3`, faturamento com `NO_SHOW` de `120.00` versus `100.00` e ranking em ordem invertida.
3. **Investigação por responsabilidade:** localização e leitura da função responsável por cada falha; comparação da implementação com a regra de negócio; correção pontual; e execução do teste correspondente, antes de avançar.
4. **Regressão integrada:** após as quatro primeiras correções, os cinco testes originais passaram. Foi então executado o programa com `data/reservas_hoteis.csv`, revelando o truncamento de leitura que os testes pequenos não detectavam.
5. **Teste adicional para o defeito não coberto:** após remover o limite, foi criado um caso com **201 reservas**, o menor conjunto capaz de revelar a antiga interrupção na linha 200.
6. **Cobertura adicional e verificações de execução:** foram testados o desempate de hotéis, o limite `--top`, o momento do arredondamento, `ROUND_HALF_UP`, o argumento `--top 0` e o caminho inexistente de entrada.
7. **Qualidade de código:** `python -m ruff check src tests` detectou uma organização de import em um teste novo; após o ajuste de espaçamento, retornou `All checks passed!`.

A abordagem foi corrigir causas identificadas, preservar a arquitetura existente e acrescentar testes somente onde ajudassem a proteger requisitos não cobertos.

## 4. Testes adicionais

| Arquivo / função | Cenário validado |
|---|---|
| `tests/test_all_reservations.py` / `test_process_all_reservations` | CSV com 201 reservas deve produzir `total_reservations == 201`. |
| `tests/test_hotel_tiebreaker.py` / `test_hotel_tiebreaker` | Hotéis de mesmo valor devem ser ordenados por `hotel_id` crescente; com `top=2`, devem retornar H01 e H02. |
| `tests/test_financial_rounding.py` / `test_round_only_after_sum` | Duas reservas de BRL `0.005` devem somar exatamente e resultar em `"0.01"`, não em `"0.02"`. |
| `tests/test_financial_rounding.py` / `test_round_half_up` | Uma reserva de BRL `0.005` deve arredondar para `"0.01"` com `ROUND_HALF_UP`. |

Os novos testes reaproveitam `run_cli()` em `tests/helpers.py` e não modificam a suíte fornecida.

## 5. Resultados de validação

### 5.1 Suíte e análise estática

```text
python -m pytest -q
9 passed

python -m ruff check src tests
All checks passed!
```

Registro da execução local informada pelo candidato após as correções.

### 5.2 Arquivo principal (`data/reservas_hoteis.csv`)

| Indicador | Antes da remoção do limite | Depois |
|---|---:|---:|
| Reservas contabilizadas | 200 | 300 |
| Confirmadas | 153 | 235 |
| Noites de quarto | 909 | 1347 |
| Total em BRL | 249543.79 | 396170.00 |

Saída final registrada:

```text
Reservas: 300 | Confirmadas: 235 | Noites: 1347 | Total BRL: 396170.00
```

### 5.3 Amostra oficial (`data/exemplo-validacao.csv`)

| Campo | Valor obtido / esperado |
|---|---:|
| `total_reservations` | 12 |
| `confirmed_reservations` | 9 |
| `cancelled_reservations` | 2 |
| `no_show_reservations` | 1 |
| `total_room_nights` | 28 |
| `total_amount_brl` | `"7566.00"` |
| `average_nightly_rate_brl` | `"270.21"` |

`by_month`: janeiro de 2025 com 8 reservas, 25 noites e `"6684.00"`; fevereiro de 2025 com 1 reserva, 3 noites e `"882.00"`.

`top_hotels`: H01 (`"1200.00"`), H02 (`"1084.00"`), H12 (`"1000.00"`), H10 (`"900.00"`) e H09 (`"882.00"`), na ordem exigida.

O arquivo JSON produzido apresentou `report_version` igual a `"1.0"` e timestamp com offset `-03:00`. Um problema de exibição de caracteres acentuados no terminal foi resolvido pela leitura com `Get-Content -Encoding UTF8 -Raw`, sem alteração do JSON.

### 5.4 Argumentos e arquivos inválidos

- `--top 0` apresentou mensagem de validação e retornou **código 2**.
- Caminho de CSV inexistente apresentou erro de entrada e retornou **código 2**.

Outros cenários de erro, como falhas inesperadas de escrita, não foram exaustivamente testados nesta investigação.

## 6. Como reproduzir

Executar na raiz do projeto com Python **3.11 ou superior**.

### PowerShell (Windows)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
$env:PYTHONPATH = "src"
python -m pytest -q
python -m ruff check src tests
python -m onfly_report --input data/exemplo-validacao.csv --rates data/taxas_cambio.csv --output output/exemplo.json
Get-Content .\output\exemplo.json -Encoding UTF8 -Raw
python -m onfly_report --input data/reservas_hoteis.csv --rates data/taxas_cambio.csv --output output/report.json
```

### Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
PYTHONPATH=src python -m pytest -q
python -m ruff check src tests
PYTHONPATH=src python -m onfly_report --input data/reservas_hoteis.csv --rates data/taxas_cambio.csv --output output/report.json
```

## 7. Uso de inteligência artificial

Houve uso de **ChatGPT (OpenAI, modelo GPT-6)** como tutor técnico, para explicações, investigação guiada, revisão de soluções, elaboração orientada de testes e auxílio na documentação. O candidato analisou o código, propôs ou implementou alterações, executou os comandos em seu ambiente e verificou os resultados. A assistência incluiu exemplos e trechos de código; não se declara que a execução foi inteiramente independente.

Documentação específica em [`uso-de-ia/declaracao.md`](uso-de-ia/declaracao.md) e registro consolidado de prompts e respostas em [`uso-de-ia/sessao.md`](uso-de-ia/sessao.md).
