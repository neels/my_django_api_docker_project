from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from coin_api.helpers import CoingeckoApiHelper


class Index(APIView):

    @method_decorator(cache_page(60 * 60 * 1))
    def get(self, request):
        """
        Landing Page
        """
        return Response(self.available_routes(), status=status.HTTP_200_OK)

    def available_routes(self):
        return {
            "available_routs": {
                "/coinList": "List of all supported coins by CoinGecko",
                "/marketCap": "Market cap for the given coin"
            }
        }


class CoinList(APIView):

    @method_decorator(cache_page(60 * 60 * 1))
    def get(self, request):
        """
        Will return list of coins
        """
        api_response, request_status = CoingeckoApiHelper().make_api_call('get_coins_list')
        return Response(api_response, status=request_status)


class MarketCap(APIView):

    @method_decorator(cache_page(60 * 60 * 1))
    def get(self, request):
        """
        Will return market_cap for given currency
        """
        if not CoingeckoApiHelper().is_required_fields_present(["coin_id", "date", "currency"], request):
            return Response({"error": "coin_id, currency and date are required"}, status=status.HTTP_400_BAD_REQUEST)

        api_response, request_status = CoingeckoApiHelper().get_history(request)

        return Response(api_response, status=request_status)
