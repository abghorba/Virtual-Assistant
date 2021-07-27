from bs4 import BeautifulSoup

import imdb
import requests
import googlehandler

class IMDbScraper():

    def get_imdb_url(self, query):
        """
            Takes in a raw query and conducts a Google search to retrieve
            the correct url.

            :param query: Movie/TV Show to search
            :type query: str
            :returns: str
        
        """
        try:
            query += ' IMDB'
            google = googlehandler.GoogleHandler()
            url = google.google_search(query)
            return url
        except Exception as e:
            print('Movie could not be found')


    def find_imdb(self, url):
        """
            Takes in a raw query and scrapes the necessary information from IMDb.

            :param query: The Movie/TV Show query received in.
            :type query: str
            :returns: dict

        """
        try:
            page = requests.get(url)
            html_content = page.text
            soup = BeautifulSoup(html_content, 'html.parser')
            title = soup.find(class_="TitleHeader__TitleText-sc-1wu6n3d-0 dxSWFG").get_text()
            year = soup.find(class_="TitleBlockMetaData__ListItemText-sc-12ein40-2 jedhex").get_text()
            title = f"{title} ({year})"
            metascore = soup.find(class_="score-meta").get_text()
            return {"title": title, "metascore": metascore}
        except Exception as e:

            print('Movie could not be found.')


    def get_movie_info(self, query):
        """
            Driver function to retrieve the movie information and review scores.

            :param query: Raw query with the Movie/TV Show being searched.
            :type query: str
            :returns: str

        """
        imdb_url = self.get_imdb_url(query)
        imdb_info = self.find_imdb(imdb_url)
        imdb_title = imdb_info['title']
        metascore = imdb_info['metascore']

        moviesDB = imdb.IMDb()
        movies = moviesDB.search_movie(imdb_title)
        id = movies[0].getID()
        movie_info = moviesDB.get_movie(id)
        title = movie_info['title']
        year = movie_info['year']
        imdb_score = movie_info['rating']

        review = f"{title} ({year}) has an IMDB Score of {imdb_score} and a Metascore of {metascore}."
        return review

def main():
    query = 'breaking bad'
   # query = 'the karate kid'
    i = IMDbScraper()
    url = i.get_imdb_url(query)
    print(url)
    stuff = i.find_imdb(url)
    print(stuff)

if __name__ == "__main__":
    main()