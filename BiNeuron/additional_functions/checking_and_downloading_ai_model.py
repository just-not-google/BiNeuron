from huggingface_hub import hf_hub_download, set_client_factory
import os
from BiNeuron.additional_functions.proxy_for_circumventing_restrictions import working_with_proxy
from BiNeuron.data.constants_for_functions import (HTTP_PROTOCOL, MAX_TIMEOUT, HF_MIRROR,
                                                    MIN_TIMEOUT_FOR_CHECK, MAX_TIMEOUT_FOR_CHECK,
                                                    NUMBER_ATTEMPTS, MAIN_PROXY_ATTEMPTS)
import logging
from typing import Optional, Dict, List
import requests
from requests.exceptions import RequestException, ConnectionError as RequestsConnectionError
from requests.models import Response
import random
from BiNeuron.data.headers_for_response import HEADERS_LIST
from BiNeuron.additional_functions.checking_integer_for_condition import checking_int_and_float
from BiNeuron.data.links_to_raw_github_proxies import PROXY_LINK_LST
import time


logger = logging.getLogger(__name__)

class ModelDownloader:
    def __init__(self,
                 repo_id: str,
                 filename: str,
                 cache_dir: Optional[str] = None,
                 subdomain: str = "",
                 token: Optional[str] = None,
                 country: Optional[str] = None,
                 protocol: str = HTTP_PROTOCOL,
                 max_timeout: int = MAX_TIMEOUT,
                 your_proxies: Optional[List[str]] = None,
                 is_working: bool = True,
                 auto_proxies: bool = True,
                 min_timeout_for_checking_availability: int = MIN_TIMEOUT_FOR_CHECK,
                 max_timeout_for_checking_availability: int = MAX_TIMEOUT_FOR_CHECK,
                 retries: int = NUMBER_ATTEMPTS,
                 github_proxies: bool = False,
                 url_lst: List[str] = PROXY_LINK_LST,
                 proxy_retries: int = NUMBER_ATTEMPTS,
                 main_retries: int = MAIN_PROXY_ATTEMPTS,
                 prefer_mirror: bool = True) -> None:
        """
        Initializes the downloader with repository and proxy settings.
        :param repo_id: Hugging Face repository ID.
        :param filename: Base model filename.
        :param cache_dir: Directory for caching.
        :param subdomain: Prefix for the filename.
        :param token: Hugging Face access token.
        :param country: Country code for proxy selection.
        :param protocol: Protocol for proxy (e.g., http).
        :param max_timeout: Maximum timeout for proxy checks.
        :param your_proxies: List of custom proxy URLs.
        :param is_working: Whether to test proxies.
        :param auto_proxies: Enable automatic proxy fallback.
        :param min_timeout_for_checking_availability: The minimum amount of time when requesting a site to check availability.
        :param max_timeout_for_checking_availability: The maximum amount of time when requesting a site to check availability.
        :param retries: The number of attempts to download the model using a proxy.
        :param github_proxies: If True, attempt to fetch proxies from GitHub raw lists first.
        :param url_lst: List of raw GitHub URLs containing proxy lists.
        :param proxy_retries: Number of attempts per URL when fetching from GitHub.
        :param main_retries: Number of times to retry obtaining a working proxy from GitHub.
        :param prefer_mirror: If True, forces using the mirror endpoint (hf-mirror.com).
        """
        logger.info("Initializing ModelDownloader")
        self.__settings_for_downloader = {
            "repo_id": repo_id,
            "filename": subdomain + filename,
            "cache_dir": cache_dir,
            "token": token,
        }

        if not checking_int_and_float(max_timeout):
            max_timeout = MAX_TIMEOUT

        if not checking_int_and_float(proxy_retries):
            proxy_retries = NUMBER_ATTEMPTS

        if not checking_int_and_float(main_retries):
            main_retries = MAIN_PROXY_ATTEMPTS

        self.__settings_for_proxy = {
            "country": country,
            "protocol": protocol,
            "max_timeout": max_timeout,
            "is_working": is_working,
            "your_proxies": your_proxies,
            "github_proxies": github_proxies,
            "url_lst": url_lst,
            "proxy_retries": proxy_retries,
            "main_retries": main_retries
        }
        self.auto_proxies = auto_proxies
        self.min_timeout_for_checking_availability = min_timeout_for_checking_availability
        self.max_timeout_for_checking_availability = max_timeout_for_checking_availability
        self.retries = retries
        self.prefer_mirror = prefer_mirror

        if self.prefer_mirror:
            os.environ["HF_ENDPOINT"] = HF_MIRROR
            logger.info("Mirror mode enabled – will use %s", HF_MIRROR)

    def __template_for_response(self,
                                url: str,
                                timeout: Optional[int] = None,
                                headers: Optional[Dict] = None) -> Response:
        """
        Sends a GET request with random timeout and headers.
        """
        logger.info("Challenge __template_for_response")
        if not checking_int_and_float(self.min_timeout_for_checking_availability):
            self.min_timeout_for_checking_availability = MIN_TIMEOUT_FOR_CHECK

        if not checking_int_and_float(self.max_timeout_for_checking_availability):
            self.max_timeout_for_checking_availability = MAX_TIMEOUT_FOR_CHECK

        if self.min_timeout_for_checking_availability > self.max_timeout_for_checking_availability:
            self.min_timeout_for_checking_availability, self.max_timeout_for_checking_availability = (
                self.max_timeout_for_checking_availability, self.min_timeout_for_checking_availability)

        if timeout is None:
            timeout = random.randint(
                self.min_timeout_for_checking_availability,
                self.max_timeout_for_checking_availability
            )

        if headers is None:
            headers = random.choice(HEADERS_LIST)

        return requests.get(url=url,
                            timeout=timeout,
                            headers=headers)

    def _setup_proxy(self) -> None:
        """
        Installs a client factory with a new proxy via working_with_proxy.
        """
        logger.info("Challenge _setup_proxy")
        set_client_factory(lambda: working_with_proxy(**self.__settings_for_proxy))

    def _try_download(self, local_files_only: bool) -> Optional[str]:
        """
        Attempts to download the model. Returns path or None on failure.
        """
        try:
            return hf_hub_download(
                **self.__settings_for_downloader,
                local_files_only=local_files_only
            )
        except Exception as e:
            logger.warning(f"Download attempt failed (local_files_only={local_files_only}): {e}")
            return None

    def _ensure_model_downloaded(self) -> str:
        """
        Loads model from cache or downloads with automatic mirror switch.
        """
        logger.info("Challenge _ensure_model_downloaded")

        cached_path = self._try_download(local_files_only=True)
        if cached_path and os.path.exists(cached_path):
            logger.info("Model found in cache.")
            return cached_path

        for attempt in range(1, self.retries + 1):
            current_endpoint = os.environ.get("HF_ENDPOINT", "https://huggingface.co")
            logger.info(f"Attempt {attempt}/{self.retries} from {current_endpoint}")
            try:
                self._setup_proxy()
                downloaded_path = self._try_download(local_files_only=False)
                if downloaded_path and os.path.exists(downloaded_path):
                    logger.info("Model successfully downloaded.")
                    return downloaded_path
            except Exception as e:
                logger.warning(f"Attempt {attempt} failed: {e}")

                if isinstance(e, (RequestsConnectionError, ConnectionError, OSError)):
                    if os.environ.get("HF_ENDPOINT") != HF_MIRROR:
                        logger.warning("Connection error detected – switching to mirror immediately.")
                        os.environ["HF_ENDPOINT"] = HF_MIRROR
                        continue
                    else:
                        logger.warning("Already on mirror, retrying...")
                        time.sleep(5)
                elif "429" in str(e).lower() or "rate limit" in str(e).lower() or "too many requests" in str(e).lower():
                    logger.warning("Rate limit detected – switching to mirror.")
                    if os.environ.get("HF_ENDPOINT") != HF_MIRROR:
                        os.environ["HF_ENDPOINT"] = HF_MIRROR
                        continue
                    else:
                        time.sleep(5)
                else:
                    time.sleep(5)

        if os.environ.get("HF_ENDPOINT") != HF_MIRROR:
            logger.warning("All attempts failed on primary endpoint. Trying mirror...")
            os.environ["HF_ENDPOINT"] = HF_MIRROR
            for attempt in range(1, self.retries + 1):
                try:
                    self._setup_proxy()
                    downloaded_path = self._try_download(local_files_only=False)
                    if downloaded_path and os.path.exists(downloaded_path):
                        logger.info("Model downloaded via mirror.")
                        return downloaded_path
                except Exception as e:
                    logger.warning(f"Mirror attempt {attempt} failed: {e}")
                    time.sleep(5)

        raise RuntimeError("Failed to download model after all retries (including mirror)")

    def _more_advanced_downloader(self) -> str:
        """
        Checks official Hugging Face endpoint, falls back to mirror or proxy.
        """
        logger.info("Challenge _more_advanced_downloader")

        if self.prefer_mirror:
            logger.info("Mirror mode active – downloading from mirror directly.")
            return self._ensure_model_downloaded()

        try:
            response = self.__template_for_response("https://huggingface.co")
            if response.status_code == 200:
                logger.info("Hugging Face service is available (Original)")
                return self._ensure_model_downloaded()
            else:
                raise RequestException
        except Exception as e:
            logger.exception(f"Hugging Face service is unavailable (Original) - {e}")
            mirror_response = self.__template_for_response(HF_MIRROR)
            if mirror_response.status_code == 200:
                logger.info("Hugging Face service is available (Mirror)")
                os.environ["HF_ENDPOINT"] = HF_MIRROR
            else:
                logger.exception("Hugging Face service is unavailable (Mirror)")
            return self._ensure_model_downloaded()

    def auto_manager_for_download(self) -> str:
        """
        Returns the local model path, using advanced downloader if auto_proxies is True.
        """
        logger.info("Challenge auto_manager_for_download")
        if self.auto_proxies:
            return self._more_advanced_downloader()
        else:
            return self._ensure_model_downloaded()