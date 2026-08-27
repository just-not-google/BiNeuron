from deep_translator import GoogleTranslator
from typing import Dict
import logging
from langdetect import detect as ln_detect
from fast_langdetect import detect as fst_detect
from AlexRadar.data.constants_for_functions import MAIN_LANGUAGE, LITE_TYPE
from typing import Optional, Literal
import deepl
from functools import lru_cache


logger = logging.getLogger(__name__)

class TranslatorText:
    def __init__(self,
                 original_text: str,
                 determinant_mode: Optional[Literal["lite", "full", "auto"]] = LITE_TYPE,
                 proxies: Optional[Dict] = None,
                 accurate_translation: bool = False,
                 your_key_for_deepl: str = "",
                 request_language: str = MAIN_LANGUAGE) -> None:
        """
        Initialize the translator with text and configuration.
        :param original_text: The text to be translated.
        :param determinant_mode: Mode for language detection ('lite', 'full', 'auto').
        :param proxies: Dictionary with proxy settings for requests.
        :param accurate_translation: If True, attempt to use DeepL first.
        :param your_key_for_deepl: API key for DeepL (required if accurate_translation is True).
        :param request_language: Target language code (default is MAIN_LANGUAGE).
        """
        logger.info("Initializing TranslatorText")
        self.original_text = original_text
        self.determinant_mode = determinant_mode
        self.proxies = proxies
        self.accurate_translation = accurate_translation
        self.your_key_for_deepl = your_key_for_deepl
        self.request_language = request_language

    def _needs_translation_to_main_language(self) -> bool:
        """
        Determine if the original text needs translation to the main language.
        Uses two language detection algorithms (langdetect and fast_langdetect)
        with fallback. Returns True if the text is not already in the main language,
        otherwise False.
        """
        logger.info("Challenge _needs_translation_to_main_language")
        try:
            answer_1 = ln_detect(self.original_text)
            logger.info("The natural language was determined by the first algorithm.")

            if answer_1 == MAIN_LANGUAGE:
                return False
            else:
                return True

        except Exception as e:
            logger.exception(f"Error when trying to determine the language of the text - {e}")
            answer_2 = fst_detect(self.original_text, model=self.determinant_mode)[0]
            logger.info("The natural language was determined by the second algorithm.")

            if answer_2["lang"] == MAIN_LANGUAGE and answer_2["score"] >= 0.9:
                return False
            else:
                return True

    @lru_cache(maxsize=None)
    def _basic_logic_text_translation(self) -> str:
        """
        Perform the actual translation using DeepL or Google Translator.
        Tries DeepL if accurate_translation is True and a key is provided,
        then falls back to Google Translator. If all fail, returns the original text.
        Results are cached by lru_cache to avoid repeated calls for the same input.
        """
        if self.accurate_translation:
            try:
                deepl_client = deepl.DeepLClient(auth_key=self.your_key_for_deepl,
                                                 proxy=self.proxies)
                result = deepl_client.translate_text(text=self.original_text,
                                                     target_lang=self.request_language)
                logger.info("The text was translated thanks to DeepL.")
                return result.text
            except Exception as e:
                logger.exception(f"Error when trying to translate text (DeepL) - {e}")

        try:
            translator = GoogleTranslator(source="auto",
                                          target=self.request_language,
                                          proxies=self.proxies)
            logger.info("The text was translated thanks to Google Translator.")
            return translator.translate(text=self.original_text)
        except Exception as e:
            logger.exception(f"Error when trying to translate text (Google Translator) - {e}")

        logger.warning("All translation attempts failed, returning original text.")
        return self.original_text

    def text_translation_into_different_language(self) -> Optional[str]:
        """
        Translate the text into the target language, with automatic fallback.
        If the first translation attempt fails due to unsupported language,
        it checks if translation to the main language is needed and retries.
        Returns the translated text or the original if all fails.
        """
        logger.info("Challenge text_translation_into_different_language")
        try:
            try:
                return self._basic_logic_text_translation()
            except Exception as e:
                logger.warning(f"Error because this translation language was not found or is not supported - {e}")
                if self._needs_translation_to_main_language():
                    self.request_language = MAIN_LANGUAGE
                    return self._basic_logic_text_translation()
                else:
                    logger.info("The text does not need to be translated.")
                    return self.original_text
        except Exception as e:
            logger.exception(f"Unexpected error in translation process - {e}")
            return self.original_text

    def main_translater(self) -> str:
        """
        Public method to start the translation process.
        Calls text_translation_into_different_language and ensures a string is returned,
        falling back to the original text if the result is None.
        """
        logger.info("Challenge main_translater")
        translated_text = self.text_translation_into_different_language()

        if translated_text is None:
            return self.original_text

        return translated_text