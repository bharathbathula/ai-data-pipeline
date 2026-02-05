print("Starting test pipeline...")

from app.core.data_loader import load_data
from app.core.eda_engine import run_eda

print("Imports successful")

df = load_data("data/raw/sample_eda_data.csv")
print("Dataset loaded")

eda = run_eda(df)
print("EDA computed")

print("EDA OUTPUT:")
print(eda)
