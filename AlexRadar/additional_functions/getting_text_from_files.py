from AlexRadar.additional_functions.text_translation import TranslatorText
import easyocr
import pymupdf
import functools
import docx2txt
import logging
from odfdo import Document
import pptx2txt2
from typing import List, Optional, Literal, Dict
from pathlib import Path
from AlexRadar.data.constants_for_functions import PHOTO_FORMATS
from AlexRadar.data.constants_for_functions import (NUMBER_ATTEMPTS, TINY_TYPE, DEVICE_OPTIONS,
                                                    MAIN_LANGUAGE, LITE_TYPE)
from AlexRadar.additional_functions.advanced_definition_text_from_image import LaunchDeepSeekOCR


logger = logging.getLogger(__name__)

def handle_errors(func):
    """
    Decorator that catches exceptions and returns an error message with the file name.
    :param func: The function to wrap.
    :return: Wrapped function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        file_name = kwargs.get('file_name')
        if file_name is None and len(args) > 0:
            file_name = args[0]
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            logger.exception(f"Error when trying to get text from a file - {e}")
            return f"<< {str(e)} >> - {file_name}"
    return wrapper

def _settings_for_translator(determinant_mode: Optional[Literal["lite", "full", "auto"]] = LITE_TYPE,
                             proxies: Optional[Dict] = None,
                             accurate_translation: bool = False,
                             your_key_for_deepl: str = "",
                             request_language: str = MAIN_LANGUAGE) -> Dict:
    """
    Builds a dictionary of parameters for initializing TranslatorText.
    :param determinant_mode: Language detection mode ('lite', 'full', 'auto').
    :param proxies: Dictionary with proxy settings for requests.
    :param accurate_translation: If True, attempt to use DeepL first.
    :param your_key_for_deepl: API key for DeepL (required if accurate_translation is True).
    :param request_language: Target language code (default is MAIN_LANGUAGE).
    :return: Dictionary with translation settings.
    """
    return {
        "determinant_mode": determinant_mode,
        "proxies": proxies,
        "accurate_translation": accurate_translation,
        "your_key_for_deepl": your_key_for_deepl,
        "request_language": request_language
    }

def _translate_text(text: str, settings: Dict) -> str:
    """
    Translates the text using the transmitted settings.
    If the text is empty or contains only whitespace, returns an empty string.
    :param text: Text to be translated.
    :param settings: Dictionary with parameters for TranslatorText.
    :return: Translated text or empty string.
    """
    if not text or not text.strip():
        return ""
    return TranslatorText(original_text=text, **settings).main_translater()

@handle_errors
def get_text_from_pdf(file_name: str,
                      translation_settings: Dict,
                      **kwargs) -> str:
    """
    Extracts and translates text from a PDF file.
    :param file_name: Path to the PDF file.
    :param translation_settings: Dict with settings for TranslatorText.
    :param kwargs: Additional unused parameters.
    :return: Translated text with a marker indicating the file name.
    """
    logger.info("Challenge get_text_from_pdf")
    doc = pymupdf.open(file_name)
    answer_text = ""
    for page in doc:
        page_text = page.get_text()
        translated = _translate_text(page_text, translation_settings)
        answer_text += f"{translated} \n\n"
    doc.close()
    logger.info("The text was received from the PDF file.")
    return f"<< {answer_text} >> - {file_name}\n"


@handle_errors
def get_text_from_word(file_name: str,
                       translation_settings: Dict,
                       **kwargs) -> str:
    """
    Extracts and translates text from a Word (.docx) file.
    :param file_name: Path to the Word file.
    :param translation_settings: Dict with settings for TranslatorText.
    :param kwargs: Additional unused parameters.
    :return: Translated text with a marker indicating the file name.
    """
    logger.info("Challenge get_text_from_word")
    full_text = docx2txt.process(file_name)
    translated = _translate_text(full_text, translation_settings)
    logger.info("The text was received from the WORD file.")
    return f"<< {translated} >> - {file_name}\n"


@handle_errors
def get_text_from_odf(file_name: str,
                      translation_settings: Dict,
                      **kwargs) -> str:
    """
    Extracts and translates text from an ODF (OpenDocument) file.
    :param file_name: Path to the ODF file.
    :param translation_settings: Dict with settings for TranslatorText.
    :param kwargs: Additional unused parameters.
    :return: Translated text with a marker indicating the file name.
    """
    logger.info("Challenge get_text_from_odf")
    doc = Document(file_name)
    all_text = []
    for element in doc.body.get_children():
        if hasattr(element, 'text'):
            all_text.append(element.text)
    org_text = '\n'.join(all_text)
    translated = _translate_text(org_text, translation_settings)
    logger.info("The text was obtained from an ODF file.")
    return f"<< {translated} >> - {file_name}\n"

@handle_errors
def get_text_from_pptx(file_name: str,
                       translation_settings: Dict,
                       **kwargs) -> str:
    """
    Extracts and translates text from a PowerPoint (.pptx) file.
    :param file_name: Path to the PowerPoint file.
    :param translation_settings: Dict with settings for TranslatorText.
    :param kwargs: Additional unused parameters.
    :return: Translated text with a marker indicating the file name.
    """
    logger.info("Challenge get_text_from_pptx")
    answer = pptx2txt2.extract_text(file_name)
    translated = _translate_text(answer, translation_settings)
    logger.info("The text was received from the PowerPoint file.")
    return f"<< {translated} >> - {file_name}\n"

@handle_errors
def getting_text_from_files(file_name: str,
                            translation_settings: Dict,
                            **kwargs) -> str:
    """
    Reads and translates text from a plain text file.
    :param file_name: Path to the text file.
    :param translation_settings: Dict with settings for TranslatorText.
    :param kwargs: Additional unused parameters.
    :return: Translated text with a marker indicating the file name.
    """
    logger.info("Challenge getting_text_from_files")
    with open(file_name, 'r', encoding='utf-8') as file:
        content = file.read()
        translated = _translate_text(content, translation_settings)
        logger.info("The text was received from a TXT file.")
        return f"<< {translated} >> - {file_name}\n"

def _easy_ocr_get_text(file_name: str,
                       lang_lst: List[str],
                       use_gpu: bool,
                       verbose: bool) -> List[str]:
    """
    Extracts text from an image using EasyOCR.
    :param file_name: Path to the image file.
    :param lang_lst: List of language codes for OCR (e.g., ['en', 'ru']).
    :param use_gpu: Whether to use GPU for OCR.
    :param verbose: Enable verbose output from EasyOCR.
    :return: List of detected text strings, or empty list on error.
    """
    logger.info("Challenge _easy_ocr_get_text")
    try:
        reader = easyocr.Reader(lang_list=lang_lst,
                                gpu=use_gpu,
                                verbose=verbose)
        result = reader.readtext(image=file_name,
                                 detail=0)
        logger.info("The text was successfully obtained thanks to EasyOCR.")
        return result
    except Exception as e:
        logger.exception(f"Error when trying to read text from a photo using EasyOCR - {e}")
        return []

@handle_errors
def logic_for_ocr(file_name: str,
                  translation_settings: Dict,
                  lang_lst: Optional[List[str]] = None,
                  with_deepseek: bool = True,
                  use_gpu: bool = False,
                  verbose: bool = False,
                  cloud_version: bool = False,
                  model_size: Literal["tiny", "small", "base", "large", "gundam"] = TINY_TYPE,
                  crop_mode: bool = False,
                  base_url: str = "https://api.siliconflow.cn/v1/chat/completions",
                  api_key_for_deepseek_ocr: Optional[str] = None,
                  timeout_for_deepseek_ocr: Optional[int] = None,
                  max_rate_limit_retries: Optional[int] = NUMBER_ATTEMPTS) -> str:
    """
    Extracts text from an image using OCR (EasyOCR or DeepSeek) and translates it.
    :param file_name: Path to the image file.
    :param translation_settings: Dict with settings for TranslatorText.
    :param lang_lst: List of language codes for OCR (used for EasyOCR). Defaults to [MAIN_LANGUAGE].
    :param with_deepseek: If True, use DeepSeek OCR; otherwise use EasyOCR.
    :param use_gpu: Whether to use GPU for OCR.
    :param verbose: Enable verbose output.
    :param cloud_version: If True, use cloud API for DeepSeek.
    :param model_size: Size of the DeepSeek model.
    :param crop_mode: Enable crop mode for DeepSeek.
    :param base_url: API base URL for DeepSeek cloud.
    :param api_key_for_deepseek_ocr: API key for DeepSeek cloud.
    :param timeout_for_deepseek_ocr: Timeout for DeepSeek requests.
    :param max_rate_limit_retries: Number of retries on rate limit.
    :return: Translated text with a marker indicating the file name.
    """
    logger.info("Challenge logic_for_ocr")

    if lang_lst is None:
        lang_lst = [MAIN_LANGUAGE]

    device = DEVICE_OPTIONS[1] if use_gpu else DEVICE_OPTIONS[0]

    if with_deepseek:
        result = LaunchDeepSeekOCR(
            photo_path=file_name,
            cloud_version=cloud_version,
            model_size=model_size,
            device=device,
            crop_mode=crop_mode,
            base_url=base_url,
            api_key_for_deepseek_ocr=api_key_for_deepseek_ocr,
            timeout_for_deepseek_ocr=timeout_for_deepseek_ocr,
            max_rate_limit_retries=max_rate_limit_retries
        ).advanced_definition_text_from_image()
    else:
        result_list = _easy_ocr_get_text(
            file_name=file_name,
            lang_lst=lang_lst,
            use_gpu=use_gpu,
            verbose=verbose
        )

        if not result_list:
            return "EasyOCR couldn't read the text from the photo."
        result = "\n".join(result_list)

    translated = _translate_text(result, translation_settings)
    final_text = f"<< {translated} >> - {file_name}\n"

    logger.info("The text was obtained from a photo.")
    return final_text

def main_get_text_from_files(file_name: str,
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
                             max_rate_limit_retries: Optional[int] = NUMBER_ATTEMPTS) -> str:
    """
    Routes the file to the appropriate extraction function based on its extension.
    :param file_name: Path to the file.
    :param lang_lst: List of language codes for OCR (used if the file is an image).
    :param use_gpu: Whether to use GPU for OCR (used if image).
    :param verbose: Enable verbose output from OCR (used if image).
    :param determinant_mode: Mode for language detection ('lite', 'full', 'auto').
    :param proxies: Dictionary with proxy settings for requests.
    :param accurate_translation: If True, attempt to use DeepL first.
    :param your_key_for_deepl: API key for DeepL (required if accurate_translation is True).
    :param request_language: Target language code (default is MAIN_LANGUAGE).
    :param cloud_version: If True, use cloud API for DeepSeek OCR.
    :param with_deepseek: If True, use DeepSeek OCR; otherwise use EasyOCR.
    :param model_size: Size of the DeepSeek model.
    :param crop_mode: Enable crop mode for DeepSeek.
    :param base_url: API base URL for DeepSeek cloud.
    :param api_key_for_deepseek_ocr: API key for DeepSeek cloud.
    :param timeout_for_deepseek_ocr: Timeout for DeepSeek requests.
    :param max_rate_limit_retries: Number of retries on rate limit.
    :return: Extracted and translated text with a file marker.
    """
    logger.info("Challenge main_get_text_from_files")
    translation_settings = _settings_for_translator(
        determinant_mode=determinant_mode,
        proxies=proxies,
        accurate_translation=accurate_translation,
        your_key_for_deepl=your_key_for_deepl,
        request_language=request_language
    )

    suffix = Path(file_name).suffix.lower()

    if suffix == '.pdf':
        return get_text_from_pdf(file_name, translation_settings)

    if suffix == '.docx':
        return get_text_from_word(file_name, translation_settings)

    if suffix == '.odf':
        return get_text_from_odf(file_name, translation_settings)

    if suffix == '.pptx':
        return get_text_from_pptx(file_name, translation_settings)

    if suffix in PHOTO_FORMATS:
        if suffix in PHOTO_FORMATS:
            return logic_for_ocr(
                file_name=file_name,
                translation_settings=translation_settings,
                lang_lst=lang_lst,
                use_gpu=use_gpu,
                verbose=verbose,
                with_deepseek=with_deepseek,
                cloud_version=cloud_version,
                model_size=model_size,
                crop_mode=crop_mode,
                base_url=base_url,
                api_key_for_deepseek_ocr=api_key_for_deepseek_ocr,
                timeout_for_deepseek_ocr=timeout_for_deepseek_ocr,
                max_rate_limit_retries=max_rate_limit_retries
            )

    return getting_text_from_files(file_name, translation_settings)