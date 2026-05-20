import pandas as pd
import numpy as np
from pathlib import Path


def generate_credit_data(num_samples: int = 1000):
    """Генерирует синтетический датасет для задачи кредитного скоринга."""
    np.random.seed(42)
    data = {
        'age': np.random.randint(18, 70, num_samples),
        'income': np.random.randint(30000, 150000, num_samples),
        'employment_years': np.random.randint(0, 25, num_samples),
        'loan_amount': np.random.randint(1000, 50000, num_samples),
        'credit_score': np.random.randint(300, 850, num_samples),
    }
    df = pd.DataFrame(data)
    risk = (df['loan_amount'] / df['income']) * 1000 - df['credit_score']
    threshold = np.percentile(risk, 70)
    df['target'] = (risk > threshold).astype(int)
    output_path = Path(__file__).resolve().parent.parent / "data" / "credit_risk_data.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)


if __name__ == "__main__":
    generate_credit_data()
