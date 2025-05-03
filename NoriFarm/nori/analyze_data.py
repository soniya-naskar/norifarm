import statistics

def analyze_shipment_data(records):
    delivered, delayed, pending = 0, 0, 0
    times = []

    for r in records:
        if r["status"] == "delivered":
            delivered += 1
        elif r["status"] == "delayed":
            delayed += 1
        elif r["status"] == "pending":
            pending += 1

        if r["delivery_time"] is not None:
            times.append(r["delivery_time"])

    avg_time = round(statistics.mean(times), 2) if times else 0.0
    return delivered, delayed, pending, avg_time
