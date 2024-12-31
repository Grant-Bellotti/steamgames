import urllib.request, json
import csv
from time import sleep

KEY = '35D7A5AF14BC52B5C3DE101B5737A903'

def appendFile(fileName, data):
    with open(fileName, "a", encoding="utf-8", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)
    print('Data saved to file.')
    return

def main():
    csvFileName = "allproducts.csv"

    # Reset the CSV file when the program starts
    with open(csvFileName, "w", encoding="utf-8", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['name', 'developers', 'appid', 'type', 'price', 'ratings', 'release date', 'genres', 'platforms'])

    # Get all ids on the store
    allProductData = None
    with urllib.request.urlopen(f'http://api.steampowered.com/ISteamApps/GetAppList/v0002/?key={KEY}&format=json') as url:
        allProductData = json.load(url)

    # Get product information by id
    count = 0
    csvData = []

    # For each product, parse data and add to file
    for product in allProductData['applist']['apps']:
        appID = str(product['appid'])

        while count < len(allProductData['applist']['apps']):
            try:
                with urllib.request.urlopen(f'https://store.steampowered.com/api/appdetails?appids={appID}') as url:
                    try:
                        productInfo = json.load(url)
                    except json.JSONDecodeError as e:
                        print(f"JSON decode error for appID {appID}: {e}")
                        appendFile(csvFileName, csvData)
                        csvData = []
                        count += 1
                        break

                    productInfo = productInfo[appID]

                    if productInfo['success']:
                        # Name
                        name = ""
                        if 'name' in productInfo['data']:
                            name = str(productInfo['data']['name'])

                        # Developers
                        developers = []
                        if 'developers' in productInfo['data']:
                            for i in range(len(productInfo['data']['developers'])):
                                developers.append(str(productInfo['data']['developers'][i]))

                        # Type
                        type = ""
                        if 'type' in productInfo['data']:
                            type = str(productInfo['data']['type'])

                        # Price
                        price = '$0.00'
                        if not productInfo['data']['is_free']:
                            if 'price_overview' in productInfo['data']:
                                price = str(productInfo['data']['price_overview']['final_formatted'])

                        # Ratings
                        rating = '0'
                        if 'recommendations' in productInfo['data']:
                            rating = str(productInfo['data']['recommendations']['total'])
                        
                        # Release Date
                        releaseDate = ""
                        if productInfo['data']['release_date']['coming_soon']:
                            releaseDate = "Coming Soon"
                        else:
                            releaseDate = str(productInfo['data']['release_date']['date'])

                        # Genres
                        genres = []
                        if 'genres' in productInfo['data']:
                            for i in range(len(productInfo['data']['genres'])):
                                genres.append(str(productInfo['data']['genres'][i]['description']))

                        # Supported Platforms
                        supportedPlatforms = []
                        if 'platforms' in productInfo['data']:
                            for platform in ['windows', 'mac', 'linux']:
                                if productInfo['data']['platforms'][platform]:
                                    supportedPlatforms.append(platform)

                        csvData.append([name, developers, appID, type, price, rating, releaseDate, genres, supportedPlatforms])
                
                count += 1
                print(f'Processed {count} products.')

                # Save every 50 processes
                if count % 50 == 0:
                    appendFile(csvFileName, csvData)
                    csvData = []

                sleep(1.5)
                break

            except Exception as e:
                print(e)
                print('Error processing, saving to file and waiting.')

                appendFile(csvFileName, csvData)
                csvData = []

                # Wait 30 seconds so don't spam server when rate limited
                sleep(30)

    # Finish writing to csv file
    if csvData:
        appendFile(csvFileName, csvData)

if __name__ == "__main__":
    main()