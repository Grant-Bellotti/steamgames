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
    """
    # Reset the CSV file when the program starts
    csvFileName = "allgames.csv"
    with open(csvFileName, "w", encoding="utf-8", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['name', 'developers', 'appid', 'type', 'price', 'ratings', 'release date', 'genres', 'platforms'])

    """
    csvFileName = "allgames.csv"
    # Get all ids on the store
    allGameData = None
    with urllib.request.urlopen(f'http://api.steampowered.com/ISteamApps/GetAppList/v0002/?key={KEY}&format=json') as url:
        allGameData = json.load(url)

    # Get game information by id
    count = 0
    csvData = []

    # For each game, parse data and add to file
    for game in allGameData['applist']['apps']:
        appID = str(game['appid'])

        # Catch up to where error was
        if count < 35236:
            count += 1
            continue

        while count < len(allGameData['applist']['apps']):
            try:
                with urllib.request.urlopen(f'https://store.steampowered.com/api/appdetails?appids={appID}') as url:
                    try:
                        gameInfo = json.load(url)
                    except json.JSONDecodeError as e:
                        print(f"JSON decode error for appID {appID}: {e}")
                        appendFile(csvFileName, csvData)
                        csvData = []
                        count += 1
                        break

                    gameInfo = gameInfo[appID]

                    if gameInfo['success']:
                        # Name
                        name = ""
                        if 'name' in gameInfo['data']:
                            name = str(gameInfo['data']['name'])

                        # Developers
                        developers = []
                        if 'developers' in gameInfo['data']:
                            for i in range(len(gameInfo['data']['developers'])):
                                developers.append(str(gameInfo['data']['developers'][i]))

                        # Type
                        type = ""
                        if 'type' in gameInfo['data']:
                            type = str(gameInfo['data']['type'])

                        # Price
                        price = '$0.00'
                        if not gameInfo['data']['is_free']:
                            if 'price_overview' in gameInfo['data']:
                                price = str(gameInfo['data']['price_overview']['final_formatted'])

                        # Ratings
                        rating = '0'
                        if 'recommendations' in gameInfo['data']:
                            rating = str(gameInfo['data']['recommendations']['total'])
                        
                        # Release Date
                        releaseDate = ""
                        if gameInfo['data']['release_date']['coming_soon']:
                            releaseDate = "Coming Soon"
                        else:
                            releaseDate = str(gameInfo['data']['release_date']['date'])

                        # Genres
                        genres = []
                        if 'genres' in gameInfo['data']:
                            for i in range(len(gameInfo['data']['genres'])):
                                genres.append(str(gameInfo['data']['genres'][i]['description']))

                        # Supported Platforms
                        supportedPlatforms = []
                        if 'platforms' in gameInfo['data']:
                            for platform in ['windows', 'mac', 'linux']:
                                if gameInfo['data']['platforms'][platform]:
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