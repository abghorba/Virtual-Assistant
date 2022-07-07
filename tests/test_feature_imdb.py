import pytest

from src.features.imdb import IMDbScraper

class TestIMDbScraper():

    @pytest.mark.parametrize(
        "movie_title,expected",
        [
            (
                "the karate kid",
                "https://www.imdb.com/title/tt0087538/"
            ),
            (
                "the silence of the lambs",
                "https://www.imdb.com/title/tt0102926/"
            ),
            (
                "jobs",
                "https://www.imdb.com/title/tt2357129/"
            ),
            (
                "",
                "Parameter 'movie_title' cannot be blank."
            ),
        ],
    )
    def test_imdb_url(self, movie_title, expected):
        """Tests the get_imdb_url function."""

        scraper = IMDbScraper()
        if not movie_title:
            with pytest.raises(ValueError) as err_info:
                imdb_url = scraper.get_imdb_url(movie_title)
            assert expected in str(err_info.value)
        else:
            imdb_url = scraper.get_imdb_url(movie_title)
            assert isinstance(imdb_url, str)
            assert imdb_url == expected

    @pytest.mark.parametrize(
        "imdb_url,expected",
        [
            (
                "https://www.imdb.com/title/tt0087538/",
                {
                    "title": "The Karate Kid (1984)",
                    "metascore": "60"
                },
            ),
            (
                "https://www.imdb.com/title/tt0102926/",
                {
                    "title": "The Silence of the Lambs (1991)",
                    "metascore": "85"
                },
            ),
            (
                "https://www.imdb.com/title/tt2357129/",
                {
                    "title": "Jobs (2013)",
                    "metascore": "44"
                },
            ),
            (
                "",
                {
                    "title": "",
                    "metascore": ""
                }
            ),
        ],
    )
    def test_find_imdb(self, imdb_url, expected):
        """Tests the find_imdb function."""

        scraper = IMDbScraper()
        imdb_info = scraper.find_imdb(imdb_url)

        assert isinstance(imdb_info, dict)
        assert len(imdb_info) == 2
        assert imdb_info == expected

    @pytest.mark.parametrize(
        "movie_title,expected",
        [
            (
                "the karate kid",
                "The Karate Kid (1984) has an IMDB Score of 7.3 and a Metascore of 60.",
            ),
            (
                "the silence of the lambs",
                "The Silence of the Lambs (1991) has an IMDB Score of 8.6 and a Metascore of 85.",
            ),
            (
                "jobs",
                "Jobs (2013) has an IMDB Score of 6.0 and a Metascore of 44."
            ),
            (
                "",
                "Parameter 'movie_title' cannot be blank."
            ),
        ],
    )
    def test_get_movie_info(self, movie_title, expected):
        """Tests the get_movie_review function."""

        scraper = IMDbScraper()
        if not movie_title:
            with pytest.raises(ValueError) as err_info:
                movie_review = scraper.get_movie_review(movie_title)
            assert expected in str(err_info.value)
        else:
            movie_review = scraper.get_movie_review(movie_title)
            assert isinstance(movie_review, str)
            assert movie_review == expected
