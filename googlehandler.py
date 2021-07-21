from googlesearch import search

import os
import time


class GoogleHandler():
    def open_webpage(self, url):
        """
            Opens a url webpage.

            :returns: None

        """
        webpage = '/usr/bin/open -a "/Applications/Google Chrome.app" ' + url
        os.system(webpage)
        time.sleep(3)


    def google_search(self, query):
        """
            Conducts a Google search with the given query.
            Relies heavily on Google's PageRank to supply the
            correct url as the first item returned in the search.

            :returns: None

        """
        link = []
        for j in search(query, tld='ca', num=10, stop=10, pause=2):
            link.append(j)
        self.open_webpage(link[0])


    def google_maps_search(self, location):
        """
            Conducts a Google maps search with the given query.

            :returns: None

        """
        location = location.replace(" ", "%20")
        location_url = "https://www.google.com/maps/place" + location
        self.open_webpage(location_url)