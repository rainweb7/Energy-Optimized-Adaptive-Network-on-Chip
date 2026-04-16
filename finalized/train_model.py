import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# =========================
# LOAD DATASET
# =========================
file_path = "D:/FYP/final/noc_dataset_realistic.csv"   # 🔁 change if needed

data = pd.read_csv(file_path)

# CLEAN COLUMN NAMES
data.columns = data.columns.str.strip()

print("Columns:", data.columns)

# =========================
# CONVERT ROW FORMAT → BEST ROUTE PER INJECTION
# =========================

# Pivot table to compare all routing for same injection rate
pivot = data.pivot_table(
    index=["Size", "Injection_Rate"],
    columns="Routing",
    values="Latency"
).reset_index()

# Rename columns for safety
pivot.columns.name = None
pivot = pivot.rename(columns={
    "DOR": "DOR_Lat",
    "VALIANT": "VALIANT_Lat",
    "RAN_MIN": "RAN_MIN_Lat"
})

print("\nPivot Table:\n", pivot.head())

# =========================
# FIND BEST ROUTE (MIN LATENCY)
# =========================
def best_route(row):
    latencies = {
        "DOR": row["DOR_Lat"],
        "VALIANT": row["VALIANT_Lat"],
        "RAN_MIN": row["RAN_MIN_Lat"]
    }
    return min(latencies, key=latencies.get)

pivot["Best_Route"] = pivot.apply(best_route, axis=1)

# =========================
# FEATURES + LABEL
# =========================
X = pivot[["Injection_Rate", "Size"]]
y = pivot["Best_Route"]

# =========================
# TRAIN MODEL
# =========================
model = RandomForestClassifier(n_estimators=100)
model.fit(X, y)

# =========================
# SAVE MODEL
# =========================
joblib.dump(model, "noc_model.pkl")

print("\n✅ Model trained and saved as noc_model.pkl")