import os
from litellm import completion
from typing import Optional, List, Dict
from BiNeuron.additional_functions.proxy_for_circumventing_restrictions import working_with_proxy
from BiNeuron.data.constants_for_functions import (
    HTTP_PROTOCOL, NUMBER_ATTEMPTS, MAIN_PROXY_ATTEMPTS,
    MAX_TOKENS, HTTPS_PROTOCOL, MAX_TIMEOUT
)
from BiNeuron.data.links_to_raw_github_proxies import PROXY_LINK_LST
import logging


logger = logging.getLogger(__name__)

def request_for_cloud_ai(
        original_text: List[Dict[str, str]],
        key_for_api: Optional[str] = None,
        model: Optional[str] = None,
        with_proxy: bool = False,
        country: Optional[str] = None,
        protocol: str = HTTP_PROTOCOL,
        max_timeout: int = MAX_TIMEOUT,
        your_proxies: Optional[List[str]] = None,
        github_proxies: bool = False,
        url_lst: List[str] = PROXY_LINK_LST,
        proxy_retries: int = NUMBER_ATTEMPTS,
        main_retries: int = MAIN_PROXY_ATTEMPTS,
        temperature: float = 0.1,
        max_tokens: int = MAX_TOKENS
) -> str:
    """
    Sends a request via LiteLLM to the API of the cloud neural network that you specified.
    :param original_text: User's input text (question or code description).
    :param key_for_api: The key for the API request.
    :param model: An AI or neural network model that will process incoming text.
    :param with_proxy: If True, a proxy is used for the request, otherwise without it.
    :param country: Country code for proxy selection (used when `github_proxies` is False).
    :param protocol: Protocol to use ('http' or 'https').
    :param max_timeout: The maximum allowed request time.
    :param your_proxies: Custom list of proxy strings (address:port). Overrides other sources.
    :param github_proxies: If True, attempt to fetch proxies from GitHub raw lists first.
    :param url_lst: List of raw GitHub URLs containing proxy lists.
    :param proxy_retries: Number of attempts per URL when fetching from GitHub.
    :param main_retries: Number of times to retry obtaining a working proxy from GitHub.
    :param temperature: Sampling temperature for generation (0.0 to 1.0).
    :param max_tokens: Maximum number of tokens to generate.
    :return: The processed text is a request from an AI or neural network in the form of a string.
    """
    logger.info("Challenge request_for_cloud_ai")
    try:
        if with_proxy:
            logger.info("A proxy for queries in cloud neural networks and AI has been enabled.")
            proxy_dict = working_with_proxy(
                version_1=False,
                country=country,
                protocol=protocol,
                your_proxies=your_proxies,
                github_proxies=github_proxies,
                url_lst=url_lst,
                proxy_retries=proxy_retries,
                max_timeout=max_timeout,
                main_retries=main_retries
            )
            os.environ["HTTP_PROXY"] = proxy_dict[HTTP_PROTOCOL]
            os.environ["HTTPS_PROXY"] = proxy_dict[HTTPS_PROTOCOL]
            os.environ["NO_PROXY"] = "localhost,127.0.0.1"

        response = completion(
            messages=original_text,
            timeout=max_timeout,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            api_key=key_for_api
        )
        logger.info("The final text was received from the cloud neural network.")
        return response['choices'][0]['message']['content']
    except Exception as e:
        logger.exception(f"Error when trying to make a request to cloud neural networks and AI - {e}")
        return f"Error - {e}"