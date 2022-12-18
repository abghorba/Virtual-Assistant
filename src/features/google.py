import ssl
import time
import webbrowser

from googlesearch import search

# Temporary workaround due to the following in Python 3.10:
# DeprecationWarning: ssl.PROTOCOL_TLS is deprecated
ssl._create_default_https_context = ssl._create_unverified_context


class GoogleHandler():

    def open_webpage(self, url):
        """
        Opens a url webpage on default browser

        :param url: String url of webpage
        :return: True if webpage opens successfully; False otherwise
        """

        if not url:
            raise ValueError("Parameter 'url' cannot be blank.")

        success = False

        try:
            webbrowser.open(url)
            time.sleep(3)
            success = True

        except Exception:
            print("Could not open webpage.")

        return success

    def google_search(self, query):
        """
        Conducts a Google search with the given query.
        Relies heavily on Google's PageRank to supply the
        correct url as the first item returned in the search.

        :param query: The query to be Google searched
        :return: String containing first url from the Google search
        """

        if not query:
            raise ValueError("Parameter 'query' cannot be blank.")

        url_link = ""

        try:
            links = []

            for url in search(query, tld="ca", num=10, stop=10, pause=2):
                links.append(url)

            url_link = links[0]

        except Exception:
            print("Could not conduct Google search.")

        return url_link

    def google_maps_search(self, location):
        """
        Conducts a Google Maps search with the given query

        :param location: Location to be searched on Google Maps
        :return: String containing the Google maps url
        """
        
        if not location:
            raise ValueError("Parameter 'location' cannot be blank.")

        location = location.replace(" ", "%20")
        location_url = "https://www.google.com/maps/place/" + location

        return location_url
