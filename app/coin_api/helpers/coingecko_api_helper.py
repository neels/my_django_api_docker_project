import datetime
import logging
from rest_framework import status
from pycoingecko import CoinGeckoAPI

logger = logging.getLogger(__name__)


class CoingeckoApiHelper:

    @staticmethod
    def make_api_call(function_to_call, params=None):
        """
        Make the call to CoinGecko and process response and status

        :param function_to_call: str
        :param params: list
        :return
        """
        if params is None:
            params = []

        request_status = status.HTTP_200_OK
        try:
            # api_response = CoinGeckoAPI().get_coins_list()
            func_name = function_to_call
            function = getattr(CoinGeckoAPI(), func_name, {})
            api_response = function(*params)
        except Exception as e:
            api_response = {"error": f"oops....Something went wrong. Please try again"}
            request_status = status.HTTP_503_SERVICE_UNAVAILABLE
            logger.error(f"Error on api call to {function_to_call} with error: {e}")

        return api_response, request_status

    @staticmethod
    def is_required_fields_present(required_fields, request_data):
        """
        Check if all of the required fields are in the request to proceed

        :param required_fields: list
        :param request_data: request:
        :return: bool
        """
        for i in required_fields:
            if i not in request_data.GET:
                return False
        return True

    @staticmethod
    def check_if_currency_supported(api_response, currency):
        """
        Check if the currency requested is available

        :param api_response: dict
        :param currency: str
        :return: bool
        """
        return True if currency in api_response.keys() else False

    @staticmethod
    def get_market_cap(request, api_response, request_status):
        """
        Returns the market cap if available or error.

        :param request: request
        :param api_response: dict
        :param request_status: status
        :return: tuple
        """

        if 'market_data' in api_response:
            market_cap = api_response['market_data']['market_cap']
            currency_lower = request.GET.get('currency').lower()

            if CoingeckoApiHelper().check_if_currency_supported(market_cap, currency_lower):
                api_response = {currency_lower: market_cap[currency_lower]}
            else:
                currency_list = ",".join(market_cap.keys())
                api_response = {"error": f"Currency '{currency_lower}' not allowed. "
                                         f"Supported currencies are {currency_list}"}
                request_status = status.HTTP_404_NOT_FOUND
        return api_response, request_status

    def get_history(self, request):
        """
        This combines two functions to keep the code compact to prccess the get_coin_history_by_id data

        :param request: request
        :return: tuple
        """
        date = request.GET.get('date')
        if not self.is_date_format_correct(date):
            return {"error": "date format should be YYYY/MM/DD"}, status.HTTP_400_BAD_REQUEST

        api_response, request_status = self.make_api_call(
            'get_coin_history_by_id',
            [
                request.GET.get('coin_id'),
                datetime.datetime.strptime(date.replace("-", "/"), "%Y/%m/%d").strftime("%d-%m-%Y")
            ]
        )

        return self.get_market_cap(request, api_response, request_status)

    @staticmethod
    def is_date_format_correct(date_to_check):
        try:
            datetime.datetime.strptime(date_to_check, '%Y/%m/%d')
        except Exception:
            return False

        return True

