from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from bs4 import BeautifulSoup
from dotenv import load_dotenv

import requests
import json
import os


@api_view(['GET'])
def getCurrencyExchangeRates(request):
    load_dotenv()

    # Access the variables
    exchange_rate_api_key = os.getenv("EXCHANGE_RATE_API_KEY")
    
    url = f"https://v6.exchangerate-api.com/v6/{exchange_rate_api_key}/latest/USD"

    # Make the HTTP GET request
    response = requests.get(url)
    parsed_response = json.loads(response.content)
    formatted_response = json.dumps(parsed_response, indent=2)

    return Response(parsed_response['conversion_rates'])
