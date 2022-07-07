import pytest

from src.features.yahoo_finance import YahooFinanceScraper


class TestYahooFinanceScraper():

    @pytest.mark.parametrize(
        "query,expected",
        [
            (
                "stock price of Tesla",
                "https://finance.yahoo.com/quote/TSLA/"
            ),
            (
                "stock price of Walmart",
                "https://finance.yahoo.com/quote/WMT/"
            ),
            (
                "stock price of Apple",
                "https://finance.yahoo.com/quote/AAPL/"
            ),
            (
                "",
                "Parameter 'query' cannot be blank."
            ),
        ],
    )
    def test_get_yahoo_finance_url(self, query, expected):
        """Tests the get_yahoo_finance_url function."""

        yahoo = YahooFinanceScraper()

        if not query:

            with pytest.raises(ValueError) as err_info:
                yahoo_finance_url = yahoo.get_yahoo_finance_url(query)

            assert expected in str(err_info.value)

        else:

            yahoo_finance_url = yahoo.get_yahoo_finance_url(query)
            assert isinstance(yahoo_finance_url, str)
            assert yahoo_finance_url == expected

    @pytest.mark.parametrize(
        "query,expected",
        [
            (
                "stock price of Tesla",
                "The stock price is $XXX.XX per share."
            ),
            (
                "stock price of Walmart",
                "The stock price is $XXX.XX per share."
            ),
            (
                "stock price of Apple",
                "The stock price is $XXX.XX per share."
            ),
            (
                "",
                "Parameter 'query' cannot be blank."
            ),
        ],
    )
    def test_get_stock_price(self, query, expected):
        """Tests the get_stock_price function."""

        yahoo = YahooFinanceScraper()

        if not query:

            with pytest.raises(ValueError) as err_info:
                stock_price_info = yahoo.get_stock_price(query)

            assert expected in str(err_info.value)

        else:

            stock_price_info = yahoo.get_stock_price(query)

            assert isinstance(stock_price_info, str)
            assert "The stock price is " in expected
            assert " per share." in expected

            stock_price_info_list = stock_price_info.split(" ")
            stock_price = stock_price_info_list[4]

            assert "$" in stock_price

            stock_price = stock_price.replace("$", "").replace(",", "")

            assert float(stock_price) > 0
