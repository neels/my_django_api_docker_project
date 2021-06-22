from django.urls import path
from coin_api.views import Index, CoinList, MarketCap

urlpatterns = [
    path('coinList', CoinList.as_view()),
    path('marketCap', MarketCap.as_view()),
    path('', Index.as_view()),
]
