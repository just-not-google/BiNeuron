from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from BiNeuron.data.constants_for_functions import MAIN_LANGUAGE
import logging


logger = logging.getLogger(__name__)

def request_anonymization(
        original_text: str,
        request_language: str = MAIN_LANGUAGE
) -> str:
    """
    Converts personal data in the source text to stubs so that the final text is anonymized.
    :param original_text: The text that is being anonymized.
    :param request_language: The language in which the request was written.
    :return: Anonymized text in the form of a string.
    """
    logger.info("Challenge request_anonymization")
    try:
        analyzer = AnalyzerEngine()
        analyze_text = analyzer.analyze(
            text=original_text,
            language=request_language
        )
        logger.info("The data has been analyzed, and the process of hiding the data in the text begins.")
        anonymizer = AnonymizerEngine()
        anonymize_text = anonymizer.anonymize(
            text=original_text,
            analyzer_results=analyze_text
        )
        logger.info("The text has been completely cleared of personal data.")
        return anonymize_text.text
    except Exception as e:
        logger.exception(f"Error when trying to anonymize source text data - {e}")
        return original_text
