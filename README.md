# RevenuePulse

RevenuePulse is a retail analytics project built to turn raw sales data into clean, query-ready insights. It ingests the Sample Superstore Excel file, standardizes and validates the data, creates monthly performance metrics, and loads the cleaned dataset into MySQL for deeper business analysis.

This project is designed for quick, reliable exploratory analysis of revenue trends, profitability, customer segments, product categories, and monthly growth patterns.

## Why this project matters

Retail teams need fast answers to questions like:

- Which months performed best?
- How is revenue trending over time?
- Which categories and sub-categories drive profit?
- How do regions and customer segments compare?
- Are discounts reducing profitability?

RevenuePulse helps answer these questions with a clean and repeatable data pipeline.

## Project highlights

- Automated data cleaning and validation
- Standardized sales and profit calculations
- Monthly revenue, profit, and growth aggregation
- MySQL-ready output for SQL analysis
- Ready-to-use insight queries for business reporting
- Simple setup for local analytics workflows

## Tech stack

- Python
- pandas
- SQLAlchemy
- PyMySQL
- MySQL
- Power BI-compatible outputs

## Project structure

```text
RevenuePulse/
├── data/
│   └── sample_-_superstore.xls
├── outputs/
│   ├── sales_clean.csv
│   └── monthly_performance.csv
├── sql/
│   └── 01_revenue_analysis.sql
├── src/
│   ├── prepare_data.py
│   └── load_to_mysql.py
├── requirements.txt
├── RevenuePulse.pbix
├── README.md
└── .gitignore
```

## Workflow

1. Load the raw sales workbook from the data folder.
2. Clean and validate key fields such as Order Date, Sales, and Profit.
3. Remove invalid rows and duplicates.
4. Generate new monthly reporting fields.
5. Export clean CSV files to the outputs folder.
6. Load the transformed dataset into a MySQL database.
7. Run SQL analysis queries to uncover trends and business performance.

## Data pipeline

The project follows a straightforward ETL flow:

- Input: Excel workbook with sales transactions
- Transformation: data quality checks, date formatting, numeric coercion, deduplication, monthly aggregation
- Output: CSVs and a MySQL sales table
- Analysis: SQL queries for KPIs and trends

## Setup

### 1. Create a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Prepare the raw data

Place your Excel workbook in the data folder. The project expects a file like:

```text
data\sample_-_superstore.xls
```

### 4. Run the data preparation step

```powershell
python src\prepare_data.py
```

This creates:

- outputs/sales_clean.csv
- outputs/monthly_performance.csv

## MySQL import

Before loading data, make sure MySQL is running locally and that the database exists.

```sql
CREATE DATABASE revenuepulse;
```

Then run:

```powershell
python src\load_to_mysql.py
```

The script will prompt you for:

- MySQL username
- MySQL password
- confirmation to replace the table contents in the revenuepulse database

It loads the cleaned sales data into a table named sales.

## SQL analysis

The SQL folder includes a ready-made analysis script at:

- sql/01_revenue_analysis.sql

This script covers key metrics such as:

- total revenue and profit
- monthly revenue and profit
- month-over-month growth
- category and sub-category performance
- regional performance
- segment performance
- discount/profitability analysis

Run the script in MySQL Workbench or another SQL client against the revenuepulse database.

## Outputs generated

### sales_clean.csv

Cleaned transaction-level sales data ready for analytics and reporting.

### monthly_performance.csv

Aggregated monthly performance metrics including:

- Revenue
- Profit
- Orders
- Profit Margin %
- MoM Growth %

## Example business questions this project can answer

- Which month had the strongest profit performance?
- Which product category is most profitable?
- How are sales and margins changing over time?
- Are regional or segment differences significant?
- Which discount levels are harming profitability?

## Recommended next steps

- Connect the cleaned MySQL table to Power BI or Tableau
- Add forecasting models for future sales trends
- Build a dashboard with KPIs and visual insights
- Extend the pipeline with automated scheduled refreshes

## License

This project is intended for learning, analytics, and internal business exploration. Use and adapt it freely for your own reporting workflow.

## Author

Built for revenue and performance analytics workflows using Python, SQL, and business data preparation.
