import requests

from bs4 import BeautifulSoup
from features.google import GoogleHandler
from imdb import IMDb


class IMDbScraper():

    def get_imdb_url(self, movie_title):
        """
        Takes in a movie name and conducts a Google
        search to retrieve the correct url.

        :param movie_title: The movie to search
        :return: String containing the IMDb URL.
        """

        if not movie_title:
            raise ValueError("Parameter 'movie_title' cannot be blank.")

        imdb_url = ""

        try:

            movie_title += " IMDb"
            google = GoogleHandler()
            imdb_url = google.google_search(movie_title)

        except Exception:
            print("Movie cannot be found.")

        return imdb_url

    def find_imdb(self, imdb_url):
        """
        Takes in the movie url and scrapes the
        necessary information from IMDb

        :param imdb_url: The url of the IMDb website
        :return: String containing the Google maps url
        """

        rating = {"title": "", "metascore": ""}

        try:

            page = requests.get(imdb_url)
            html_content = page.text
            soup = BeautifulSoup(html_content, "html.parser")
            title_html = soup.find(attrs={"data-testid": "hero-title-block__title"})
            title = title_html.get_text()
            year_html = soup.find(class_="ipc-link ipc-link--baseAlt ipc-link--inherit-color sc-8c396aa2-1 WIUyh")
            year = year_html.get_text()
            title_and_year = f"{title} ({year})"
            metascore_html = soup.find(class_="score-meta")
            metascore = metascore_html.get_text()

            rating["title"] = title_and_year
            rating["metascore"] = metascore

        except Exception:
            print("Movie cannot be found.")

        return rating

    def get_movie_review(self, movie_title):
        """
        Driver function to retrieve the movie review scores.

        :param movie_title: Movie being searched
        :return: String containing the movie review.
        """

        if not movie_title:
            raise ValueError("Parameter 'movie_title' cannot be blank.")

        review = ""

        try:
            # Use Google search to find the IMDb webpage
            imdb_url = self.get_imdb_url(movie_title)
            imdb_info = self.find_imdb(imdb_url)

            imdb_title = imdb_info["title"]
            metascore = imdb_info["metascore"]

            # Use IMDb object after scraping the title off the webpage
            moviesDB = IMDb()
            movies = moviesDB.search_movie(imdb_title)
            id = movies[0].getID()
            movie_info = moviesDB.get_movie(id)
            title = movie_info["title"]
            year = movie_info["year"]
            imdb_score = movie_info["rating"]

            review = f"{title} ({year}) has an IMDB Score of {imdb_score} and a Metascore of {metascore}."
            
        except Exception:
            print("Movie cannot be found.")

        return review
