import urllib.request, json
import csv
from time import sleep

# Append to csv file
def appendFile(fileName, data):
    with open(fileName, "a", encoding="utf-8", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)
    print('Data saved to file.')
    return

def main():
    csvFileRead = "allgames.csv"
    csvFileWrite = "allgamesdone.csv"

    # Reset the CSV file when the program starts
    with open(csvFileWrite, "w", encoding="utf-8", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['name', 'developers', 'publishers', 'appid', 'type', 'price', 'positive-ratings', 'negative-ratings', 'release-date', 'genres', 'tags', 'platforms'])

    allGameData = []
    with open(csvFileRead, mode='r', encoding="utf-8", newline='') as file:
        csvReader = csv.DictReader(file)

        for row in csvReader:
            allGameData.append(row)

    count = 0
    csvData = []
    
    # For each game, parse data and add to file
    for game in allGameData:
        gameInfo = None
        gameID = game['appid']

        while count < len(allGameData):
            # Try to open url
            try:
                with urllib.request.urlopen(f'https://steamspy.com/api.php?request=appdetails&appid={gameID}') as url:
                    # Try to save data from website
                    try:
                        gameInfo = json.load(url)
                    
                    # If json format unable to be acquired
                    except json.JSONDecodeError as e:
                        print(f"JSON decode error for appID {gameID}: {e}")
                        appendFile(csvFileWrite, csvData)
                        csvData = []
                        count += 1
                        break
                break

            # If error occured with opening website (most likely accessing too fast)
            except Exception as e:
                print(f"Error processing for appID {gameID}, saving to file and waiting. Error: {e}")
                appendFile(csvFileWrite, csvData)
                csvData = []

                # Wait 30 seconds so don't spam server when rate limited
                sleep(30)
                continue

        name = game['name']
        developers = game['developers']

        # Publishers
        publishers = ""
        if 'publisher' in gameInfo:
            publishers = gameInfo['publisher']

        #appid = game['gameid']
        type = game['type']
        price = game['price']

        # Ratings (positive and negative)
        pRating = ''
        if 'positive' in gameInfo:
            pRating = str(gameInfo['positive'])
        nRating = ''
        if 'negative' in gameInfo:
            nRating = str(gameInfo['negative'])
        
        releaseDate = game['release date']
        genres = game['genres']

        # Tags (user made)
        tags = ""
        if 'tags' in gameInfo:
            if not gameInfo['tags'] == []:
                tags = ", ".join(list(gameInfo['tags'].keys()))

        supportedPlatforms = game['platforms']

        csvData.append([name, developers, publishers, gameID, type, price, pRating, nRating, releaseDate, genres, tags, supportedPlatforms])
        
        count += 1
        print(f'Processed {count} games.')

        # Save every 50 processes
        if count % 50 == 0:
            appendFile(csvFileWrite, csvData)
            csvData = []

        sleep(1)

    # Finish writing to csv file
    if csvData:
        appendFile(csvFileWrite, csvData)

if __name__ == "__main__":
    main()