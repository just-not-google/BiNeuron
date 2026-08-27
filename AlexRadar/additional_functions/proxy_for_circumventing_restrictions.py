from free_proxy_server import ProxyClient, ProxyFilter
from typing import List, Optional, Dict
import httpx
import random
from AlexRadar.data.constants_for_functions import (HTTP_PROTOCOL, HTTPS_PROTOCOL, MAX_TIMEOUT,
                                                    NUMBER_ATTEMPTS, MAIN_PROXY_ATTEMPTS)
from AlexRadar.additional_functions.proxy_from_raw_github import check_github_proxy
from AlexRadar.data.links_to_raw_github_proxies import PROXY_LINK_LST
import logging


logger = logging.getLogger(__name__)

def proxy_for_circumventing_restrictions(country: str,
                                         protocol: str,
                                         max_timeout: int,
                                         is_working: bool) -> Optional[List[str]]:
    """
    Fetches a list of proxy servers matching the given filters.
    :param country: Target country code for proxies.
    :param protocol: Protocol (e.g., 'http' or 'https').
    :param max_timeout: Maximum timeout in seconds.
    :param is_working: If True, only return working proxies.
    :return: List of proxy strings 'address:port', or None on error.
    """
    logger.info("Challenge proxy_for_circumventing_restrictions")
    try:
        client = ProxyClient()
        filters = ProxyFilter(
            country=country,
            protocol=protocol,
            max_timeout=max_timeout,
            working_only=is_working
        )
        proxies = client.get_proxies(filters)

        answer_lst = []
        for proxy in proxies:
            answer_lst.append(f"{proxy.address}:{proxy.port}")

        logger.info("A list of proxies to bypass has been compiled.")
        return answer_lst
    except Exception as e:
        logger.exception(f"Error when trying to get a list of proxies to bypass - {e}")
        return None

def working_with_proxy(country: Optional[str] = None,
                       protocol: str = HTTP_PROTOCOL,
                       max_timeout: int = MAX_TIMEOUT,
                       is_working: bool = True,
                       version_1: bool = True,
                       your_proxies: Optional[List[str]] = None,
                       github_proxies: bool = False,
                       url_lst: List[str] = PROXY_LINK_LST,
                       proxy_retries: int = NUMBER_ATTEMPTS,
                       main_retries: int = MAIN_PROXY_ATTEMPTS) -> httpx.Client or Dict:
    """
    Returns an httpx client or proxy dictionary configured with a selected proxy.
    :param country: Country code for proxy selection (used when `github_proxies` is False).
    :param protocol: Protocol to use ('http' or 'https').
    :param max_timeout: Timeout (seconds) for proxy availability checks.
    :param is_working: Only consider working proxies.
    :param version_1: If True, return `httpx.Client`; else return `Dict` with proxy URLs.
    :param your_proxies: Custom list of proxy strings (address:port). Overrides other sources.
    :param github_proxies: If True, attempt to fetch proxies from GitHub raw lists first.
    :param url_lst: List of raw GitHub URLs containing proxy lists.
    :param proxy_retries: Number of attempts per URL when fetching from GitHub.
    :param main_retries: Number of times to retry obtaining a working proxy from GitHub.
    :return: Configured client or proxy dictionary.
    """
    logger.info("Challenge working_with_proxy")
    main_proxy = None

    if your_proxies is not None:
        main_proxy = random.choice(your_proxies)
    elif github_proxies:
        main_proxy = check_github_proxy(
            url_lst=url_lst,
            retries=proxy_retries,
            main_retries=main_retries
        )

    if main_proxy is None:
        proxies = proxy_for_circumventing_restrictions(
            country=country,
            protocol=protocol,
            max_timeout=max_timeout,
            is_working=is_working
        )
        if proxies is None:
            logger.error("No working proxies were found.")
            raise RuntimeError("No working proxies available.")
        main_proxy = random.choice(proxies)

    logger.info("The updated proxy client has been built.")

    if version_1:
        return httpx.Client(proxy=f"{HTTP_PROTOCOL}://{main_proxy}")
    else:
        return {
            HTTP_PROTOCOL: f"{HTTP_PROTOCOL}://{main_proxy}",
            HTTPS_PROTOCOL: f"{HTTPS_PROTOCOL}://{main_proxy}"
        }


