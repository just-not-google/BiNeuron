from dataclasses import dataclass
from typing import Optional, Literal, List
from BiNeuron.data.preferences_in_ai import PREFERENCES_IN_AI_LIST
from BiNeuron.data.links_to_raw_github_proxies import PROXY_LINK_LST
from BiNeuron.data.constants_for_functions import (NUMBER_ATTEMPTS, MAX_TOKENS, TYPE_DEFAULT,
                                                   LITE_TYPE, MAIN_LANGUAGE, HTTP_PROTOCOL,
                                                   MAX_TIMEOUT, MIN_TIMEOUT_FOR_CHECK,
                                                   MAX_TIMEOUT_FOR_CHECK, MAIN_PROXY_ATTEMPTS,
                                                   TINY_TYPE)
import logging


logger = logging.getLogger(__name__)

@dataclass
class ModelConfig:
    """
    Configuration for AI model selection and downloading.
    :param preferences_in_ai: Preferred model family (e.g., 'deepseek', 'qwen').
    Must be a value from PREFERENCES_IN_AI_LIST.
    :param models_dir: Directory where downloaded models are cached.
    :param type_computer: Predefined computer power level ('easy', 'middle', 'hard', 'very_hard').
    If None, it is auto-detected via benchmarking.
    :param repo_id: Explicit Hugging Face repository ID (e.g., 'deepseek-ai/deepseek-coder-6.7b').
    Overrides automatic model selection.
    :param filename: Filename of the model inside the repository (e.g., 'model.Q4_K_M.gguf').
    Must be used together with repo_id.
    :param your_token_for_hf: Hugging Face access token (optional, for private models).
    :param subdomain: Prefix to add to the model filename during download.
    :param retries: Number of attempts to download the model using a proxy.
    :param prefer_mirror: If True, forces using the mirror endpoint (hf-mirror.com).
    """
    preferences_in_ai: str = PREFERENCES_IN_AI_LIST[0]
    models_dir: str = "./models"
    type_computer: Optional[Literal["easy", "middle", "hard", "very_hard"]] = None
    repo_id: Optional[str] = None
    filename: Optional[str] = None
    your_token_for_hf: Optional[str] = None
    subdomain: str = ""
    retries: int = NUMBER_ATTEMPTS
    prefer_mirror: bool = True

@dataclass
class LLMConfig:
    """
    Configuration for large language model generation parameters.
    :param verbose: Enables verbose output from the underlying LLM.
    :param n_ctx: Context window size for the model. If None, uses model default.
    :param n_gpu_layers: Number of GPU layers to offload. 0 means CPU-only.
    :param echo: Whether to echo the prompt in the AI output.
    :param max_tokens: Maximum number of tokens to generate.
    :param temperature: Sampling temperature for generation (0.0 to 1.0).
    """
    verbose: bool = False
    n_ctx: Optional[int] = None
    n_gpu_layers: int = 0
    echo: bool = False
    max_tokens: int = MAX_TOKENS
    temperature: float = 0.1

@dataclass
class PromptConfig:
    """
    Configuration for the system prompt used by the AI.
    :param main_prompt_mode: Predefined prompt scenario from ALL_MAIN_PROMPTS
    ('default', 'testing', 'explanation', 'no_comments', 'refactor', 'debug',
    'code_review', 'documentation', 'scaffold', 'security_hardening', 'algorithm_strategy').
    :param main_prompt: Custom system prompt. If provided, overrides main_prompt_mode.
    """
    main_prompt_mode: Literal["default", "testing", "explanation", "no_comments",
    "refactor", "debug", "code_review", "documentation", "scaffold",
    "security_hardening", "algorithm_strategy"] = TYPE_DEFAULT
    main_prompt: Optional[str] = None

@dataclass
class TranslationConfig:
    """
    Configuration for text translation and language detection.
    :param determinant_mode: Mode for language detection ('lite', 'full', 'auto').
    :param accurate_translation: If True, tries DeepL API first (requires key) before Google.
    :param your_key_for_deepl: DeepL API key (required if accurate_translation is True).
    :param request_language: Target language code for translation (default MAIN_LANGUAGE).
    :param local_trans: If True, uses ArgosTranslate for fully offline translation.
    :param from_code_lang: Source language code for local translation (e.g., 'en', 'ru').
    """
    determinant_mode: Optional[Literal["lite", "full", "auto"]] = LITE_TYPE
    accurate_translation: bool = False
    your_key_for_deepl: str = ""
    request_language: str = MAIN_LANGUAGE
    local_trans: bool = False
    from_code_lang: str = ""

@dataclass
class LanguageDetectionConfig:
    """
    Configuration for programming language detection.
    :param with_ai_orchestrator: If True, uses AI model to detect the programming language
    from the request and file contents (more accurate).
    :param proprietary_algorithms: If True and AI is disabled, uses keyword-based detection
    (faster but less accurate).
    """
    with_ai_orchestrator: bool = True
    proprietary_algorithms: bool = False

@dataclass
class ProxyConfig:
    """
    Configuration for proxy usage and rotation.
    :param country: Country code for proxy selection (e.g., 'ru', 'us').
    :param protocol: Proxy protocol (default 'http').
    :param max_timeout: Maximum timeout (seconds) for proxy availability checks.
    :param is_working: If True, only working proxies are used.
    :param auto_proxies: Enable automatic fallback to proxies if the primary connection fails.
    :param your_proxies_dict: Custom list of proxy URLs; overrides automatic discovery.
    :param min_timeout_for_checking_availability: Minimum timeout for connection checks.
    :param max_timeout_for_checking_availability: Maximum timeout for connection checks.
    :param github_proxies: If True, fetches proxies from GitHub raw lists first.
    :param url_lst: List of raw GitHub URLs containing proxy lists.
    :param proxy_retries: Number of attempts per URL when fetching from GitHub.
    :param main_retries: Number of times to retry obtaining a working proxy from GitHub.
    """
    country: Optional[str] = None
    protocol: str = HTTP_PROTOCOL
    max_timeout: int = MAX_TIMEOUT
    is_working: bool = True
    auto_proxies: bool = True
    your_proxies_dict: Optional[List[str]] = None
    min_timeout_for_checking_availability: int = MIN_TIMEOUT_FOR_CHECK
    max_timeout_for_checking_availability: int = MAX_TIMEOUT_FOR_CHECK
    github_proxies: bool = False
    url_lst: List[str] = PROXY_LINK_LST
    proxy_retries: int = NUMBER_ATTEMPTS
    main_retries: int = MAIN_PROXY_ATTEMPTS

@dataclass
class OCRConfig:
    """
    Configuration for optical character recognition (OCR).
    :param lang_lst: List of language codes for OCR (e.g., ['en', 'ru']). Used if file is an image.
    :param use_gpu_for_ocr: Whether to use GPU for OCR.
    :param with_ocr: If True, includes image files for OCR processing in virtual storage.
    :param cloud_version: If True, uses cloud API for DeepSeek OCR instead of local model.
    :param with_deepseek: If True, uses DeepSeek OCR; otherwise uses EasyOCR.
    :param model_size: Size of the DeepSeek model ('tiny', 'small', 'base', 'large', 'gundam').
    :param crop_mode: If True, splits large images into fragments for detailed recognition.
    :param base_url: API endpoint URL for DeepSeek cloud service.
    :param api_key_for_deepseek_ocr: API key for DeepSeek cloud service.
    :param timeout_for_deepseek_ocr: Timeout (seconds) for DeepSeek API requests.
    :param max_rate_limit_retries: Number of retry attempts on rate limit errors.
    """
    lang_lst: Optional[List[str]] = None
    use_gpu_for_ocr: bool = False
    with_ocr: bool = False
    cloud_version: bool = False
    with_deepseek: bool = True
    model_size: Literal["tiny", "small", "base", "large", "gundam"] = TINY_TYPE
    crop_mode: bool = False
    base_url: str = "https://api.siliconflow.cn/v1/chat/completions"
    api_key_for_deepseek_ocr: Optional[str] = None
    timeout_for_deepseek_ocr: Optional[int] = None
    max_rate_limit_retries: Optional[int] = NUMBER_ATTEMPTS

@dataclass
class FileConfig:
    """
    Configuration for virtual storage and file editing.
    :param virtual_storage: If True, enables virtual storage mode to process entire folders.
    :param virtual_storage_path: Path to the virtual storage folder.
    :param writing_response_to_file: If True, saves the AI response to a timestamped text file.
    :param editing_files: If True, enables automatic file creation and modification via AI
    (two-stage pipeline with a JSON formatter).
    :param deleting_files: If True, enables automatic file deletion via AI
    (uses a separate prompt that allows `null` values for deletion).
    """
    virtual_storage: bool = False
    virtual_storage_path: Optional[str] = None
    writing_response_to_file: bool = False
    editing_files: bool = False
    deleting_files: bool = False

@dataclass
class SafetyConfig:
    """
    Configuration for content safety and filtering.
    :param filter_for_swearing: If True, blocks responses containing profanity
    and returns a predefined template response.
    """
    filter_for_swearing: bool = False