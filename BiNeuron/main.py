from typing import Dict, Optional, List
from datetime import datetime
from huggingface_hub import model_info
import os
import logging
from BiNeuron.data.preferences_in_ai import PREFERENCES_IN_AI_LIST
from BiNeuron.additional_functions.proxy_for_circumventing_restrictions import working_with_proxy
from BiNeuron.additional_functions.text_translation import TranslatorText
from BiNeuron.data.models_for_programming_languages import MODELS_DICT
from BiNeuron.additional_functions.defining_programming_language import DefiningProgrammingLanguage
from BiNeuron.data.models_and_file_names import MODELS_AND_FILE_NAMES
from BiNeuron.additional_functions.checking_and_downloading_ai_model import ModelDownloader
from BiNeuron.additional_functions.launching_ai_model_and_requesting import launching_ai_model_and_requesting
from BiNeuron.data.variants_industrial_scenarios import ALL_MAIN_PROMPTS
from BiNeuron.additional_functions.determining_computer_power import determining_type_computer
from BiNeuron.data.constants_for_functions import (TYPES_POWER, PROJECT_NAME, GOOGLE_TRANSLATE_URL,
                                                   DEEPL_TRANSLATE_URL, TYPE_FORMATS, MAIN_REPO_ID,
                                                   MAIN_FILENAME, NOT_UNREAD_FILES, TYPE_DEFAULT,
                                                   NUMBER_ATTEMPTS)
from BiNeuron.additional_functions.definition_swearing import definition_swearing
from BiNeuron.data.answer_against_profanity import ANSWER_AGAINST_PROFANITY
from BiNeuron.additional_functions.checking_site_access import checking_site_access
from BiNeuron.additional_functions.logic_virtual_storage import logic_virtual_storage
from BiNeuron.data.prompt_for_json_formatter import PROMPT_FOR_JSON_FORMATTER
from BiNeuron.additional_functions.logic_editing_files import logic_editing_files
from BiNeuron.data.prompt_json_deleting import PROMPT_JSON_DELETING
from BiNeuron.additional_functions.deleting_files_thanks_to_ai import deleting_files_thanks_to_ai
from BiNeuron.data.configs import (ModelConfig, LLMConfig, PromptConfig, TranslationConfig,
                                   LanguageDetectionConfig, ProxyConfig, OCRConfig, FileConfig,
                                   SafetyConfig)
from BiNeuron import main_logger


logger = logging.getLogger(__name__)

class BiNeuron:
    def __init__(self,
                 request: str,
                 additional_files: Optional[List[str]] = None,
                 model_conf: Optional[ModelConfig] = None,
                 llm_conf: Optional[LLMConfig] = None,
                 prompt_conf: Optional[PromptConfig] = None,
                 translation_conf: Optional[TranslationConfig] = None,
                 language_detection_conf: Optional[LanguageDetectionConfig] = None,
                 proxy_conf: Optional[ProxyConfig] = None,
                 ocr_conf: Optional[OCRConfig] = None,
                 file_conf: Optional[FileConfig] = None,
                 safety_conf: Optional[SafetyConfig] = None) -> None:
        """
        Initialize a BiNeuron instance with all necessary configuration.
        All configuration is grouped into dataclasses (ModelConfig, LLMConfig, PromptConfig,
        TranslationConfig, LanguageDetectionConfig, ProxyConfig, OCRConfig, FileConfig,
        SafetyConfig). If any config is not provided, a default instance is created.
        :param request: User's input text (question or code description).
        :param additional_files: List of file paths to include as context for language detection.
        :param model_conf: Configuration for model selection, repository, filename, and cache.
        :param llm_conf: Configuration for LLM generation (temperature, max_tokens, etc.).
        :param prompt_conf: Configuration for the system prompt (mode and custom prompt).
        :param translation_conf: Configuration for text translation (mode, proxy, DeepL, local).
        :param language_detection_conf: Configuration for programming language detection.
        :param proxy_conf: Configuration for proxy usage (country, timeouts, retries).
        :param ocr_conf: Configuration for OCR (language list, GPU, DeepSeek, model size, etc.).
        :param file_conf: Configuration for virtual storage and file editing/deletion.
        :param safety_conf: Configuration for content filtering (profanity).
        """
        logger.info("Initializing BiNeuron")
        self.request = request
        self.additional_files = additional_files
        self.model_conf = model_conf or ModelConfig()
        self.llm_conf = llm_conf or LLMConfig()
        self.prompt_conf = prompt_conf or PromptConfig()
        self.translation_conf = translation_conf or TranslationConfig()
        self.language_detection_conf = language_detection_conf or LanguageDetectionConfig()
        self.proxy_conf = proxy_conf or ProxyConfig()
        self.ocr_conf = ocr_conf or OCRConfig()
        self.file_conf = file_conf or FileConfig()
        self.safety_conf = safety_conf or SafetyConfig()
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
        if self.translation_conf.accurate_translation:
            logger.info("DeepL was chosen as the main translator.")
            verification_link = DEEPL_TRANSLATE_URL
        else:
            logger.info("Google Translate was chosen as the main translator.")
            verification_link = GOOGLE_TRANSLATE_URL

        if not checking_site_access(verification_link):
            logger.info("The requested translator site is unavailable, we are enabling proxy operation.")
            self.proxies_lst = working_with_proxy(
                country=self.proxy_conf.country,
                protocol=self.proxy_conf.protocol,
                max_timeout=self.proxy_conf.max_timeout,
                is_working=self.proxy_conf.is_working,
                version_1=False,
                your_proxies=self.proxy_conf.your_proxies_dict,
                github_proxies=self.proxy_conf.github_proxies,
                url_lst=self.proxy_conf.url_lst,
                proxy_retries=self.proxy_conf.proxy_retries,
                main_retries=self.proxy_conf.main_retries
            )

    def __settings_for_translator(self) -> Dict:
        """
        Build a dictionary of translation parameters.
        Calls `__settings_for_proxy` to ensure proxy configuration is up to date,
        then returns a dictionary containing all parameters needed for `TranslatorText`.
        :return: Dictionary with keys: determinant_mode, proxies, accurate_translation,
        your_key_for_deepl, request_language, local_trans, from_code_lang.
        """
        logger.info("Challenge __settings_for_translator")
        self.__settings_for_proxy()

        return {
            "determinant_mode": self.translation_conf.determinant_mode,
            "proxies": self.proxies_lst,
            "accurate_translation": self.translation_conf.accurate_translation,
            "your_key_for_deepl": self.translation_conf.your_key_for_deepl,
            "request_language": self.translation_conf.request_language,
            "local_trans": self.translation_conf.local_trans,
            "from_code_lang": self.translation_conf.from_code_lang
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
            path=self.file_conf.virtual_storage_path,
            with_ocr=self.ocr_conf.with_ocr
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
        `self.programmer_langs`, and the full file context is stored in `self.files_context`.
        """
        logger.info("Challenge _defining_prog_lang")
        self.__different_translation()

        if self.file_conf.virtual_storage:
            self._virtual_storage_operation()

        logger.info("The beginning of the definition of the necessary programming languages in the user's request.")
        defining_obj = DefiningProgrammingLanguage(
            translated_text=self.translated_text,
            unread_files=self.unread_files,
            additional_files=self.additional_files,
            with_ai_orchestrator=self.language_detection_conf.with_ai_orchestrator,
            proprietary_algorithms=self.language_detection_conf.proprietary_algorithms,
            lang_lst=self.ocr_conf.lang_lst,
            use_gpu=self.ocr_conf.use_gpu_for_ocr,
            verbose=self.llm_conf.verbose,
            **self.__settings_for_translator(),
            cloud_version=self.ocr_conf.cloud_version,
            with_deepseek=self.ocr_conf.with_deepseek,
            model_size=self.ocr_conf.model_size,
            crop_mode=self.ocr_conf.crop_mode,
            base_url=self.ocr_conf.base_url,
            api_key_for_deepseek_ocr=self.ocr_conf.api_key_for_deepseek_ocr,
            timeout_for_deepseek_ocr=self.ocr_conf.timeout_for_deepseek_ocr,
            max_rate_limit_retries=self.ocr_conf.max_rate_limit_retries,
            prefer_mirror=self.model_conf.prefer_mirror
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
        logger.info(f"Challenge __special_defining_type_ai_model with preference {self.model_conf.preferences_in_ai}")
        ai_value = None

        if self.model_conf.preferences_in_ai in PREFERENCES_IN_AI_LIST:
            ai_value = self.model_conf.preferences_in_ai
        else:
            logger.warning(f"{ai_value} - this model was not found in the prepared list.")
            ai_value = PREFERENCES_IN_AI_LIST[0]

        logger.info(f"{ai_value.capitalize()} is selected as the default model.")
        return models_dict[ai_value]

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
        current `repo_id` and computer type. The result is stored back into `model_conf`.
        :return: The model filename to be downloaded.
        """
        logger.info("Challenge _main_defining_type_ai_model")
        if (self.model_conf.type_computer is None) or (not self.model_conf.type_computer in TYPES_POWER):
            self.model_conf.type_computer = determining_type_computer()
            logger.info(f"The computer type is determined automatically: {self.model_conf.type_computer}")
        else:
            logger.info(f"The computer type is set by the user: {self.model_conf.type_computer}")

        filename = MODELS_AND_FILE_NAMES[self.model_conf.repo_id]
        full_filename = filename[self.model_conf.type_computer]

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
            "repo_id": self.model_conf.repo_id,
            "filename": self.model_conf.filename,
            "cache_dir": self.model_conf.models_dir,
            "subdomain": self.model_conf.subdomain,
            "token": self.model_conf.your_token_for_hf,
            "country": self.proxy_conf.country,
            "protocol": self.proxy_conf.protocol,
            "max_timeout": self.proxy_conf.max_timeout,
            "your_proxies": self.proxy_conf.your_proxies_dict,
            "is_working": self.proxy_conf.is_working,
            "auto_proxies": self.proxy_conf.auto_proxies,
            "min_timeout_for_checking_availability": self.proxy_conf.min_timeout_for_checking_availability,
            "max_timeout_for_checking_availability": self.proxy_conf.max_timeout_for_checking_availability,
            "retries": self.model_conf.retries,
            "github_proxies": self.proxy_conf.github_proxies,
            "url_lst": self.proxy_conf.url_lst,
            "proxy_retries": self.proxy_conf.proxy_retries,
            "main_retries": self.proxy_conf.main_retries,
            "prefer_mirror": self.model_conf.prefer_mirror
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
        `_main_defining_type_ai_model`, saved into `model_conf`, and then downloaded
        using `__template_for_download_models`.
        """
        logger.info("Challenge __automatic_model_selection")
        logger.info("The beginning of defining the repository of the model and the file inside this repository for later download.")
        self.model_conf.repo_id = self._defining_type_ai_model()
        self.model_conf.filename = self._main_defining_type_ai_model()
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
        if ((self.model_conf.repo_id is None and self.model_conf.filename is None) or
                (model_info(self.model_conf.repo_id).pipeline_tag != "text-generation")):
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
        `TYPE_DEFAULT`. The final prompt is stored in `prompt_conf.main_prompt`.
        """
        logger.info("Challenge _creating_main_prompt")
        if not self.prompt_conf.main_prompt_mode in ALL_MAIN_PROMPTS.keys():
            logger.info("The default main technical prompt has been selected.")
            self.prompt_conf.main_prompt_mode = TYPE_DEFAULT

        if self.prompt_conf.main_prompt is None:
            logger.info("The preset mode for prompta is selected.")
            self.prompt_conf.main_prompt = ALL_MAIN_PROMPTS[self.prompt_conf.main_prompt_mode]

    def _creating_chat_record(self, ai_answer: str) -> None:
        """
        Save the AI response to a file if `writing_response_to_file` is enabled.
        The file name includes the project name and a timestamp to avoid overwriting.
        The content is written as plain text.
        :param ai_answer: The AI-generated response to be saved.
        """
        logger.info("Challenge _creating_chat_record")
        if self.file_conf.writing_response_to_file:
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
        The list starts with the system prompt (from `prompt_conf.main_prompt`),
        followed by the conversation history, and finally the current user message
        (from `self.translated_text`).
        :return: A list of messages suitable for the AI model's chat API.
        """
        logger.info("Challenge _build_messages")
        messages = [{"role": "system", "content": self.prompt_conf.main_prompt}]
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
            "models_dir": self.model_conf.models_dir,
            "n_ctx": self.llm_conf.n_ctx,
            "n_gpu_layers": self.llm_conf.n_gpu_layers,
            "verbose": self.llm_conf.verbose,
            "echo": self.llm_conf.echo,
            "max_tokens": self.llm_conf.max_tokens,
            "temperature": self.llm_conf.temperature,
            "prefer_mirror": self.model_conf.prefer_mirror
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
        Additionally, if `editing_files` is enabled in `file_conf`, the primary model's
        response is passed (along with the full file context and unread file names) to a
        second model (Qwen) that converts the changes into a strict JSON object.
        The JSON is then applied via `logic_editing_files` to modify the actual
        files on disk. If the JSON parsing fails, up to `NUMBER_ATTEMPTS` attempts
        are made to regenerate it. If `deleting_files` is also enabled, files marked
        with `null` in the JSON are deleted via `deleting_files_thanks_to_ai`.
        :param user_text: Optional new user input; if given, replaces the current request.
        :return: The AI-generated response (the primary model's answer, not the JSON).
        """
        logger.info("Challenge _send_message")
        if user_text is not None:
            self.request = user_text
            self.translated_text = None
            self.__different_translation()

        if self.safety_conf.filter_for_swearing:
            logger.info("Checking for profanity.")
            if definition_swearing(text=self.translated_text):
                logger.warning("Profanity detected, returning a template response.")
                return ANSWER_AGAINST_PROFANITY

        self._creating_main_prompt()

        messages = self._build_messages()

        logger.info("Starting the AI response generation.")
        ai_answer = launching_ai_model_and_requesting(
            messages=messages,
            repo_id=self.model_conf.repo_id,
            filename=self.model_conf.filename,
            template_prompt=self.prompt_conf.main_prompt,
            **self.__settings_for_launching_ai_model()
        )
        logger.info("AI response received, length: %d characters", len(ai_answer))

        self._add_to_history("user", self.translated_text)
        self._add_to_history("assistant", ai_answer)

        self._creating_chat_record(ai_answer=ai_answer)

        if self.file_conf.editing_files:
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
                template_prompt = None

                if self.file_conf.deleting_files:
                    template_prompt = PROMPT_JSON_DELETING
                else:
                    template_prompt = PROMPT_FOR_JSON_FORMATTER

                json_answer = launching_ai_model_and_requesting(
                    messages=final_messages,
                    repo_id=MAIN_REPO_ID,
                    filename=MAIN_FILENAME,
                    template_prompt=template_prompt,
                    **self.__settings_for_launching_ai_model()
                )
                file_answer = logic_editing_files(str_json=json_answer)

                if file_answer is False:
                    continue
                else:
                    if self.file_conf.deleting_files:
                        logger.info("The deletion of the file from the list has begun.")
                        deleting_files_thanks_to_ai(answer_json=file_answer)

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