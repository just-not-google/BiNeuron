from AlexRadar.additional_functions.getting_text_from_files import main_get_text_from_files
from AlexRadar.additional_functions.detect_programming_language import detect_programming_language
from typing import List, Optional, Literal, Dict
from AlexRadar.data.hint_words_for_defining_programming_languages import HINT_WORDS
from AlexRadar.additional_functions.logic_orchestra.orchestrator_ai_models import orchestrator_ai_models
from AlexRadar.data.constants_for_functions import (TYPE_DEFAULT, MARKER_FOR_FILES, MAIN_LANGUAGE,
                                                    LITE_TYPE, TINY_TYPE, NUMBER_ATTEMPTS)
import logging


logger = logging.getLogger(__name__)

class DefiningProgrammingLanguage:
    def __init__(self,
                 translated_text: str,
                 unread_files: Optional[List[str]] = None,
                 additional_files: Optional[List[str]] = None,
                 with_ai_orchestrator: bool = False,
                 proprietary_algorithms: bool = False,
                 lang_lst: Optional[List[str]] = None,
                 use_gpu: bool = False,
                 verbose: bool = False,
                 determinant_mode: Optional[Literal["lite", "full", "auto"]] = LITE_TYPE,
                 proxies: Optional[Dict] = None,
                 accurate_translation: bool = False,
                 your_key_for_deepl: str = "",
                 request_language: str = MAIN_LANGUAGE,
                 cloud_version: bool = False,
                 with_deepseek: bool = True,
                 model_size: Literal["tiny", "small", "base", "large", "gundam"] = TINY_TYPE,
                 crop_mode: bool = False,
                 base_url: str = "https://api.siliconflow.cn/v1/chat/completions",
                 api_key_for_deepseek_ocr: Optional[str] = None,
                 timeout_for_deepseek_ocr: Optional[int] = None,
                 max_rate_limit_retries: Optional[int] = NUMBER_ATTEMPTS,
                 prefer_mirror: bool = True) -> None:
        """
        Initialize the language detector with all necessary configuration.
        :param translated_text: The already-translated user input.
        :param unread_files: List of file paths that were not readable (used only for context).
        :param additional_files: List of file paths to extract and include in analysis.
        :param with_ai_orchestrator: If True, use an AI model to detect languages.
        :param proprietary_algorithms: If True, use keyword-based detection (ignored if AI is enabled).
        :param lang_lst: Language codes for OCR when extracting text from images.
        :param use_gpu: Whether to use GPU for OCR.
        :param verbose: Enable verbose output from OCR and other submodules.
        :param determinant_mode: Translation detection mode ('lite', 'full', 'auto').
        :param proxies: Proxy settings for translation services.
        :param accurate_translation: If True, use DeepL (with key) instead of Google Translate.
        :param your_key_for_deepl: API key for DeepL translation.
        :param request_language: Target language code for translation (default MAIN_LANGUAGE).
        :param cloud_version: If True, use cloud API for DeepSeek OCR.
        :param with_deepseek: If True, use DeepSeek OCR; otherwise use EasyOCR.
        :param model_size: DeepSeek model size.
        :param crop_mode: Enable crop mode for DeepSeek OCR.
        :param base_url: Base URL for DeepSeek cloud API.
        :param api_key_for_deepseek_ocr: API key for DeepSeek cloud.
        :param timeout_for_deepseek_ocr: Timeout for DeepSeek requests.
        :param max_rate_limit_retries: Number of retries on rate limit errors.
        :param prefer_mirror: If True, forces using the mirror endpoint (hf-mirror.com).
        """
        logger.info("Initializing DefiningProgrammingLanguage")
        self.translated_text = translated_text
        self.unread_files = unread_files
        self.additional_files = additional_files
        self.with_ai_orchestrator = with_ai_orchestrator
        self.proprietary_algorithms = proprietary_algorithms
        self.prefer_mirror = prefer_mirror
        self.settings_for_get_text = {
            "lang_lst": lang_lst,
            "use_gpu": use_gpu,
            "verbose": verbose,
            "determinant_mode": determinant_mode,
            "proxies": proxies,
            "accurate_translation": accurate_translation,
            "your_key_for_deepl": your_key_for_deepl,
            "request_language": request_language,
            "cloud_version": cloud_version,
            "with_deepseek": with_deepseek,
            "model_size": model_size,
            "crop_mode": crop_mode,
            "base_url": base_url,
            "api_key_for_deepseek_ocr": api_key_for_deepseek_ocr,
            "timeout_for_deepseek_ocr": timeout_for_deepseek_ocr,
            "max_rate_limit_retries": max_rate_limit_retries
        }

    def defining_programming_language_for_files(self) -> str:
        """
        Process each file in `additional_files`, extract its text, detect its language,
        and return a formatted string with file name and detected language.
        For each file, the method calls `main_get_text_from_files` with the stored settings,
        then uses `detect_programming_language` on the extracted text to guess the language.
        The result is a multiline string where each line is:
        "file_path - detected_language: extracted_text"
        :return: A string containing language annotations for all processed files,
        joined by newlines. If no files are provided, returns an empty string.
        """
        logger.info("Challenge defining_programming_language_for_files")
        answer_file = []

        for file in self.additional_files:
            value = main_get_text_from_files(file,
                                             **self.settings_for_get_text)
            key = f"{file} - {detect_programming_language(value)}"
            answer = f"{key}: {value}"
            answer_file.append(answer)

        logger.info("Programming languages have been defined for each attached file.")
        return "\n".join(answer_file)

    def defining_programming_language_for_str(self) -> str:
        """
        Determine the primary programming language from the combined text and file context.
        The method works as follows:
        1. If `additional_files` is provided, appends file markers, unread file names (if any),
           and the language‑annotated file content to `translated_text`.
        2. Detects languages using one of three methods:
           - If `with_ai_orchestrator` is True, uses `orchestrator_ai_models`.
           - Else if `proprietary_algorithms` is True, uses keyword matching from `HINT_WORDS`.
           - Else uses `detect_programming_language` (library‑based).
        3. If the detection yields more than one language or none, returns `TYPE_DEFAULT`.
        4. Otherwise, returns the single detected language identifier.
        :return: A single language identifier string, or `TYPE_DEFAULT` if ambiguous / none.
        """
        logger.info("Challenge defining_programming_language_for_str")
        if not self.additional_files is None:
            self.translated_text += MARKER_FOR_FILES

            if not self.unread_files is None:
                self.translated_text += "\n".join(self.unread_files)

            self.translated_text += self.defining_programming_language_for_files()
            logger.info("Added all files to the text.")

        prog_langs_lst = []

        if self.with_ai_orchestrator:
            prog_langs_lst = orchestrator_ai_models(user_prompt=self.translated_text,
                                                    prefer_mirror=self.prefer_mirror)
            logger.info("Programming languages have been defined by AI.")
        else:
            if self.proprietary_algorithms:
                for prog_lang, hint_words in HINT_WORDS.items():
                    for hw in hint_words:
                        if hw in self.translated_text.lower():
                            prog_langs_lst.append(prog_lang)
                            break
            else:
                prog_langs_lst = detect_programming_language(self.translated_text)
            logger.info("Programming languages were defined by an algorithm.")

        ln_lst = len(prog_langs_lst)

        if ln_lst > 1 or ln_lst == 0:
            logger.info("A multilingual AI model was chosen.")
            return TYPE_DEFAULT

        logger.info("A highly specialized AI model was chosen for a single programming language.")
        return prog_langs_lst[0]