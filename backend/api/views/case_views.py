from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

import requests
import json
import os

from .private_keys import *
from .dictionary_definitions import *

@api_view(['GET'])
def getCsCaseDetails(request):
    # URL of the API call
    csCaseDetailsResponse = []
    csCaseNames = []
    csCasePrices = []
    csCaseImages = []
    csCaseQuantiy = []

    params = {
        'query': 'case',
        'start': 0,
        'count': 50,
        'search_descriptions': 0,
        'sort_column': 'default',
        'sort_dir': 'desc',
        'appid': 730,
        'category_730_ItemSet[]': 'any',
        'category_730_ProPlayer[]': 'any',
        'category_730_StickerCapsule[]': 'any',
        'category_730_TournamentTeam[]': 'any',
        'category_730_Weapon[]': 'any',
        'category_730_Type[]': 'tag_CSGO_Type_WeaponCase'
    }

    url = "https://steamcommunity.com/market/search/render/"

    # Make the HTTP GET request
    response = requests.get(url, params=params)
    parsed_response = json.loads(response.content)
    formatted_response = json.dumps(parsed_response, indent=2)
    soup = BeautifulSoup(parsed_response["results_html"], 'html.parser')

    for tag in soup.find_all(class_='market_listing_num_listings_qty'):
        csCaseQuantiy.append(tag.text)

    for tag in soup.find_all(class_='sale_price'):
        csCasePrices.append(tag.text)
        # print("----------------------")
    
    for tag in soup.find_all(class_='market_listing_item_name'):
        csCaseNames.append(tag.text)
        # print("----------------------")

    for tag in soup.find_all(class_='market_listing_item_img'):
        csCaseImages.append(tag['srcset'].split(' '))
        # print("----------------------")

    
    for i in range(len(csCaseNames)):
        caseDetails = {
            "caseName" : csCaseNames[i],
            "casePrice" : csCasePrices[i],
            "csCaseQuantiy" : csCaseQuantiy[i],
            "caseUrlLink" : csCaseImages[i],
        }

        csCaseDetailsResponse.append(caseDetails)

    print(len(csCaseDetailsResponse))

    return Response(csCaseDetailsResponse)

# careful when spamming this api call
# there is a chance of getting rate limited for an hour so try again after an hour lol
@api_view(['POST'])
def getCsCaseOrderHistory(request):
    # URL of the API call
    # url = "https://steamcommunity.com/market/itemordershistogram?country=PH&language=english&currency=12&item_nameid=176288467&two_factor=0"

    url = "https://steamcommunity.com/market/itemordershistogram"

    params = {
        "country": "PH",
        "language": "english",
        "currency": currencies[request.data['itemCurrency']],
        "item_nameid": myCaseDictionary[request.data['itemName']],
        "two_factor": 0
    }

    response = requests.get(url, params=params)
    parsed_response = json.loads(response.content)
    formatted_response = json.dumps(parsed_response, indent=2)

    return Response([parsed_response['buy_order_graph'], parsed_response['sell_order_graph']])

# THIS API CALL GETS ALL THE DAILY PRICE OF A CASE AND NUMBER OF CASES SOLD IN THAT SPECIFIC DAY
# DONT USE THIS API CALL SINCE IT WILL CREATE A JSON FILE EVERYTIME WE CALL IT
@api_view(['POST'])
def getCsCasePriceHistory(request):

    today = datetime.now()
    last_month = today - timedelta(days=32)  # Assuming a month is approximately 30 days
    
    today_date = today.date()
    last_month_date = last_month.date()

    # Format the dates as "Month Day Year" (e.g., "May 30 2023")
    today_formatted = today_date.strftime("%b %d %Y")
    last_month_formatted = last_month_date.strftime("%b %d %Y")

    print(today_formatted)
    print(last_month_formatted)
    # URL of the API call
    # url = "https://steamcommunity.com/market/pricehistory/?currency=12&appid=730&market_hash_name=Revolution%20Case"
    # session_cookie = '952d26f2161da77da75e9ea2'
    url = "https://steamcommunity.com/market/pricehistory/"

    # Define the parameters as a dictionary
    params = {
        "currency": currencies[request.data['itemCurrency']],
        "market_hash_name": request.data['itemName'],
        "appid": 730,   
    }
    
    # Set up the request headers with the session cookie
    # we need to use the steamLoginSecure
    # https://stackoverflow.com/questions/31961868/how-to-retrieve-steam-market-price-history
    cookie = {'steamLoginSecure': steamLoginSecure}

    # Make the HTTP GET request with the custom headers
    response = requests.get(url, cookies=cookie, params=params)

    # response = requests.get(url)
    parsed_response = json.loads(response.content)
    formatted_response = json.dumps(parsed_response, indent=2)

    
    # Specify the file path where you want to save the JSON data
    directory_path = "case_history_price"

    output_file_path = os.path.join(directory_path, request.data['itemName'].lower().replace(" ", "-") + "-price-history.json")

    # Create the directory if it doesn't exist
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    counter = 0
    dataPriceHistory = []

    for i in parsed_response['prices']:
        counter += 1
        caseDateInformation = {
            "date" : i[0],
            "casePrice" : i[1],
            "numOfCaseSold" : int(i[2]),
        }

        dataPriceHistory.append(caseDateInformation)
        if last_month_formatted in i[0]:
            print("FOUND!!")
            break
    
    currentDate = parsed_response['prices'][counter][0][:11]
    print("THE CURRENT DATE IS:", currentDate)
    dateInformation = [parsed_response['prices'][counter][0], parsed_response['prices'][counter][1], int(parsed_response['prices'][counter][2])]
    ctrDivisor = 1
    for i in parsed_response['prices'][counter+1:]:
        if currentDate == i[0][:11]:
            print(True)
            dateInformation[1] += i[1]
            dateInformation[2] += int(i[2])
            ctrDivisor += 1
        else:
            print(False)
            currentDate = i[0][:11]
            
            caseDateInformation = {
                "date" : dateInformation[0],
                "casePrice" : round(dateInformation[1] / ctrDivisor, 3),
                "numOfCaseSold" : dateInformation[2],
            }
            dataPriceHistory.append(caseDateInformation)
            dateInformation = [i[0], i[1], int(i[2])]
            ctrDivisor = 1
       
    with open(output_file_path, "w") as output_file:
        json.dump({"caseName": request.data['itemName'], "casePriceHistory": dataPriceHistory}, output_file, indent=2) 
    
    return Response(parsed_response['prices'][-750:])


    



