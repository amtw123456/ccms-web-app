from django.urls import path
from api.view.views import *

urlpatterns = [
    path('get-case-price', getCsCasePrice),
    path('get-case-item-order-histogram', getCsCaseOrderHistory),
    path('get-case-item-price-history', getCsCasePriceHistory),
    path('get-cookie', getcookie),
]