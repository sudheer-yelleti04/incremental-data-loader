🧩 Change Data Capture (CDC) Automation System

>📘 Project Description

This project automates a Change Data Capture (CDC) pipeline using Python and Excel files — ideal for small to mid-scale data engineering use cases or prototyping CDC before moving to a database or Airflow environment.

The pipeline reads new raw data files (Excel), tracks changes using Status Flags (I, U, D) and Timestamps, and maintains:

* CDC Layer (latest snapshot)
* Historic Layer (complete history of all events)
* Backup Layer (archive of processed raw files)

Each new raw file is automatically processed, appended to history, compared against existing data, and the latest CDC snapshot is updated.

>🏗️ Folder Structure
<img width="843" height="276" alt="image" src="https://github.com/user-attachments/assets/7cde9ee6-cd60-4401-9110-afe3e1fa634c" />


* 🧠 How It Works

>🩸 Step 1 — (Raw Layer)

Drop your latest Excel file into the raw_folder/.
Each file must contain:
ID, Statusflag (I, U, D), and Timestamp columns.

Example:

| ID | Name         | Email                                     | Statusflag | Timestamp           |
| -- | ------------ | ----------------------------------------- | ---------- | ------------------- |
| 1  | John Smith   | [john@email.com](mailto:john@email.com)   | I          | 2025-11-01 10:00:00 |
| 1  | John Smith   | [john@email.com](mailto:john@email.com)   | U          | 2025-11-03 14:30:00 |
| 2  | Priya Sharma | [priya@email.com](mailto:priya@email.com) | I          | 2025-11-04 09:15:00 |

>🧾 Step 2 — (Historic Layer)

The system appends every incoming record to a single Excel file:
historic_folder/historic_data.xlsx

🕓 This acts as a full audit trail — nothing is ever deleted here.

>🧮 Step 3 — (CDC Layer)

The script merges the new raw data with the existing CDC snapshot:

* Sorts by ID and Timestamp
* Keeps only the latest record per ID
* Removes records where Statusflag = D

🟢 Output → cdc_folder/cdc_data_latest.xlsx
(always exactly one file, representing the latest state)

>🗄️ Step 4 — (Archive Layer)

After processing, the raw Excel file is timestamped and moved to:
archived_folder/

Example:
archived_folder/raw_data_2025_11_05_20251105_144533.xlsx

>⚙️ Run Instructions

1️⃣ Create Environment

bash
python -m venv venv
source venv/bin/activate       # macOS/Linux
OR
venv\Scripts\activate          # Windows


2️⃣ Install Dependencies

bash
pip install pandas openpyxl

3️⃣ Run Script

bash
python cdc_script.py

4️⃣ Check Outputs

* 📜 historic_folder/historic_data.xlsx → all event history
* 📊 cdc_folder/cdc_data_latest.xlsx → latest snapshot
* 📦 archived_folder/ → archived raw file

>🧩 CDC Logic Explained

| Flag | Meaning | Behavior in CDC Layer             |
| ---- | ------- | --------------------------------- |
| I    | Insert  | New record is added               |
| U    | Update  | Old record replaced with new data |
| D    | Delete  | Record removed from CDC snapshot  |

>🧾 Example Output Summary

📂 Using latest raw file: raw_folder/raw_data_2025_11_05.xlsx
🕓 Historic layer updated: historic_folder/historic_data.xlsx
✅ CDC layer updated: cdc_folder/cdc_data_latest.xlsx

>📊 Change Summary

  Inserted: 3 records
  Updated: 4 records
  Deleted: 1 records

📦 Moved raw file to backup: archived_folder/raw_data_2025_11_05_20251105_144533.xlsx
🎯 CDC + Historic process completed successfully!

🛠️ Technologies Used

| Tool          | Purpose                     |
| ------------- | --------------------------- |
| 🐍 Python     | Main language               |
| 🧮 Pandas     | Data processing & CDC logic |
| 📘 OpenPyXL   | Excel I/O operations        |
| 🧰 OS, Shutil | File and folder management  |

>✅ Key Advantages

* 🧾 Transparent, human-readable Excel pipeline
* 🔁 Maintains both historic & current datasets
* 💾 Automatically handles backup and cleanup
* 🧠 Simple, modular, and Airflow-ready
* 🌍 Cross-platform and lightweight

>⚠️ Limitations

* ❌ Not suitable for very large datasets (>100K rows)
* ❌ Sequential file processing only (single-threaded)
* ❌ No inbuilt data validation — assumes clean input
* ❌ Excel-based I/O can slow down large ETL workloads

>🚀 Future Enhancements

* 🧮 Add cdc_run_log.xlsx to capture run stats
* ⏰ Integrate with Apache Airflow for scheduling
* 🗃️ Upgrade to SQL/Delta Lake storage
* 🧩 Add schema validation & data quality checks
* 📈 Include dashboard/reporting module


>👨‍💻 Author

Yelleti Sudheer Kumar
💼 Data Engineering Enthusiast | ETL | Python | Airflow
📧 sudheeryelleti@gmail.com

>🌟 Support

If you like this project, please ⭐ star the repository — it helps others discover it!
Contributions and suggestions are always welcome 💬
