import pandas as pd
from pathlib import Path


def test_credit_dataset_integrity():
    """Проверяет наличие файла и структуру столбцов сгенерированного датасета."""
    data_path = Path(__file__).resolve().parent.parent / "data" / "credit_risk_data.csv"
    assert data_path.exists(), "Файл датасета credit_risk_data.csv не найден"
    df = pd.read_csv(data_path)
    assert not df.empty, "Датасет пустой"
    assert len(df) == 1000, f"Ожидалось 1000 строк, получено {len(df)}"
    required_columns = ['age', 'income', 'employment_years', 'loan_amount', 'credit_score', 'target']
    for col in required_columns:
        assert col in df.columns, f"Отсутствует обязательная колонка: {col}"
    assert set(df['target'].unique()).issubset({0, 1}), "Колонка target должна содержать только 0 и 1"
