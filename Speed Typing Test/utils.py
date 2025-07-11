import csv

def export_to_csv(filename, records):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Uživatel", "WPM", "Přesnost", "Režim", "Datum"])
        for r in records:
            writer.writerow([r["username"], r["wpm"], r["accuracy"], r["mode"], r["date"]])

def export_to_txt(filename, records):
    with open(filename, "w", encoding="utf-8") as f:
        for r in records:
            f.write(f"{r['username']} | {r['wpm']} WPM | {r['accuracy']}% | {r['mode']} | {r['date']}\n")