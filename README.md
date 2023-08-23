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
