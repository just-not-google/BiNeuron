from typing import Optional, List, Dict, Literal
from datetime import datetime
from huggingface_hub import model_info
import os
import logging
from BiNeuron.additional_functions.proxy_for_circumventing_restrictions import working_with_proxy
from BiNeuron.additional_functions.text_translation import TranslatorText
from BiNeuron.data.preferences_in_ai import PreferenceInAI
from BiNeuron.data.models_for_programming_languages import MODELS_DICT
from BiNeuron.additional_functions.defining_programming_language import DefiningProgrammingLanguage
from BiNeuron.data.models_and_file_names import MODELS_AND_FILE_NAMES
from BiNeuron.additional_functions.checking_and_downloading_ai_model import ModelDownloader
from BiNeuron.additional_functions.launching_ai_model_and_requesting import launching_ai_model_and_requesting
from BiNeuron.data.variants_industrial_scenarios import ALL_MAIN_PROMPTS
from BiNeuron.additional_functions.determining_computer_power import determining_type_computer
from BiNeuron.data.constants_for_functions import (TYPE_DEFAULT, HTTP_PROTOCOL, TYPES_POWER,
                                                   PROJECT_NAME, MAX_TIMEOUT, MAX_TOKENS,
                                                   MIN_TIMEOUT_FOR_CHECK, MAX_TIMEOUT_FOR_CHECK,
                                                   MAIN_LANGUAGE, NUMBER_ATTEMPTS, MAIN_PROXY_ATTEMPTS,
                                                   GOOGLE_TRANSLATE_URL, DEEPL_TRANSLATE_URL, TYPE_FORMATS,
                                                   TINY_TYPE, LITE_TYPE, MAIN_REPO_ID, MAIN_FILENAME,
                                                   NOT_UNREAD_FILES)
from BiNeuron.additional_functions.definition_swearing import definition_swearing
from BiNeuron.data.answer_against_profanity import ANSWER_AGAINST_PROFANITY
from BiNeuron.data.links_to_raw_github_proxies import PROXY_LINK_LST
from BiNeuron.additional_functions.checking_site_access import checking_site_access
from BiNeuron.additional_functions.logic_virtual_storage import logic_virtual_storage
from BiNeuron.data.prompt_for_json_formatter import PROMPT_FOR_JSON_FORMATTER
from BiNeuron.additional_functions.logic_editing_files import logic_editing_files
from BiNeuron import main_logger


logger = logging.getLogger(__name__)

class BiNeuron:
    def __init__(self,
                 request: str,
                 preferences_in_ai: PreferenceInAI = PreferenceInAI.DEEPSEEK,
                 filter_for_swearing: bool = False,
                 additional_files: Optional[List[str]] = None,
                 models_dir: str = "./models",
                 with_ai_orchestrator: bool = True,
                 verbose: bool = False,
                 n_ctx: Optional[int] = None,
                 n_gpu_layers: int = 0,
                 echo: bool = False,
                 max_tokens: int = MAX_TOKENS,
                 your_token_for_hf: Optional[str] = None,
                 subdomain: str = "",
                 country: Optional[str] = None,
                 protocol: str = HTTP_PROTOCOL,
                 max_timeout: int = MAX_TIMEOUT,
                 is_working: bool = True,
                 type_computer: Optional[Literal["easy", "middle", "hard", "very_hard"]] = None,
                 auto_proxies: bool = True,
                 writing_response_to_file: bool = False,
                 your_proxies_dict: Optional[List[str]] = None,
                 determinant_mode: Optional[Literal["lite", "full", "auto"]] = LITE_TYPE,
                 accurate_translation: bool = False,
                 your_key_for_deepl: str = "",
                 proprietary_algorithms: bool = False,
                 repo_id: Optional[str] = None,
                 filename: Optional[str] = None,
                 min_timeout_for_checking_availability: int = MIN_TIMEOUT_FOR_CHECK,
                 max_timeout_for_checking_availability: int = MAX_TIMEOUT_FOR_CHECK,
                 request_language: str = MAIN_LANGUAGE,
                 main_prompt_mode: Literal["default", "testing", "explanation", "no_comments",
                 "refactor", "debug", "code_review", "documentation", "scaffold",
                 "security_hardening", "algorithm_strategy"] = TYPE_DEFAULT,
                 main_prompt: Optional[str] = None,
                 temperature: float = 0.1,
                 retries: int = NUMBER_ATTEMPTS,
                 github_proxies: bool = False,
                 url_lst: List[str] = PROXY_LINK_LST,
                 proxy_retries: int = NUMBER_ATTEMPTS,
                 main_retries: int = MAIN_PROXY_ATTEMPTS,
                 lang_lst: Optional[List[str]] = None,
                 use_gpu_for_ocr: bool = False,
                 virtual_storage: bool = False,
                 virtual_storage_path: Optional[str] = None,
                 with_ocr: bool = False,
                 cloud_version: bool = False,
                 with_deepseek: bool = True,
                 model_size: Literal["tiny", "small", "base", "large", "gundam"] = TINY_TYPE,
                 crop_mode: bool = False,
                 base_url: str = "https://api.siliconflow.cn/v1/chat/completions",
                 api_key_for_deepseek_ocr: Optional[str] = None,
                 timeout_for_deepseek_ocr: Optional[int] = None,
                 max_rate_limit_retries: Optional[int] = NUMBER_ATTEMPTS,
                 prefer_mirror: bool = True,
                 editing_files: bool = False) -> None:
        """
        Initialize an BiNeuron instance with all necessary configuration.
        :param request: User's input text (question or code description).
        :param preferences_in_ai: Preferred AI model family (DeepSeek, Qwen, etc.).
        :param filter_for_swearing: If True, blocks responses containing profanity.
        :param additional_files: List of file paths to include as context for language detection.
        :param models_dir: Directory to cache downloaded models.
        :param with_ai_orchestrator: If True, uses AI to detect programming language (otherwise heuristics).
        :param verbose: Enables verbose output from the underlying LLM.
        :param n_ctx: Context window size for the model; uses model default if None.
        :param n_gpu_layers: Number of GPU layers to offload; 0 means CPU-only.
        :param echo: Whether to echo the prompt in the AI output.
        :param max_tokens: Maximum number of tokens to generate.
        :param your_token_for_hf: Hugging Face access token for private models (optional).
        :param subdomain: Prefix to add to the model filename during download.
        :param country: Country code for proxy selection (e.g., 'ru').
        :param protocol: Proxy protocol (default 'http').
        :param max_timeout: Maximum timeout (seconds) for proxy availability checks.
        :param is_working: If True, only proxies that pass the availability test are used.
        :param type_computer: Predefined computer power level ('easy', 'middle', 'hard', 'very_hard'). If None, it is auto-detected.
        :param auto_proxies: Enable automatic fallback to proxies if the primary connection fails.
        :param writing_response_to_file: If True, saves the AI response to a timestamped text file.
        :param your_proxies_dict: Custom list of proxy URLs; overrides automatic discovery.
        :param determinant_mode: Language detection mode for translation ('lite', 'full', 'auto').
        :param accurate_translation: If True, tries DeepL API (requires key) before Google Translate.
        :param your_key_for_deepl: DeepL API key (required if accurate_translation=True).
        :param proprietary_algorithms: If True, uses keyword-based language detection (faster but less accurate).
        :param repo_id: Explicit Hugging Face repository ID; overrides automatic model selection.
        :param filename: Filename of the model inside the repository; must be used with repo_id.
        :param min_timeout_for_checking_availability: Minimum timeout (seconds) for connection checks.
        :param max_timeout_for_checking_availability: Maximum timeout (seconds) for connection checks.
        :param request_language: Target language code for translation (default MAIN_LANGUAGE, e.g., 'en').
        :param main_prompt_mode: Predefined system prompt scenario (default, testing, explanation, etc.).
        :param main_prompt: Custom system prompt; overrides main_prompt_mode if provided.
        :param temperature: Sampling temperature for the AI response (0.0 to 1.0).
        :param retries: Number of attempts to download the model.
        :param github_proxies: If True, attempt to fetch proxies from GitHub raw lists first.
        :param url_lst: List of raw GitHub URLs containing proxy lists.
        :param proxy_retries: Number of attempts per URL when fetching from GitHub.
        :param main_retries: Number of times to retry obtaining a working proxy from GitHub.
        :param lang_lst: List of language codes for OCR (used if the file is an image).
        :param use_gpu_for_ocr: Whether to use GPU for OCR (used if image).
        :param virtual_storage: If True, enables virtual storage mode to process entire folders.
        :param virtual_storage_path: Path to the virtual storage folder.
        :param with_ocr: If True, includes image files for OCR processing.
        :param cloud_version: If True, uses cloud API for DeepSeek OCR instead of local model.
        :param with_deepseek: If True, uses DeepSeek OCR for image text extraction; otherwise uses EasyOCR.
        :param model_size: Size of the DeepSeek model ('tiny', 'small', 'base', 'large', 'gundam').
        :param crop_mode: If True, splits large images into fragments for more detailed recognition.
        :param base_url: API endpoint URL for DeepSeek cloud service.
        :param api_key_for_deepseek_ocr: API key for DeepSeek cloud service.
        :param timeout_for_deepseek_ocr: Timeout (seconds) for DeepSeek API requests.
        :param max_rate_limit_retries: Number of retry attempts on rate limit errors.
        :param prefer_mirror: If True, forces using the mirror endpoint (hf-mirror.com).
        :param editing_files: If True, the files are automatically created and modified.
        """
        logger.info("Initializing BiNeuron")
        self.request = request
        self.preferences_in_ai = preferences_in_ai
        self.filter_for_swearing = filter_for_swearing
        self.additional_files = additional_files
        self.models_dir = models_dir
        self.with_ai_orchestrator = with_ai_orchestrator
        self.verbose = verbose
        self.n_ctx = n_ctx
        self.n_gpu_layers = n_gpu_layers
        self.echo = echo
        self.max_tokens = max_tokens
        self.your_token_for_hf = your_token_for_hf
        self.subdomain = subdomain
        self.country = country
        self.protocol = protocol
        self.max_timeout = max_timeout
        self.is_working = is_working
        self.type_computer = type_computer
        self.auto_proxies = auto_proxies
        self.writing_response_to_file = writing_response_to_file
        self.your_proxies_dict = your_proxies_dict
        self.determinant_mode = determinant_mode
        self.accurate_translation = accurate_translation
        self.your_key_for_deepl = your_key_for_deepl
        self.proprietary_algorithms = proprietary_algorithms
        self.repo_id = repo_id
        self.filename = filename
        self.min_timeout_for_checking_availability = min_timeout_for_checking_availability
        self.max_timeout_for_checking_availability = max_timeout_for_checking_availability
        self.request_language = request_language
        self.main_prompt_mode = main_prompt_mode
        self.main_prompt = main_prompt
        self.temperature = temperature
        self.retries = retries
        self.github_proxies = github_proxies
        self.url_lst = url_lst
        self.proxy_retries = proxy_retries
        self.main_retries = main_retries
        self.lang_lst = lang_lst
        self.use_gpu_for_ocr = use_gpu_for_ocr
        self.virtual_storage = virtual_storage
        self.virtual_storage_path = virtual_storage_path
        self.with_ocr = with_ocr
        self.cloud_version = cloud_version
        self.with_deepseek = with_deepseek
        self.model_size = model_size
        self.crop_mode = crop_mode
        self.base_url = base_url
        self.api_key_for_deepseek_ocr = api_key_for_deepseek_ocr
        self.timeout_for_deepseek_ocr = timeout_for_deepseek_ocr
        self.max_rate_limit_retries = max_rate_limit_retries
        self.prefer_mirror = prefer_mirror
        self.editing_files = editing_files
        self.translated_text = None
        self.programmer_langs = None
        self.proxies_lst = None
        self.history = []
        self.unread_files = None
        self.files_context = None

    def __settings_for_proxy(self) -> None:
        """
        Check if proxy is needed for translation and configure it if necessary.
        Determines which translation service (DeepL or Google Translate) is selected,
        checks its availability via `checking_site_access`, and if unavailable,
        fetches a working proxy using `working_with_proxy`. The proxy list is stored
        in `self.proxies_lst`.
        """
        logger.info("Challenge __settings_for_proxy")
        if self.accurate_translation:
            logger.info("DeepL was chosen as the main translator.")
            verification_link = DEEPL_TRANSLATE_URL
        else:
            logger.info("Google Translate was chosen as the main translator.")
            verification_link = GOOGLE_TRANSLATE_URL

        if not checking_site_access(verification_link):
            logger.info("The requested translator site is unavailable, we are enabling proxy operation.")
            self.proxies_lst = working_with_proxy(
                country=self.country,
                protocol=self.protocol,
                max_timeout=self.max_timeout,
                is_working=self.is_working,
                version_1=False,
                your_proxies=self.your_proxies_dict,
                github_proxies=self.github_proxies,
                url_lst=self.url_lst,
                proxy_retries=self.proxy_retries,
                main_retries=self.main_retries
            )

    def __settings_for_translator(self) -> Dict:
        """
        Build a dictionary of translation parameters.
        Calls `__settings_for_proxy` to ensure proxy configuration is up to date,
        then returns a dictionary containing all parameters needed for `TranslatorText`.
        :return: Dictionary with keys: determinant_mode, proxies, accurate_translation,
        your_key_for_deepl, request_language.
        """
        logger.info("Challenge __settings_for_translator")
        self.__settings_for_proxy()

        return {
            "determinant_mode": self.determinant_mode,
            "proxies": self.proxies_lst,
            "accurate_translation": self.accurate_translation,
            "your_key_for_deepl": self.your_key_for_deepl,
            "request_language": self.request_language
        }

    def __different_translation(self) -> None:
        """
        Translate the user request into the target language using the configured proxy list.
        Uses `__settings_for_translator` to obtain translation parameters,
        instantiates a `TranslatorText` object, and stores the translated text in
        `self.translated_text`. If translation fails, the original text is kept.
        """
        logger.info("Challenge __different_translation")

        logger.info("The original text has been translated into English for a better understanding of AI.")
        self.translated_text = TranslatorText(original_text=self.request,
                                              **self.__settings_for_translator()).main_translater()

    def _virtual_storage_operation(self) -> None:
        """
        Process virtual storage to extract file lists.
        Calls `logic_virtual_storage` with the configured path and OCR settings,
        then updates `self.additional_files` with readable files and `self.unread_files`
        with files that could not be processed.
        """
        logger.info("Challenge _virtual_storage_operation")
        answer = logic_virtual_storage(
            path=self.virtual_storage_path,
            with_ocr=self.with_ocr,
            **self.__settings_for_translator()
        )
        logger.info("Additional files were overwritten to the files contained in the virtual storage.")
        self.additional_files = answer[TYPE_FORMATS[0]]
        self.unread_files = answer[TYPE_FORMATS[1]]

    def _defining_prog_lang(self) -> None:
        """
        Determine the programming language(s) present in the request and any additional files.
        First calls `__different_translation` to translate the user input,
        then processes virtual storage if enabled.
        Finally, uses `DefiningProgrammingLanguage` to detect the language(s)
        from the translated text and file contents. The result is stored in
        `self.programmer_langs`.
        """
        logger.info("Challenge _defining_prog_lang")
        self.__different_translation()

        if self.virtual_storage:
            self._virtual_storage_operation()

        logger.info("The beginning of the definition of the necessary programming languages in the user's request.")
        defining_obj = DefiningProgrammingLanguage(
            translated_text=self.translated_text,
            unread_files=self.unread_files,
            additional_files=self.additional_files,
            with_ai_orchestrator=self.with_ai_orchestrator,
            proprietary_algorithms=self.proprietary_algorithms,
            lang_lst=self.lang_lst,
            use_gpu=self.use_gpu_for_ocr,
            verbose=self.verbose,
            **self.__settings_for_translator(),
            cloud_version=self.cloud_version,
            with_deepseek=self.with_deepseek,
            model_size=self.model_size,
            crop_mode=self.crop_mode,
            base_url=self.base_url,
            api_key_for_deepseek_ocr=self.api_key_for_deepseek_ocr,
            timeout_for_deepseek_ocr=self.timeout_for_deepseek_ocr,
            max_rate_limit_retries=self.max_rate_limit_retries,
            prefer_mirror=self.prefer_mirror
        )
        self.programmer_langs = defining_obj.defining_programming_language_for_str()
        self.files_context = defining_obj.translated_text
        logger.info(f"The programming language is defined: {self.programmer_langs}")

    def _defining_ai_model(self) -> str or Dict:
        """
        Select the AI model(s) corresponding to the detected programming language.
        Calls `_defining_prog_lang` to ensure language is known, then looks up the model
        in `MODELS_DICT`. Returns a model identifier (string) for a specific language or
        a dictionary of multilingual options for the default language.
        :return: Either a single model ID (string) or a dictionary mapping PreferenceInAI to model IDs.
        """
        logger.info("Challenge _defining_ai_model")
        self._defining_prog_lang()
        model = MODELS_DICT[self.programmer_langs]
        logger.info(f"A model has been selected: {model}")
        return model

    def __special_defining_type_ai_model(self, models_dict: Dict) -> str:
        """
        Choose the specific multilingual model based on the user's preference.
        :param models_dict: Dictionary mapping PreferenceInAI values to model repository IDs.
        :return: The repository ID of the selected multilingual model.
        """
        logger.info(f"Challenge __special_defining_type_ai_model with preference {self.preferences_in_ai}")
        if self.preferences_in_ai == PreferenceInAI.QWEN:
            logger.info("Qwen is selected for the default language.")
            return models_dict[PreferenceInAI.QWEN.value]
        elif self.preferences_in_ai == PreferenceInAI.MINIMAX:
            logger.info("MiniMax is selected for the default language.")
            return models_dict[PreferenceInAI.MINIMAX.value]
        elif self.preferences_in_ai == PreferenceInAI.CODE_LLAMA:
            logger.info("CodeLlama is selected for the default language.")
            return models_dict[PreferenceInAI.CODE_LLAMA.value]
        elif self.preferences_in_ai == PreferenceInAI.MELLUM:
            logger.info("Mellum is selected for the default language.")
            return models_dict[PreferenceInAI.MELLUM.value]
        elif self.preferences_in_ai == PreferenceInAI.WIZARD:
            logger.info("Wizard is selected for the default language.")
            return models_dict[PreferenceInAI.WIZARD.value]
        else:
            logger.info("DeepSeek is selected for the default language.")
            return models_dict[PreferenceInAI.DEEPSEEK.value]

    def _defining_type_ai_model(self) -> str:
        """
        Determine the final model repository ID based on language and user preference.
        If the detected language is `TYPE_DEFAULT` (unknown/multilingual), it calls
        `__special_defining_type_ai_model` to pick a multilingual model. Otherwise,
        it returns the language-specific model from `_defining_ai_model`.
        :return: The Hugging Face repository ID of the selected model.
        """
        logger.info("Challenge _defining_type_ai_model")
        ai_model = self._defining_ai_model()
        if self.programmer_langs == TYPE_DEFAULT:
            logger.info("The language is not defined (default) — we select a multilingual model.")
            result = self.__special_defining_type_ai_model(ai_model)
            logger.info(f"A multilingual model has been selected: {result}")
            return result
        else:
            logger.info(f"A specialized model has been selected: {ai_model}")
            return ai_model

    def _main_defining_type_ai_model(self) -> str:
        """
        Return the exact model filename based on computer power and the selected repository.
        If `type_computer` is not set or invalid, it is auto-detected via `determining_type_computer`.
        Then uses `MODELS_AND_FILE_NAMES` to retrieve the appropriate file name for the
        current `repo_id` and computer type.
        :return: The model filename to be downloaded.
        """
        logger.info("Challenge _main_defining_type_ai_model")
        if (self.type_computer is None) or (not self.type_computer in TYPES_POWER):
            self.type_computer = determining_type_computer()
            logger.info(f"The computer type is determined automatically: {self.type_computer}")
        else:
            logger.info(f"The computer type is set by the user: {self.type_computer}")

        filename = MODELS_AND_FILE_NAMES[self.repo_id]
        full_filename = filename[self.type_computer]

        logger.info(f"A model variant file for your type of PC has been selected in the repository.")
        return full_filename

    def __settings_for_model_downloader(self) -> Dict:
        """
        Compile all parameters needed for the ModelDownloader into a single dictionary.
        :return: A dictionary containing keys such as 'repo_id', 'filename', 'cache_dir',
        'token', proxy settings, timeout values and retry configurations.
        """
        logger.info("Challenge __settings_for_model_downloader")
        return {
            "repo_id": self.repo_id,
            "filename": self.filename,
            "cache_dir": self.models_dir,
            "subdomain": self.subdomain,
            "token": self.your_token_for_hf,
            "country": self.country,
            "protocol": self.protocol,
            "max_timeout": self.max_timeout,
            "your_proxies": self.your_proxies_dict,
            "is_working": self.is_working,
            "auto_proxies": self.auto_proxies,
            "min_timeout_for_checking_availability": self.min_timeout_for_checking_availability,
            "max_timeout_for_checking_availability": self.max_timeout_for_checking_availability,
            "retries": self.retries,
            "github_proxies": self.github_proxies,
            "url_lst": self.url_lst,
            "proxy_retries": self.proxy_retries,
            "main_retries": self.main_retries,
            "prefer_mirror": self.prefer_mirror
        }

    def __template_for_download_models(self) -> None:
        """
        Execute the model download using the current configuration.
        Instantiates `ModelDownloader` with the settings from `__settings_for_model_downloader`
        and invokes its `auto_manager_for_download` method to handle the download logic.
        """
        logger.info("Challenge __template_for_download_models")
        model_dwn = ModelDownloader(**self.__settings_for_model_downloader())
        model_dwn.auto_manager_for_download()

    def __non_automatic_model_selection(self) -> None:
        """
        Download a user-specified model (non-automatic mode).
        Uses the `repo_id` and `filename` provided by the user (or defaults). If the download
        fails, the exception is propagated to `_check_and_download_ai_model` which may fall back
        to automatic selection.
        """
        logger.info("Challenge __non_automatic_model_selection")
        logger.info(f"Model starts downloading from repository (Non-automatic mode).")
        self.__template_for_download_models()

    def __automatic_model_selection(self) -> None:
        """
        Automatically select and download the best model based on language and computer power.
        The `repo_id` and `filename` are determined by `_defining_type_ai_model` and
        `_main_defining_type_ai_model`, then downloaded using `__template_for_download_models`.
        """
        logger.info("Challenge __automatic_model_selection")
        logger.info("The beginning of defining the repository of the model and the file inside this repository for later download.")
        self.repo_id = self._defining_type_ai_model()
        self.filename = self._main_defining_type_ai_model()
        logger.info(f"Model starts downloading from repository (Automatic mode).")
        self.__template_for_download_models()

    def _check_and_download_ai_model(self) -> None:
        """
        Main entry point for downloading the AI model.
        Decides between automatic and non-automatic selection:
        - If both `repo_id` and `filename` are None, runs automatic selection.
        - Otherwise, attempts non-automatic; if it fails, falls back to automatic selection.
        Additionally, checks if the repository is a text-generation model; if not, switches to auto.
        """
        logger.info("Challenge _check_and_download_ai_model")
        if ((self.repo_id is None and self.filename is None) or
                (model_info(self.repo_id).pipeline_tag != "text-generation")):
            logger.warning("Your model does not meet the condition, automatic mode is enabled.")
            self.__automatic_model_selection()
        else:
            try:
                self.__non_automatic_model_selection()
            except Exception as e:
                logger.warning(f"Error when trying to load this model from Hugging Face - {e}")
                self.__automatic_model_selection()
        logger.info("Has the model been uploaded successfully or already exists in the cache.")

    def _creating_main_prompt(self) -> None:
        """
        Select or construct the system prompt for the AI.
        If `main_prompt` is not provided, it uses the predefined prompt corresponding to
        `main_prompt_mode` from `ALL_MAIN_PROMPTS`. If the mode is invalid, it defaults to
        `TYPE_DEFAULT`. The final prompt is stored in `self.main_prompt`.
        """
        logger.info("Challenge _creating_main_prompt")
        if not self.main_prompt_mode in ALL_MAIN_PROMPTS.keys():
            logger.info("The default main technical prompt has been selected.")
            self.main_prompt_mode = TYPE_DEFAULT

        if self.main_prompt is None:
            logger.info("The preset mode for prompta is selected.")
            self.main_prompt = ALL_MAIN_PROMPTS[self.main_prompt_mode]

    def _creating_chat_record(self, ai_answer: str) -> None:
        """
        Save the AI response to a file if `writing_response_to_file` is enabled.
        The file name includes the project name and a timestamp to avoid overwriting.
        The content is written as plain text.
        :param ai_answer: The AI-generated response to be saved.
        """
        logger.info("Challenge _creating_chat_record")
        if self.writing_response_to_file:
            filename = f"{PROJECT_NAME}_{datetime.now()}.txt"
            with open(filename, "w", encoding="utf-8") as file:
                file.write(ai_answer)
            logger.info(f"The response is saved to a file {filename}")

    def _add_to_history(self, role: str, content: str) -> None:
        """
        Append a message to the conversation history.
        The history is stored as a list of dictionaries with 'role' and 'content' keys.
        This is used to maintain context across multiple turns in a chat session.
        :param role: The role of the speaker ('user' or 'assistant').
        :param content: The message content.
        """
        logger.info("Challenge _add_to_history")
        self.history.append({"role": role, "content": content})

    def _build_messages(self) -> List[Dict[str, str]]:
        """
        Construct the full message list for the AI model.
        The list starts with the system prompt, followed by the conversation history,
        and finally the current user message (from `self.translated_text`).
        :return: A list of messages suitable for the AI model's chat API.
        """
        logger.info("Challenge _build_messages")
        messages = [{"role": "system", "content": self.main_prompt}]
        messages.extend(self.history)
        messages.append({"role": "user", "content": self.translated_text})
        logger.info("A list of all requests for AI has been generated.")
        return messages

    def __settings_for_launching_ai_model(self) -> Dict:
        """
        A dictionary of necessary parameters for configuring the Model Launcher.
        :return: Dictionary of the values 'models_dir', 'n_ctx', 'n_gpu_layers'
        and similar values needed for the model.
        """
        logger.info("Challenge __settings_for_launching_ai_model")
        return {
            "models_dir": self.models_dir,
            "n_ctx": self.n_ctx,
            "n_gpu_layers": self.n_gpu_layers,
            "verbose": self.verbose,
            "echo": self.echo,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "prefer_mirror": self.prefer_mirror
        }

    def _send_message(self, user_text: Optional[str] = None) -> str:
        """
        Send a message to the AI model and return the response.
        If `user_text` is provided, it updates the request and re-translates it.
        If profanity filtering is enabled, it checks the translated text and returns
        a predefined response if profanity is detected.
        The method then builds the system prompt, constructs the messages,
        invokes the primary AI model, logs the response, updates the conversation
        history, and optionally saves the response to a file.
        Additionally, if `editing_files` is enabled, the primary model's response
        is passed (along with the full file context and unread file names) to a
        second model (Qwen) that converts the changes into a strict JSON object.
        The JSON is then applied via `logic_editing_files` to modify the actual
        files on disk. If the JSON parsing fails, up to `self.retries` attempts
        are made to regenerate it.
        :param user_text: Optional new user input; if given, replaces the current request.
        :return: The AI-generated response (the primary model's answer, not the JSON).
        """
        logger.info("Challenge _send_message")
        if user_text is not None:
            self.request = user_text
            self.translated_text = None
            self.__different_translation()

        if self.filter_for_swearing:
            logger.info("Checking for profanity.")
            if definition_swearing(text=self.translated_text):
                logger.warning("Profanity detected, returning a template response.")
                return ANSWER_AGAINST_PROFANITY

        self._creating_main_prompt()

        messages = self._build_messages()

        logger.info("Starting the AI response generation.")
        ai_answer = launching_ai_model_and_requesting(
            messages=messages,
            repo_id=self.repo_id,
            filename=self.filename,
            template_prompt=self.main_prompt,
            **self.__settings_for_launching_ai_model()
        )
        logger.info("AI response received, length: %d characters", len(ai_answer))

        self._add_to_history("user", self.translated_text)
        self._add_to_history("assistant", ai_answer)

        self._creating_chat_record(ai_answer=ai_answer)

        if self.editing_files:
            logger.info("Automatic file modification has been selected thanks to AI.")
            is_json = False
            un_files = None

            if self.unread_files:
                un_files = "\n".join(self.unread_files)
            else:
                un_files = NOT_UNREAD_FILES

            final_messages = (
                f"{'=' * 5}PROJECT ROOT{'=' * 5}\n{os.getcwd()}\n"
                f"{'=' * 5}ALL USER CONTEXT AND READ FILES{'=' * 5}\n"
                f"{self.files_context}\n"
                f"{'=' * 5}ALL UNREAD FILES{'=' * 5}\n"
                f"{un_files}\n"
                f"{'=' * 5}THE FINAL RESPONSE FROM THE AI MODEL{'=' * 5}\n"
                f"{ai_answer}\n")

            for attempt in range(NUMBER_ATTEMPTS):
                logger.info(f"Attempt number {attempt} to change files automatically.")
                json_answer = launching_ai_model_and_requesting(
                    messages=final_messages,
                    repo_id=MAIN_REPO_ID,
                    filename=MAIN_FILENAME,
                    template_prompt=PROMPT_FOR_JSON_FORMATTER,
                    **self.__settings_for_launching_ai_model()
                )
                file_answer = logic_editing_files(str_json=json_answer)

                if file_answer is False:
                    continue
                else:
                    is_json = True
                    break

            if is_json:
                logger.info("After a number of attempts, the file modification was successful.")
            else:
                logger.warning("For all attempts, the files could not be overwritten, the usual response was given.")

        return ai_answer

    def final_ai_request(self) -> str:
        """
        Execute the full pipeline and return the AI response for a single-shot request.
        This is the primary method for non-interactive usage. It ensures the model is
        downloaded, translates the request if not already done, and calls `_send_message`.
        :return: The final AI-generated response.
        """
        logger.info("Challenge final_ai_request")
        self._check_and_download_ai_model()

        if self.translated_text is None:
            self.__different_translation()

        return self._send_message()

    def chat(self) -> None:
        """
        Start an interactive chat session with the AI.
        Downloads the model (if not already done), then enters a loop where the user
        can type messages and receive AI responses. The conversation history is
        maintained across turns. Type 'exit' or press Ctrl+C/Ctrl+D to end the session.
        """
        self._check_and_download_ai_model()

        print("The dialogue has begun. To exit, enter 'exit'.")

        while True:
            try:
                user_input = input("You: ")
            except (KeyboardInterrupt, EOFError):
                print("\nThe dialog is completed.")
                break

            if user_input.strip().lower() == "exit":
                print("See you soon.")
                break

            answer = self._send_message(user_text=user_input)
            print(f"AI: {answer}")


if __name__ == "__main__":
    biNeuron = BiNeuron(request="")
    biNeuron.chat()