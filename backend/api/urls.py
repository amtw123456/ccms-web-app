from django.urls import path
from api.views.case_views import *
from api.views.currency_views import *
from api.views.routes_views import *

urlpatterns = [
    path('get-case-details', getCsCaseDetails),
    path('get-case-item-order-histogram', getCsCaseOrderHistory),
    path('get-case-item-price-history', getCsCasePriceHistory),



    path("get-currency-exchange-rate", getCurrencyExchangeRates)
]