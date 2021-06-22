import pytest
from coin_api.helpers import CoingeckoApiHelper as helper


class TestCoinHelper():
    mock_data = ""

    def setup_method(self):
        self.mock_data = {"market_data": {"market_cap": {"gbp": 5391575812.385138, "zar": 108109882171.42863, }}}

    def test_api_call_function_with_ping(self):
        data, status = helper().make_api_call('ping')
        assert status == 200
        assert data['gecko_says'] == '(V3) To the Moon!'

    def test_market_cap_supported_currency(self):
        currency_supported = helper().check_if_currency_supported(self.mock_data['market_data']['market_cap'], 'zar')
        assert currency_supported is True

    def test_market_cap_currency_not_supported(self):
        currency_supported = helper().check_if_currency_supported(self.mock_data['market_data']['market_cap'], 'ggg')
        assert currency_supported is False

    def test_date_format_incorrect(self):
        assert helper().is_date_format_correct('12/03/2021') is False

    def test_date_format_correct(self):
        assert helper().is_date_format_correct('2021/06/21') is True
