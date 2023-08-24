from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

import requests
import json
from bs4 import BeautifulSoup

@api_view(['GET'])
def getCsCasePrice(request):
    # URL of the API call
    url = "https://steamcommunity.com/market/search/render/?query=case&start=0&count=40&search_descriptions=0&sort_column=default&sort_dir=desc&appid=730&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Type%5B%5D=tag_CSGO_Type_WeaponCase"

    # Make the HTTP GET request
    response = requests.get(url)
    parsed_response = json.loads(response.content)
    formatted_response = json.dumps(parsed_response, indent=2)
    csCaseNames = []
    caseCasePrices = []


    soup = BeautifulSoup(parsed_response["results_html"], 'html.parser')
    for tag in soup.find_all(class_='sale_price'):
        caseCasePrices.append(tag.text)
        print("----------------------")
    

    for tag in soup.find_all(class_='market_listing_item_name'):
        csCaseNames.append(tag.text)
        print("----------------------")

    print(csCaseNames)
    print(caseCasePrices)

    return Response([csCaseNames, caseCasePrices])
# Create your views here.
