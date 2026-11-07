# Logistics, Delivery & Returns Dashboard

**Python Programming Capstone Project**

## Project Overview

This project analyzes logistics operations, shipment delivery performance, and product returns. It uses seven related CSV datasets and a Python notebook to inspect data quality, clean and standardize records, validate relationships, and prepare data for analysis.

The interactive dashboard was developed with **Streamlit** and **Plotly**. The exported charts in this repository provide static views of the key delivery and returns metrics.

## Executive Summary

See [`Executive Summary.txt`](Executive%20Summary.txt) for the project findings. Highlights reported in the project summary include:

- **15,000 orders** covered by the dashboard.
- **77.9% delivery success rate**.
- **4.0 days average delivery lead time** (valid delivery records, 1–7 days).
- **8.0% overall return rate**.
- Courier delivery success rates ranged from **76.6% to 78.5%**.
- The most frequent return reasons were **Changed Mind**, **Defective**, and **Missing Parts**.

## Repository Contents

```text
Logistics_Delivery_Returns_GitHub_Submission/
├── README.md
├── Executive Summary.txt
├── logistics_analysis.ipynb
├── app.py                         # Interactive Streamlit dashboard
├── requirements.txt
├── data/                         # Original input CSV files (7 datasets)
├── cleaned_data/                 # Cleaned/exported CSV files
│   ├── Cleaned_customers.csv
│   ├── Cleaned_products.csv
│   ├── Cleaned_orders.csv
│   ├── Cleaned_order_items.csv
│   ├── Cleaned_payments.csv
│   ├── Cleaned_shipments.csv
│   └── Cleaned_returns.csv
└── Charts/                       # Exported PNG charts
    ├── Chart1_Delivery_Lead_Time.png
    ├── Chart2_Courier_Delivery_Success_Rate.png
    ├── Chart3_Monthly_Shipment_Performance.png
    ├── Chart4_Shipment_Status_Breakdown.png
    ├── Chart5_Top_Return_Reasons.png
    └── Chart6_Return_Rate_by_Product_Category.png
```

## Tools & Libraries

- Python
- Pandas
- NumPy
- Matplotlib (for exported PNG charts)
- Streamlit and Plotly (interactive dashboard)

## Data Preparation

## Run the Interactive Streamlit Dashboard

The dashboard code is in `app.py`. It reads the seven cleaned CSV files from `cleaned_data/`.

1. Open a terminal in the repository root folder.
2. Install the dependencies (if you have not already):

   ```bash
   pip install -r requirements.txt
   ```

3. Start the dashboard:

   ```bash
   streamlit run app.py
   ```

4. Streamlit will open the dashboard in your browser. If it does not open automatically, use the local URL shown in the terminal (usually `http://localhost:8501`).

**Important:** Keep the `cleaned_data/` folder and its lowercase CSV filenames together with `app.py`. The dashboard expects these exact names: `customers.csv`, `products.csv`, `orders.csv`, `order_items.csv`, `payments.csv`, `shipments.csv`, and `returns.csv`.

## Data Preparation

The notebook documents the following workflow:

1. Load the seven source datasets.
2. Inspect dataset dimensions, column names, missing values, and duplicates.
3. Check primary-key uniqueness and foreign-key relationships.
4. Remove exact duplicate rows.
5. Fill selected missing customer and refund-status values.
6. Standardize product category labels.
7. Convert unit prices and payment amounts to numeric values.
8. Parse shipment dates and calculate delivery lead time.
9. Validate delivery-date sequence and shipment status consistency.
10. Convert selected date columns and export cleaned datasets.

**Data note:** Missing customer email and phone fields are filled with default placeholder values in the notebook. These are cleaning placeholders, not verified contact details.

## How to Run the Notebook

1. Download or clone this repository.
2. Install Python 3.10 or later.
3. Open a terminal in the repository's root folder.
4. Install the required libraries:

   ```bash
   pip install -r requirements.txt
   ```

5. Start Jupyter Notebook:

   ```bash
   jupyter notebook
   ```

6. Open `logistics_analysis.ipynb` and run the cells from top to bottom.

The notebook expects the original CSV files to remain in the `data/` folder. It writes cleaned CSV files to `cleaned_data/`.

## Charts

The `Charts/` folder contains six exported PNG charts:

1. Delivery lead-time distribution
2. Courier delivery success rate
3. Monthly shipment delivery performance
4. Shipment status breakdown
5. Top return reasons
6. Return rate by product category

## Project Scope

This repository contains the data preparation notebook, source and cleaned datasets, project summary, and exported charts. The interactive Streamlit application source is not included in this submission package.
