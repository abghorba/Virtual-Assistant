from googlesearch import search

import os
import time


class GoogleHandler():
    def open_webpage(self, url):
        """
            Opens a url webpage.

            :returns: bool

        """
        try:
            webpage = '/usr/bin/open -a "/Applications/Google Chrome.app" ' + url
            os.system(webpage)
            time.sleep(3)
            return True
        except Exception as e:
            print("Could not open webpage.")
            return False


    def google_search(self, query):
        """
            Conducts a Google search with the given query.
            Relies heavily on Google's PageRank to supply the
            correct url as the first item returned in the search.

            :returns: URL as a str

        """
        try:
            links = []
            for url in search(query, tld='ca', num=10, stop=10, pause=2):
                links.append(url)
            
            return links[0]
        except Exception as e:
            print("Could not conduct Google search.")


    def google_maps_search(self, location):
        """
            Conducts a Google maps search with the given query.

            :returns: URL as a str

        """
        location = location.replace(" ", "%20")
        location_url = "https://www.google.com/maps/place/" + location

        return location_url