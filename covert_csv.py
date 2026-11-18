import csv

with open("sales.csv", "r", newline="", encoding="utf-8-sig") as source:
    reader = csv.DictReader(source, delimiter=";")

    with open("sales_neon.csv", "w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(reader)

print("CSV converted successfully.")