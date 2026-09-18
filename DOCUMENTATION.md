<details>
<summary>🇬🇧 English</summary>

## Overview

`BiNeuron` is the main class of the **biNeuron** package. It orchestrates the entire workflow:

- **Language detection** - determines the programming language(s) from the user request and attached files.
- **Model selection** - automatically picks the best-suited GGUF model (language-specific or multilingual) based on the detected language and your computer’s performance.
- **Download & caching** - downloads the selected model from Hugging Face (with proxy/mirror support).
- **Prompt engineering** - builds a system prompt according to the desired scenario (default, testing, explanation, refactoring, etc.).
- **AI inference** - sends the request to the loaded LLM and returns the response.
- **File editing (optional)** - if enabled, the AI response is parsed and used to directly edit files on disk.
- **Interactive chat** - supports multi-turn conversations with history.

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

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `request` | `str` | **required** | The user’s input text (question, code description, or task). |
| `additional_files` | `Optional[List[str]]` | `None` | List of file paths whose content is included as context for the AI. |
| `model_conf` | `Optional[ModelConfig]` | `None` → defaults | Model selection, repo/filename, cache dir, HF token, mirror preference. |
| `llm_conf` | `Optional[LLMConfig]` | `None` → defaults | LLM generation parameters (temperature, max_tokens, n_ctx, GPU layers). |
| `prompt_conf` | `Optional[PromptConfig]` | `None` → defaults | System prompt mode and/or custom system prompt. |
| `translation_conf` | `Optional[TranslationConfig]` | `None` → defaults | Translation / language detection settings, DeepL key, local translation. |
| `language_detection_conf` | `Optional[LanguageDetectionConfig]` | `None` → defaults | Programming language detection (AI orchestrator or heuristics). |
| `proxy_conf` | `Optional[ProxyConfig]` | `None` → defaults | Proxy usage, timeouts, retries, GitHub proxy list. |
| `ocr_conf` | `Optional[OCRConfig]` | `None` → defaults | OCR settings, DeepSeek cloud, GPU, crop mode. |
| `file_conf` | `Optional[FileConfig]` | `None` → defaults | Virtual storage, response-to-file, automatic file editing / deletion. |
| `safety_conf` | `Optional[SafetyConfig]` | `None` → defaults | Content safety (profanity filter). |

---

## Configuration dataclasses

### `ModelConfig`

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `preferences_in_ai` | `str` | `"deepseek"` | Preferred multilingual model family (`deepseek`, `qwen`, `minimax`, `code_llama`, `mellum`, `wizard`, `starcoder`, `yi_coder`, `codegemma`, `devstral`, `granite`, `codestral`, `codegeex4`, `opencode_interpreter`, `ornith_1_0`, `kat_dev`, `magistral_small`, `laguna_xs`, `breeze`). |
| `models_dir` | `str` | `"./models"` | Directory to cache downloaded GGUF models. |
| `type_computer` | `Optional[Literal["easy","middle","hard","very_hard"]]` | `None` | Predefined PC performance level for quantization selection. If `None`, auto-detected via benchmark. |
| `repo_id` | `Optional[str]` | `None` | Explicit Hugging Face repository ID. If `None`, automatic selection is used. |
| `filename` | `Optional[str]` | `None` | Model filename inside the repository (used with `repo_id`). |
| `your_token_for_hf` | `Optional[str]` | `None` | Hugging Face access token for private/gated models. |
| `subdomain` | `str` | `""` | Optional prefix added to the model filename during download. |
| `retries` | `int` | `5` (`NUMBER_ATTEMPTS`) | Number of download attempts on error. |
| `prefer_mirror` | `bool` | `True` | Use Hugging Face mirror (`hf-mirror.com`) for downloads. |

### `LLMConfig`

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `verbose` | `bool` | `False` | Enable verbose output from `llama-cpp-python`. |
| `n_ctx` | `Optional[int]` | `None` | Context window size in tokens. `None` = model default. |
| `n_gpu_layers` | `int` | `0` | Number of model layers offloaded to GPU (`0` = CPU only). |
| `echo` | `bool` | `False` | Echo the prompt in the response (legacy string mode). |
| `max_tokens` | `int` | `8192` (`MAX_TOKENS`) | Maximum tokens generated in the response. |
| `temperature` | `float` | `0.1` | Sampling temperature (0.0–1.0). |

### `PromptConfig`

| Field | Type | Default | Description                                          |
|-------|------|---------|------------------------------------------------------|
| `main_prompt_mode` | `Literal["default","testing","explanation","no_comments","refactor","debug","code_review","documentation","scaffold","security_hardening","algorithm_strategy"]` | `"default"` | Predefined system prompt scenario.                   |
| `main_prompt` | `Optional[str]` | `None` | Custom system prompt - overrides `main_prompt_mode`. |

### `TranslationConfig`

| Field | Type | Default | Description                                                                   |
|-------|------|---------|-------------------------------------------------------------------------------|
| `determinant_mode` | `Optional[Literal["lite","full","auto"]]` | `"lite"` | Natural language detection mode (passed to `fast_langdetect`).                |
| `accurate_translation` | `bool` | `False` | Use DeepL API (requires `your_key_for_deepl`) instead of Google Translate.    |
| `your_key_for_deepl` | `str` | `""` | DeepL API key - required if `accurate_translation=True`.                      |
| `request_language` | `str` | `"en"` (`MAIN_LANGUAGE`) | Target language code for translation.                                         |
| `local_trans` | `bool` | `False` | Use ArgosTranslate for fully offline translation.                             |
| `from_code_lang` | `str` | `""` | Source language code for local translation (used only if `local_trans=True`). |

### `LanguageDetectionConfig`

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `with_ai_orchestrator` | `bool` | `True` | Use an AI model to detect the programming language. |
| `proprietary_algorithms` | `bool` | `False` | Use the built-in keyword dictionary (only when `with_ai_orchestrator=False`). |

### `ProxyConfig`

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `country` | `Optional[str]` | `None` | Country code (e.g., `"ru"`) for proxy filtering. |
| `protocol` | `str` | `"http"` | Proxy protocol (`"http"` or `"https"`). |
| `max_timeout` | `int` | `1000` (`MAX_TIMEOUT`) | Max timeout (seconds) for proxy availability checks. |
| `is_working` | `bool` | `True` | Use only working (verified) proxies. |
| `auto_proxies` | `bool` | `True` | Automatically enable proxy fallback when the primary host is unreachable. |
| `your_proxies_dict` | `Optional[List[str]]` | `None` | Custom proxy list (e.g., `["192.168.1.1:8080"]`). Overrides automatic discovery. |
| `min_timeout_for_checking_availability` | `int` | `10` (`MIN_TIMEOUT_FOR_CHECK`) | Minimum timeout for connection checks. |
| `max_timeout_for_checking_availability` | `int` | `30` (`MAX_TIMEOUT_FOR_CHECK`) | Maximum timeout for connection checks. |
| `github_proxies` | `bool` | `False` | Fetch proxy lists from raw GitHub URLs. |
| `url_lst` | `List[str]` | `PROXY_LINK_LST` | List of raw GitHub URLs with proxy lists. |
| `proxy_retries` | `int` | `5` (`NUMBER_ATTEMPTS`) | Attempts per URL when fetching proxies from GitHub. |
| `main_retries` | `int` | `10` (`MAIN_PROXY_ATTEMPTS`) | Retry cycles to obtain a working proxy. |

### `OCRConfig`

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `lang_lst` | `Optional[List[str]]` | `None` | Language codes for EasyOCR (e.g., `["en","ru"]`). |
| `use_gpu_for_ocr` | `bool` | `False` | Use GPU for OCR. |
| `with_ocr` | `bool` | `False` | Enable OCR for images when scanning virtual storage. |
| `cloud_version` | `bool` | `False` | Use DeepSeek cloud API instead of the local model. |
| `with_deepseek` | `bool` | `True` | Use DeepSeek OCR; if `False`, fallback to EasyOCR. |
| `model_size` | `Literal["tiny","small","base","large","gundam"]` | `"tiny"` | Size of the local DeepSeek OCR model. |
| `crop_mode` | `bool` | `False` | Split large images into 4 parts for detailed recognition. |
| `base_url` | `str` | `"https://api.siliconflow.cn/v1/chat/completions"` | API endpoint for DeepSeek cloud. |
| `api_key_for_deepseek_ocr` | `Optional[str]` | `None` | API key for DeepSeek cloud. |
| `timeout_for_deepseek_ocr` | `Optional[int]` | `None` | Timeout (seconds) for DeepSeek cloud requests. |
| `max_rate_limit_retries` | `Optional[int]` | `5` (`NUMBER_ATTEMPTS`) | Retries on rate-limit errors. |

### `FileConfig`

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `virtual_storage` | `bool` | `False` | Enable virtual storage mode – scan `virtual_storage_path`. |
| `virtual_storage_path` | `Optional[str]` | `None` | Root folder for virtual storage. |
| `writing_response_to_file` | `bool` | `False` | Save the AI response to a timestamped text file. |
| `editing_files` | `bool` | `False` | Enable automatic file editing via JSON generation. |
| `deleting_files` | `bool` | `False` | Enable automatic file deletion via AI. Works with `editing_files=True`. |

### `SafetyConfig`

| Field | Type | Default | Description                                                                |
|-------|------|---------|----------------------------------------------------------------------------|
| `filter_for_swearing` | `bool` | `False` | Enable profanity filter - returns a predefined safe response if triggered. |

---

## Notes

- All constants (`MAX_TOKENS`, `NUMBER_ATTEMPTS`, `MAIN_LANGUAGE`, etc.) are defined in `BiNeuron.data.constants_for_functions`.
- Config dataclasses are defined in `BiNeuron.data.configs`.
- Language-specific and multilingual model mappings live in `BiNeuron.data.models_for_programming_languages` and `BiNeuron.data.models_and_file_names`.
- Logging is configured by `main_logger.py` - errors are written to `errors.log`.

</details>

<details>
<summary>🇷🇺 Русский</summary>

## Обзор

`BiNeuron` — главный класс пакета **biNeuron**. Он управляет всем процессом:

- **Определение языка** - определяет язык(и) программирования из запроса пользователя и прикреплённых файлов.
- **Выбор модели** - автоматически подбирает наилучшую GGUF-модель (специализированную или мультиязычную) на основе определённого языка и производительности вашего компьютера.
- **Загрузка и кэширование** - скачивает выбранную модель с Hugging Face (с поддержкой прокси и зеркал).
- **Формирование промпта** - создаёт системную инструкцию в соответствии с выбранным сценарием (стандартный, тестирование, объяснение, рефакторинг и т.д.).
- **Инференс ИИ** - отправляет запрос в загруженную LLM и возвращает ответ.
- **Редактирование файлов (опционально)** - если включено, ответ ИИ парсится и используется для прямого изменения файлов на диске.
- **Интерактивный чат** - поддерживает многошаговые диалоги с историей.

> **Обратите внимание (breaking change):** начиная с текущей версии `BiNeuron` больше не принимает десятки плоских именованных аргументов.  
> Вместо этого все опции сгруппированы в **dataclass-классы** (`ModelConfig`, `LLMConfig`, `PromptConfig`, `TranslationConfig`, `LanguageDetectionConfig`, `ProxyConfig`, `OCRConfig`, `FileConfig`, `SafetyConfig`) из `BiNeuron.data.configs`.  
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

| Параметр | Тип | По умолчанию | Описание |
|----------|-----|--------------|----------|
| `request` | `str` | **обязательный** | Основной запрос пользователя (вопрос, описание задачи или код). |
| `additional_files` | `Optional[List[str]]` | `None` | Список путей к файлам, содержимое которых добавляется как контекст. |
| `model_conf` | `Optional[ModelConfig]` | `None` → defaults | Выбор модели, репозиторий/файл, папка кэша, HF-токен, зеркало. |
| `llm_conf` | `Optional[LLMConfig]` | `None` → defaults | Параметры генерации LLM (temperature, max_tokens, n_ctx, GPU-слои). |
| `prompt_conf` | `Optional[PromptConfig]` | `None` → defaults | Режим системного промпта и/или кастомный системный промпт. |
| `translation_conf` | `Optional[TranslationConfig]` | `None` → defaults | Настройки перевода/определения языка, ключ DeepL, локальный перевод. |
| `language_detection_conf` | `Optional[LanguageDetectionConfig]` | `None` → defaults | Определение языка программирования (ИИ-оркестратор или эвристики). |
| `proxy_conf` | `Optional[ProxyConfig]` | `None` → defaults | Прокси, таймауты, повторы, GitHub-списки прокси. |
| `ocr_conf` | `Optional[OCRConfig]` | `None` → defaults | OCR, облачный DeepSeek, GPU, crop-режим. |
| `file_conf` | `Optional[FileConfig]` | `None` → defaults | Виртуальное хранилище, запись ответа в файл, авто-редактирование и удаление файлов. |
| `safety_conf` | `Optional[SafetyConfig]` | `None` → defaults | Безопасность контента (фильтр мата). |

---

## Dataclass-конфигурации

### `ModelConfig`

| Поле | Тип | По умолчанию | Описание                                                                                                                                                                                                                                                                                            |
|------|-----|--------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `preferences_in_ai` | `str` | `"deepseek"` | Предпочитаемое семейство мультиязычных моделей (`deepseek`, `qwen`, `minimax`, `code_llama`, `mellum`, `wizard`, `starcoder`, `yi_coder`, `codegemma`, `devstral`, `granite`, `codestral`, `codegeex4`, `opencode_interpreter`, `ornith_1_0`, `kat_dev`, `magistral_small`, `laguna_xs`, `breeze`). |
| `models_dir` | `str` | `"./models"` | Директория кэша GGUF-моделей.                                                                                                                                                                                                                                                                       |
| `type_computer` | `Optional[Literal["easy","middle","hard","very_hard"]]` | `None` | Уровень производительности ПК. Если `None` — авто-определение через бенчмарк.                                                                                                                                                                                                                       |
| `repo_id` | `Optional[str]` | `None` | Явный Hugging Face repo ID. Если `None` - авто-выбор.                                                                                                                                                                                                                                               |
| `filename` | `Optional[str]` | `None` | Имя файла модели в репозитории (используется с `repo_id`).                                                                                                                                                                                                                                          |
| `your_token_for_hf` | `Optional[str]` | `None` | HF-токен для приватных/gated-моделей.                                                                                                                                                                                                                                                               |
| `subdomain` | `str` | `""` | Префикс к имени файла модели при скачивании.                                                                                                                                                                                                                                                        |
| `retries` | `int` | `5` (`NUMBER_ATTEMPTS`) | Число попыток скачивания при ошибке.                                                                                                                                                                                                                                                                |
| `prefer_mirror` | `bool` | `True` | Использовать зеркало HF (`hf-mirror.com`).                                                                                                                                                                                                                                                          |

### `LLMConfig`

| Поле | Тип | По умолчанию | Описание                                                      |
|------|-----|--------------|---------------------------------------------------------------|
| `verbose` | `bool` | `False` | Подробный вывод `llama-cpp-python`.                           |
| `n_ctx` | `Optional[int]` | `None` | Размер контекстного окна в токенах. `None` = значение модели. |
| `n_gpu_layers` | `int` | `0` | Кол-во слоёв на GPU (`0` - только CPU).                       |
| `echo` | `bool` | `False` | Эхо-промпта в ответе (устаревший строковый режим).            |
| `max_tokens` | `int` | `8192` (`MAX_TOKENS`) | Максимум токенов в ответе.                                    |
| `temperature` | `float` | `0.1` | Температура выборки (0.0–1.0).                                |

### `PromptConfig`

| Поле | Тип | По умолчанию | Описание                                                     |
|------|-----|--------------|--------------------------------------------------------------|
| `main_prompt_mode` | `Literal["default","testing","explanation","no_comments","refactor","debug","code_review","documentation","scaffold","security_hardening","algorithm_strategy"]` | `"default"` | Предустановленный сценарий системного промпта.               |
| `main_prompt` | `Optional[str]` | `None` | Кастомный системный промпт - перекрывает `main_prompt_mode`. |

### `TranslationConfig`

| Поле | Тип | По умолчанию | Описание                                                                 |
|------|-----|--------------|--------------------------------------------------------------------------|
| `determinant_mode` | `Optional[Literal["lite","full","auto"]]` | `"lite"` | Режим определения языка (передаётся в `fast_langdetect`).                |
| `accurate_translation` | `bool` | `False` | Использовать DeepL (нужен `your_key_for_deepl`) вместо Google Translate. |
| `your_key_for_deepl` | `str` | `""` | Ключ DeepL - обязателен при `accurate_translation=True`.                 |
| `request_language` | `str` | `"en"` (`MAIN_LANGUAGE`) | Целевой язык перевода.                                                   |
| `local_trans` | `bool` | `False` | Полностью офлайн-перевод через ArgosTranslate.                           |
| `from_code_lang` | `str` | `""` | Исходный язык для локального перевода (только при `local_trans=True`).   |

### `LanguageDetectionConfig`

| Поле | Тип | По умолчанию | Описание |
|------|-----|--------------|----------|
| `with_ai_orchestrator` | `bool` | `True` | Использовать ИИ-модель для определения языка программирования. |
| `proprietary_algorithms` | `bool` | `False` | Использовать встроенный словарь ключевых слов (только при `with_ai_orchestrator=False`). |

### `ProxyConfig`

| Поле | Тип | По умолчанию | Описание |
|------|-----|--------------|----------|
| `country` | `Optional[str]` | `None` | Код страны для фильтрации прокси. |
| `protocol` | `str` | `"http"` | Протокол прокси (`"http"` или `"https"`). |
| `max_timeout` | `int` | `1000` (`MAX_TIMEOUT`) | Макс. таймаут проверки прокси (сек). |
| `is_working` | `bool` | `True` | Только рабочие прокси. |
| `auto_proxies` | `bool` | `True` | Автоматически включать прокси-фолбэк. |
| `your_proxies_dict` | `Optional[List[str]]` | `None` | Пользовательский список прокси. |
| `min_timeout_for_checking_availability` | `int` | `10` (`MIN_TIMEOUT_FOR_CHECK`) | Мин. таймаут проверки соединения. |
| `max_timeout_for_checking_availability` | `int` | `30` (`MAX_TIMEOUT_FOR_CHECK`) | Макс. таймаут проверки соединения. |
| `github_proxies` | `bool` | `False` | Брать прокси со списков на GitHub raw. |
| `url_lst` | `List[str]` | `PROXY_LINK_LST` | Список raw-URL GitHub со списками прокси. |
| `proxy_retries` | `int` | `5` (`NUMBER_ATTEMPTS`) | Попыток на URL при получении прокси с GitHub. |
| `main_retries` | `int` | `10` (`MAIN_PROXY_ATTEMPTS`) | Циклов повторного получения рабочего прокси. |

### `OCRConfig`

| Поле | Тип | По умолчанию | Описание |
|------|-----|--------------|----------|
| `lang_lst` | `Optional[List[str]]` | `None` | Языковые коды для EasyOCR. |
| `use_gpu_for_ocr` | `bool` | `False` | Использовать GPU для OCR. |
| `with_ocr` | `bool` | `False` | OCR для изображений при сканировании виртуального хранилища. |
| `cloud_version` | `bool` | `False` | Облачный API DeepSeek вместо локальной модели. |
| `with_deepseek` | `bool` | `True` | DeepSeek OCR; при `False` — EasyOCR. |
| `model_size` | `Literal["tiny","small","base","large","gundam"]` | `"tiny"` | Размер локальной модели DeepSeek OCR. |
| `crop_mode` | `bool` | `False` | Разбивать большие изображения на 4 части. |
| `base_url` | `str` | `"https://api.siliconflow.cn/v1/chat/completions"` | API-эндпоинт облачного DeepSeek. |
| `api_key_for_deepseek_ocr` | `Optional[str]` | `None` | API-ключ облачного DeepSeek. |
| `timeout_for_deepseek_ocr` | `Optional[int]` | `None` | Таймаут запросов к облачному DeepSeek (сек). |
| `max_rate_limit_retries` | `Optional[int]` | `5` (`NUMBER_ATTEMPTS`) | Повторы при rate-limit. |

### `FileConfig`

| Поле | Тип | По умолчанию | Описание |
|------|-----|--------------|----------|
| `virtual_storage` | `bool` | `False` | Режим виртуального хранилища (сканировать `virtual_storage_path`). |
| `virtual_storage_path` | `Optional[str]` | `None` | Корневая папка виртуального хранилища. |
| `writing_response_to_file` | `bool` | `False` | Сохранять ответ ИИ в текстовый файл с меткой времени. |
| `editing_files` | `bool` | `False` | Авто-редактирование файлов через JSON. |
| `deleting_files` | `bool` | `False` | Авто-удаление файлов через ИИ (совместно с `editing_files=True`). |

### `SafetyConfig`

| Поле | Тип | По умолчанию | Описание                                                                     |
|------|-----|--------------|------------------------------------------------------------------------------|
| `filter_for_swearing` | `bool` | `False` | Фильтр ненормативной лексики - возвращает безопасный ответ при срабатывании. |

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

- Все константы (`MAX_TOKENS`, `NUMBER_ATTEMPTS`, `MAIN_LANGUAGE` и др.) - в `BiNeuron.data.constants_for_functions`.
- Dataclass-конфиги - в `BiNeuron.data.configs`.
- Модели для языков и уровней производительности - в `BiNeuron.data.models_for_programming_languages` и `BiNeuron.data.models_and_file_names`.
- Логирование настраивается в `main_logger.py` - ошибки пишутся в `errors.log`.

</details>

<details>
<summary>🇨🇳 中文</summary>

## 概述

`BiNeuron` 是 **biNeuron** 包的主类。它协调整个工作流程：

- **语言检测** - 从用户请求和附加文件中确定编程语言。
- **模型选择** - 根据检测到的语言和计算机性能，自动选择最合适的 GGUF 模型（特定语言或多语言）。
- **下载与缓存** - 从 Hugging Face 下载所选模型（支持代理和镜像）。
- **提示词工程** - 根据所需场景（默认、测试、解释、重构等）构建系统提示。
- **AI 推理** - 将请求发送给已加载的大语言模型并返回响应。
- **文件编辑（可选）** - 如果启用，将解析 AI 响应并直接用于修改磁盘上的文件。
- **交互式聊天** - 支持带历史记录的多轮对话。

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

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `request` | `str` | **必需** | 用户的输入文本（问题、代码描述或任务）。 |
| `additional_files` | `Optional[List[str]]` | `None` | 文件路径列表，其内容将作为上下文提供给 AI。 |
| `model_conf` | `Optional[ModelConfig]` | `None` → 默认 | 模型选择、仓库/文件名、缓存目录、HF 令牌、镜像偏好。 |
| `llm_conf` | `Optional[LLMConfig]` | `None` → 默认 | LLM 生成参数（temperature、max_tokens、n_ctx、GPU 层数）。 |
| `prompt_conf` | `Optional[PromptConfig]` | `None` → 默认 | 系统提示模式及/或自定义系统提示。 |
| `translation_conf` | `Optional[TranslationConfig]` | `None` → 默认 | 翻译/语言检测、DeepL 密钥、本地翻译。 |
| `language_detection_conf` | `Optional[LanguageDetectionConfig]` | `None` → 默认 | 编程语言检测（AI 编排器或启发式）。 |
| `proxy_conf` | `Optional[ProxyConfig]` | `None` → 默认 | 代理、超时、重试、GitHub 代理列表。 |
| `ocr_conf` | `Optional[OCRConfig]` | `None` → 默认 | OCR、DeepSeek 云、GPU、裁剪模式。 |
| `file_conf` | `Optional[FileConfig]` | `None` → 默认 | 虚拟存储、回复写入文件、自动编辑/删除文件。 |
| `safety_conf` | `Optional[SafetyConfig]` | `None` → 默认 | 内容安全（脏话过滤）。 |

---

## 配置 dataclass

### `ModelConfig`

| 字段 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `preferences_in_ai` | `str` | `"deepseek"` | 首选多语言模型系列（`deepseek`、`qwen`、`minimax`、`code_llama`、`mellum`、`wizard`、`starcoder`、`yi_coder`、`codegemma`、`devstral`、`granite`、`codestral`、`codegeex4`、`opencode_interpreter`、`ornith_1_0`、`kat_dev`、`magistral_small`、`laguna_xs`、`breeze`）。 |
| `models_dir` | `str` | `"./models"` | GGUF 模型缓存目录。 |
| `type_computer` | `Optional[Literal["easy","middle","hard","very_hard"]]` | `None` | 预定义计算机性能级别。若为 `None` 则通过基准测试自动检测。 |
| `repo_id` | `Optional[str]` | `None` | 显式 Hugging Face 仓库 ID。若为 `None` 则自动选择。 |
| `filename` | `Optional[str]` | `None` | 仓库内的模型文件名（与 `repo_id` 一起使用）。 |
| `your_token_for_hf` | `Optional[str]` | `None` | 用于私有/受限模型的 HF 访问令牌。 |
| `subdomain` | `str` | `""` | 下载时添加到模型文件名前的可选前缀。 |
| `retries` | `int` | `5` (`NUMBER_ATTEMPTS`) | 出错时的下载尝试次数。 |
| `prefer_mirror` | `bool` | `True` | 使用 HF 镜像（`hf-mirror.com`）。 |

### `LLMConfig`

| 字段 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `verbose` | `bool` | `False` | 启用 `llama-cpp-python` 详细输出。 |
| `n_ctx` | `Optional[int]` | `None` | 上下文窗口大小（token）。`None` = 模型默认。 |
| `n_gpu_layers` | `int` | `0` | 卸载到 GPU 的层数（`0` 表示仅 CPU）。 |
| `echo` | `bool` | `False` | 在响应中回显提示（遗留字符串模式）。 |
| `max_tokens` | `int` | `8192` (`MAX_TOKENS`) | 响应中生成的最大 token 数。 |
| `temperature` | `float` | `0.1` | 采样温度（0.0–1.0）。 |

### `PromptConfig`

| 字段 | 类型 | 默认值 | 描述                               |
|------|------|--------|----------------------------------|
| `main_prompt_mode` | `Literal["default","testing","explanation","no_comments","refactor","debug","code_review","documentation","scaffold","security_hardening","algorithm_strategy"]` | `"default"` | 预定义的系统提示场景。                      |
| `main_prompt` | `Optional[str]` | `None` | 自定义系统提示 - 覆盖 `main_prompt_mode`。 |

### `TranslationConfig`

| 字段 | 类型 | 默认值 | 描述                                                         |
|------|------|--------|------------------------------------------------------------|
| `determinant_mode` | `Optional[Literal["lite","full","auto"]]` | `"lite"` | 自然语言检测模式（传递给 `fast_langdetect`）。                           |
| `accurate_translation` | `bool` | `False` | 使用 DeepL API（需要 `your_key_for_deepl`）而不是 Google Translate。 |
| `your_key_for_deepl` | `str` | `""` | DeepL API 密钥 - 若 `accurate_translation=True` 则必需。          |
| `request_language` | `str` | `"en"` (`MAIN_LANGUAGE`) | 翻译目标语言代码。                                                  |
| `local_trans` | `bool` | `False` | 使用 ArgosTranslate 进行完全离线翻译。                                |
| `from_code_lang` | `str` | `""` | 本地翻译的源语言代码（仅当 `local_trans=True` 时使用）。                     |

### `LanguageDetectionConfig`

| 字段 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `with_ai_orchestrator` | `bool` | `True` | 使用 AI 模型检测编程语言。 |
| `proprietary_algorithms` | `bool` | `False` | 使用内置关键词词典（仅当 `with_ai_orchestrator=False` 时）。 |

### `ProxyConfig`

| 字段 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `country` | `Optional[str]` | `None` | 用于代理过滤的国家代码（例如 `"ru"`）。 |
| `protocol` | `str` | `"http"` | 代理协议（`"http"` 或 `"https"`）。 |
| `max_timeout` | `int` | `1000` (`MAX_TIMEOUT`) | 代理可用性检查的最大超时时间（秒）。 |
| `is_working` | `bool` | `True` | 仅使用有效的（已验证的）代理。 |
| `auto_proxies` | `bool` | `True` | 当主主机不可达时自动启用代理回退。 |
| `your_proxies_dict` | `Optional[List[str]]` | `None` | 自定义代理列表（例如 `["192.168.1.1:8080"]`）。 |
| `min_timeout_for_checking_availability` | `int` | `10` (`MIN_TIMEOUT_FOR_CHECK`) | 连接检查的最小超时时间（秒）。 |
| `max_timeout_for_checking_availability` | `int` | `30` (`MAX_TIMEOUT_FOR_CHECK`) | 连接检查的最大超时时间（秒）。 |
| `github_proxies` | `bool` | `False` | 从 GitHub raw URL 获取代理列表。 |
| `url_lst` | `List[str]` | `PROXY_LINK_LST` | 包含代理列表的 GitHub raw URL 列表。 |
| `proxy_retries` | `int` | `5` (`NUMBER_ATTEMPTS`) | 从 GitHub 获取代理时每个 URL 的尝试次数。 |
| `main_retries` | `int` | `10` (`MAIN_PROXY_ATTEMPTS`) | 获取有效代理的重试周期数。 |

### `OCRConfig`

| 字段 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `lang_lst` | `Optional[List[str]]` | `None` | EasyOCR 的语言代码列表。 |
| `use_gpu_for_ocr` | `bool` | `False` | 对 OCR 使用 GPU。 |
| `with_ocr` | `bool` | `False` | 扫描虚拟存储时为图像启用 OCR。 |
| `cloud_version` | `bool` | `False` | 使用 DeepSeek 云 API 而不是本地模型。 |
| `with_deepseek` | `bool` | `True` | 使用 DeepSeek OCR；若为 `False` 则回退到 EasyOCR。 |
| `model_size` | `Literal["tiny","small","base","large","gundam"]` | `"tiny"` | 本地 DeepSeek OCR 模型的大小。 |
| `crop_mode` | `bool` | `False` | 将大图像分割成 4 部分以进行更详细的识别。 |
| `base_url` | `str` | `"https://api.siliconflow.cn/v1/chat/completions"` | DeepSeek 云的 API 端点。 |
| `api_key_for_deepseek_ocr` | `Optional[str]` | `None` | DeepSeek 云的 API 密钥。 |
| `timeout_for_deepseek_ocr` | `Optional[int]` | `None` | DeepSeek 云请求的超时时间（秒）。 |
| `max_rate_limit_retries` | `Optional[int]` | `5` (`NUMBER_ATTEMPTS`) | 遇到速率限制错误时的重试次数。 |

### `FileConfig`

| 字段 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `virtual_storage` | `bool` | `False` | 启用虚拟存储模式 – 扫描 `virtual_storage_path`。 |
| `virtual_storage_path` | `Optional[str]` | `None` | 虚拟存储的根文件夹路径。 |
| `writing_response_to_file` | `bool` | `False` | 将 AI 响应保存到带时间戳的文本文件。 |
| `editing_files` | `bool` | `False` | 启用通过 JSON 生成的自动文件编辑。 |
| `deleting_files` | `bool` | `False` | 启用通过 AI 的自动文件删除（与 `editing_files=True` 一起使用）。 |

### `SafetyConfig`

| 字段 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `filter_for_swearing` | `bool` | `False` | 启用脏话过滤 – 触发时返回预定义的安全响应。 |

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

- 所有常量（例如 `MAX_TOKENS`、`NUMBER_ATTEMPTS`、`MAIN_LANGUAGE`）均在 `BiNeuron.data.constants_for_functions` 中定义。
- 配置 dataclass 定义于 `BiNeuron.data.configs`。
- 特定语言和多语言模型的映射存储在 `BiNeuron.data.models_for_programming_languages` 和 `BiNeuron.data.models_and_file_names` 中。
- 日志记录由 `main_logger.py` 配置 - 错误写入 `errors.log`。

</details>