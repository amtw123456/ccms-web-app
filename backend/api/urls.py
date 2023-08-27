from django.urls import path
from api.views.case_views import *
from api.views.currency_views import *
from api.views.routes_views import *

urlpatterns = [
    path("", getViewRoutes),
    path("view-case-routes", getCaseViews),
    path("view-currency-routes", getCurrencyViews),

    path('get-all-case-details', getCsCaseDetails),
    path('get-case-item-order-histogram', getCsCaseOrderHistory),
    path('get-case-item-price-history-daily', getCsCasePriceHistoryDaily),

    path('retreive-specific-case-item-price-history-daily',retreiveSpecificCaseDailyPriceHistoryFromDatabase),

    path('put-specific-case-item-price-history-daily', putSpecficCaseDailyPriceHistoryToDatabase),
    path('put-all-case-item-price-history-daily', putAllCaseDailyPriceHistoryToDatabase),

    path('create-all-case-item-price-history-daily', createAllCsCaseDailyPriceHistoryDaily),
    path('create-specific-case-item-price-history-daily', createSpecificCsCasePriceHistoryDaily),

    path("get-all-currency-exchange-rate", getCurrencyExchangeRates),
]