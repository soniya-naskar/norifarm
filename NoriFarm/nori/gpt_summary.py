import openai
import yaml

def load_config(config_path="config/settings.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def generate_summary(delivered, delayed, pending, avg_time, last_week, today):
    config = load_config()
    openai.api_key = config["openai_api_key"]

    prompt = (
        f"Generate a professional weekly shipment summary:\n"
        f"- Delivered: {delivered}\n"
        f"- Delayed: {delayed}\n"
        f"- Pending: {pending}\n"
        f"- Average Delivery Time: {avg_time} hours\n"
        f"- Week: {last_week.date()} to {today.date()}"
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0.7,
    )
    return response.choices[0].message["content"].strip()
