from typing import Optional, List, Dict, Literal
from pathlib import Path
from AlexRadar.data.supported_formats import SUPPORTED_FORMATS_WITHOUT_PHOTO, PHOTO_SUPPORTED_FORMATS
from AlexRadar.data.constants_for_functions import TYPE_FORMATS
from AlexRadar.additional_functions.text_translation import TranslatorText
from AlexRadar.data.constants_for_functions import MAIN_LANGUAGE
import logging


logger = logging.getLogger(__name__)

def extraction_all_files(path: str) -> List[str]:
    """
    Retrieves all paths to files located in this folder.
    :param path: The location of your virtual storage.
    :return: List of file paths.
    """
    logger.info("Challenge extraction_all_files")
    try:
        folder_path = Path(rf"{path}")
        answer_lst = []
        for item in folder_path.rglob('*'):
            if item.is_file():
                answer_lst.append(str(item))
        logger.info("All file paths from this folder have been retrieved.")
        return answer_lst
    except Exception as e:
        logger.exception(f"An error occurred when trying to get file paths in a folder - {e}")
        return []

def logic_virtual_storage(path: Optional[str] = None,
                          with_ocr: bool = False,
                          determinant_mode: Optional[Literal["lite", "full", "auto"]] = "lite",
                          proxies: Optional[Dict] = None,
                          accurate_translation: bool = False,
                          your_key_for_deepl: str = "",
                          request_language: str = MAIN_LANGUAGE) -> Dict:
    """
    Checking the unsorted list of files for certain conditions.
    :param path: The location of your virtual storage.
    :param with_ocr: If there are photos among your files.
    :param determinant_mode: Mode for language detection ('lite', 'full', 'auto').
    :param proxies: Dictionary with proxy settings for requests.
    :param accurate_translation: If True, attempt to use DeepL first.
    :param your_key_for_deepl: API key for DeepL (required if accurate_translation is True).
    :param request_language: Target language code (default is MAIN_LANGUAGE).
    :return: Dictionary of files read and unread by the program.
    """
    logger.info("Challenge logic_virtual_storage")
    if path is None:
        logger.warning("The path to the virtual storage was not specified.")
        return dict()

    file_paths = extraction_all_files(path=path)
    supported_formats = SUPPORTED_FORMATS_WITHOUT_PHOTO.copy()

    if with_ocr:
        supported_formats.extend(PHOTO_SUPPORTED_FORMATS)

    if not file_paths:
        logger.warning("No files were found in the folder you specified.")
        return dict()

    filtered_list = []
    other_list = []
    for file in file_paths:
        is_supported = False
        for main_format in supported_formats:
            if main_format in str(file).lower():
                is_supported = True
                break

        trans_file = TranslatorText(
            original_text=path,
            determinant_mode=determinant_mode,
            proxies=proxies,
            accurate_translation=accurate_translation,
            your_key_for_deepl=your_key_for_deepl,
            request_language=request_language
        ).main_translater()

        if is_supported:
            filtered_list.append(trans_file)
        else:
            other_answer = f"<< The program could not read the text of the file >> - {trans_file}"
            other_list.append(other_answer)

    logger.info("A dictionary of read and unread file paths has been obtained.")
    return {
        TYPE_FORMATS[0]: filtered_list,
        TYPE_FORMATS[1]: other_list
    }