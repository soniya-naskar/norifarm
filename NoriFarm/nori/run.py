from fetch_data import load_config, connect_to_sheet, get_weekly_data
from analyze_data import analyze_shipment_data
from gpt_summary import generate_summary
from write_back import write_summary_to_sheet

def main():
    config = load_config()
    sheet = connect_to_sheet(config["credentials_path"], config["google_sheet_name"])
    records, today, last_week = get_weekly_data(sheet)

    if not records:
        print("No shipment data found for the past week.")
        return

    delivered, delayed, pending, avg_time = analyze_shipment_data(records)

    summary = generate_summary(delivered, delayed, pending, avg_time, last_week, today)
    print("\n📦 Weekly Shipment Summary:\n", summary)

    write_summary_to_sheet(
        config["credentials_path"],
        config["google_sheet_name"],
        config["summary_sheet_name"],
        today.date(),
        summary
    )

    with open(f"summary_outputs/summary_{today.date()}.txt", "w") as f:
         f.write(summary)


if __name__ == "__main__":
    main()
