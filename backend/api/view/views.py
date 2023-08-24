from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

import requests
import json

from .privatekeys import *
from bs4 import BeautifulSoup

@api_view(['GET'])
def getCsCasePrice(request):
    # URL of the API call
    csCaseNames = []
    csCasePrices = []
    csCaseImages = []


    url = "https://steamcommunity.com/market/search/render/?query=case&start=0&count=40&search_descriptions=0&sort_column=default&sort_dir=desc&appid=730&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Type%5B%5D=tag_CSGO_Type_WeaponCase"

    # Make the HTTP GET request
    response = requests.get(url)
    parsed_response = json.loads(response.content)
    formatted_response = json.dumps(parsed_response, indent=2)





    soup = BeautifulSoup(parsed_response["results_html"], 'html.parser')
    for tag in soup.find_all(class_='sale_price'):
        csCasePrices.append(tag.text)
        # print("----------------------")
    
    for tag in soup.find_all(class_='market_listing_item_name'):
        csCaseNames.append(tag.text)
        # print("----------------------")

    for tag in soup.find_all(class_='market_listing_item_img'):
        csCaseImages.append(tag['srcset'].split(' '))
        # print("----------------------")


    return Response([csCaseNames, csCasePrices, csCaseImages])


# i'm getting rate limited for an hour so try again after an hour lol
@api_view(['GET'])
def getCsCaseOrderHistory(request):
    # URL of the API call
    url = "https://steamcommunity.com/market/itemordershistogram?country=PH&language=english&currency=12&item_nameid=176288467&two_factor=0"

    # Make the HTTP GET request
    response = requests.get(url)
    parsed_response = json.loads(response.content)
    formatted_response = json.dumps(parsed_response, indent=2)

    return Response([parsed_response['buy_order_graph'], parsed_response['sell_order_graph']])

@api_view(['GET'])
def getCsCasePriceHistory(request):
    # URL of the API call
    url = "https://steamcommunity.com/market/pricehistory/?currency=12&appid=730&market_hash_name=Glove%20Case"
    # url = "https://steamcommunity.com/market/pricehistory/?country=PT&currency=3&appid=730&market_hash_name=Glove%20Case%20Key"
    # url = "https://steamcommunity.com/market/pricehistory/?currency=12&appid=730&market_hash_name=Revolution%20Case"
    # session_cookie = '952d26f2161da77da75e9ea2'
    
    # Set up the request headers with the session cookie
    # we need to use the steamLoginSecure
    # https://stackoverflow.com/questions/31961868/how-to-retrieve-steam-market-price-history
    cookie = {'steamLoginSecure': steamLoginSecure}

    # Make the HTTP GET request with the custom headers
    response = requests.get(url, cookies=cookie)

    # response = requests.get(url)
    parsed_response = json.loads(response.content)
    formatted_response = json.dumps(parsed_response, indent=2)
    print(formatted_response)
    return Response(parsed_response['prices'])

@api_view(['GET'])
def getcookie(request):  
    cookie = request.COOKIES['https://steamcommunity.com/']  
    return Response("steam @: "+  cookie);  


    



