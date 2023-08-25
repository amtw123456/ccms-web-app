from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from bs4 import BeautifulSoup

import requests
import json

from .privatekeys import *

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
            'method' : 'GET',
            'body' : None,
            'description' : 'Displays a Counter Strike: Global Offensive case order history.'
        },    
            {
            'Endpoint' : '/get-case-item-price-history',
            'method' : 'GET',
            'body' : None,
            'description' : 'Displays a Counter Strike: Global Offensive case price history.'
        },    
    ]


    return Response(routes)