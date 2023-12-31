from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone
from collections import OrderedDict
from dotenv import load_dotenv

import requests
import time
import json
import ast
import os

from .dictionary_definitions import *
from ..serializers import *
from ..models import *

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
# IF WE USE THIS API CALL ON OUR VERCEL DEPLOYMENT WE WILL GET AN ERROR Exception Value: [Errno 30] Read-only file system
@api_view(['POST'])
def createAllCsCaseDailyPriceHistoryDaily(request):
    load_dotenv()

    steam_login = os.getenv("STEAM_LOGIN_SECURE")

    for caseName in myCaseDictionary:
        print(caseName)
        time.sleep(3)
        today = datetime.now()
        last_month = today - timedelta(days=32)  # Assuming a month is approximately 30 days
        
        today_date = today.date()
        last_month_date = last_month.date()

        # Format the dates as "Month Day Year" (e.g., "May 30 2023")
        today_formatted = today_date.strftime("%b %d %Y")
        last_month_formatted = last_month_date.strftime("%b %d %Y")

        # URL of the API call
        # url = "https://steamcommunity.com/market/pricehistory/?currency=12&appid=730&market_hash_name=Revolution%20Case"
        # session_cookie = '952d26f2161da77da75e9ea2'
        url = "https://steamcommunity.com/market/pricehistory/"

        # Define the parameters as a dictionary
        params = {
            "currency": currencies[request.data['itemCurrency']],
            "market_hash_name": caseName,
            "appid": 730,   
        }
        
        # Set up the request headers with the session cookie
        # we need to use the steamLoginSecure
        # https://stackoverflow.com/questions/31961868/how-to-retrieve-steam-market-price-history
        cookie = {'steamLoginSecure': steam_login}

        # Make the HTTP GET request with the custom headers
        response = requests.get(url, cookies=cookie, params=params)

        # response = requests.get(url)
        parsed_response = json.loads(response.content)
        formatted_response = json.dumps(parsed_response, indent=2)

        # Specify the file path where you want to save the JSON data
        directory_path = "case_history_price"

        output_file_path = os.path.join(directory_path, caseName.lower().replace(" ", "-").replace(":", "") + "-price-history-in-" + request.data['itemCurrency'] + ".json")

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
                # print("FOUND!!")
                break
        
        currentDate = parsed_response['prices'][counter][0][:11]
        dateInformation = [parsed_response['prices'][counter][0], parsed_response['prices'][counter][1], int(parsed_response['prices'][counter][2])]
        ctrDivisor = 1
        for i in parsed_response['prices'][counter+1:]:
            if currentDate == i[0][:11]:
                dateInformation[1] += i[1]
                dateInformation[2] += int(i[2])
                ctrDivisor += 1
            else:
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
            json.dump({"caseName": caseName, "currentTimeCreatedInUtc": datetime.now(timezone.utc), "casePriceHistoryDaily": dataPriceHistory}, output_file, indent=2, default=str) 
    
    return Response("Created json files")


# THIS API CALL GETS ALL THE DAILY PRICE OF A CASE AND NUMBER OF CASES SOLD IN THAT SPECIFIC DAY
# DONT USE THIS API CALL SINCE IT WILL CREATE A JSON FILE EVERYTIME WE CALL IT
# IF WE USE THIS API CALL ON OUR VERCEL DEPLOYMENT WE WILL GET AN ERROR Exception Value: [Errno 30] Read-only file system
@api_view(['POST'])
def createSpecificCsCasePriceHistoryDaily(request):
    load_dotenv()

    steam_login = os.getenv("STEAM_LOGIN_SECURE")

    today = datetime.now()
    last_month = today - timedelta(days=32)  # Assuming a month is approximately 30 days
    
    today_date = today.date()
    last_month_date = last_month.date()

    # Format the dates as "Month Day Year" (e.g., "May 30 2023")
    today_formatted = today_date.strftime("%b %d %Y")
    last_month_formatted = last_month_date.strftime("%b %d %Y")

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
    cookie = {'steamLoginSecure': steam_login}

    # Make the HTTP GET request with the custom headers
    response = requests.get(url, cookies=cookie, params=params)

    # response = requests.get(url)
    parsed_response = json.loads(response.content)
    formatted_response = json.dumps(parsed_response, indent=2)

    # Specify the file path where you want to save the JSON data
    directory_path = "case_history_price"

    output_file_path = os.path.join(directory_path, request.data['itemName'].lower().replace(" ", "-").replace(":", "") + "-price-history-in-" + request.data['itemCurrency'] + ".json")

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
            break
    
    currentDate = parsed_response['prices'][counter][0][:11]
    dateInformation = [parsed_response['prices'][counter][0], parsed_response['prices'][counter][1], int(parsed_response['prices'][counter][2])]
    ctrDivisor = 1
    for i in parsed_response['prices'][counter+1:]:
        if currentDate == i[0][:11]:
            dateInformation[1] += i[1]
            dateInformation[2] += int(i[2])
            ctrDivisor += 1
        else:
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
        json.dump({"caseName": request.data['itemName'], "currentTimeCreatedInUtc": datetime.now(timezone.utc) ,"casePriceHistoryDaily": dataPriceHistory}, output_file, indent=2, default=str) 
    
    return Response({"caseName": request.data['itemName'], "currentTimeCreatedInUtc": datetime.now(timezone.utc) ,"casePriceHistoryDaily": dataPriceHistory})

@api_view(['POST'])
def getCsCasePriceHistoryDaily(request):
    load_dotenv()

    steam_login = os.getenv("STEAM_LOGIN_SECURE")

    today = datetime.now()
    last_month = today - timedelta(days=32)  # Assuming a month is approximately 30 days
    
    today_date = today.date()
    last_month_date = last_month.date()

    # Format the dates as "Month Day Year" (e.g., "May 30 2023")
    today_formatted = today_date.strftime("%b %d %Y")
    last_month_formatted = last_month_date.strftime("%b %d %Y")

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
    cookie = {'steamLoginSecure': steam_login}

    # Make the HTTP GET request with the custom headers
    response = requests.get(url, cookies=cookie, params=params)

    # response = requests.get(url)
    parsed_response = json.loads(response.content)
    formatted_response = json.dumps(parsed_response, indent=2)

    # Create the directory if it doesn't exist

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
            break
    
    currentDate = parsed_response['prices'][counter][0][:11]
    dateInformation = [parsed_response['prices'][counter][0], parsed_response['prices'][counter][1], int(parsed_response['prices'][counter][2])]
    ctrDivisor = 1

    for i in parsed_response['prices'][counter+1:]:
        if currentDate == i[0][:11]:
            dateInformation[1] += i[1]
            dateInformation[2] += int(i[2])
            ctrDivisor += 1
        else:
            currentDate = i[0][:11]
            
            caseDateInformation = {
                "date" : dateInformation[0],
                "casePrice" : round(dateInformation[1] / ctrDivisor, 3),
                "numOfCaseSold" : dateInformation[2],
            }
            dataPriceHistory.append(caseDateInformation)
            dateInformation = [i[0], i[1], int(i[2])]
            ctrDivisor = 1

    return Response({"caseName": request.data['itemName'], "currentTimeCreatedInUtc": datetime.now(timezone.utc) , "casePriceHistoryDaily": dataPriceHistory})



@api_view(['POST'])
def putSpecficCaseDailyPriceHistoryToDatabase(request):

    load_dotenv()

    steam_login = os.getenv("STEAM_LOGIN_SECURE")

    today = datetime.now()
    last_month = today - timedelta(days=32)  # Assuming a month is approximately 30 days
    
    today_date = today.date()
    last_month_date = last_month.date()

    # Format the dates as "Month Day Year" (e.g., "May 30 2023")
    today_formatted = today_date.strftime("%b %d %Y")
    last_month_formatted = last_month_date.strftime("%b %d %Y")

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
    cookie = {'steamLoginSecure': steam_login}

    # Make the HTTP GET request with the custom headers
    response = requests.get(url, cookies=cookie, params=params)

    # response = requests.get(url)
    parsed_response = json.loads(response.content)
    formatted_response = json.dumps(parsed_response, indent=2)

    # Create the directory if it doesn't exist

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
            break
    
    currentDate = parsed_response['prices'][counter][0][:11]
    dateInformation = [parsed_response['prices'][counter][0], parsed_response['prices'][counter][1], int(parsed_response['prices'][counter][2])]
    ctrDivisor = 1

    for i in parsed_response['prices'][counter+1:]:
        if currentDate == i[0][:11]:
            dateInformation[1] += i[1]
            dateInformation[2] += int(i[2])
            ctrDivisor += 1
        else:
            currentDate = i[0][:11]
            
            caseDateInformation = {
                "date" : dateInformation[0],
                "casePrice" : round(dateInformation[1] / ctrDivisor, 3),
                "numOfCaseSold" : dateInformation[2],
            }
            dataPriceHistory.append(caseDateInformation)
            dateInformation = [i[0], i[1], int(i[2])]
            ctrDivisor = 1

    serializer = DailyCasePriceHistoryInformationSerializer(data={"caseName": request.data['itemName'], "currentTimeCreatedInUtc": datetime.now(timezone.utc) , "casePriceHistoryDaily": dataPriceHistory})
    
    if serializer.is_valid():
        try:
            serializer.save()
        except Exception as e:
            return Response(data={"message": "Error saving to database"})
        
    return Response(data={"message": "Case information successfully saved to database"})
    

@api_view(['POST'])
def putAllCaseDailyPriceHistoryToDatabase(request):
    load_dotenv()

    steam_login = os.getenv("STEAM_LOGIN_SECURE")

    for caseName in myCaseDictionary:
        # time.sleep(6)
        today = datetime.now()
        last_month = today - timedelta(days=32)  # Assuming a month is approximately 30 days
        
        today_date = today.date()
        last_month_date = last_month.date()

        # Format the dates as "Month Day Year" (e.g., "May 30 2023")
        today_formatted = today_date.strftime("%b %d %Y")
        last_month_formatted = last_month_date.strftime("%b %d %Y")

        # URL of the API call
        # url = "https://steamcommunity.com/market/pricehistory/?currency=12&appid=730&market_hash_name=Revolution%20Case"
        # session_cookie = '952d26f2161da77da75e9ea2'
        url = "https://steamcommunity.com/market/pricehistory/"

        # Define the parameters as a dictionary
        params = {
            "currency": currencies[request.data['itemCurrency']],
            "market_hash_name": caseName,
            "appid": 730,   
        }
        
        # Set up the request headers with the session cookie
        # we need to use the steamLoginSecure
        # https://stackoverflow.com/questions/31961868/how-to-retrieve-steam-market-price-history
        cookie = {'steamLoginSecure': steam_login}

        # Make the HTTP GET request with the custom headers
        response = requests.get(url, cookies=cookie, params=params)

        # response = requests.get(url)
        parsed_response = json.loads(response.content)
        formatted_response = json.dumps(parsed_response, indent=2)

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
                # print("FOUND!!")
                break
        
        currentDate = parsed_response['prices'][counter][0][:11]
        dateInformation = [parsed_response['prices'][counter][0], parsed_response['prices'][counter][1], int(parsed_response['prices'][counter][2])]
        ctrDivisor = 1
        for i in parsed_response['prices'][counter+1:]:
            if currentDate == i[0][:11]:
                dateInformation[1] += i[1]
                dateInformation[2] += int(i[2])
                ctrDivisor += 1
            else:
                currentDate = i[0][:11]
                
                caseDateInformation = {
                    "date" : dateInformation[0],
                    "casePrice" : round(dateInformation[1] / ctrDivisor, 3),
                    "numOfCaseSold" : dateInformation[2],
                }
                dataPriceHistory.append(caseDateInformation)
                dateInformation = [i[0], i[1], int(i[2])]
                ctrDivisor = 1

        serializer = DailyCasePriceHistoryInformationSerializer(data={"caseName": caseName, "currentTimeCreatedInUtc": datetime.now(timezone.utc) , "casePriceHistoryDaily": dataPriceHistory})
    
        if serializer.is_valid():
            try:
                serializer.save()
            except Exception as e:
                return Response(data={"message": "Error saving to database"})
    
    return Response(data={"message": "All case information successfully saved to database"})

@api_view(['POST'])
def retreiveSpecificCaseDailyPriceHistoryFromDatabase(request):
    caseInformation = DailyCasePriceHistoryInformation.objects.filter(caseName=request.data['caseName'])
    serializer = DailyCasePriceHistoryInformationSerializer(caseInformation, many=True)

    # initially our serializer.data[0]["casePriceHistoryDaily"] contains a string that was once a list of dictionary objects
    serialized_data = serializer.data[0]["casePriceHistoryDaily"]

    # this turns the value of serializer.data[0]["casePriceHistoryDaily"] into a list which we will iterate over
    list_form = eval(serialized_data)

    for i in range(len(list(list_form))):
        # converts the current list_form[index] value into a dictionary initially it was OrderedDict([('date', 'Jul 01 2022 01: +0'), ('casePrice', 1061.734), ('numOfCaseSold', 6647)])
        # after applying the dict on the current list_form index it will now be like this a proper dictionary { "date": "Jul 01 2022 01: +0", "casePrice": 1061.734, "numOfCaseSold": 6647 },
        list_form[i] = dict(list_form[i])

    serializer.data[0]["casePriceHistoryDaily"] = list_form

    return Response(serializer.data)


@api_view(['PUT'])
def updateSpecificCaseDailyPriceHistoryFromDatabase(request):

    # initially our serializer.data[0]["casePriceHistoryDaily"] contains a string that was once a list of dictionary objects

    load_dotenv()

    steam_login = os.getenv("STEAM_LOGIN_SECURE")

    today = datetime.now()
    last_month = today - timedelta(days=32)  # Assuming a month is approximately 30 days
    
    today_date = today.date()
    last_month_date = last_month.date()

    # Format the dates as "Month Day Year" (e.g., "May 30 2023")
    today_formatted = today_date.strftime("%b %d %Y")
    last_month_formatted = last_month_date.strftime("%b %d %Y")

    # URL of the API call
    # url = "https://steamcommunity.com/market/pricehistory/?currency=12&appid=730&market_hash_name=Revolution%20Case"
    # session_cookie = '952d26f2161da77da75e9ea2'
    url = "https://steamcommunity.com/market/pricehistory/"

    # Define the parameters as a dictionary
    params = {
        "currency": currencies["PHP"],
        "market_hash_name": request.data['caseName'],
        "appid": 730,   
    }
    
    # Set up the request headers with the session cookie
    # we need to use the steamLoginSecure
    # https://stackoverflow.com/questions/31961868/how-to-retrieve-steam-market-price-history
    cookie = {'steamLoginSecure': steam_login}

    # Make the HTTP GET request with the custom headers
    response = requests.get(url, cookies=cookie, params=params)

    # response = requests.get(url)
    parsed_response = json.loads(response.content)
    formatted_response = json.dumps(parsed_response, indent=2)

    # Create the directory if it doesn't exist

    counter = 0
    dataPriceHistory = []

    for i in parsed_response['prices']:
        counter += 1
        caseDataInformation = {
            "date" : i[0],
            "casePrice" : i[1],
            "numOfCaseSold" : int(i[2]),
        }

        dataPriceHistory.append(caseDataInformation)
        if last_month_formatted in i[0]:
            break
    
    currentDate = parsed_response['prices'][counter][0][:11]
    dataInformation = [parsed_response['prices'][counter][0], parsed_response['prices'][counter][1], int(parsed_response['prices'][counter][2])]
    ctrDivisor = 1

    for i in parsed_response['prices'][counter+1:]:
        if currentDate == i[0][:11]:
            dataInformation[1] += i[1]
            dataInformation[2] += int(i[2])
            ctrDivisor += 1
        else:
            currentDate = i[0][:11]
            
            caseDataInformation = {
                "date" : dataInformation[0],
                "casePrice" : round(dataInformation[1] / ctrDivisor, 3),
                "numOfCaseSold" : dataInformation[2],
            }
            dataPriceHistory.append(caseDataInformation)
            dataInformation = [i[0], i[1], int(i[2])]
            ctrDivisor = 1

    # caseInformation.save()

    DailyCasePriceHistoryInformation.objects.filter(caseName=request.data['caseName']).update(currentTimeCreatedInUtc=datetime.now(timezone.utc), casePriceHistoryDaily=dataPriceHistory)

    return Response(data={"message": "Successfully edited case information"})
    


