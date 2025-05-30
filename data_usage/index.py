import csv
import math
import ast
import re
import enchant

d = enchant.Dict("en_US")

TOPAMOUNT = 15
POSITIVETONEGATIVEPERCENTAGE = .85

productFileName = "(5-23-25)_allproducts.csv"
gameFileName = "(5-23-25)_allgames.csv"

def getHighestRatedByFile(fileName):
    appIDs = []
    highestRows = []

    with open(fileName, mode='r', encoding="utf-8", newline='') as file:
        csvReader = csv.DictReader(file)

        for row in csvReader:
            positiveReviews = int(row['positive-ratings'])
            negativeReviews = int(row['negative-ratings'])
            currentTotalReviews = positiveReviews + negativeReviews

            if currentTotalReviews == 0 or "$" not in row['price']:
                continue

            positivePercent = positiveReviews / currentTotalReviews

            if positivePercent >= POSITIVETONEGATIVEPERCENTAGE:
                # if the highest rows list not full
                if len(highestRows) < TOPAMOUNT:
                    appIDs.append(int(row['appid']))
                    highestRows.append(row)

                # If the highest rows list is full, replace the lowest one if it is less than current checking row
                elif int(row['appid']) not in appIDs:
                    minReview = math.inf
                    minIndex = -1

                    for i in range(len(highestRows)):
                        totalHighestReviews = int(highestRows[i]['positive-ratings']) + int(highestRows[i]['negative-ratings'])

                        if totalHighestReviews < minReview:
                            minReview = totalHighestReviews
                            minIndex = i
                    
                    if minReview < currentTotalReviews:
                        appIDs[minIndex] = int(row['appid'])
                        highestRows[minIndex] = row

    return highestRows

def nicePrint(data):
    # Header
    print('─' * 60)
    print(f'{"Title":<30} | {"Price":<10} | Release Date')
    print('─' * 60)

    for product in data:
        print(f'{product['name']:<30} | {product['price']:<10} | {product['release-date']}')

    print('─' * 60)

def extractTagsAndGenres(fileName, column):
    columnItems = set()

    with open(fileName, mode='r', encoding="utf-8", newline='') as file:
        csvReader = csv.DictReader(file)

        for row in csvReader:
            columnContent = ast.literal_eval(row[column])

            if not columnContent:
                continue

            # print (columnContent)

            for item in columnContent:
                if re.fullmatch(r'[A-Za-z0-9 &\-\+]+', item):
                    columnItems.add(item)

    columnItems = list(columnItems)
    englishItems = []

    for i in range(len(columnItems)):
        addWord = True
        for word in columnItems[i].replace('-', ' ').split():
            if not d.check(word):
                for exception in ['&', 'rpg', 'vr', '3d', '2d', 'pvp', 'pve', 'lgbt', 'em']:
                    if exception not in word.lower() and not isinstance(word, (int)):
                        addWord = False
                        break

            if not addWord:
                break
        
        if addWord:
            englishItems.append(columnItems[i])

    englishItems.sort()

    print(f'--------- {column} ---------')
    print (englishItems)
    print('------------------')

            

def main():
    # bestGames = getHighestRatedByFile(gameFileName)
    # bestProducts = getHighestRatedByFile(productFileName)

    # nicePrint(bestGames)
    # nicePrint(bestProducts)

    extractTagsAndGenres(gameFileName, 'genres')
    extractTagsAndGenres(gameFileName, 'tags')

if __name__ == "__main__":
    main()