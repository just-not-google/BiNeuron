from BiNeuron.additional_functions.text_translation import TranslatorText
import easyocr
import pymupdf
import functools
import docx2txt
import logging
from odfdo import Document
import pptx2txt2
from typing import List, Optional, Literal, Dict
from pathlib import Path
from BiNeuron.data.supported_formats import PHOTO_SUPPORTED_FORMATS
from BiNeuron.data.constants_for_functions import (NUMBER_ATTEMPTS, TINY_TYPE, DEVICE_OPTIONS,
                                                   MAIN_LANGUAGE, LITE_TYPE, EASY_OCR,
                                                   DEFINITION_OPTION_LIST, MARKER_FOR_WEBSITES,
                                                   API_BASE_URL)
from BiNeuron.additional_functions.advanced_definition_text_from_image import LaunchDeepSeekOCR
from markitdown import MarkItDown
from epub2txt import epub2txt
import mobi
import shutil
from fb2reader import fb2book
from paddleocr import PaddleOCR
from html2text import html2text
from BiNeuron.additional_functions.checking_site_access import main_template_requests
from BiNeuron.additional_functions.request_anonymization import request_anonymization


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

class GettingTextFromFiles:
    def __init__(self,
                 file_name: str,
                 lang_lst: Optional[List[str]] = None,
                 use_gpu: bool = False,
                 verbose: bool = False,
                 determinant_mode: Optional[Literal["lite", "full", "auto"]] = LITE_TYPE,
                 proxies: Optional[Dict] = None,
                 accurate_translation: bool = False,
                 your_key_for_deepl: str = "",
                 request_language: str = MAIN_LANGUAGE,
                 local_trans: bool = False,
                 from_code_lang: str = "",
                 cloud_version: bool = False,
                 model_size: Literal["tiny", "small", "base", "large", "gundam"] = TINY_TYPE,
                 crop_mode: bool = False,
                 base_url: str = API_BASE_URL,
                 api_key_for_deepseek_ocr: Optional[str] = None,
                 timeout_for_deepseek_ocr: Optional[int] = None,
                 max_rate_limit_retries: Optional[int] = NUMBER_ATTEMPTS,
                 use_websites: bool = False,
                 websites_sources_information: Optional[List[str]] = None,
                 paddle_lang: str = MAIN_LANGUAGE,
                 definition_option: Literal["paddle_ocr", "easy_ocr", "deepseek_ocr"] = EASY_OCR,
                 anonymize_text: bool = False) -> None:
        """
        Initialization of parameters for getting text from files of different formats.
        :param file_name: The link to the file from which you want to extract the text.
        :param lang_lst: Language codes for OCR when extracting text from images.
        :param use_gpu: Whether to use GPU for OCR.
        :param verbose: Enable verbose output from OCR and other submodules.
        :param determinant_mode: Translation detection mode ('lite', 'full', 'auto').
        :param proxies: Proxy settings for translation services.
        :param accurate_translation: If True, use DeepL (with key) instead of Google Translate.
        :param your_key_for_deepl: API key for DeepL translation.
        :param request_language: Target language code for translation (default MAIN_LANGUAGE).
        :param local_trans: Using a local translator for text, without requests to the clouds and API.
        :param from_code_lang: Source language code for local translation (e.g., 'en', 'ru').
        :param cloud_version: If True, uses cloud API for DeepSeek OCR.
        :param model_size: Size of the DeepSeek model.
        :param crop_mode: If True, splits large images into fragments.
        :param base_url: API endpoint URL for DeepSeek cloud service.
        :param api_key_for_deepseek_ocr: API key for DeepSeek cloud service.
        :param timeout_for_deepseek_ocr: Timeout (seconds) for DeepSeek API requests.
        :param max_rate_limit_retries: Number of retry attempts on rate limit errors.
        :param use_websites: Use text from websites.
        :param websites_sources_information: The Internet sources from which the text is taken.
        :param paddle_lang: The main language code is needed for Paddle OCR to determine.
        :param definition_option: Choose an OCR system from 3 ready-made ones.
        :param anonymize_text: If True, it anonymizes personal data in a general request to the AI.
        """
        logger.info("Initializing GettingTextFromFiles")
        self.file_name = file_name
        self.lang_lst = lang_lst
        self.use_gpu = use_gpu
        self.verbose = verbose
        self.cloud_version = cloud_version
        self.model_size = model_size
        self.crop_mode = crop_mode
        self.base_url = base_url
        self.api_key_for_deepseek_ocr = api_key_for_deepseek_ocr
        self.timeout_for_deepseek_ocr = timeout_for_deepseek_ocr
        self.max_rate_limit_retries = max_rate_limit_retries
        self.use_websites = use_websites
        self.websites_sources_information = websites_sources_information
        self.paddle_lang = paddle_lang
        self.definition_option = definition_option
        self.anonymize_text = anonymize_text
        self.translation_settings = {
            "determinant_mode": determinant_mode,
            "proxies": proxies,
            "accurate_translation": accurate_translation,
            "your_key_for_deepl": your_key_for_deepl,
            "request_language": request_language,
            "local_trans": local_trans,
            "from_code_lang": from_code_lang
        }

    def trans_text(self, orig_text: str) -> str:
        """
        Additional functionality for translating text for each file type separately and anonymizing
        the text before sending it to the translator if 'self.anonymize_text' is True.
        :param orig_text: The source text that needs to be translated.
        :return: Translated and anonymized (optional) text as a string.
        """
        logger.info("Challenge trans_text")

        if self.anonymize_text:
            orig_text = request_anonymization(
                original_text=orig_text,
                request_language=self.translation_settings["request_language"])

        return TranslatorText(orig_text, **self.translation_settings).main_translater()

    @handle_errors
    def get_text_from_pdf(self) -> str:
        """
        Extracts and translates text from a PDF file.
        :return: Translated text with a marker indicating the file name.
        """
        logger.info("Challenge get_text_from_pdf")
        doc = pymupdf.open(self.file_name)
        answer_text = ""
        for page in doc:
            page_text = page.get_text()
            answer_text += f"{self.trans_text(page_text)} \n\n"
        doc.close()
        logger.info("The text was received from the PDF file.")
        return f"<< {answer_text} >> - {self.file_name}\n"

    @handle_errors
    def get_text_from_word(self) -> str:
        """
        Extracts and translates text from a Word (.docx) file.
        :return: Translated text with a marker indicating the file name.
        """
        logger.info("Challenge get_text_from_word")
        full_text = docx2txt.process(self.file_name)
        logger.info("The text was received from the WORD file.")
        return f"<< {self.trans_text(full_text)} >> - {self.file_name}\n"

    @handle_errors
    def get_text_from_odf(self) -> str:
        """
        Extracts and translates text from an ODF (OpenDocument) file.
        :return: Translated text with a marker indicating the file name.
        """
        logger.info("Challenge get_text_from_odf")
        doc = Document(self.file_name)
        all_text = []
        for element in doc.body.get_children():
            if hasattr(element, 'text'):
                all_text.append(element.text)
        org_text = '\n'.join(all_text)
        logger.info("The text was obtained from an ODF file.")
        return f"<< {self.trans_text(org_text)} >> - {self.file_name}\n"

    @handle_errors
    def get_text_from_pptx(self) -> str:
        """
        Extracts and translates text from a PowerPoint (.pptx) file.
        :return: Translated text with a marker indicating the file name.
        """
        logger.info("Challenge get_text_from_pptx")
        answer = pptx2txt2.extract_text(self.file_name)
        logger.info("The text was received from the PowerPoint file.")
        return f"<< {self.trans_text(answer)} >> - {self.file_name}\n"

    @handle_errors
    def get_text_from_xlsx(self) -> str:
        """
        Extracts and translates text from a Excel (.xlsx, .xls) file.
        :return: Translated text with a marker indicating the file name.
        """
        logger.info("Challenge get_text_from_xlsx")
        md = MarkItDown()
        result = md.convert(self.file_name).text_content
        logger.info("The text was obtained from an Excel file.")
        return f"<< {self.trans_text(result)} >> - {self.file_name}\n"

    @handle_errors
    def get_text_from_epub(self) -> str:
        """
        Extracts and translates text from an e-book file (.epub).
        :return: Translated text with a marker indicating the file name.
        """
        logger.info("Challenge get_text_from_epub")
        result = epub2txt(self.file_name)
        logger.info("The text was received from an e-book.")
        return f"<< {self.trans_text(result)} >> - {self.file_name}\n"

    @handle_errors
    def get_text_from_mobi(self) -> str:
        """
        Extracts and translates text from a MOBI (.mobi) file.
        :return: Translated text with a marker indicating the file name.
        """
        logger.info("Challenge get_text_from_mobi")
        tempdir, filepath = mobi.extract(self.file_name)
        with open(filepath, "r") as f:
            content = f.read()
            shutil.rmtree(tempdir)
            logger.info("The text was obtained from a MOBI file.")
            return f"<< {self.trans_text(content)}>> - {self.file_name}\n"

    @handle_errors
    def get_text_from_fb2(self) -> str:
        """
        Extracts and translates text from a FB2 (.fb2) file.
        :return: Translated text with a marker indicating the file name.
        """
        logger.info("Challenge get_text_from_fb2")
        book = fb2book(self.file_name)
        authors = book.get_authors()
        title = book.get_title()
        content = book.get_body()
        all_text = (f"Authors: {authors}\n"
                    f"Title: {title}\n"
                    f"The text of the book itself: {content}\n")
        logger.info("The text was obtained from an FB2 file.")
        return f"<< {self.trans_text(all_text)} >> - {self.file_name}\n"

    @handle_errors
    def getting_text_from_files(self) -> str:
        """
        Reads and translates text from a plain text file.
        :return: Translated text with a marker indicating the file name.
        """
        logger.info("Challenge getting_text_from_files")
        with open(self.file_name, 'r', encoding='utf-8') as file:
            content = file.read()
            logger.info("The text was received from a TXT file.")
            return f"<< {self.trans_text(content)} >> - {self.file_name}\n"

    def _easy_ocr_get_text(self) -> List[str]:
        """
        Extracts text from an image using EasyOCR.
        :return: List of detected text strings, or empty list on error.
        """
        logger.info("Challenge _easy_ocr_get_text")
        try:
            reader = easyocr.Reader(lang_list=self.lang_lst,
                                    gpu=self.use_gpu,
                                    verbose=self.verbose)
            result = reader.readtext(image=self.file_name,
                                     detail=0)
            logger.info("The text was successfully obtained thanks to EasyOCR.")
            return result
        except Exception as e:
            logger.exception(f"Error when trying to read text from a photo using EasyOCR - {e}")
            return []

    def _paddle_ocr_get_text(self) -> str:
        """
        Extracts text from an image using Paddle OCR.
        :return: Text from the original photo as a string.
        """
        try:
            logger.info("Challenge _paddle_ocr_get_text")
            text = PaddleOCR(lang=self.paddle_lang,
                             use_gpu=self.use_gpu,
                             show_log=self.verbose)
            logger.info("The information is obtained from the photo using Paddle OCR.")
            return text.ocr(self.file_name,
                            cls=True)
        except Exception as e:
            logger.exception(f"Error when trying to get text using Paddle OCR - {e}")
            return ""

    @handle_errors
    def logic_for_ocr(self) -> str:
        """
        Extracts text from an image using OCR (EasyOCR or DeepSeek) and translates it.
        :return: Translated text with a marker indicating the file name.
        """
        logger.info("Challenge logic_for_ocr")

        if self.lang_lst is None:
            self.lang_lst = [MAIN_LANGUAGE]

        device = DEVICE_OPTIONS[1] if self.use_gpu else DEVICE_OPTIONS[0]
        result = None

        if self.definition_option == DEFINITION_OPTION_LIST[2]:
            result = LaunchDeepSeekOCR(
                photo_path=self.file_name,
                cloud_version=self.cloud_version,
                model_size=self.model_size,
                device=device,
                crop_mode=self.crop_mode,
                base_url=self.base_url,
                api_key_for_deepseek_ocr=self.api_key_for_deepseek_ocr,
                timeout_for_deepseek_ocr=self.timeout_for_deepseek_ocr,
                max_rate_limit_retries=self.max_rate_limit_retries
            ).advanced_definition_text_from_image()
        elif self.definition_option == DEFINITION_OPTION_LIST[1]:
            result_list = self._easy_ocr_get_text()

            if not result_list:
                return "EasyOCR couldn't read the text from the photo."

            result = "\n".join(result_list)
        elif self.definition_option == DEFINITION_OPTION_LIST[0]:
            result = self._paddle_ocr_get_text()

        final_text = f"<< {self.trans_text(result)} >> - {self.file_name}\n"
        logger.info("The text was obtained from a photo.")
        return final_text

    def getting_text_from_website(self, goal_url: str) -> str:
        """
        Getting clean text from an HTML website template that is specified by URL.
        :param goal_url: The link of the website to which the request is being sent.
        :return: Clean text from the website.
        """
        logger.info("Challenge getting_text_from_website")
        res_text = main_template_requests(url=goal_url).text
        try:
            logger.info("Received clean text (without HTML tags) from the site.")
            answer = html2text(res_text)
            return f"<< {self.trans_text(answer)} >> - {goal_url}\n"
        except Exception as e:
            logger.exception(f"Error when trying to get clear text from the HTML template of the website - {e}")
            return res_text

    def additional_supported_files_to_read(self) -> Dict:
        """
        All additional binary file formats that the program can
        read and extract text from there.
        :return: A dictionary, where the value is the format itself,
        and the value is the function that reads this file.
        """
        logger.info("Challenge additional_supported_files_to_read")
        return {
            ".pdf": self.get_text_from_pdf,
            ".docx": self.get_text_from_word,
            ".odf": self.get_text_from_odf,
            ".pptx": self.get_text_from_pptx,
            ".xlsx": self.get_text_from_xlsx,
            ".xls": self.get_text_from_xlsx,
            ".epub": self.get_text_from_epub,
            ".mobi": self.get_text_from_mobi,
            ".fb2": self.get_text_from_fb2
        }

    def main_get_text_from_files(self) -> str:
        """
        Routes the file to the appropriate extraction function based on its extension.
        :return: Extracted and translated text with a file marker.
        """
        logger.info("Challenge main_get_text_from_files")

        if self.use_websites:
            if (not self.websites_sources_information is None and
                    len(self.websites_sources_information) > 0):
                answer = MARKER_FOR_WEBSITES
                answer_lst = []
                for web_source in self.websites_sources_information:
                    answer_lst.append(self.getting_text_from_website(web_source))
                answer += "\n".join(answer_lst)

        add_supported_files = self.additional_supported_files_to_read()
        suffix = Path(self.file_name).suffix.lower()

        if suffix in add_supported_files:
            return add_supported_files[suffix](self.file_name)

        if suffix in PHOTO_SUPPORTED_FORMATS:
            return self.logic_for_ocr()

        return self.getting_text_from_files(self.file_name)