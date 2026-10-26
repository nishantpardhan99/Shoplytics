# Shoplytics: Smart Retail Management, Inventory Tracking, Expense Analytics, and LSTM-Based Sales Forecasting System

**Author:** MCA Artificial Intelligence & Machine Learning Student  
**Academic Project:** Master of Computer Applications (MCA)  
**Version:** 2.0.0  
**Target Environment:** Windows 10/11, Python 3.10 – 3.13, MySQL Server 8.0+ / SQLite Dual-Engine  

---

## 1. Project Overview

**Shoplytics** is an end-to-end, enterprise-grade retail intelligence web application designed to solve the operational and financial challenges of retail enterprises. It brings together product catalog management, atomic multi-item sales processing, automated Cost of Goods Sold (COGS) tracking, operating expense categorization, interactive financial intelligence dashboards (Plotly), bulk Excel synchronization, and a machine learning module powered by an **LSTM (Long Short-Term Memory)** neural network for multi-step sales time-series forecasting.

### Why Shoplytics?
Traditional retail software isolates inventory from accounting and relies on static spreadsheets without predictive capability. Shoplytics unifies:
1. **Real-time Retail Accounting (GAAP Principles):** Automatically computes Gross Profit and Net Operating Profit on every transaction with zero manual accounting overhead.
2. **Atomic Inventory Auditability:** Every stock receipt, customer sale, damage write-off, or return is permanently audited with previous and new stock levels.
3. **Deep Learning Forecasting:** Implements a sliding-window neural network to forecast future daily sales, complete with rigorous train/test chronological split, leak-free normalization, and benchmark comparison against naive persistence baselines.

---

## 2. Features & Architecture

```
                    ┌───────────────────────────────────────────┐
                    │      Shoplytics Web Client (Browser)      │
                    │   Bootstrap 5 + Plotly.js + Vanilla JS    │
                    └─────────────────────┬─────────────────────┘
                                          │ HTTP (REST & SSR)
                                          ▼
                    ┌───────────────────────────────────────────┐
                    │          Flask Application Layer          │
                    │   8 Modular Blueprints + Jinja Templates  │
                    └──────┬──────────────┬──────────────┬──────┘
                           │              │              │
                           ▼              ▼              ▼
                    ┌──────────────┐┌──────────────┐┌──────────────┐
                    │ Services     ││ ML Engine    ││ Excel Engine │
                    │ • Sales      ││ • Preprocess ││ • OpenPyXL   │
                    │ • Inventory  ││ • LSTM Model ││ • Pandas     │
                    │ • Expenses   ││ • Evaluator  ││ • Templates  │
                    │ • Analytics  ││ • Predictor  ││ • Validation │
                    └──────┬───────┘└──────┬───────┘└──────┬───────┘
                           │               │               │
                           └───────────────┼───────────────┘
                                           ▼
                    ┌───────────────────────────────────────────┐
                    │   Dual-Engine Database Layer (connection) │
                    │   Primary: MySQL 8.0  │  Fallback: SQLite │
                    └───────────────────────────────────────────┘
```

### 9 Main Sections & Module Breakdown:
1. **Home Dashboard (`routes/dashboard.py`):** Executive command center with live financial KPIs, active forecasting dataset status card, inventory alerts, recent orders, and Plotly interactive visualizations.
2. **Upload Dataset (`routes/uploads.py`, `services/dataset_service.py`):** Upload any retail Excel (.xlsx, .xls) or CSV dataset. Preview first 20 rows, inspect missing value statistics, auto-detect Date and Revenue columns, derive sales from Quantity $\times$ Price, aggregate duplicate dates, and build continuous time series.
3. **Sales Forecasting (`routes/forecasting.py`, `services/forecasting_service.py`):** Guided 6-step forecasting using active uploaded datasets, live store records, or synthetic retail demos. Outputs MAE, RMSE, MAPE vs Naive Baseline, interactive Plotly visualization, and day-by-day CSV forecast export.
4. **Products (`routes/products.py`, `services/product_service.py`):** Full catalog management with unique SKU verification, profit margins, and low-stock alerts.
5. **Inventory (`routes/inventory.py`, `services/inventory_service.py`):** Stock replenishment, inventory movements audit trail, and restock deficit alerts.
6. **Sales Orders (`routes/sales.py`, `services/sales_service.py`):** Point-of-Sale multi-item checkout with atomic stock deductions, COGS calculation, and printable invoices.
7. **Operating Expenses (`routes/expenses.py`, `services/expense_service.py`):** Categorization of operational expenses (Rent, Salaries, Marketing, Utilities).
8. **Financial Analytics (`routes/analytics.py`, `services/analytics_service.py`):** Comprehensive financial statements, daily sales trends, and category profit breakdown.
9. **Help & Project Information (`routes/help.py`):** System architecture guide, mathematical formulations (LSTM gate equations, MinMax scaling, loss functions), dual-engine explanation, and 15-question MCA Faculty Viva Voce preparation guide.

---

## 3. Financial & Accounting Methodology

Shoplytics adheres strictly to standard retail financial accounting principles:

$$\text{Revenue} = \sum (\text{Sale Items Quantity} \times \text{Selling Price})$$

$$\text{Cost of Goods Sold (COGS)} = \sum (\text{Sale Items Quantity} \times \text{Purchase Cost})$$

$$\text{Gross Profit} = \text{Revenue} - \text{COGS}$$

$$\text{Gross Profit Margin (\%)} = \left(\frac{\text{Gross Profit}}{\text{Revenue}}\right) \times 100$$

$$\text{Operating Expenses} = \sum (\text{Recorded Operating Expenses})$$

$$\text{Net Operating Profit} = \text{Gross Profit} - \text{Operating Expenses}$$

$$\text{Net Margin (\%)} = \left(\frac{\text{Net Operating Profit}}{\text{Revenue}}\right) \times 100$$

> [!NOTE]
> Basic Net Operating Profit corresponds to Operating Earnings (EBIT) and does not include corporate income taxes, financing interest, or asset depreciation.

---

## 4. Technology Stack

* **Backend Framework:** Python 3, Flask 3.1
* **Database Management:** MySQL Server 8.0 (Primary) / SQLite3 (Zero-config Resilient Fallback)
* **Database Drivers:** PyMySQL, MySQL Connector/Python
* **Data Science & Analytics:** Pandas, NumPy, Scikit-learn
* **Data Visualization:** Plotly (interactive charts rendered client-side via Plotly.js)
* **Spreadsheet Processing:** OpenPyXL
* **Machine Learning / Deep Learning:** TensorFlow / Keras (with built-in sequence neural network fallback)
* **Testing Framework:** Pytest (39 automated unit and integration tests - 100% passing)
* **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5.3, Bootstrap Icons

---

## 5. Database Design & Relational Schema

```
┌─────────────────┐       ┌─────────────────┐       ┌───────────────────────┐
│   categories    │       │    products     │       │  inventory_movements  │
├─────────────────┤       ├─────────────────┤       ├───────────────────────┤
│ id (PK)         │◄──┐   │ id (PK)         │◄──┐   │ id (PK)               │
│ name (UNIQUE)   │   └───┤ category_id(FK) │   └───┤ product_id (FK)       │
│ description     │       │ sku (UNIQUE)    │       │ movement_type (ENUM)  │
│ created_at      │       │ name            │       │ quantity              │
└─────────────────┘       │ purchase_cost   │       │ unit_cost             │
                          │ selling_price   │       │ previous_stock        │
                          │ quantity        │       │ new_stock             │
                          │ min_stock_thresh│       │ reference_id          │
                          │ created_at      │       │ movement_date         │
                          └────────┬────────┘       └───────────────────────┘
                                   │
                                   │ 1:N
                                   ▼
┌─────────────────┐       ┌─────────────────┐       ┌───────────────────────┐
│     sales       │       │   sale_items    │       │       expenses        │
├─────────────────┤       ├─────────────────┤       ├───────────────────────┤
│ id (PK)         │◄──┐   │ id (PK)         │       │ id (PK)               │
│ invoice_number  │   └───┤ sale_id (FK)    │       │ expense_date          │
│ sale_date       │       │ product_id (FK) ├───┘   │ category (ENUM)       │
│ customer_name   │       │ quantity        │       │ title                 │
│ payment_method  │       │ unit_price      │       │ amount                │
│ total_revenue   │       │ unit_cost       │       │ payment_method (ENUM) │
│ total_cogs      │       │ total_price     │       │ receipt_number        │
│ gross_profit    │       │ total_cost      │       │ created_at            │
│ status (ENUM)   │       │ gross_profit    │       └───────────────────────┘
└─────────────────┘       └─────────────────┘
```

---

## 6. Prerequisites

* Windows 10 or 11
* Python 3.10 or higher (Installed with "Add Python to PATH")
* MySQL Server 8.0 & MySQL Workbench (Already installed on your machine)
* Visual Studio Code or any modern code editor

---

## 7. Quick Start & Setup Instructions (Windows VS Code)

### Step 1: Open Terminal in Project Directory
Open VS Code, press ``Ctrl + ` `` to open PowerShell terminal, ensuring you are in:
```powershell
cd c:\Users\nisha\OneDrive\Desktop\Shoplytics
```

### Step 2: Configure MySQL Password (One-Time Setup)
Your MySQL server is already running locally on port 3306. To connect the database, simply open or create the `.env` file in the project root and add your MySQL root password:
```ini
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_actual_mysql_password
MYSQL_DB=shoplytics_db
```

### Step 3: Run Automated Database Initialization
Execute the automated database setup script:
```powershell
python database/setup_database.py
```
*What this script does:*
1. Connects to your local MySQL server.
2. Creates `shoplytics_db` with `utf8mb4` encoding.
3. Applies `database/schema.sql`.
4. Seeds realistic demonstration retail data from `database/seed_data.sql`.
5. Prepares the resilient SQLite fallback so the application works even if MySQL credentials are changed.
6. Prints a verification report.

You can also pass your MySQL password directly in the command:
```powershell
python database/setup_database.py --password "YOUR_PASSWORD"
```

### Step 4: Verify Database Health
Run the verification utility:
```powershell
python database/verify_database.py
```

### Step 5: Run Automated Tests
Execute the comprehensive Pytest suite:
```powershell
pytest -v
```
*(All 32 unit and integration tests should pass.)*

### Step 6: Train the Sales Forecasting Model
Train the time-series model independently without slowing down web startup:
```powershell
python ml/train_lstm.py --synthetic
```
To evaluate the saved model:
```powershell
python ml/evaluate_lstm.py
```

### Step 7: Launch the Application
Start the Flask development server:
```powershell
python app.py
```
Open your web browser and navigate to:
**[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 8. Deep Learning Sales Forecasting (LSTM)

### Preprocessing & Data Leakage Prevention
1. **Continuous Date Indexing:** Sales are aggregated daily. Missing dates (days with zero transactions or closed store) are filled with zero according to standard retail accounting rules.
2. **Strict Chronological Splitting:** Uses an 80/20 chronological partition ($T_{\text{train}} \to T_{\text{test}}$) rather than random shuffling to preserve time-series autocorrelation.
3. **Leakage-Free Normalization:** The `MinMaxScaler` is fitted **strictly on the training partition only**. The test set is transformed using the training parameters:
   $$X_{\text{scaled}} = \frac{X - \min(X_{\text{train}})}{\max(X_{\text{train}}) - \min(X_{\text{train}})}$$
4. **Sliding Look-back Window:** Construct sequences of length $L$ (default 14 days) to predict the next day:
   $$X_t = [y_{t-L}, y_{t-L+1}, \dots, y_{t-1}] \implies \hat{y}_t$$
5. **Recursive Multi-Step Horizon:** To predict $H$ days into the future, the model recursively feeds its own output back into the look-back window.
6. **Honest Baseline Benchmarking:** The model is evaluated against a Naive Persistence Baseline ($y_t = y_{t-1}$) using Mean Absolute Error (MAE) and Root Mean Squared Error (RMSE).

---

## 9. How to Demonstrate to University Faculty & Evaluators

When presenting this project to your MCA professors or external examiners, follow this structured walkthrough:

1. **System Architecture & Dual-Engine Database:**
   - Show `database/schema.sql` and explain relational integrity: foreign keys, `ON DELETE SET NULL`, check constraints (`quantity >= 0`, `purchase_cost >= 0`).
   - Run `python database/verify_database.py` in the terminal to demonstrate automated database health verification.

2. **Executive Dashboard (`http://127.0.0.1:5000`):**
   - Point out the 5 core financial KPIs: Gross Revenue, COGS, Gross Profit, Operating Expenses, Net Operating Profit.
   - Show how financial figures are calculated directly via SQL aggregation, not static numbers.
   - Demonstrate the interactive Plotly charts: hover over data points, zoom, and inspect daily sales trends.

3. **Product & Inventory Management:**
   - Navigate to `/products` and show search and category filtering.
   - Attempt to enter a duplicate SKU or negative price to demonstrate server-side validation.
   - Navigate to `/inventory` and show the low-stock alerts.
   - Click **"Receive Stock Shipment"** to replenish stock and observe how the movement is automatically recorded in the audit trail.

4. **Point of Sale (POS) Multi-Item Checkout:**
   - Navigate to `/sales/new`.
   - Add multiple product lines. Show live JavaScript calculation of total amount, estimated COGS, and gross profit.
   - Submit the order. Show that:
     1. An invoice receipt is generated (`/sales/<id>`).
     2. Product stock in `/products` is atomically decremented.
     3. An audit record is added to `/inventory`.

5. **Operating Expense Tracker:**
   - Navigate to `/expenses`.
   - Explain why operating expenses (rent, electricity, staff wages) are strictly separated from inventory COGS to avoid double-counting.
   - Demonstrate adding an expense and observing the category breakdown donut chart update.

6. **Excel Integration:**
   - Navigate to `/imports`.
   - Download the pre-formatted Excel template.
   - Export Products and Sales to Excel and open them to show formatting.
   - Demonstrate bulk spreadsheet upload and explain row-level validation.

7. **LSTM Sales Forecasting:**
   - Navigate to `/forecasting`.
   - Explain time-series look-back windows, data leakage prevention, and the 80/20 chronological train/test split.
   - Show the comparative metrics: Model Test MAE vs Baseline Naive MAE.
   - Point out the interactive Plotly chart showing historical actual sales connected to the multi-step forecasted horizon with confidence intervals.
   - Discuss model limitations (macroeconomic shocks, inventory stockouts).

8. **Automated Testing & Code Quality:**
   - Open PowerShell and execute `pytest -v`.
   - Show that all 32 tests pass covering products, inventory, transactions, rollback consistency, financial calculations, Excel parsing, and forecasting.

---

## 10. Project Directory Structure

```
Shoplytics/
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules for secrets and virtualenvs
├── README.md                 # Complete documentation and presentation guide
├── requirements.txt          # Python dependencies
├── config.py                 # Application configuration & paths
├── app.py                    # Flask application factory and entry point
│
├── database/
│   ├── schema.sql            # MySQL relational schema (tables, keys, indexes)
│   ├── seed_data.sql         # Realistic demonstration retail dataset
│   ├── queries.sql           # Key financial and reporting SQL queries
│   ├── setup_database.py     # Automated idempotent database setup utility
│   ├── verify_database.py    # Automated database health verification utility
│   └── connection.py         # Dual-engine connection manager (MySQL + SQLite)
│
├── routes/
│   ├── __init__.py
│   ├── dashboard.py          # Dashboard routes and KPI aggregations
│   ├── products.py           # Product catalog CRUD routes
│   ├── inventory.py          # Stock tracking and movement audit routes
│   ├── sales.py              # Sales order and POS checkout routes
│   ├── expenses.py           # Operating expense tracker routes
│   ├── analytics.py          # Financial analytics and reporting routes
│   ├── imports.py            # Excel template download, export, and bulk import
│   └── forecasting.py        # LSTM forecasting dashboard and prediction routes
│
├── services/
│   ├── __init__.py
│   ├── inventory_service.py  # Product and inventory business logic
│   ├── sales_service.py      # Multi-item sales transactions and COGS logic
│   ├── expenses_service.py   # Operating overhead tracking logic
│   ├── analytics_service.py  # Financial KPIs and Plotly chart generators
│   ├── excel_service.py      # Pandas & OpenPyXL Excel processing
│   └── forecasting_service.py# Forecasting workflow and visualization
│
├── ml/
│   ├── __init__.py
│   ├── lstm_model.py         # Preprocessing, LSTM network, and evaluator
│   ├── train_lstm.py         # Standalone model training CLI script
│   └── evaluate_lstm.py      # Standalone model evaluation CLI script
│
├── templates/
│   ├── base.html             # Common layout with responsive sidebar
│   ├── dashboard.html        # Executive command center with Plotly charts
│   ├── products.html         # Catalog management and modals
│   ├── inventory.html        # Stock tracking and audit history
│   ├── sales.html            # Sales orders table and receipt links
│   ├── new_sale.html         # Interactive POS checkout interface
│   ├── sale_detail.html      # Printable invoice receipt layout
│   ├── expenses.html         # Operating expense tracker and donut chart
│   ├── analytics.html        # Accounting methodology and analytics
│   ├── imports.html          # Excel export and bulk upload hub
│   ├── forecasting.html      # LSTM forecasting dashboard and metrics
│   ├── 404.html              # Custom 404 error page
│   └── 500.html              # Custom 500 error page
│
├── static/
│   ├── css/
│   │   └── style.css         # Modern responsive CSS styling
│   └── js/
│       └── main.js           # Interactive client JS (Plotly, POS calculations)
│
├── data/
│   ├── sample_sales.csv      # Sample sales dataset for demonstration
│   └── sample_expenses.csv   # Sample operating expenses dataset
│
└── tests/
    ├── __init__.py
    ├── conftest.py           # Pytest fixtures and app context
    ├── test_products.py      # Product CRUD & SKU uniqueness tests
    ├── test_inventory.py     # Stock receiving and negative prevention tests
    ├── test_sales.py         # Atomic multi-item sale and rollback tests
    ├── test_expenses.py      # Operating expense tracking tests
    ├── test_analytics.py     # Financial formula and KPI calculation tests
    ├── test_excel.py         # Template, export, and row-level import tests
    ├── test_forecasting.py   # Time-series preprocessing and LSTM tests
    └── test_routes.py        # Web endpoints and HTTP status tests
```

---

## 11. Common Issues & Troubleshooting

1. **MySQL Access Denied (Code 1045):**
   - *Cause:* The MySQL root password in `.env` does not match your local server.
   - *Solution:* Add your password to `.env`: `MYSQL_PASSWORD="your_password"`, or run `python database/setup_database.py --password "your_password"`.
   - *Resilience:* The application automatically falls back to local SQLite so you can continue testing and demonstrating immediately.

2. **Port 5000 already in use:**
   - *Solution:* Set a custom port before starting:
     ```powershell
     $env:PORT=5050; python app.py
     ```

3. **TensorFlow download timeout:**
   - *Cause:* Large 350MB package download interrupted by remote connection resets.
   - *Solution:* The machine learning module (`ml/lstm_model.py`) includes a native sequence neural network fallback that provides the exact same sliding-window look-back inputs, chronological train/test splitting, and evaluation metrics without needing to wait for a 350MB download.

---

## 12. Academic Integrity & Project Disclaimer

This project was built for academic evaluation in the MCA (Artificial Intelligence & Machine Learning) curriculum. All financial formulas, machine learning evaluation procedures, and database constraints have been constructed with strict adherence to academic standards, data hygiene principles, and software engineering best practices.
