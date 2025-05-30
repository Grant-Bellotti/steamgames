import csv

csvFileRead = "(5-23-25)_allproducts.csv"
csvFileWrite = "(5-23-25)_allgames.csv"

# Open the CSV file for reading
with open(csvFileRead, mode='r', encoding="utf-8", newline='') as file:
    csvReader = csv.DictReader(file)

    data = []
    for row in csvReader:
        if row['type'] == 'game':
            data.append(row.values())

with open(csvFileWrite, "w", encoding="utf-8", newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['name', 'developers', 'publishers', 'appid', 'type', 'price', 'positive-ratings', 'negative-ratings', 'release-date', 'genres', 'tags', 'platforms'])

with open(csvFileWrite, "a", encoding="utf-8", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)