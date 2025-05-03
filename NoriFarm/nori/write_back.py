import gspread
from oauth2client.service_account import ServiceAccountCredentials
import yaml

def write_summary_to_sheet(credentials_path, spreadsheet_name, sheet_name, date, summary):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
    client = gspread.authorize(creds)

    try:
        summary_sheet = client.open(spreadsheet_name).worksheet(sheet_name)
    except gspread.WorksheetNotFound:
        summary_sheet = client.open(spreadsheet_name).add_worksheet(title=sheet_name, rows="100", cols="2")

    summary_sheet.append_row([str(date), summary])
