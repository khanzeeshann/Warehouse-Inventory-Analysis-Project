"""Generate the synthetic warehouse inventory dataset (seeded, reproducible)."""
import numpy as np
import pandas as pd

rng = np.random.default_rng(20)
N = 1200

categories = {
    "Electronics":   (["Wireless Mouse", "USB-C Cable", "Bluetooth Speaker", "Power Bank", "Webcam", "Keyboard"], (350, 4500)),
    "Home & Kitchen": (["Mixer Grinder", "Pressure Cooker", "Water Bottle", "Lunch Box", "Cookware Set", "Storage Jar"], (150, 3200)),
    "Apparel":       (["Cotton T-Shirt", "Denim Jeans", "Hoodie", "Sports Socks", "Track Pants", "Cap"], (120, 1800)),
    "Grocery":       (["Basmati Rice 5kg", "Cooking Oil 1L", "Tea Pack", "Pulses 1kg", "Spice Box", "Biscuit Carton"], (40, 600)),
    "Stationery":    (["Notebook Pack", "Gel Pen Box", "Marker Set", "Desk Organiser", "Sticky Notes", "File Folder"], (20, 450)),
    "Sports":        (["Yoga Mat", "Dumbbell Set", "Football", "Badminton Racket", "Skipping Rope", "Resistance Band"], (180, 3800)),
}
suppliers = {  # supplier: (mean lead time, std, mean defect %)
    "Apex Traders":      (6, 1.2, 1.8),
    "BlueLine Supplies": (9, 1.8, 2.6),
    "CityWave Pvt Ltd":  (12, 2.5, 3.4),
    "Delta Components":  (7, 1.5, 1.2),
    "EastGate Imports":  (18, 4.0, 4.8),
    "FastTrack Goods":   (5, 1.0, 2.2),
    "GreenField Co":     (14, 3.0, 3.0),
}
locations = ["Delhi-NCR Hub", "Mumbai Hub", "Bengaluru Hub", "Kolkata Hub", "Hyderabad Hub"]

rows = []
cat_names = list(categories)
sup_names = list(suppliers)
for i in range(1, N + 1):
    cat = rng.choice(cat_names, p=[0.2, 0.2, 0.17, 0.17, 0.13, 0.13])
    names, (lo, hi) = categories[cat]
    sup = rng.choice(sup_names)
    lt_mu, lt_sd, df_mu = suppliers[sup]
    lead = max(2, int(round(rng.normal(lt_mu, lt_sd))))
    cost = round(float(np.exp(rng.uniform(np.log(lo), np.log(hi)))), 2)
    daily = max(0.0, round(float(rng.gamma(2.0, 6.0)), 1))
    if rng.random() < 0.04:
        daily = 0.0                                   # items with no sales
    safety = daily * rng.uniform(2, 6)
    reorder = int(round(daily * lead + safety))
    # stock expressed as days of cover so we get a mix of risk / healthy / overstock
    cover = rng.choice(["low", "ok", "high"], p=[0.2, 0.58, 0.22])
    if cover == "low":
        stock = int(rng.uniform(0, 1.05) * reorder)
    elif cover == "ok":
        stock = int(reorder * rng.uniform(1.1, 2.2) + daily * rng.uniform(5, 25))
    else:
        stock = int(max(reorder * 2, daily * rng.uniform(95, 260)) + rng.integers(20, 120))
    if daily == 0:
        stock = int(rng.integers(0, 400))
    defect = round(float(max(0.1, rng.normal(df_mu, 0.8))), 2)
    rows.append({
        "SKU_ID": f"SKU{1000 + i}",
        "Product_Name": rng.choice(names),
        "Category": cat,
        "Supplier": sup,
        "Warehouse_Location": rng.choice(locations, p=[0.28, 0.24, 0.2, 0.14, 0.14]),
        "Current_Stock": stock,
        "Reorder_Level": reorder,
        "Avg_Daily_Sales": daily,
        "Unit_Cost": cost,
        "Lead_Time_Days": lead,
        "Defect_Return_Rate_Pct": defect,
    })

df = pd.DataFrame(rows)

# a few unusually long lead times (disruptions) for the IQR task
out_idx = rng.choice(df.index, 18, replace=False)
df.loc[out_idx, "Lead_Time_Days"] = rng.integers(32, 48, size=18)

# inject realistic data-quality problems
df.loc[rng.choice(df.index, 32, replace=False), "Lead_Time_Days"] = np.nan
df.loc[rng.choice(df.index, 26, replace=False), "Unit_Cost"] = np.nan
dups = df.sample(12, random_state=7)
df = pd.concat([df, dups], ignore_index=True).sample(frac=1, random_state=3).reset_index(drop=True)

df.to_csv("data/20_warehouse_inventory.csv", index=False)
print(df.shape)
print(df.isna().sum()[df.isna().sum() > 0])
print("dup SKU rows:", df.duplicated("SKU_ID").sum())
