Note you have to be logged into steam for some queries to work

https://steamcommunity.com/market/search/render/?query=&start=1490&count=10&search_descriptions=0&sort_column=price&sort_dir=desc&appid=730&norender=1&market_hash_name=Operation%20Vanguard%20Weapon%20Case

https://steamcommunity.com/market/priceoverview/?country=PH&currency=5&appid=730&market_hash_name=Operation%20Vanguard%20Weapon%20Case

https://steamcommunity.com/market/pricehistory/?appid=730&market_hash_name=P90%20|%20Blind%20Spot%20(Field-Tested)

https://steamcommunity.com/market/priceoverview/?appid=730&currency=39&market_hash_name=StatTrak%E2%84%A2%20M4A1-S%20|%20Hyper%20Beast%20(Minimal%20Wear)

https://steamcommunity.com/market/priceoverview/?appid=730&currency=39&market_hash_name=Danger%20Zone%20Case

THIS WILL BE OUR API CALL TO GET ALL OF THE CASES

https://steamcommunity.com/market/search/render/?query=case&start=0&count=40&search_descriptions=0&sort_column=default&sort_dir=desc&appid=730&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Type%5B%5D=tag_CSGO_Type_WeaponCase

THIS WILL BE OUR API CALL TO GET PRICE HISTORY OF THE GLOVE CASE
https://steamcommunity.com/market/pricehistory/?appid=730&market_hash_name=Glove%20Case%20Key

Above are some of the sample API calls we will use for our steam market API website.

    myCaseDictionary = {
        "Shadow Case" : 67060949,
        "Glove Case": 175854202,
        "Dreams & Nightmares Case": 176288467,
        "Revolver Case" : 84444464,
        "Horizon Case" : 175999886,
        "Snakebite Case" : 176240926,
        "Recoil Case" : 176321160,
        "Revolution Case" : 176358765,
        "Falchion Case" : 49359031,
        "Gamma Case" : 156110183,
        "Clutch Case" : 175966708,
        "Operation Riptide Case" : 176264317,
        "Operation Hydra Case" : 175896275,
        "Shattered Web Case" : 176096390,
        "Operation Bravo Case" : 1546282,
        "Chroma 2 Case" : 40091990,
        "Spectrum 2 Case" : 175917239,
        "CS20 Case" : 176091756,
        "Chroma 3 Case" : 149865785,
        "Prisma 2 Case" : 176118270,
        "eSports 2013 Case" : 1269049,
        "Operation Vanguard Weapon Case" : 23853214,
        "Winter Offensive Weapon Case" : 3438414,
        "Operation Broken Fang Case" : 176209154,
        "Operation Breakout Weapon Case" : 14962905,
        "Operation Phoenix Weapon Case" : 7177182,
        "CS:GO Weapon Case 2" : 1913364,
        "eSports 2014 Summer Case" : 15490346,
        "eSports 2013 Winter Case" : 15490345,
        "CS:GO Weapon Case 3" : 6820494,
        "Prisma Case": 176042493,
        "Operation Wildfire Case": 139654771,
        "Danger Zone Case": 176024744,
        "Chroma Case": 29205213,
        "Fracture Case": 176185874,
        "Spectrum Case": 175880240,
        "Huntsman Weapon Case": 8987853,
        "Gamma 2 Case" : 165027636

    }

Now how will I do this? Will I create a database that will contain all data relating the price history of an item?

TECHSTACK TO USE:
Frontend: React.js, Tailwind,
Backend: Node.js, Django
Database: MongoDB

Where to deploy: AWS Amplify or Vercel

Things to do
1. Determine where our data will come from
    - basically my idea is to use steam API calls that would display real time price data of an item
    - For the historical data of of csgo case item we will use steam's api call to get the historic data of a particular case and then put that in a mongodb database
2. Once we have determined which API calls to use from steam then we will create our backend service using django
    - To do this determine first which API calls will be used "LIST THEM DOWN"
    - Create backend service but first put the historical price item the cases to our mongodb database
        - We do this by using beautiful soup and the json package in python to correctly scrape the data we gotten from the steam API call
3. Create a temporary mock up for our frontend to test API calls
4. Once we have created our Database we then deploy the database to mongodb atlas 
5.
6.
