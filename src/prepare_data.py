
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUTPUTS = ROOT / "outputs"
OUTPUTS.mkdir(exist_ok=True)

files = list(DATA.glob("*.xlsx")) + list(DATA.glob("*.xls"))

if not files:
    raise FileNotFoundError(
        "Put the Sample Superstore Excel workbook inside the data folder."
    )

file = files[0]
df = pd.read_excel(file)

# Standardize column names
df.columns = [str(c).strip() for c in df.columns]

# Validate required fields
required = ["Order Date", "Sales", "Profit"]
missing = [c for c in required if c not in df.columns]

if missing:
    raise ValueError(
        f"Missing columns: {missing}. "
        f"Available columns: {list(df.columns)}"
    )

# Clean and validate data
df["Order Date"] = pd.to_datetime(
    df["Order Date"], errors="coerce"
)
df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")
df["Profit"] = pd.to_numeric(df["Profit"], errors="coerce")

before = len(df)
df = df.dropna(
    subset=["Order Date", "Sales", "Profit"]
).drop_duplicates().copy()

# Create monthly reporting fields
df["Order Month"] = (
    df["Order Date"].dt.to_period("M").dt.to_timestamp()
)

df.to_csv(OUTPUTS / "sales_clean.csv", index=False)

# Aggregate monthly performance
monthly = (
    df.groupby("Order Month", as_index=False)
    .agg(
        Revenue=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order ID", "nunique"),
    )
    .sort_values("Order Month")
)

monthly["Profit Margin %"] = (
    monthly["Profit"] / monthly["Revenue"].replace(0, float("nan")) * 100
)

monthly["MoM Growth %"] = (
    monthly["Revenue"].pct_change() * 100
)

monthly.to_csv(
    OUTPUTS / "monthly_performance.csv", index=False
)

print("Data preparation completed successfully.")
print(f"Source file: {file.name}")
print(f"Rows before cleaning: {before:,}")
print(f"Rows after cleaning: {len(df):,}")
print(
    f"Date range: {df['Order Date'].min().date()} "
    f"to {df['Order Date'].max().date()}"
)
print(f"Cleaned data: {OUTPUTS / 'sales_clean.csv'}")
print(f"Monthly summary: {OUTPUTS / 'monthly_performance.csv'}")
