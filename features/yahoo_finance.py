import requests

from bs4 import BeautifulSoup
from features.google import GoogleHandler


class YahooFinanceScraper():

    def get_yahoo_finance_url(self, query):
        """
        Takes in a raw query and conducts a Google
        search to retrieve the correct url

        :param query: Google search query containing company name
        :return: String URL of the company's Yahoo Finance webpage.
        """

        if not query:
            raise ValueError("Parameter 'query' cannot be blank.")

        yahoo_finance_url = ""

        try:
            query += " Yahoo Finance"
            google = GoogleHandler()
            yahoo_finance_url = google.google_search(query)

        except Exception:
            print("This company is not found on Yahoo Finance.")

        return yahoo_finance_url

    def get_stock_price(self, query):
        """
        Scrapes the Yahoo Finance website for the stock price

        :param query: Google search query containing company name
        :return: String containg the company's stock price
        """

        if not query:
            raise ValueError("Parameter 'query' cannot be blank.")

        stock_price_information = ""

        try:
            yahoo_finance_url = self.get_yahoo_finance_url(query)
            page = requests.get(yahoo_finance_url)
            html_content = page.text
            soup = BeautifulSoup(html_content, "html.parser")
            stock_price = soup.find(
                class_="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"
            ).get_text()
            stock_price_information = f"The stock price is ${stock_price} per share."

        except Exception:
            print("Stock price cannot be retrieved.")

        return stock_price_information
