from badwords import ProfanityFilter
from AlexRadar.data.constants_for_functions import MAIN_LANGUAGE
import logging


logger = logging.getLogger(__name__)

def definition_swearing(text: str) -> bool:
    """
    Checks if the given text contains profanity or aggressive language.
    :param text: The input text to check.
    :return: True if profanity or aggression is detected, False otherwise.
    """
    logger.info("Challenge definition_swearing")
    try:
        swear_filter = ProfanityFilter()
        swear_filter.init(languages=[MAIN_LANGUAGE])
        logger.info("We have checked your request for foul language and aggression.")
        return swear_filter.filter_text(text=text)
    except Exception as e:
        logger.exception(f"Error when trying to identify mate and aggression in your request - {e}")
        return False