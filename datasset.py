import pandas as pd
import numpy as np
import gspread
from google.oauth2.service_account import Credentials

# 1. Generate the Data
np.random.seed(42)
n_orders = 200

order_time = pd.date_range(start="2024-01-01 08:00:00", periods=n_orders, freq="30min")

payment_delay = np.random.randint(5, 15, n_orders)
verification_delay = np.random.randint(60, 150, n_orders)   # bottleneck
packaging_delay = np.random.randint(10, 20, n_orders)
shipping_delay = np.random.randint(20, 40, n_orders)
delivery_delay = np.random.randint(240, 400, n_orders)

df = pd.DataFrame({
    "Order_ID": range(1000, 1000 + n_orders),
    "Order_Time": order_time
})

df["Payment_Time"] = df["Order_Time"] + pd.to_timedelta(payment_delay, unit="m")
df["Verification_Time"] = df["Payment_Time"] + pd.to_timedelta(verification_delay, unit="m")
df["Packaging_Time"] = df["Verification_Time"] + pd.to_timedelta(packaging_delay, unit="m")
df["Shipping_Time"] = df["Packaging_Time"] + pd.to_timedelta(shipping_delay, unit="m")
df["Delivery_Time"] = df["Shipping_Time"] + pd.to_timedelta(delivery_delay, unit="m")

# Save to CSV locally
df.to_csv("orders_dataset.csv", index=False)
print("Dataset created locally!")

# -----------------------------
# Connect to Google Sheets
# -----------------------------

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Ensure your JSON file path is correct
creds = Credentials.from_service_account_file("bold-hallway-452117-j5-0cc3fe0b9b42.json", scopes=scope)
client = gspread.authorize(creds)

# Open the sheet
sheet = client.open_by_key("1ojKZA-wkKb86bDaMJYAaejozFoHCCUYkYBeBis6sVzw").sheet1

# -----------------------------
# Prepare Data for Upload
# -----------------------------

# CRITICAL FIX: Convert all Timestamp columns to strings before uploading
# Google Sheets API cannot handle Pandas Timestamp objects directly.
df_upload = df.copy()
for col in df_upload.select_dtypes(include=['datetime64']).columns:
    df_upload[col] = df_upload[col].dt.strftime('%Y-%m-%d %H:%M:%S')

# -----------------------------
# Upload Data to Sheets
# -----------------------------

sheet.clear()

# Create the data list: Header + Rows
data_to_push = [df_upload.columns.values.tolist()] + df_upload.values.tolist()

sheet.update(data_to_push)

print("Data uploaded to Google Sheets successfully!")
