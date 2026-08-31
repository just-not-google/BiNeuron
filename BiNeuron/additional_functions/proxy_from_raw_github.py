import requests
from requests import Response
from requests.exceptions import RequestException
from typing import List, Optional, Dict
from BiNeuron.data.headers_for_response import HEADERS_LIST
from BiNeuron.data.constants_for_functions import (MIN_TIMEOUT_FOR_CHECK, MAX_TIMEOUT_FOR_CHECK,
                                                    PROTOCOL_LST, HTTP_PROTOCOL, HTTPS_PROTOCOL)
import random
import logging


logger = logging.getLogger(__name__)

def _template_for_requests() -> Dict:
    """
    Return common request parameters.
    """
    logger.info("Challenge __template_for_requests")
    return {
        "headers": random.choice(HEADERS_LIST),
        "timeout": random.randint(MIN_TIMEOUT_FOR_CHECK, MAX_TIMEOUT_FOR_CHECK)
    }

def _response_for_raw_github(url_lst: List[str],
                             retries: int) -> Optional[Response]:
    """
    Sending a request for a working link and issuing a Response object.
    :param url_lst: A list of links to proxy lists from GitHub in RAW form.
    :param retries: Number of attempts to request a RAW GitHub link.
    :return: The Response object if at least one link is working, otherwise None.
    """
    logger.info("Challenge _response_for_raw_github")
    for attempt in url_lst:
        try:
            for resp in range(retries):
                response = requests.get(attempt,
                                        **_template_for_requests())

                if response.status_code == 200:
                    if not response.text.strip():
                        break
                    logger.info("The request was successful, and the Response object was received.")
                    return response

        except RequestException as e:
            logger.warning(f"This link ({attempt}) is not working properly - {e}")
            continue
    logger.info("None of the links were working.")
    return None

def _bringing_to_clean_look(proxy_str: str) -> str:
    """
    Clearing the proxy and restoring it to its normal appearance.
    :param proxy_str: The source proxy.
    :return: A clean proxy without protocols.
    """
    logger.info("Challenge _bringing_to_clean_look")
    for protocol in PROTOCOL_LST:

        if protocol in proxy_str:
            logger.info("The protocol was found in the proxy.")
            proxy_str = proxy_str.replace(protocol, "")

    return proxy_str

def _github_proxies(url_lst: List[str],
                   retries: int = 5) -> str:
    """
    Selects a working proxy from the ready-made list.
    :param url_lst: A list of links to proxy lists. By default, RAW_GITHUB_URLS.
    :param retries: Number of request attempts.
    :return: The final proxy for further work.
    """
    logger.info("Challenge _github_proxies")
    answer = _response_for_raw_github(url_lst=url_lst,
                                      retries=retries)

    if answer is None:
        raise RuntimeError("No valid links were found to request and receive a proxy.")

    final_proxy = random.choice(answer.text.split())
    final_answer = _bringing_to_clean_look(final_proxy)

    logger.info(f"A proxy was obtained to bypass the Hugging Face lock.")
    return final_answer

def check_github_proxy(url_lst: List[str],
                       retries: int,
                       main_retries: int) -> Optional[str]:
    """
    Test proxies from GitHub and return a working one.
    :param url_lst: List of raw GitHub URLs.
    :param retries: Number of attempts per URL.
    :param main_retries: Number of times to try obtaining a proxy.
    :return: Working proxy string or None.
    """
    logger.info("Challenge check_github_proxy")
    for attempt in range(main_retries):
        logger.info(f"Checking proxy with {main_retries} main retries.")
        proxy = _github_proxies(url_lst=url_lst,
                               retries=retries)
        proxies = {
            HTTP_PROTOCOL: PROTOCOL_LST[0] + proxy,
            HTTPS_PROTOCOL: PROTOCOL_LST[1] + proxy,
        }
        try:
            logger.info("The proxy has been checked for functionality.")
            response = requests.get("http://httpbin.org/ip",
                                    **_template_for_requests(),
                                    proxies=proxies)

            if response.status_code == 200:
                logger.info("The proxy has been verified and it is currently working.")
                return proxy

        except RequestException as e:
            logger.warning(f"This proxy ({attempt}) does not fit the standard and an error is returned - {e}")
            continue
    logger.info("After going through all the attempts, a working proxy was not found.")
    return None