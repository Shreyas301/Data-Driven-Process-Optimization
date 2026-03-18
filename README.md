# Data-Driven-Process-Optimization

An end-to-end Python pipeline that generates synthetic logistics data, identifies process bottlenecks, applies optimization logic, and syncs the results to Google Sheets for real-time KPI tracking.

---

## 🚀 Overview

This project simulates a supply chain workflow for **Everphone**, tracking an order from the initial timestamp through to final delivery. It consists of two main stages:
1.  **Dataset Creation**: Generating realistic order lifecycle data.
2.  **Process Optimization**: Identifying the "Verification" bottleneck and simulating a 91% efficiency improvement.

## 🛠️ Tech Stack

* **Language:** Python 3.10+
* **Data Analysis:** Pandas, NumPy
* **Google Sheets API:** `gspread`, `google-auth`
* **Storage:** Local CSV & Cloud-based Google Sheets

---

## 📊 Process Workflow

The system tracks five key milestones for every order:
* **Payment Duration**: Time taken to clear funds.
* **Verification Duration**: Document and credit checks (**Identified Bottleneck**).
* **Packaging Duration**: Warehouse preparation.
* **Shipping Duration**: Handover to logistics partners.
* **Delivery Duration**: Last-mile transit.

---

## ⚙️ Setup & Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/everphone-optimization.git](https://github.com/your-username/everphone-optimization.git)
    cd everphone-optimization
    ```

2.  **Install dependencies:**
    ```bash
    pip install pandas numpy gspread google-auth
    ```

3.  **Google Sheets Credentials:**
    * Place your Service Account JSON file (`bold-hallway-....json`) in the root directory.
    * Share your Google Sheet with the `client_email` found inside the JSON file.
    * Update `SHEET_ID` in the scripts.

---

## 📈 Optimization Results

Based on the latest run, the system identified and optimized the **Verification** stage:

| Metric | Before Optimization | After Optimization |
| :--- | :--- | :--- |
| **Internal Processing Time** | 155.53 min | 63.23 min |
| **Verification Duration** | 101.86 min | 9.56 min |
| **Total Time Saved** | **92.30 min per order** | — |

---

## 📂 File Structure

* `datasset.py`: Generates the `orders_dataset.csv` and uploads the raw data to the primary sheet.
* `optimization.py`: Performs KPI calculation, detects bottlenecks, and updates the `results` worksheet.
* `orders_dataset.csv`: Local backup of the generated synthetic data.

---

## ⚠️ Troubleshooting

* **Timestamp Error:** If you encounter `Object of type Timestamp is not JSON serializable`, ensure the script converts datetime columns to strings before the `gspread` upload.
* **404 Error:** Double-check that the `SHEET_ID` in the code matches your browser's URL and that the Service Account has "Editor" permissions.
