from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from bs4 import BeautifulSoup

import requests
import json

from .privatekeys import *

@api_view(['GET'])
def getViewRoutes(request):
    


    return Response()


@api_view(['GET'])
def getCurrencyViews(request):
    


    return Response()


@api_view(['GET'])
def getCaseViews(request):
    


    return Response()