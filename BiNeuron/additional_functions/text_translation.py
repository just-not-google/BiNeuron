from deep_translator import GoogleTranslator
from typing import Dict
import logging
from langdetect import detect as ln_detect
from fast_langdetect import detect as fst_detect
from BiNeuron.data.constants_for_functions import MAIN_LANGUAGE, LITE_TYPE
from typing import Optional, Literal, Union
import deepl
from functools import lru_cache
import argostranslate.package
import argostranslate.translate


logger = logging.getLogger(__name__)

class TranslatorText:
    def __init__(self,
                 original_text: str,
                 determinant_mode: Optional[Literal["lite", "full", "auto"]] = LITE_TYPE,
                 proxies: Optional[Dict] = None,
                 accurate_translation: bool = False,
                 your_key_for_deepl: str = "",
                 request_language: str = MAIN_LANGUAGE,
                 local_trans: bool = False,
                 from_code_lang: str = "") -> None:
        """
        Initialize the translator with text and configuration.
        :param original_text: The text to be translated.
        :param determinant_mode: Mode for language detection ('lite', 'full', 'auto').
        :param proxies: Dictionary with proxy settings for requests (used by DeepL and Google).
        :param accurate_translation: If True, attempt to use DeepL first (requires key).
        :param your_key_for_deepl: API key for DeepL (required if accurate_translation is True).
        :param request_language: Target language code (default is MAIN_LANGUAGE).
        :param local_trans: If True, use ArgosTranslate for fully offline translation.
        :param from_code_lang: Source language code for local translation (e.g., 'en', 'ru').
        """
        logger.info("Initializing TranslatorText")
        self.original_text = original_text
        self.determinant_mode = determinant_mode
        self.proxies = proxies
        self.accurate_translation = accurate_translation
        self.your_key_for_deepl = your_key_for_deepl
        self.request_language = request_language
        self.local_trans = local_trans
        self.from_code_lang = from_code_lang

    def _local_translator(self) -> Union[str, bool]:
        """
        Fully local text translation using ArgosTranslate.
        Attempts to find and install a language package for the given source
        and target languages, then translates the text completely offline.
        Note: the current implementation re-downloads the language package on every
        call, which is inefficient. Consider caching installed packages to avoid
        redundant downloads.
        :return: Translated text as a string on success, or False on failure.
        """
        logger.info("Challenge local_translator")
        try:
            available_packages = argostranslate.package.load_available_packages()
            package_to_install = next(filter(
                lambda x: x.from_code == self.from_code_lang
                          and x.to_code == self.request_language,
                available_packages))
            argostranslate.package.install_from_path(package_to_install.download())
            translated_text = argostranslate.translate.translate(self.original_text,
                                                                 from_code=self.from_code_lang,
                                                                 to_code=self.request_language)

            logger.info("The translated text of the local type was received.")
            return translated_text
        except Exception as e:
            logger.exception(f"An error occurred while trying to translate the text locally - {e}")
            return False

    def _needs_translation_to_main_language(self) -> bool:
        """
        Determine if the original text needs translation to the main language.
        Uses two language detection algorithms (langdetect and fast_langdetect)
        with fallback. Returns True if the text is not already in the main language,
        otherwise False.
        :return: True if translation to the main language is needed, False otherwise.
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
        Note: lru_cache on an instance method caches per-instance (since `self` is part
        of the key), so cross-instance caching does not occur.
        :return: Translated text, or the original text if all attempts fail.
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
        If local translation is enabled and a source language code is provided,
        it attempts to use ArgosTranslate first. If that fails or is disabled,
        it falls back to DeepL or Google Translator.
        If the first attempt fails due to an unsupported language, it checks
        whether translation to the main language is needed and retries.
        If all attempts fail, returns the original text.
        :return: Translated text, or the original text if all attempts fail.
        """
        logger.info("Challenge text_translation_into_different_language")
        try:
            try:
                if self.local_trans and len(self.from_code_lang) > 0:
                    answer = self._local_translator()

                    if isinstance(answer, str):
                        return answer

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
        Validates that the input text is not empty or whitespace-only.
        Calls `text_translation_into_different_language` and ensures a string
        is returned, falling back to the original text if the result is None.
        :return: Translated text, or an empty string if the input was empty.
        """
        logger.info("Challenge main_translater")
        if not self.original_text or not self.original_text.strip():
            return ""

        translated_text = self.text_translation_into_different_language()

        if translated_text is None:
            return self.original_text

        return translated_text