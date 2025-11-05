import os
import shutil
import pandas as pd
from datetime import datetime

# -----------------------------------
# Configuration
# -----------------------------------

RAW_FOLDER = "copy your raw_layer"           # eg:"C:/Users/ASUS/Desktop/cdc_project/raw_layer"
HISTORIC_FOLDER = "copy your historic_layer" # eg:"C:/Users/ASUS/Desktop/cdc_project/historic_layer"
CDC_FOLDER = "copy yourcdc_layer"            # eg:"C:/Users/ASUS/Desktop/cdc_project/cdc_layer"
ARCHIVE_FOLDER = "copy yourarchive_layer"    # eg:"C:/Users/ASUS/Desktop/cdc_project/archive_layer"

# File paths
CDC_FILE = os.path.join(CDC_FOLDER, "cdc_data_latest.xlsx")
HISTORIC_FILE = os.path.join(HISTORIC_FOLDER, "historic_data.xlsx")

# Ensure required folders exist
for folder in [RAW_FOLDER, HISTORIC_FOLDER, CDC_FOLDER, ARCHIVE_FOLDER]:
    os.makedirs(folder, exist_ok=True)

# -----------------------------------
# Step 1: Get latest raw Excel file
# -----------------------------------
def get_latest_raw_file(folder):
    excel_files = [f for f in os.listdir(folder) if f.endswith(".xlsx")]
    if not excel_files:
        raise FileNotFoundError("❌ No Excel files found in raw_folder.")
    excel_files.sort(key=lambda f: os.path.getmtime(os.path.join(folder, f)), reverse=True)
    latest_file = os.path.join(folder, excel_files[0])
    print(f"📂 Using latest raw file: {latest_file}")
    return latest_file

# -----------------------------------
# Step 2: Load data
# -----------------------------------
def load_raw_data(file_path):
    df = pd.read_excel(file_path)
    if 'Timestamp' not in df.columns or 'Statusflag' not in df.columns:
        raise ValueError("❌ Missing required columns: 'Timestamp' or 'Statusflag'.")
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    return df

def load_existing_cdc():
    if os.path.exists(CDC_FILE):
        print(f"🗂 Loading existing CDC layer: {CDC_FILE}")
        cdc_df = pd.read_excel(CDC_FILE)
        cdc_df['Timestamp'] = pd.to_datetime(cdc_df['Timestamp'])
        return cdc_df
    else:
        print("⚠️ No existing CDC file found. Starting fresh.")
        return pd.DataFrame()

def load_existing_historic():
    if os.path.exists(HISTORIC_FILE):
        historic_df = pd.read_excel(HISTORIC_FILE)
        historic_df['Timestamp'] = pd.to_datetime(historic_df['Timestamp'])
        return historic_df
    else:
        print("⚠️ No existing historic file found. Creating new one.")
        return pd.DataFrame()

# -----------------------------------
# Step 3: Append to Historic Layer
# -----------------------------------
def update_historic_layer(raw_df):
    historic_df = load_existing_historic()
    combined_df = pd.concat([historic_df, raw_df], ignore_index=True)
    combined_df.to_excel(HISTORIC_FILE, index=False)
    print(f"🕓 Historic layer updated: {HISTORIC_FILE}")

# -----------------------------------
# Step 4: Apply CDC Logic
# -----------------------------------
def apply_cdc_logic(raw_df, existing_cdc_df):
    if not existing_cdc_df.empty:
        combined_df = pd.concat([existing_cdc_df, raw_df], ignore_index=True)
    else:
        combined_df = raw_df.copy()

    combined_df = combined_df.sort_values(by=['ID', 'Timestamp'], ascending=[True, False])

    # Keep latest per ID
    latest_df = combined_df.drop_duplicates(subset='ID', keep='first')

    # Exclude deleted
    cdc_df = latest_df[latest_df['Statusflag'] != 'D'].copy()

    return cdc_df, combined_df

# -----------------------------------
# Step 5: Save Final CDC File
# -----------------------------------
def save_cdc_output(df):
    if os.path.exists(CDC_FILE):
        os.remove(CDC_FILE)
    df.to_excel(CDC_FILE, index=False)
    print(f"✅ CDC layer updated: {CDC_FILE}")

# -----------------------------------
# Step 6: Move Raw File to Backup
# -----------------------------------
def move_to_backup(file_path):
    filename = os.path.basename(file_path)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{os.path.splitext(filename)[0]}_{timestamp}.xlsx"
    backup_path = os.path.join(ARCHIVE_FOLDER, backup_name)
    shutil.move(file_path, backup_path)
    print(f"📦 Moved raw file to backup: {backup_path}")

# -----------------------------------
# Step 7: Log Summary
# -----------------------------------
def log_summary(df):
    summary = df['Statusflag'].value_counts().to_dict()
    print("\n📊 Change Summary:")
    for k, v in summary.items():
        action = {'I': 'Inserted', 'U': 'Updated', 'D': 'Deleted'}.get(k, k)
        print(f"  {action}: {v} records")

# -----------------------------------
# Main Execution
# -----------------------------------
if __name__ == "__main__":
    try:
        raw_file = get_latest_raw_file(RAW_FOLDER)
        raw_df = load_raw_data(raw_file)
        existing_cdc_df = load_existing_cdc()

        # Step A: Append to Historic layer first
        update_historic_layer(raw_df)

        # Step B: Apply CDC logic and update current snapshot
        cdc_df, combined_df = apply_cdc_logic(raw_df, existing_cdc_df)
        save_cdc_output(cdc_df)

        # Step C: Log + move to backup
        log_summary(combined_df)
        move_to_backup(raw_file)

        print("\n🎯 CDC + Historic process completed successfully!")
    except Exception as e:
        print("🚨 Error:", e)
