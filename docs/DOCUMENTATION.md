<details>
<summary>🇬🇧 English</summary>

## Overview

`BiNeuron` is the main class of the **biNeuron** package. It orchestrates the entire workflow:

* **Language detection**: determines the programming language(s) from the user request and attached files.
* **Model selection**: automatically picks the best suited GGUF model (language specific or multilingual) based on the detected language and your computer performance.
* **Download and caching**: downloads the selected model from Hugging Face (with proxy and mirror support).
* **Prompt engineering**: builds a system prompt according to the desired scenario (default, testing, explanation, refactoring, etc.).
* **AI inference**: sends the request to the loaded LLM and returns the response.
* **File editing (optional)**: if enabled, the AI response is parsed and used to directly edit files on disk.
* **Interactive chat**: supports multi turn conversations with history.

> **Note (breaking change):** starting from the current version, `BiNeuron` no longer accepts dozens of flattened keyword arguments.  
> Instead, all options are grouped into **dataclasses** (`ModelConfig`, `LLMConfig`, `PromptConfig`, `TranslationConfig`, `LanguageDetectionConfig`, `ProxyConfig`, `OCRConfig`, `FileConfig`, `SafetyConfig`) defined in `BiNeuron.data.configs`.  
> Pass any subset of them; omitted configs get safe defaults.

---

## Constructor

```python
BiNeuron(
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
    safety_conf: Optional[SafetyConfig] = None,
) -> None
```

Parameters:

* `request` (`str`, **required**): the user input text (question, code description, or task).
* `additional_files` (`Optional[List[str]]`, default `None`): list of file paths whose content is included as context for the AI.
* `model_conf` (`Optional[ModelConfig]`, default `None`): model selection, repo, filename, cache dir, HF token, mirror preference. Falls back to defaults.
* `llm_conf` (`Optional[LLMConfig]`, default `None`): LLM generation parameters (temperature, max_tokens, n_ctx, GPU layers). Falls back to defaults.
* `prompt_conf` (`Optional[PromptConfig]`, default `None`): system prompt mode and/or custom system prompt. Falls back to defaults.
* `translation_conf` (`Optional[TranslationConfig]`, default `None`): translation and language detection settings, DeepL key, local translation. Falls back to defaults.
* `language_detection_conf` (`Optional[LanguageDetectionConfig]`, default `None`): programming language detection (AI orchestrator or heuristics). Falls back to defaults.
* `proxy_conf` (`Optional[ProxyConfig]`, default `None`): proxy usage, timeouts, retries, GitHub proxy list. Falls back to defaults.
* `ocr_conf` (`Optional[OCRConfig]`, default `None`): OCR settings, DeepSeek cloud, GPU, crop mode. Falls back to defaults.
* `file_conf` (`Optional[FileConfig]`, default `None`): virtual storage, response to file, automatic file editing and deletion. Falls back to defaults.
* `safety_conf` (`Optional[SafetyConfig]`, default `None`): content safety (profanity filter, anonymization). Falls back to defaults.

---

## Configuration dataclasses

### `ModelConfig`

* `preferences_in_ai` (`str`, default `"deepseek"`): preferred multilingual model family. Allowed values: `deepseek`, `qwen`, `minimax`, `code_llama`, `mellum`, `wizard`, `starcoder`, `yi_coder`, `codegemma`, `devstral`, `granite`, `codestral`, `codegeex4`, `opencode_interpreter`, `ornith_1_0`, `kat_dev`, `magistral_small`, `laguna_xs`, `breeze`.
* `models_dir` (`str`, default `"./models"`): directory to cache downloaded GGUF models.
* `type_computer` (`Optional[Literal["easy","middle","hard","very_hard"]]`, default `None`): predefined PC performance level for quantization selection. If `None`, auto detected via benchmark.
* `repo_id` (`Optional[str]`, default `None`): explicit Hugging Face repository ID. If `None`, automatic selection is used.
* `filename` (`Optional[str]`, default `None`): model filename inside the repository (used with `repo_id`).
* `your_token_for_hf` (`Optional[str]`, default `None`): Hugging Face access token for private or gated models.
* `subdomain` (`str`, default `""`): optional prefix added to the model filename during download.
* `retries` (`int`, default `5`, constant `NUMBER_ATTEMPTS`): number of download attempts on error.
* `prefer_mirror` (`bool`, default `True`): use Hugging Face mirror (`hf-mirror.com`) for downloads.

### `LLMConfig`

* `verbose` (`bool`, default `False`): enable verbose output from `llama-cpp-python`.
* `n_ctx` (`Optional[int]`, default `None`): context window size in tokens. `None` means model default.
* `n_gpu_layers` (`int`, default `0`): number of model layers offloaded to GPU. `0` means CPU only.
* `echo` (`bool`, default `False`): echo the prompt in the response (legacy string mode).
* `max_tokens` (`int`, default `8192`, constant `MAX_TOKENS`): maximum tokens generated in the response.
* `temperature` (`float`, default `0.1`): sampling temperature (0.0 to 1.0).

### `PromptConfig`

* `main_prompt_mode` (`Literal["default","testing","explanation","no_comments","refactor","debug","code_review","documentation","scaffold","security_hardening","algorithm_strategy"]`, default `"default"`): predefined system prompt scenario.
* `main_prompt` (`Optional[str]`, default `None`): custom system prompt. Overrides `main_prompt_mode`.
* `improving_user_experience` (`bool`, default `False`): rewrite the user request into a clear, structured prompt via a local small model before sending it to the primary AI.

### `TranslationConfig`

* `determinant_mode` (`Optional[Literal["lite","full","auto"]]`, default `"lite"`): natural language detection mode (passed to `fast_langdetect`).
* `accurate_translation` (`bool`, default `False`): use DeepL API (requires `your_key_for_deepl`) instead of Google Translate.
* `your_key_for_deepl` (`str`, default `""`): DeepL API key. Required if `accurate_translation=True`.
* `request_language` (`str`, default `"en"`, constant `MAIN_LANGUAGE`): target language code for translation.
* `local_trans` (`bool`, default `False`): use ArgosTranslate for fully offline translation.
* `from_code_lang` (`str`, default `""`): source language code for local translation (used only if `local_trans=True`).

### `LanguageDetectionConfig`

* `with_ai_orchestrator` (`bool`, default `True`): use an AI model to detect the programming language.
* `proprietary_algorithms` (`bool`, default `False`): use the built in keyword dictionary (only when `with_ai_orchestrator=False`).

### `ProxyConfig`

* `country` (`Optional[str]`, default `None`): country code (e.g., `"ru"`) for proxy filtering.
* `protocol` (`str`, default `"http"`): proxy protocol, `"http"` or `"https"`.
* `max_timeout` (`int`, default `1000`, constant `MAX_TIMEOUT`): max timeout in seconds for proxy availability checks.
* `is_working` (`bool`, default `True`): use only working (verified) proxies.
* `auto_proxies` (`bool`, default `True`): automatically enable proxy fallback when the primary host is unreachable.
* `your_proxies_dict` (`Optional[List[str]]`, default `None`): custom proxy list (e.g., `["192.168.1.1:8080"]`). Overrides automatic discovery.
* `min_timeout_for_checking_availability` (`int`, default `10`, constant `MIN_TIMEOUT_FOR_CHECK`): minimum timeout for connection checks.
* `max_timeout_for_checking_availability` (`int`, default `30`, constant `MAX_TIMEOUT_FOR_CHECK`): maximum timeout for connection checks.
* `github_proxies` (`bool`, default `False`): fetch proxy lists from raw GitHub URLs.
* `url_lst` (`List[str]`, default `PROXY_LINK_LST`): list of raw GitHub URLs with proxy lists.
* `proxy_retries` (`int`, default `5`, constant `NUMBER_ATTEMPTS`): attempts per URL when fetching proxies from GitHub.
* `main_retries` (`int`, default `10`, constant `MAIN_PROXY_ATTEMPTS`): retry cycles to obtain a working proxy.

### `OCRConfig`

* `lang_lst` (`Optional[List[str]]`, default `None`): language codes for EasyOCR (e.g., `["en","ru"]`).
* `use_gpu_for_ocr` (`bool`, default `False`): use GPU for OCR.
* `with_ocr` (`bool`, default `False`): enable OCR for images when scanning virtual storage.
* `cloud_version` (`bool`, default `False`): use DeepSeek cloud API instead of the local model.
* `definition_option` (`Literal["easy_ocr","deepseek_ocr"]`, default `"easy_ocr"`): choose the OCR engine.
* `model_size` (`Literal["tiny","small","base","large","gundam"]`, default `"tiny"`): size of the local DeepSeek OCR model.
* `crop_mode` (`bool`, default `False`): split large images into four parts for detailed recognition.
* `base_url` (`str`, default `"https://api.siliconflow.cn/v1/chat/completions"`): API endpoint for DeepSeek cloud.
* `api_key_for_deepseek_ocr` (`Optional[str]`, default `None`): API key for DeepSeek cloud.
* `timeout_for_deepseek_ocr` (`Optional[int]`, default `None`): timeout in seconds for DeepSeek cloud requests.
* `max_rate_limit_retries` (`Optional[int]`, default `5`, constant `NUMBER_ATTEMPTS`): retries on rate limit errors.

### `FileConfig`

* `virtual_storage` (`bool`, default `False`): enable virtual storage mode and scan `virtual_storage_path`.
* `virtual_storage_path` (`Optional[str]`, default `None`): root folder for virtual storage.
* `writing_response_to_file` (`bool`, default `False`): save the AI response to a timestamped text file.
* `editing_files` (`bool`, default `False`): enable automatic file editing via JSON generation.
* `deleting_files` (`bool`, default `False`): enable automatic file deletion via AI. Works together with `editing_files=True`.
* `use_websites` (`bool`, default `False`): fetch text from websites listed in `websites_sources_information` and add it to the request context.
* `websites_sources_information` (`Optional[List[str]]`, default `None`): list of URLs to scrape as additional context.
* `compress_text` (`bool`, default `False`): compress the assembled file context with a local small model to reduce token usage.
* `ignored_files` (`Optional[List[str]]`, default `None`): files or paths that should be skipped when reading a virtual storage folder.

### `SafetyConfig`

* `filter_for_swearing` (`bool`, default `False`): enable profanity filter, returning a predefined safe response if triggered.
* `anonymize_text` (`bool`, default `False`): anonymize the user request with Microsoft Presidio before sending it to translation services or AI models.

---

## Example usage

```python
from BiNeuron import BiNeuron
from BiNeuron.data.configs import (
    ModelConfig, LLMConfig, PromptConfig, TranslationConfig,
    LanguageDetectionConfig, ProxyConfig, OCRConfig, FileConfig, SafetyConfig,
)

agent = BiNeuron(
    request="Write a Python function to compute factorial.",
    additional_files=None,
    model_conf=ModelConfig(preferences_in_ai="qwen", prefer_mirror=True),
    llm_conf=LLMConfig(max_tokens=2048, temperature=0.2),
    prompt_conf=PromptConfig(main_prompt_mode="default"),
    translation_conf=TranslationConfig(request_language="en"),
    safety_conf=SafetyConfig(filter_for_swearing=True),
)

print(agent.final_ai_request())
```

---

## Notes

* All constants (`MAX_TOKENS`, `NUMBER_ATTEMPTS`, `MAIN_LANGUAGE`, etc.) are defined in `BiNeuron.data.constants_for_functions`.
* Config dataclasses are defined in `BiNeuron.data.configs`.
* Language specific and multilingual model mappings live in `BiNeuron.data.models_for_programming_languages` and `BiNeuron.data.models_and_file_names`.
* Logging is configured by `main_logger.py`. Errors are written to `errors.log`.

</details>

<details>
<summary>🇷🇺 Русский</summary>

## Обзор

`BiNeuron` это главный класс пакета **biNeuron**. Он управляет всем процессом:

* **Определение языка**: определяет язык или языки программирования из запроса пользователя и прикреплённых файлов.
* **Выбор модели**: автоматически подбирает наилучшую GGUF модель (специализированную или мультиязычную) на основе определённого языка и производительности вашего компьютера.
* **Загрузка и кэширование**: скачивает выбранную модель с Hugging Face (с поддержкой прокси и зеркал).
* **Формирование промпта**: создаёт системную инструкцию в соответствии с выбранным сценарием (стандартный, тестирование, объяснение, рефакторинг и так далее).
* **Инференс ИИ**: отправляет запрос в загруженную LLM и возвращает ответ.
* **Редактирование файлов (опционально)**: если включено, ответ ИИ парсится и используется для прямого изменения файлов на диске.
* **Интерактивный чат**: поддерживает многошаговые диалоги с историей.

> **Обратите внимание (breaking change):** начиная с текущей версии `BiNeuron` больше не принимает десятки плоских именованных аргументов.  
> Вместо этого все опции сгруппированы в **dataclass классы** (`ModelConfig`, `LLMConfig`, `PromptConfig`, `TranslationConfig`, `LanguageDetectionConfig`, `ProxyConfig`, `OCRConfig`, `FileConfig`, `SafetyConfig`) из `BiNeuron.data.configs`.  
> Передавайте любое подмножество; отсутствующие конфиги получают безопасные значения по умолчанию.

---

## Конструктор

```python
BiNeuron(
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
    safety_conf: Optional[SafetyConfig] = None,
) -> None
```

Параметры:

* `request` (`str`, **обязательный**): основной запрос пользователя (вопрос, описание задачи или код).
* `additional_files` (`Optional[List[str]]`, по умолчанию `None`): список путей к файлам, содержимое которых добавляется как контекст.
* `model_conf` (`Optional[ModelConfig]`, по умолчанию `None`): выбор модели, репозиторий и файл, папка кэша, HF токен, зеркало. При `None` используются значения по умолчанию.
* `llm_conf` (`Optional[LLMConfig]`, по умолчанию `None`): параметры генерации LLM (temperature, max_tokens, n_ctx, GPU слои). При `None` используются значения по умолчанию.
* `prompt_conf` (`Optional[PromptConfig]`, по умолчанию `None`): режим системного промпта и или кастомный системный промпт. При `None` используются значения по умолчанию.
* `translation_conf` (`Optional[TranslationConfig]`, по умолчанию `None`): настройки перевода и определения языка, ключ DeepL, локальный перевод. При `None` используются значения по умолчанию.
* `language_detection_conf` (`Optional[LanguageDetectionConfig]`, по умолчанию `None`): определение языка программирования (ИИ оркестратор или эвристики). При `None` используются значения по умолчанию.
* `proxy_conf` (`Optional[ProxyConfig]`, по умолчанию `None`): прокси, таймауты, повторы, GitHub списки прокси. При `None` используются значения по умолчанию.
* `ocr_conf` (`Optional[OCRConfig]`, по умолчанию `None`): OCR, облачный DeepSeek, GPU, crop режим. При `None` используются значения по умолчанию.
* `file_conf` (`Optional[FileConfig]`, по умолчанию `None`): виртуальное хранилище, запись ответа в файл, авто редактирование и удаление файлов. При `None` используются значения по умолчанию.
* `safety_conf` (`Optional[SafetyConfig]`, по умолчанию `None`): безопасность контента (фильтр мата, анонимизация). При `None` используются значения по умолчанию.

---

## Dataclass конфигурации

### `ModelConfig`

* `preferences_in_ai` (`str`, по умолчанию `"deepseek"`): предпочитаемое семейство мультиязычных моделей. Допустимые значения: `deepseek`, `qwen`, `minimax`, `code_llama`, `mellum`, `wizard`, `starcoder`, `yi_coder`, `codegemma`, `devstral`, `granite`, `codestral`, `codegeex4`, `opencode_interpreter`, `ornith_1_0`, `kat_dev`, `magistral_small`, `laguna_xs`, `breeze`.
* `models_dir` (`str`, по умолчанию `"./models"`): директория кэша GGUF моделей.
* `type_computer` (`Optional[Literal["easy","middle","hard","very_hard"]]`, по умолчанию `None`): уровень производительности ПК. Если `None`, определяется автоматически через бенчмарк.
* `repo_id` (`Optional[str]`, по умолчанию `None`): явный Hugging Face repo ID. Если `None`, используется авто выбор.
* `filename` (`Optional[str]`, по умолчанию `None`): имя файла модели в репозитории (используется с `repo_id`).
* `your_token_for_hf` (`Optional[str]`, по умолчанию `None`): HF токен для приватных или gated моделей.
* `subdomain` (`str`, по умолчанию `""`): префикс к имени файла модели при скачивании.
* `retries` (`int`, по умолчанию `5`, константа `NUMBER_ATTEMPTS`): число попыток скачивания при ошибке.
* `prefer_mirror` (`bool`, по умолчанию `True`): использовать зеркало HF (`hf-mirror.com`).

### `LLMConfig`

* `verbose` (`bool`, по умолчанию `False`): подробный вывод `llama-cpp-python`.
* `n_ctx` (`Optional[int]`, по умолчанию `None`): размер контекстного окна в токенах. `None` означает значение модели.
* `n_gpu_layers` (`int`, по умолчанию `0`): количество слоёв на GPU. `0` означает только CPU.
* `echo` (`bool`, по умолчанию `False`): эхо промпта в ответе (устаревший строковый режим).
* `max_tokens` (`int`, по умолчанию `8192`, константа `MAX_TOKENS`): максимум токенов в ответе.
* `temperature` (`float`, по умолчанию `0.1`): температура выборки (от 0.0 до 1.0).

### `PromptConfig`

* `main_prompt_mode` (`Literal["default","testing","explanation","no_comments","refactor","debug","code_review","documentation","scaffold","security_hardening","algorithm_strategy"]`, по умолчанию `"default"`): предустановленный сценарий системного промпта.
* `main_prompt` (`Optional[str]`, по умолчанию `None`): кастомный системный промпт. Перекрывает `main_prompt_mode`.
* `improving_user_experience` (`bool`, по умолчанию `False`): переписывать запрос пользователя в чёткий структурированный промпт через локальную малую модель перед отправкой основной ИИ.

### `TranslationConfig`

* `determinant_mode` (`Optional[Literal["lite","full","auto"]]`, по умолчанию `"lite"`): режим определения языка (передаётся в `fast_langdetect`).
* `accurate_translation` (`bool`, по умолчанию `False`): использовать DeepL (нужен `your_key_for_deepl`) вместо Google Translate.
* `your_key_for_deepl` (`str`, по умолчанию `""`): ключ DeepL. Обязателен при `accurate_translation=True`.
* `request_language` (`str`, по умолчанию `"en"`, константа `MAIN_LANGUAGE`): целевой язык перевода.
* `local_trans` (`bool`, по умолчанию `False`): полностью офлайн перевод через ArgosTranslate.
* `from_code_lang` (`str`, по умолчанию `""`): исходный язык для локального перевода (только при `local_trans=True`).

### `LanguageDetectionConfig`

* `with_ai_orchestrator` (`bool`, по умолчанию `True`): использовать ИИ модель для определения языка программирования.
* `proprietary_algorithms` (`bool`, по умолчанию `False`): использовать встроенный словарь ключевых слов (только при `with_ai_orchestrator=False`).

### `ProxyConfig`

* `country` (`Optional[str]`, по умолчанию `None`): код страны для фильтрации прокси.
* `protocol` (`str`, по умолчанию `"http"`): протокол прокси, `"http"` или `"https"`.
* `max_timeout` (`int`, по умолчанию `1000`, константа `MAX_TIMEOUT`): максимальный таймаут проверки прокси в секундах.
* `is_working` (`bool`, по умолчанию `True`): только рабочие проверенные прокси.
* `auto_proxies` (`bool`, по умолчанию `True`): автоматически включать прокси фолбэк, когда основной хост недоступен.
* `your_proxies_dict` (`Optional[List[str]]`, по умолчанию `None`): пользовательский список прокси (например `["192.168.1.1:8080"]`). Переопределяет авто обнаружение.
* `min_timeout_for_checking_availability` (`int`, по умолчанию `10`, константа `MIN_TIMEOUT_FOR_CHECK`): минимальный таймаут проверки соединения.
* `max_timeout_for_checking_availability` (`int`, по умолчанию `30`, константа `MAX_TIMEOUT_FOR_CHECK`): максимальный таймаут проверки соединения.
* `github_proxies` (`bool`, по умолчанию `False`): брать прокси со списков на GitHub raw.
* `url_lst` (`List[str]`, по умолчанию `PROXY_LINK_LST`): список raw URL GitHub со списками прокси.
* `proxy_retries` (`int`, по умолчанию `5`, константа `NUMBER_ATTEMPTS`): попыток на URL при получении прокси с GitHub.
* `main_retries` (`int`, по умолчанию `10`, константа `MAIN_PROXY_ATTEMPTS`): циклов повторного получения рабочего прокси.

### `OCRConfig`

* `lang_lst` (`Optional[List[str]]`, по умолчанию `None`): языковые коды для EasyOCR.
* `use_gpu_for_ocr` (`bool`, по умолчанию `False`): использовать GPU для OCR.
* `with_ocr` (`bool`, по умолчанию `False`): OCR для изображений при сканировании виртуального хранилища.
* `cloud_version` (`bool`, по умолчанию `False`): облачный API DeepSeek вместо локальной модели.
* `definition_option` (`Literal["easy_ocr","deepseek_ocr"]`, по умолчанию `"easy_ocr"`): выбор OCR движка.
* `model_size` (`Literal["tiny","small","base","large","gundam"]`, по умолчанию `"tiny"`): размер локальной модели DeepSeek OCR.
* `crop_mode` (`bool`, по умолчанию `False`): разбивать большие изображения на четыре части.
* `base_url` (`str`, по умолчанию `"https://api.siliconflow.cn/v1/chat/completions"`): API эндпоинт облачного DeepSeek.
* `api_key_for_deepseek_ocr` (`Optional[str]`, по умолчанию `None`): API ключ облачного DeepSeek.
* `timeout_for_deepseek_ocr` (`Optional[int]`, по умолчанию `None`): таймаут запросов к облачному DeepSeek в секундах.
* `max_rate_limit_retries` (`Optional[int]`, по умолчанию `5`, константа `NUMBER_ATTEMPTS`): повторы при rate limit.

### `FileConfig`

* `virtual_storage` (`bool`, по умолчанию `False`): режим виртуального хранилища, сканировать `virtual_storage_path`.
* `virtual_storage_path` (`Optional[str]`, по умолчанию `None`): корневая папка виртуального хранилища.
* `writing_response_to_file` (`bool`, по умолчанию `False`): сохранять ответ ИИ в текстовый файл с меткой времени.
* `editing_files` (`bool`, по умолчанию `False`): авто редактирование файлов через JSON.
* `deleting_files` (`bool`, по умолчанию `False`): авто удаление файлов через ИИ. Работает совместно с `editing_files=True`.
* `use_websites` (`bool`, по умолчанию `False`): загружать текст с сайтов из `websites_sources_information` и добавлять в контекст запроса.
* `websites_sources_information` (`Optional[List[str]]`, по умолчанию `None`): список URL для скрапинга как дополнительный контекст.
* `compress_text` (`bool`, по умолчанию `False`): сжимать собранный контекст файлов через локальную малую модель для экономии токенов.
* `ignored_files` (`Optional[List[str]]`, по умолчанию `None`): файлы или пути, которые нужно пропускать при чтении папки виртуального хранилища.

### `SafetyConfig`

* `filter_for_swearing` (`bool`, по умолчанию `False`): фильтр ненормативной лексики, возвращает безопасный ответ при срабатывании.
* `anonymize_text` (`bool`, по умолчанию `False`): анонимизировать запрос пользователя через Microsoft Presidio перед отправкой в сервисы перевода или ИИ модели.

---

## Пример использования

```python
from BiNeuron import BiNeuron
from BiNeuron.data.configs import (
    ModelConfig, LLMConfig, PromptConfig, TranslationConfig,
    LanguageDetectionConfig, ProxyConfig, OCRConfig, FileConfig, SafetyConfig,
)

agent = BiNeuron(
    request="Напиши функцию Python для вычисления факториала.",
    additional_files=None,
    model_conf=ModelConfig(preferences_in_ai="qwen", prefer_mirror=True),
    llm_conf=LLMConfig(max_tokens=2048, temperature=0.2),
    prompt_conf=PromptConfig(main_prompt_mode="default"),
    translation_conf=TranslationConfig(request_language="en"),
    safety_conf=SafetyConfig(filter_for_swearing=True),
)

print(agent.final_ai_request())
```

---

## Примечания

* Все константы (`MAX_TOKENS`, `NUMBER_ATTEMPTS`, `MAIN_LANGUAGE` и другие) находятся в `BiNeuron.data.constants_for_functions`.
* Dataclass конфиги находятся в `BiNeuron.data.configs`.
* Модели для языков и уровней производительности находятся в `BiNeuron.data.models_for_programming_languages` и `BiNeuron.data.models_and_file_names`.
* Логирование настраивается в `main_logger.py`. Ошибки пишутся в `errors.log`.

</details>

<details>
<summary>🇨🇳 中文</summary>

## 概述

`BiNeuron` 是 **biNeuron** 包的主类。它协调整个工作流程：

* **语言检测**：从用户请求和附加文件中确定编程语言。
* **模型选择**：根据检测到的语言和计算机性能，自动选择最合适的 GGUF 模型（特定语言或多语言）。
* **下载与缓存**：从 Hugging Face 下载所选模型（支持代理和镜像）。
* **提示词工程**：根据所需场景（默认、测试、解释、重构等）构建系统提示。
* **AI 推理**：将请求发送给已加载的大语言模型并返回响应。
* **文件编辑（可选）**：如果启用，将解析 AI 响应并直接用于修改磁盘上的文件。
* **交互式聊天**：支持带历史记录的多轮对话。

> **注意（破坏性变更）：** 从当前版本起，`BiNeuron` 不再接受大量扁平化的关键字参数。  
> 所有选项被分组到 **dataclass 配置类** 中（`ModelConfig`、`LLMConfig`、`PromptConfig`、`TranslationConfig`、`LanguageDetectionConfig`、`ProxyConfig`、`OCRConfig`、`FileConfig`、`SafetyConfig`），定义于 `BiNeuron.data.configs`。  
> 可只传入部分配置；未传入的将使用安全默认值。

---

## 构造函数

```python
BiNeuron(
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
    safety_conf: Optional[SafetyConfig] = None,
) -> None
```

参数：

* `request` (`str`，**必需**)：用户的输入文本（问题、代码描述或任务）。
* `additional_files` (`Optional[List[str]]`，默认 `None`)：文件路径列表，其内容将作为上下文提供给 AI。
* `model_conf` (`Optional[ModelConfig]`，默认 `None`)：模型选择、仓库、文件名、缓存目录、HF 令牌、镜像偏好。若为 `None` 则使用默认值。
* `llm_conf` (`Optional[LLMConfig]`，默认 `None`)：LLM 生成参数（temperature、max_tokens、n_ctx、GPU 层数）。若为 `None` 则使用默认值。
* `prompt_conf` (`Optional[PromptConfig]`，默认 `None`)：系统提示模式及或自定义系统提示。若为 `None` 则使用默认值。
* `translation_conf` (`Optional[TranslationConfig]`，默认 `None`)：翻译和语言检测、DeepL 密钥、本地翻译。若为 `None` 则使用默认值。
* `language_detection_conf` (`Optional[LanguageDetectionConfig]`，默认 `None`)：编程语言检测（AI 编排器或启发式）。若为 `None` 则使用默认值。
* `proxy_conf` (`Optional[ProxyConfig]`，默认 `None`)：代理、超时、重试、GitHub 代理列表。若为 `None` 则使用默认值。
* `ocr_conf` (`Optional[OCRConfig]`，默认 `None`)：OCR、DeepSeek 云、GPU、裁剪模式。若为 `None` 则使用默认值。
* `file_conf` (`Optional[FileConfig]`，默认 `None`)：虚拟存储、回复写入文件、自动编辑和删除文件。若为 `None` 则使用默认值。
* `safety_conf` (`Optional[SafetyConfig]`，默认 `None`)：内容安全（脏话过滤、匿名化）。若为 `None` 则使用默认值。

---

## 配置 dataclass

### `ModelConfig`

* `preferences_in_ai` (`str`，默认 `"deepseek"`)：首选多语言模型系列。允许值：`deepseek`、`qwen`、`minimax`、`code_llama`、`mellum`、`wizard`、`starcoder`、`yi_coder`、`codegemma`、`devstral`、`granite`、`codestral`、`codegeex4`、`opencode_interpreter`、`ornith_1_0`、`kat_dev`、`magistral_small`、`laguna_xs`、`breeze`。
* `models_dir` (`str`，默认 `"./models"`)：GGUF 模型缓存目录。
* `type_computer` (`Optional[Literal["easy","middle","hard","very_hard"]]`，默认 `None`)：预定义计算机性能级别。若为 `None` 则通过基准测试自动检测。
* `repo_id` (`Optional[str]`，默认 `None`)：显式 Hugging Face 仓库 ID。若为 `None` 则自动选择。
* `filename` (`Optional[str]`，默认 `None`)：仓库内的模型文件名（与 `repo_id` 一起使用）。
* `your_token_for_hf` (`Optional[str]`，默认 `None`)：用于私有或受限模型的 HF 访问令牌。
* `subdomain` (`str`，默认 `""`)：下载时添加到模型文件名前的可选前缀。
* `retries` (`int`，默认 `5`，常量 `NUMBER_ATTEMPTS`)：出错时的下载尝试次数。
* `prefer_mirror` (`bool`，默认 `True`)：使用 HF 镜像（`hf-mirror.com`）。

### `LLMConfig`

* `verbose` (`bool`，默认 `False`)：启用 `llama-cpp-python` 详细输出。
* `n_ctx` (`Optional[int]`，默认 `None`)：上下文窗口大小（token）。`None` 表示模型默认。
* `n_gpu_layers` (`int`，默认 `0`)：卸载到 GPU 的层数。`0` 表示仅 CPU。
* `echo` (`bool`，默认 `False`)：在响应中回显提示（遗留字符串模式）。
* `max_tokens` (`int`，默认 `8192`，常量 `MAX_TOKENS`)：响应中生成的最大 token 数。
* `temperature` (`float`，默认 `0.1`)：采样温度（0.0 到 1.0）。

### `PromptConfig`

* `main_prompt_mode` (`Literal["default","testing","explanation","no_comments","refactor","debug","code_review","documentation","scaffold","security_hardening","algorithm_strategy"]`，默认 `"default"`)：预定义的系统提示场景。
* `main_prompt` (`Optional[str]`，默认 `None`)：自定义系统提示。覆盖 `main_prompt_mode`。
* `improving_user_experience` (`bool`，默认 `False`)：在发送给主 AI 之前，通过本地小型模型将用户请求重写为清晰、结构化的提示。

### `TranslationConfig`

* `determinant_mode` (`Optional[Literal["lite","full","auto"]]`，默认 `"lite"`)：自然语言检测模式（传递给 `fast_langdetect`）。
* `accurate_translation` (`bool`，默认 `False`)：使用 DeepL API（需要 `your_key_for_deepl`）而不是 Google Translate。
* `your_key_for_deepl` (`str`，默认 `""`)：DeepL API 密钥。若 `accurate_translation=True` 则必需。
* `request_language` (`str`，默认 `"en"`，常量 `MAIN_LANGUAGE`)：翻译目标语言代码。
* `local_trans` (`bool`，默认 `False`)：使用 ArgosTranslate 进行完全离线翻译。
* `from_code_lang` (`str`，默认 `""`)：本地翻译的源语言代码（仅当 `local_trans=True` 时使用）。

### `LanguageDetectionConfig`

* `with_ai_orchestrator` (`bool`，默认 `True`)：使用 AI 模型检测编程语言。
* `proprietary_algorithms` (`bool`，默认 `False`)：使用内置关键词词典（仅当 `with_ai_orchestrator=False` 时）。

### `ProxyConfig`

* `country` (`Optional[str]`，默认 `None`)：用于代理过滤的国家代码（例如 `"ru"`）。
* `protocol` (`str`，默认 `"http"`)：代理协议，`"http"` 或 `"https"`。
* `max_timeout` (`int`，默认 `1000`，常量 `MAX_TIMEOUT`)：代理可用性检查的最大超时时间（秒）。
* `is_working` (`bool`，默认 `True`)：仅使用有效的（已验证的）代理。
* `auto_proxies` (`bool`，默认 `True`)：当主主机不可达时自动启用代理回退。
* `your_proxies_dict` (`Optional[List[str]]`，默认 `None`)：自定义代理列表（例如 `["192.168.1.1:8080"]`）。覆盖自动发现。
* `min_timeout_for_checking_availability` (`int`，默认 `10`，常量 `MIN_TIMEOUT_FOR_CHECK`)：连接检查的最小超时时间（秒）。
* `max_timeout_for_checking_availability` (`int`，默认 `30`，常量 `MAX_TIMEOUT_FOR_CHECK`)：连接检查的最大超时时间（秒）。
* `github_proxies` (`bool`，默认 `False`)：从 GitHub raw URL 获取代理列表。
* `url_lst` (`List[str]`，默认 `PROXY_LINK_LST`)：包含代理列表的 GitHub raw URL 列表。
* `proxy_retries` (`int`，默认 `5`，常量 `NUMBER_ATTEMPTS`)：从 GitHub 获取代理时每个 URL 的尝试次数。
* `main_retries` (`int`，默认 `10`，常量 `MAIN_PROXY_ATTEMPTS`)：获取有效代理的重试周期数。

### `OCRConfig`

* `lang_lst` (`Optional[List[str]]`，默认 `None`)：EasyOCR 的语言代码列表。
* `use_gpu_for_ocr` (`bool`，默认 `False`)：对 OCR 使用 GPU。
* `with_ocr` (`bool`，默认 `False`)：扫描虚拟存储时为图像启用 OCR。
* `cloud_version` (`bool`，默认 `False`)：使用 DeepSeek 云 API 而不是本地模型。
* `definition_option` (`Literal["easy_ocr","deepseek_ocr"]`，默认 `"easy_ocr"`)：选择 OCR 引擎。
* `model_size` (`Literal["tiny","small","base","large","gundam"]`，默认 `"tiny"`)：本地 DeepSeek OCR 模型的大小。
* `crop_mode` (`bool`，默认 `False`)：将大图像分割成四部分以进行更详细的识别。
* `base_url` (`str`，默认 `"https://api.siliconflow.cn/v1/chat/completions"`)：DeepSeek 云的 API 端点。
* `api_key_for_deepseek_ocr` (`Optional[str]`，默认 `None`)：DeepSeek 云的 API 密钥。
* `timeout_for_deepseek_ocr` (`Optional[int]`，默认 `None`)：DeepSeek 云请求的超时时间（秒）。
* `max_rate_limit_retries` (`Optional[int]`，默认 `5`，常量 `NUMBER_ATTEMPTS`)：遇到速率限制错误时的重试次数。

### `FileConfig`

* `virtual_storage` (`bool`，默认 `False`)：启用虚拟存储模式，扫描 `virtual_storage_path`。
* `virtual_storage_path` (`Optional[str]`，默认 `None`)：虚拟存储的根文件夹路径。
* `writing_response_to_file` (`bool`，默认 `False`)：将 AI 响应保存到带时间戳的文本文件。
* `editing_files` (`bool`，默认 `False`)：启用通过 JSON 生成的自动文件编辑。
* `deleting_files` (`bool`，默认 `False`)：启用通过 AI 的自动文件删除。与 `editing_files=True` 一起使用。
* `use_websites` (`bool`，默认 `False`)：从 `websites_sources_information` 中列出的网站抓取文本并添加到请求上下文。
* `websites_sources_information` (`Optional[List[str]]`，默认 `None`)：作为附加上下文抓取的 URL 列表。
* `compress_text` (`bool`，默认 `False`)：使用本地小型模型压缩组装的上下文，减少 token 使用。
* `ignored_files` (`Optional[List[str]]`，默认 `None`)：读取虚拟存储文件夹时应跳过的文件或路径。

### `SafetyConfig`

* `filter_for_swearing` (`bool`，默认 `False`)：启用脏话过滤，触发时返回预定义的安全响应。
* `anonymize_text` (`bool`，默认 `False`)：在发送到翻译服务或 AI 模型之前，使用 Microsoft Presidio 匿名化用户请求。

---

## 使用示例

```python
from BiNeuron import BiNeuron
from BiNeuron.data.configs import (
    ModelConfig, LLMConfig, PromptConfig, TranslationConfig,
    LanguageDetectionConfig, ProxyConfig, OCRConfig, FileConfig, SafetyConfig,
)

agent = BiNeuron(
    request="用 Python 写一个计算阶乘的函数。",
    additional_files=None,
    model_conf=ModelConfig(preferences_in_ai="qwen", prefer_mirror=True),
    llm_conf=LLMConfig(max_tokens=2048, temperature=0.2),
    prompt_conf=PromptConfig(main_prompt_mode="default"),
    translation_conf=TranslationConfig(request_language="en"),
    safety_conf=SafetyConfig(filter_for_swearing=True),
)

print(agent.final_ai_request())
```

---

## 备注

* 所有常量（例如 `MAX_TOKENS`、`NUMBER_ATTEMPTS`、`MAIN_LANGUAGE`）均在 `BiNeuron.data.constants_for_functions` 中定义。
* 配置 dataclass 定义于 `BiNeuron.data.configs`。
* 特定语言和多语言模型的映射存储在 `BiNeuron.data.models_for_programming_languages` 和 `BiNeuron.data.models_and_file_names` 中。
* 日志记录由 `main_logger.py` 配置。错误写入 `errors.log`。

</details>