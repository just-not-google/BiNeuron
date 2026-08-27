from codelang_detect import detect
from whats_that_code.election import guess_language_all_methods
from typing import List
from AlexRadar.data.abbreviations_full_names_programming_languages import LANG_SHORTCUT_TO_FULL
import logging


logger = logging.getLogger(__name__)

def detect_programming_language(text: str) -> List[str]:
    """
    Detects programming language(s) from the given text using two independent libraries.
    :param text: The source code or text to analyze.
    :return: A unique list of full programming language names.
    """
    try:
        logger.info("Challenge detect_programming_language")
        answer_lst = []
        answer_lst.append(LANG_SHORTCUT_TO_FULL[detect(text)])
        answer_lst.append(guess_language_all_methods(text))
        logger.info("Programming languages were defined due to 2 extraneous and independent algorithms.")
        return list(set(answer_lst))
    except Exception as e:
        logger.exception(f"Error when trying to recognize the necessary programming languages - {e}")
        return []