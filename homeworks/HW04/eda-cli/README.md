# S04 – eda_cli: мини-EDA для CSV

Небольшое CLI-приложение для базового анализа CSV-файлов.
Используется в рамках Семинара 03 курса «Инженерия ИИ».

## Требования

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) установлен в систему

## Инициализация проекта

В корне проекта (S03):

```bash
uv sync
```

Эта команда:

- создаст виртуальное окружение `.venv`;
- установит зависимости из `pyproject.toml`;
- установит сам проект `eda-cli` в окружение.

## Запуск CLI

### Краткий обзор

```bash
uv run eda-cli overview data/example.csv
```

Параметры:

- `--sep` – разделитель (по умолчанию `,`);
- `--encoding` – кодировка (по умолчанию `utf-8`).

### Полный EDA-отчёт

```bash
uv run eda-cli report data/example.csv --out-dir reports
```

В результате в каталоге `reports/` появятся:

- `report.md` – основной отчёт в Markdown;
- `summary.csv` – таблица по колонкам;
- `missing.csv` – пропуски по колонкам;
- `correlation.csv` – корреляционная матрица (если есть числовые признаки);
- `top_categories/*.csv` – top-k категорий по строковым признакам;
- `hist_*.png` – гистограммы числовых колонок;
- `missing_matrix.png` – визуализация пропусков;
- `correlation_heatmap.png` – тепловая карта корреляций.

## Тесты

```bash
uv run pytest -q
```

##  Новые функции 

Команда `report` поддерживает дополнительные параметры:

- `--title TEXT` — для создания собственного заголовка отчета
- `--top-k-categories INT` — для количества топ-значений у категориальных признаков
 `--json-summary` — сохраняет краткую сводку в `summary.json`
Пример:
```bash
uv run eda-cli report data/example.csv --title "Анализ клиентов" --top-k-categories 3 --out-dir my_report
uv run eda-cli report data/example.csv --title "Анализ клиентов" --top-k-categories 3 --json-summary --out-dir my_report
```

### Команда `head`

Показывает первые N строк датасета.

```bash
uv run eda-cli head data/example.csv --n 5
```


- `category_distribution.png` –  горизонтальный bar-chart с градиентной раскраской для самой частой категориальной колонки.


## HTTP API

Проект также предоставляет REST API на базе FastAPI.

### Запуск сервера

```bash
uv run uvicorn eda_cli.api:app --reload --port 8000
```
### Эндпоинты

Проверка работоспособности сервиса.

GET /health
```bash
curl http://localhost:8000/health
```

Оценка качества датасета по CSV-файлу.

POST /quality-from-csv
```bash
curl -F "file=@data/example.csv" http://localhost:8000/quality-from-csv
```

Возвращает первые N строк датасета.

POST /head-from-csv
```bash
curl -F "file=@data/example.csv" -F "n=3" http://localhost:8000/head-from-csv
```

Статистика по работе сервиса.

GET /metrics
```bash
curl http://localhost:8000/metrics
```
