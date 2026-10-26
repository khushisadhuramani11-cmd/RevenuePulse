
from pathlib import Path
from getpass import getpass

import pandas as pd
from sqlalchemy import create_engine, URL, text

ROOT = Path(__file__).resolve().parents[1]
CSV_FILE = ROOT / "outputs" / "sales_clean.csv"

if not CSV_FILE.exists():
    raise FileNotFoundError(f"CSV not found: {CSV_FILE}")

# Ask for credentials without saving your password in the code.
username = input("MySQL username (usually root): ").strip()
password = getpass("MySQL password: ")

connection_url = URL.create(
    drivername="mysql+pymysql",
    username=username,
    password=password,
    host="localhost",
    port=3306,
    database="revenuepulse",
)

engine = create_engine(connection_url)

try:
    # Verify that the database connection works.
    with engine.connect() as connection:
        print("Connected to MySQL:", connection.execute(
            text("SELECT DATABASE()")
        ).scalar())

    df = pd.read_csv(CSV_FILE)

    # Standardize column names for SQL.
    df.columns = [
        col.strip().lower().replace(" ", "_")
        for col in df.columns
    ]

    # Convert dates to proper date values.
    for col in ["order_date", "ship_date", "order_month"]:
        if col in df.columns:
            df[col] = pd.to_datetime(
                df[col], errors="coerce"
            ).dt.date

    print(f"Rows ready to load: {len(df):,}")
    print("Columns:", df.columns.tolist())

    # IMPORTANT: This replaces the existing sales table.
    # Use only because we are restarting the import after
    # the wizard failed, and do not want a duplicate import.
    confirm = input(
        "Replace revenuepulse.sales with this CSV? Type YES: "
    )

    if confirm != "YES":
        print("Import cancelled. No table was replaced.")
    else:
        df.to_sql(
            name="sales",
            con=engine,
            if_exists="replace",
            index=False,
            chunksize=1000,
        )

        with engine.connect() as connection:
            count = connection.execute(
                text("SELECT COUNT(*) FROM sales")
            ).scalar()

        print(f"Import successful. Rows in MySQL: {count:,}")

finally:
    engine.dispose()
