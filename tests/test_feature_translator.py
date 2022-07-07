import pytest

from src.features.translate import TranslatorHandler


class TestTranslator():

    @pytest.mark.parametrize(
        "text,language,expected_translation,expected_pronounciation,expected_langcode",
        [
            (
                "Hello world!",
                "spanish",
                "¡Hola Mundo!",
                None,
                "es"
            ),
            (
                "Hello world!",
                "french",
                "Bonjour le monde!",
                None,
                "fr"
            ),
            (
                "Thank you for testing the virtual assistant.",
                "russian",
                "Спасибо за тестирование виртуального помощника.",
                "Spasibo za testirovaniye virtualʹnogo pomoshchnika.",
                "ru",
            ),
            (
                "",
                "spanish",
                "Text cannot be blank.",
                "",
                ""
            ),
            (
                "I don't know what to translate to!",
                "",
                "Language cannot be blank.",
                "",
                "",
            ),
        ],
    )
    def test_translate(self, text, language, expected_translation,
                       expected_pronounciation, expected_langcode):
        """Tests the translate function."""

        translator = TranslatorHandler()

        if not (text and language):

            with pytest.raises(ValueError) as err_info:
                translated_text = translator.translate(text, language)

            assert expected_translation in str(err_info.value)

        else:

            translated_text = translator.translate(text, language)

            assert translated_text[0] == expected_translation
            assert translated_text[1] == expected_pronounciation
            assert translated_text[2] == expected_langcode
