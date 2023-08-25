from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from bs4 import BeautifulSoup

import requests
import json

from .private_keys import *


@api_view(['GET'])
def getCurrencyExchangeRates(request):
    
    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_RATE_API_KEY}/latest/USD"

    # Make the HTTP GET request
    response = requests.get(url)
    parsed_response = json.loads(response.content)
    formatted_response = json.dumps(parsed_response, indent=2)

    return Response(parsed_response['conversion_rates'])
