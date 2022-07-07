from googletrans import Translator, LANGCODES


class TranslatorHandler():
    
    def translate(self, text, language):
        """
        Takes a text string and translates to
        language of choice

        :param text: English text to translate
        :param language: The language to translate to
        :return: List [text, pronounciation, language code]
        """
        
        if not text:
            raise ValueError("Text cannot be blank.")

        if not language:
            raise ValueError("Language cannot be blank.")

        translated = []

        try:
            translator = Translator()
            language_code = LANGCODES[language]
            translated_text = translator.translate(text, src="en", dest=language_code)
            translated = [
                translated_text.text,
                translated_text.pronunciation,
                language_code,
            ]
            
        except Exception:
            print("This text cannot be translated.")

        return translated
