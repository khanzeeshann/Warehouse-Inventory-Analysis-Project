# Warehouse Inventory & Stockout Risk Analysis

**Python, NumPy & Pandas Individual Industry Project**
Student: Zeeshan Khan | Addmission No.: 2026B15410225

## Overview
This project analyses a warehouse inventory dataset to find products at risk of running out of stock, products that are overstocked, how much money is tied up in inventory, and which suppliers are slow or unreliable. It finishes with five recommendations that are calculated from the data.

> The dataset is **synthetic** (created for teaching). Results describe this dataset only and show associations, not proof of cause and effect.

## Repository structure
```
/SRS/Project20_SRS.docx      Software Requirements Specification
/src/warehouse_inventory_analysis.ipynb          Main notebook (all 15 tasks, with outputs)
/src/make_dataset.py         Script that generated the synthetic dataset (seeded)
/data/20_warehouse_inventory.csv   Raw dataset (1,212 rows, includes duplicates and gaps)
/data/cleaned_inventory.csv  Cleaned dataset with calculated columns
/outputs/                    Result tables, charts and summary text
README.md
```

## How to run
1. Install Python 3.10+ and the libraries: `pip install pandas numpy matplotlib jupyter`
2. Open a terminal in the repository folder and run `jupyter notebook`
3. Open `src/warehouse_inventory_analysis.ipynb` and choose **Kernel > Restart & Run All**
4. The notebook reads `data/20_warehouse_inventory.csv` and writes results to `/outputs` and `/data`.

(To regenerate the dataset: run `python src/make_dataset.py` from the repository root.)

## Dataset columns
`SKU_ID, Product_Name, Category, Supplier, Warehouse_Location, Current_Stock, Reorder_Level, Avg_Daily_Sales, Unit_Cost, Lead_Time_Days, Defect_Return_Rate_Pct`

## Method summary
| Step | What was done |
|---|---|
| Cleaning | Removed exact duplicate SKU rows; filled missing `Lead_Time_Days` with the supplier median and `Unit_Cost` with the category median; kept flag columns |
| Value | `Inventory_Value = Current_Stock x Unit_Cost` |
| Stockout risk | `Current_Stock <= Reorder_Level` |
| Days of stock | `Current_Stock / Avg_Daily_Sales`, NaN when sales are 0 (no divide-by-zero) |
| Overstock | more than 90 days of stock, or stock with zero sales |
| Outliers | IQR method on lead time (Q3 + 1.5 x IQR) |
| Status labels | `np.select`: Critical, Low, Overstock, otherwise Optimal (rules in the notebook) |

## Key results
Open the notebook for the full tables. Headline figures (from the executed notebook):
* 1,200 unique SKUs after removing 12 duplicate rows (1,212 raw rows)
* 233 SKUs (19.4%) at stockout risk; 172 of them are Critical
* 291 SKUs (24.2%) overstocked, holding 63.6% of total inventory value
* EastGate Imports ranks last on supplier reliability; FastTrack Goods ranks first
* The top 10 SKUs hold 14.4% of inventory value

## Limitations
* Synthetic data; no seasonality, promotions or supplier contracts.
* Average daily sales is treated as constant.
* Imputed values are estimates (flagged in the cleaned data).
* All findings are associations in this dataset, not proof of cause and effect.
