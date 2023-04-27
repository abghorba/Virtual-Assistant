import pytest

from src.features.dictionary import DictionarySearcher


class TestDictionarySearcher:
    @pytest.mark.parametrize(
        "word,expected",
        [
            (
                "bitter",
                (
                    "1) Noun: English term for a dry sharp-tasting ale with strong flavor of hops (usually on draft.\n"
                    "2) Noun: The taste experience when quinine or coffee is taken into the mouth.\n"
                    "3) Noun: The property of having a harsh unpleasant taste.\n"
                    "4) Verb: Make bitter.\n"
                    "5) Adjective: Marked by strong resentment or cynicism.\n"
                    "6) Adjective: Very difficult to accept or bear.\n"
                    "7) Adjective: Harsh or corrosive in tone.\n"
                    "8) Adjective: Expressive of severe grief or regret.\n"
                    "9) Adjective: Proceeding from or exhibiting great hostility or animosity.\n"
                    "10) Adjective: Causing a sharp and acrid taste experience.\n"
                    "11) Adjective: Causing a sharply painful or stinging sensation; used especially of cold.\n"
                    "12) Adverb: Extremely and sharply.\n"
                ),
            ),
            (
                "finance",
                (
                    "1) Noun: The commercial activity of providing funds and capital.\n"
                    "2) Noun: The branch of economics that studies the management of money and other assets.\n"
                    "3) Noun: The management of money and credit and banking and investments.\n"
                    "4) Verb: Obtain or provide money for.\n"
                    "5) Verb: Sell or provide on credit.\n"
                ),
            ),
            (
                "Tesla",
                (
                    "1) Noun: A unit of magnetic flux density equal to one weber per square meter.\n"
                    "2) Noun: United states electrical engineer and inventor (born in croatia but of serbian descent.\n"
                    "3) Noun: 1856-1943.\n"
                ),
            ),
            ("", "Parameter 'word' cannot be blank."),
        ],
    )
    def test_search_definition(self, word, expected):
        """Tests the search_definition function."""

        dictionary = DictionarySearcher()

        if not word:
            with pytest.raises(ValueError) as err_info:
                definition = dictionary.search_definition(word)

            assert expected in str(err_info.value)

        else:
            definition = dictionary.search_definition(word)

            assert isinstance(definition, str)
            assert definition == expected
