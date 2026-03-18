import pandas as pd
import matplotlib.pyplot as plt
import gspread
from google.oauth2.service_account import Credentials

# -----------------------------
# 0. Connect to Google Sheets
# -----------------------------

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file("bold-hallway-452117-j5-0cc3fe0b9b42.json", scopes=scope)
client = gspread.authorize(creds)

# 🔴 Replace with your Sheet ID
sheet = client.open_by_key("1ojKZA-wkKb86bDaMJYAaejozFoHCCUYkYBeBis6sVzw").sheet1

data = sheet.get_all_records()

df = pd.DataFrame(data)

# Safety check
if df.empty:
    print("No data found in Google Sheet.")
    exit()


# -----------------------------
# 1. Load Dataset (from Sheets)
# -----------------------------

df['Order_Time'] = pd.to_datetime(df['Order_Time'])
df['Payment_Time'] = pd.to_datetime(df['Payment_Time'])
df['Verification_Time'] = pd.to_datetime(df['Verification_Time'])
df['Packaging_Time'] = pd.to_datetime(df['Packaging_Time'])
df['Shipping_Time'] = pd.to_datetime(df['Shipping_Time'])
df['Delivery_Time'] = pd.to_datetime(df['Delivery_Time'])


# -----------------------------
# 2. Calculate Stage Durations
# -----------------------------

df['payment_duration'] = (df['Payment_Time'] - df['Order_Time']).dt.total_seconds()/60
df['verification_duration'] = (df['Verification_Time'] - df['Payment_Time']).dt.total_seconds()/60
df['packaging_duration'] = (df['Packaging_Time'] - df['Verification_Time']).dt.total_seconds()/60
df['shipping_duration'] = (df['Shipping_Time'] - df['Packaging_Time']).dt.total_seconds()/60
df['delivery_duration'] = (df['Delivery_Time'] - df['Shipping_Time']).dt.total_seconds()/60


# -----------------------------
# 3. Compute Process KPIs
# -----------------------------

kpis = df[['payment_duration',
           'verification_duration',
           'packaging_duration',
           'shipping_duration',
           'delivery_duration']].mean()

print("\nCurrent Process KPIs (minutes):")
print(kpis)


# -----------------------------
# 4. Detect Internal Bottleneck
# -----------------------------

internal_process = kpis.drop('delivery_duration')

bottleneck_stage = internal_process.idxmax()

print("\nDetected Internal Bottleneck:", bottleneck_stage)


# -----------------------------
# 5. Automatically Estimate Optimization Factor
# -----------------------------

fastest_stage = internal_process.min()

bottleneck_time = internal_process.max()

optimization_factor = fastest_stage / bottleneck_time

print("\nEstimated Optimization Factor:", round(optimization_factor,2))


# -----------------------------
# 6. Apply Optimization
# -----------------------------

optimized_df = df.copy()

optimized_df[bottleneck_stage] = optimized_df[bottleneck_stage] * optimization_factor


# -----------------------------
# 7. Recalculate Optimized KPIs
# -----------------------------

optimized_kpis = optimized_df[['payment_duration',
                               'verification_duration',
                               'packaging_duration',
                               'shipping_duration',
                               'delivery_duration']].mean()

print("\nOptimized Process KPIs:")
print(optimized_kpis)


# -----------------------------
# 8. Compare Internal Processing Time
# -----------------------------

before_time = internal_process.sum()

after_time = optimized_kpis[['payment_duration',
                             'verification_duration',
                             'packaging_duration',
                             'shipping_duration']].sum()

print("\nInternal Processing Time Before:", round(before_time,2),"minutes")
print("Internal Processing Time After:", round(after_time,2),"minutes")

print("\nTime Saved per Order:", round(before_time - after_time,2),"minutes")


# -----------------------------
# 9. Visualization
# -----------------------------

labels = ["Payment","Verification","Packaging","Shipping","Delivery"]

before = kpis.values
after = optimized_kpis.values

x = range(len(labels))

plt.figure(figsize=(10,6))

plt.bar([i-0.2 for i in x], before, width=0.4, label="Before Optimization")
plt.bar([i+0.2 for i in x], after, width=0.4, label="After Optimization")

plt.xticks(x, labels)

plt.ylabel("Minutes")
plt.title("Automated Process Optimization Impact")

plt.legend()

plt.tight_layout()

plt.show()


# -----------------------------
# 10. (Optional) Write Results Back to Sheets
# -----------------------------

try:
    result_sheet = client.open_by_key("1ojKZA-wkKb86bDaMJYAaejozFoHCCUYkYBeBis6sVzw").worksheet("results")
except:
    result_sheet = client.open_by_key("1ojKZA-wkKb86bDaMJYAaejozFoHCCUYkYBeBis6sVzw").add_worksheet(title="results", rows="20", cols="10")

result_sheet.clear()

result_data = [
    ["Stage","Before","After"],
    ["Payment", kpis[0], optimized_kpis[0]],
    ["Verification", kpis[1], optimized_kpis[1]],
    ["Packaging", kpis[2], optimized_kpis[2]],
    ["Shipping", kpis[3], optimized_kpis[3]],
    ["Delivery", kpis[4], optimized_kpis[4]],
    ["Bottleneck", bottleneck_stage, ""],
    ["Time Saved", round(before_time - after_time,2), ""]
]

result_sheet.update(result_data, "A1")
