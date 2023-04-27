from PyDictionary import PyDictionary


class DictionarySearcher:
    def search_definition(self, word):
        """
        Searches for the definition of a word and returns
        all definitions

        :param word: English word we want to define
        :return: String containg word's definition
        """

        if not word:
            raise ValueError("Parameter 'word' cannot be blank.")

        definition = ""
        dictionary = PyDictionary()

        try:
            definitions = dictionary.meaning(word)
            definition_number = 1
            definitions_text = []

            for type in definitions:
                for meaning in definitions[type]:
                    current_meaning = f"{str(definition_number)}) {type}: {meaning.capitalize()}.\n"
                    definitions_text.append(current_meaning)
                    definition_number += 1

            definition = "".join(definitions_text)

        except Exception:
            print("This word does not exist in the English dictionary.")

        return definition
