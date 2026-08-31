import requests
from BiNeuron.additional_functions.proxy_from_raw_github import _template_for_requests
import logging


logger = logging.getLogger(__name__)

def checking_site_access(url: str) -> bool:
    """
    Verifying access to the site via a simple GET request.
    :param url: The link of the site to be checked.
    :return: If available, then True, otherwise False.
    """
    logger.info("Challenge checking_site_access")
    try:
        response = requests.get(url,
                                **_template_for_requests())

        if response.status_code != 200:
            logger.info(f"The site ({url}) is unavailable.")
            return False

        logger.info(f"The site ({url}) is available.")
        return True
    except Exception as e:
        logger.exception(f"An error occurred while trying to access the site - {e}")
        return False
