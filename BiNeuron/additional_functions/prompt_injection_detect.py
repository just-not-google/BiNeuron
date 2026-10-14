from pytector import PromptInjectionDetector
from typing import Literal
from BiNeuron.data.constants_for_functions import DEBERTA_CONST
import logging


logger = logging.getLogger(__name__)

def prompt_injection_detect(
        text: str,
        ai_model: Literal["deberta", "distilbert", "onnx"] = DEBERTA_CONST
) -> bool:
    """
    Determines in the text whether there is a prompt injection or not.
    :param text: The text that is being checked.
    :param ai_model: An AI model from ready-made ones that will be an analyzer.
    :return: Boolean variable. True if the injection is found, otherwise False.
    """
    logger.info("Challenge prompt_injection_detect")
    try:
        detector = PromptInjectionDetector(model_name_or_url=ai_model)
        answer = detector.detect_injection(text)
        logger.info("A result has been obtained regarding the prompta analysis.")
        return answer[0]
    except Exception as e:
        logger.exception(f"An error occurred when trying to analyze prompta for injections - {e}")
        return True
