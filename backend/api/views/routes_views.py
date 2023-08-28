from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from bs4 import BeautifulSoup

import requests
import json

# API call to get the api endpoints relating to their views
@api_view(['GET'])
def getViewRoutes(request):
    routes = [
            {
            'Endpoint' : '/view-case-routes',
            'method' : 'GET',
            'body' : None,
            'description' : 'Displays all the endpoints for getting "Counter Strike: Global Offensive" cases information.'
        },
            {
            'Endpoint' : '/view-currency-routes',
            'method' : 'GET',
            'body' : None,
            'description' : 'Displays all the endpoints for getting currency related information.'
        },    
    ]


    return Response(routes)

# API call to get the api endpoints relating to currency related information
@api_view(['GET'])
def getCurrencyViews(request):
    routes = [
            {
            'Endpoint' : '/get-all-currency-exchange-rate',
            'method' : 'GET',
            'body' : None,
            'description' : 'Displays all currency exchange rate conversion information.'
        },
    ]
    
    return Response(routes)

# API call to get the api endpoints relating to Counter Strike: Global Offensive case information
@api_view(['GET'])
def getCaseViews(request):
    routes = [
            {
            'Endpoint' : '/get-all-case-details',
            'method' : 'GET',
            'body' : None,
            'description' : 'Displays all Counter Strike: Global Offensive case information'
        },
            {
            'Endpoint' : '/get-case-item-order-histogram',
            'method' : 'POST',
            'body' : {
                "currency": "CURRENCY_SYMBOL(PHP)",
                "item_nameid": "CASE_NAME(Snakebite Case)",
            },
            'description' : 'Displays a Counter Strike: Global Offensive case order history. You can use PHP and Snakebite Case as the request body'
        }, 
            {
            'Endpoint' : '/get-case-item-price-history-daily',
            'method' : 'POST',
            'body' : {
                "itemCurrency": "CURRENCY_SYMBOL(PHP)",
                "itemName": "CASE_NAME(Snakebite Case)",
            },
            'description' : 'Displays a Counter Strike: Global Offensive case daily price history you have to add to your private_keys your steamLoginSecure string.'
        },
             {
            'Endpoint' : '/retreive-specific-case-item-price-history-daily',
            'method' : 'POST',
            'body' : {
                "itemCurrency": "CURRENCY_SYMBOL(PHP)",
                "itemName": "CASE_NAME(Snakebite Case)",
            },
            'description' : 'Gets a specific case daily price information in the database of our website'
        }, 
            {
            'Endpoint' : '/put-specific-case-item-price-history-daily',
            'method' : 'POST',
            'body' : {
                "itemCurrency": "CURRENCY_SYMBOL(PHP)",
                "itemName": "CASE_NAME(Snakebite Case)",
            },
            'description' : 'Puts the data of a specific case daily price information in the game Counter Strike: Global Offensive to the mongodb database of the website this api call needs your steamLoginSecure string.'
        },  
            {
            'Endpoint' : '/put-all-case-item-price-history-daily',
            'method' : 'POST',
            'body' : {
                "itemCurrency": "CURRENCY_SYMBOL(PHP)",
                "itemName": "CASE_NAME(Snakebite Case)",
            },
            'description' : 'Puts the data of all the cases daily price information in the game Counter Strike: Global Offensive to the mongodb database of the website this api call needs your steamLoginSecure string.'
        },  
            {
            'Endpoint' : '/update-specific-case-item-price-history-daily',
            'method' : 'PUT',
            'body' : {
                "itemCurrency": "CURRENCY_SYMBOL(PHP)",
                "itemName": "CASE_NAME(Snakebite Case)",
            },
            'description' : 'Updates the data of a specific cases daily price information in the game Counter Strike: Global Offensive to the mongodb database of the website this api call needs your steamLoginSecure string.'
        },  
            {
            'Endpoint' : '/create-all-case-item-price-history-daily',
            'method' : 'POST',
            'body' : {
                "itemCurrency": "CURRENCY_SYMBOL(PHP)",
                "itemName": "CASE_NAME(Snakebite Case)",
            },
            'description' : 'We should only use this in our backend locally this creates a json file for all cases in the game Counter Strike: Global Offensive the data information will be the daily price history you have to add to your private_keys your steamLoginSecure string.'
        },     
            {
            'Endpoint' : '/create-specific-case-item-price-history-daily',
            'method' : 'POST',
            'body' : {
                "itemCurrency": "CURRENCY_SYMBOL(PHP)",
                "itemName": "CASE_NAME(Snakebite Case)",
            },
            'description' : 'We should only use this in our backend locally this creates a json file for a specific case in the game Counter Strike: Global Offensive the data information will be the daily price history you have to add to your private_keys your steamLoginSecure string.'
        },   
    ]


    return Response(routes)