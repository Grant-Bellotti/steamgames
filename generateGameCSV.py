import csv
import ast

csvFileRead = "allproducts.csv"
csvFileWrite = "allgames.csv"

# Open the CSV file for reading
with open(csvFileRead, mode='r', encoding="utf-8", newline='') as file:
    csvReader = csv.DictReader(file)

    data = []
    for row in csvReader:
        if row['type'] == 'game':
            row['developers'] = ", ".join(ast.literal_eval(row['developers'])) 
            row['genres'] = ", ".join(ast.literal_eval(row['genres']))
            row['platforms'] = ", ".join(ast.literal_eval(row['platforms'])) 
            
            data.append(row.values())

with open(csvFileWrite, "w", encoding="utf-8", newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['name', 'developers', 'appid', 'type', 'price', 'ratings', 'release date', 'genres', 'platforms'])

with open(csvFileWrite, "a", encoding="utf-8", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)