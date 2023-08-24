from django.urls import path
from api.view.views import *

urlpatterns = [
    path('get-case-price', getCsCasePrice),
]