import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta
import yaml

def load_config(config_path="C:\\Users\\user\\OneDrive\\Desktop\\NoriFarm\\config\\settings.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def connect_to_sheet(credentials_path, sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
    client = gspread.authorize(creds)
    return client.open(sheet_name).sheet1

def get_weekly_data(sheet):
    today = datetime.today()
    last_week = today - timedelta(days=7)
    rows = sheet.get_all_values()
    headers = rows[0]
    data_rows = rows[1:]

    date_idx = headers.index("Date")
    #status_idx = headers.index("Status")
    status_idx = next((i for i, h in enumerate(headers) if h.strip().lower() == "status"), -1)
    if status_idx == -1:
       raise ValueError("Status column not found in headers: " + str(headers))

    #time_idx = headers.index("Delivery Time (hrs)")
    time_idx = next((i for i, h in enumerate(headers) if h.strip().lower() == "delivery time (hrs)"), None)
    if time_idx is None:
      raise ValueError("Could not find 'Delivery Time (hrs)' in headers: " + str(headers))


    print("Headers received from sheet:", headers)
    print("HEADERS FROM SHEET:", headers)
      # DEBUGGING: Print headers and indexes
    print("Headers:", headers)
    print("Date Index:", date_idx)
    print("Status Index:", status_idx)
    print("Time Index:", time_idx)

    today = datetime.today().date()
    last_week = today - timedelta(days=7)

    # DEBUGGING: Print today's and last week's date
    print("Today:", today)
    print("Last week:", last_week)

    #filtered_records = []


    records = []
    for row in data_rows:
        try:
            row_date = datetime.strptime(row[date_idx], "%Y-%m-%d")
            if last_week <= row_date <= today:
                records.append({
                    "date": row_date,
                    "status": row[status_idx].strip().lower(),
                    "delivery_time": float(row[time_idx]) if row[time_idx] else None
                })
        except:
            continue
    return records, today, last_week
