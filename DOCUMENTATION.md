<details>
<summary>🇬🇧 English</summary>

## Overview

`BiNeuron` is the main class of the **biNeuron** package. It orchestrates the entire workflow:

- **Language detection** – determines the programming language(s) from the user request and attached files.
- **Model selection** – automatically picks the best-suited GGUF model (language-specific or multilingual) based on the detected language and your computer’s performance.
- **Download & caching** – downloads the selected model from Hugging Face (with proxy/mirror support).
- **Prompt engineering** – builds a system prompt according to the desired scenario (default, testing, explanation, refactoring, etc.).
- **AI inference** – sends the request to the loaded LLM and returns the response.
- **File editing (optional)** – if enabled, the AI response is parsed and used to directly edit files on disk.
- **Interactive chat** – supports multi-turn conversations with history.

---

## Constructor Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `request` | `str` | **required** | The user’s input text (question, code description, or task). |
| `preferences_in_ai` | `PreferenceInAI` | `PreferenceInAI.DEEPSEEK` | Preferred AI model family for multilingual mode: `DEEPSEEK`, `QWEN`, `MINIMAX`, `CODE_LLAMA`, `MELLUM`, `WIZARD`. |
| `filter_for_swearing` | `bool` | `False` | Enable profanity filter – if detected, a predefined safe response is returned. |
| `additional_files` | `Optional[List[str]]` | `None` | List of file paths whose content will be included as context for the AI. |
| `models_dir` | `str` | `"./models"` | Directory to cache downloaded GGUF models. |
| `with_ai_orchestrator` | `bool` | `True` | Use an AI model to detect the programming language; otherwise use heuristics. |
| `verbose` | `bool` | `False` | Enable verbose output from the `llama-cpp-python` engine. |
| `n_ctx` | `Optional[int]` | `None` | Context window size in tokens. If `None`, the model’s default is used. |
| `n_gpu_layers` | `int` | `0` | Number of model layers to offload to GPU (`0` = CPU only). |
| `echo` | `bool` | `False` | Echo the prompt in the response (legacy string mode). |
| `max_tokens` | `int` | `MAX_TOKENS` (8192) | Maximum number of tokens to generate in the response. |
| `your_token_for_hf` | `Optional[str]` | `None` | Hugging Face access token for private or gated models. |
| `subdomain` | `str` | `""` | Optional prefix added to the model filename during download. |
| `country` | `Optional[str]` | `None` | Country code (e.g., `"ru"`) for proxy filtering. |
| `protocol` | `str` | `"http"` | Proxy protocol (`"http"` or `"https"`). |
| `max_timeout` | `int` | `MAX_TIMEOUT` (1000) | Maximum timeout (seconds) for proxy availability checks. |
| `is_working` | `bool` | `True` | Use only working (verified) proxies. |
| `type_computer` | `Optional[Literal["easy", "middle", "hard", "very_hard"]]` | `None` | Predefined computer performance level for model quantization selection. If `None`, it is auto‑detected via a benchmark. |
| `auto_proxies` | `bool` | `True` | Automatically enable proxy fallback when the primary host is unreachable. |
| `writing_response_to_file` | `bool` | `False` | Save the AI response to a timestamped text file. |
| `your_proxies_dict` | `Optional[List[str]]` | `None` | Custom proxy list (e.g., `["192.168.1.1:8080"]`). Overrides automatic discovery. |
| `determinant_mode` | `Optional[Literal["lite", "full", "auto"]]` | `"lite"` | Mode for natural language detection during translation (passed to `fast_langdetect`). |
| `accurate_translation` | `bool` | `False` | Use DeepL API for translation (requires `your_key_for_deepl`) instead of Google Translate. |
| `your_key_for_deepl` | `str` | `""` | DeepL API key – required if `accurate_translation=True`. |
| `proprietary_algorithms` | `bool` | `False` | Use the built‑in keyword dictionary for language detection (only when `with_ai_orchestrator=False`). |
| `repo_id` | `Optional[str]` | `None` | Explicit Hugging Face repository ID. If `None`, automatic selection is used. |
| `filename` | `Optional[str]` | `None` | Model file name inside the repository (must be used with `repo_id`). |
| `min_timeout_for_checking_availability` | `int` | `MIN_TIMEOUT_FOR_CHECK` (10) | Minimum timeout (seconds) for connection checks to websites. |
| `max_timeout_for_checking_availability` | `int` | `MAX_TIMEOUT_FOR_CHECK` (30) | Maximum timeout (seconds) for connection checks. |
| `request_language` | `str` | `"en"` | Target language code for translation (e.g., `"en"`, `"ru"`). |
| `main_prompt_mode` | `Literal["default", "testing", "explanation", "no_comments", "refactor", "debug", "code_review", "documentation", "scaffold", "security_hardening", "algorithm_strategy"]` | `"default"` | Predefined system prompt scenario. |
| `main_prompt` | `Optional[str]` | `None` | Custom system prompt – overrides `main_prompt_mode`. |
| `temperature` | `float` | `0.1` | Sampling temperature (0.0–1.0) – higher values increase creativity. |
| `retries` | `int` | `NUMBER_ATTEMPTS` (5) | Number of download attempts in case of errors. |
| `github_proxies` | `bool` | `False` | Fetch proxy lists from raw GitHub URLs (instead of using `free-proxy-server`). |
| `url_lst` | `List[str]` | `PROXY_LINK_LST` | List of raw GitHub URLs containing proxy lists. |
| `proxy_retries` | `int` | `NUMBER_ATTEMPTS` (5) | Number of attempts per URL when fetching proxies from GitHub. |
| `main_retries` | `int` | `MAIN_PROXY_ATTEMPTS` (10) | Number of retry cycles to obtain a working proxy from GitHub. |
| `lang_lst` | `Optional[List[str]]` | `None` | Language codes (e.g., `["en", "ru"]`) for EasyOCR. |
| `use_gpu_for_ocr` | `bool` | `False` | Use GPU for OCR (EasyOCR / DeepSeek). |
| `virtual_storage` | `bool` | `False` | Enable virtual storage mode – scan the folder at `virtual_storage_path`. |
| `virtual_storage_path` | `Optional[str]` | `None` | Path to the root folder for virtual storage. |
| `with_ocr` | `bool` | `False` | Enable OCR for images when scanning virtual storage. |
| `cloud_version` | `bool` | `False` | Use DeepSeek cloud API instead of the local model. |
| `with_deepseek` | `bool` | `True` | Use DeepSeek OCR; if `False`, fallback to EasyOCR. |
| `model_size` | `Literal["tiny", "small", "base", "large", "gundam"]` | `"tiny"` | Size of the local DeepSeek OCR model. |
| `crop_mode` | `bool` | `False` | Split large images into 4 parts for more detailed recognition (DeepSeek only). |
| `base_url` | `str` | `"https://api.siliconflow.cn/v1/chat/completions"` | API endpoint for DeepSeek cloud. |
| `api_key_for_deepseek_ocr` | `Optional[str]` | `None` | API key for DeepSeek cloud – required if `cloud_version=True`. |
| `timeout_for_deepseek_ocr` | `Optional[int]` | `None` | Timeout (seconds) for DeepSeek cloud requests. If `None`, a random value is used. |
| `max_rate_limit_retries` | `Optional[int]` | `NUMBER_ATTEMPTS` | Number of retries on rate‑limit errors from DeepSeek cloud. |
| `prefer_mirror` | `bool` | `True` | Use the Hugging Face mirror (`hf-mirror.com`) for downloads. |
| `editing_files` | `bool` | `False` | Enable automatic file editing via JSON generation and disk write. |

---

## Notes

- All constants (e.g., `MAX_TOKENS`, `NUMBER_ATTEMPTS`, `MAIN_LANGUAGE`) are defined in `BiNeuron.data.constants_for_functions`.
- The `PreferenceInAI` enum is imported from `BiNeuron.data.preferences_in_ai`.
- Language‑specific and multilingual model mappings are stored in `BiNeuron.data.models_for_programming_languages` and `BiNeuron.data.models_and_file_names`.
- Logging is configured by `main_logger.py` – errors are written to `errors.log`.

</details>

<details>
<summary>🇷🇺 Русский</summary>

## Обзор

`BiNeuron` — главный класс пакета **biNeuron**. Он управляет всем процессом:

- **Определение языка** – определяет язык(и) программирования из запроса пользователя и прикреплённых файлов.
- **Выбор модели** – автоматически подбирает наилучшую GGUF-модель (специализированную или мультиязычную) на основе определённого языка и производительности вашего компьютера.
- **Загрузка и кэширование** – скачивает выбранную модель с Hugging Face (с поддержкой прокси и зеркал).
- **Формирование промпта** – создаёт системную инструкцию в соответствии с выбранным сценарием (стандартный, тестирование, объяснение, рефакторинг и т.д.).
- **Инференс ИИ** – отправляет запрос в загруженную LLM и возвращает ответ.
- **Редактирование файлов (опционально)** – если включено, ответ ИИ парсится и используется для прямого изменения файлов на диске.
- **Интерактивный чат** – поддерживает многошаговые диалоги с историей.

---

## Параметры конструктора

| Параметр | Тип | По умолчанию | Описание |
|----------|-----|--------------|----------|
| `request` | `str` | **обязательный** | Основной запрос пользователя (вопрос, описание задачи или код). |
| `preferences_in_ai` | `PreferenceInAI` | `PreferenceInAI.DEEPSEEK` | Предпочитаемое семейство ИИ-моделей для мультиязычного режима: `DEEPSEEK`, `QWEN`, `MINIMAX`, `CODE_LLAMA`, `MELLUM`, `WIZARD`. |
| `filter_for_swearing` | `bool` | `False` | Включить фильтр ненормативной лексики – при обнаружении возвращается стандартный безопасный ответ. |
| `additional_files` | `Optional[List[str]]` | `None` | Список путей к файлам, содержимое которых будет добавлено как контекст для ИИ. |
| `models_dir` | `str` | `"./models"` | Директория для кэширования скачанных GGUF-моделей. |
| `with_ai_orchestrator` | `bool` | `True` | Использовать ИИ для определения языка программирования; иначе эвристики. |
| `verbose` | `bool` | `False` | Включить подробный вывод из движка `llama-cpp-python`. |
| `n_ctx` | `Optional[int]` | `None` | Размер контекстного окна в токенах. Если `None`, используется стандарт модели. |
| `n_gpu_layers` | `int` | `0` | Количество слоёв модели, выгружаемых на GPU (`0` – только CPU). |
| `echo` | `bool` | `False` | Эхо-промпта в ответе (строковый режим). |
| `max_tokens` | `int` | `MAX_TOKENS` (8192) | Максимальное количество токенов в генерируемом ответе. |
| `your_token_for_hf` | `Optional[str]` | `None` | Токен доступа к Hugging Face для приватных или gated-моделей. |
| `subdomain` | `str` | `""` | Префикс, добавляемый к имени файла модели при скачивании. |
| `country` | `Optional[str]` | `None` | Код страны (например, `"ru"`) для фильтрации прокси. |
| `protocol` | `str` | `"http"` | Протокол прокси (`"http"` или `"https"`). |
| `max_timeout` | `int` | `MAX_TIMEOUT` (1000) | Максимальное время ожидания (сек) при проверке прокси. |
| `is_working` | `bool` | `True` | Использовать только рабочие (проверенные) прокси. |
| `type_computer` | `Optional[Literal["easy", "middle", "hard", "very_hard"]]` | `None` | Уровень производительности ПК для выбора квантизации модели. Если `None`, определяется автоматически через бенчмарк. |
| `auto_proxies` | `bool` | `True` | Автоматически включать прокси при недоступности основного хоста. |
| `writing_response_to_file` | `bool` | `False` | Сохранять ответ ИИ в текстовый файл с временной меткой. |
| `your_proxies_dict` | `Optional[List[str]]` | `None` | Пользовательский список прокси (например, `["192.168.1.1:8080"]`). Отменяет автоматический поиск. |
| `determinant_mode` | `Optional[Literal["lite", "full", "auto"]]` | `"lite"` | Режим определения естественного языка при переводе (передаётся в `fast_langdetect`). |
| `accurate_translation` | `bool` | `False` | Использовать DeepL API для перевода (требуется `your_key_for_deepl`) вместо Google Translate. |
| `your_key_for_deepl` | `str` | `""` | API-ключ DeepL – обязателен, если `accurate_translation=True`. |
| `proprietary_algorithms` | `bool` | `False` | Использовать встроенный словарь ключевых слов для определения языка (только если `with_ai_orchestrator=False`). |
| `repo_id` | `Optional[str]` | `None` | Явный идентификатор репозитория на Hugging Face. Если `None`, используется автоматический выбор. |
| `filename` | `Optional[str]` | `None` | Имя файла модели внутри репозитория (используется вместе с `repo_id`). |
| `min_timeout_for_checking_availability` | `int` | `MIN_TIMEOUT_FOR_CHECK` (10) | Минимальный таймаут (сек) при проверке доступности сайтов. |
| `max_timeout_for_checking_availability` | `int` | `MAX_TIMEOUT_FOR_CHECK` (30) | Максимальный таймаут (сек) при проверке доступности сайтов. |
| `request_language` | `str` | `"en"` | Целевой язык для перевода (например, `"en"`, `"ru"`). |
| `main_prompt_mode` | `Literal["default", "testing", "explanation", "no_comments", "refactor", "debug", "code_review", "documentation", "scaffold", "security_hardening", "algorithm_strategy"]` | `"default"` | Предустановленный сценарий системного промпта. |
| `main_prompt` | `Optional[str]` | `None` | Пользовательский системный промпт – заменяет `main_prompt_mode`. |
| `temperature` | `float` | `0.1` | Температура выборки (0.0–1.0) – выше значение = больше креативности. |
| `retries` | `int` | `NUMBER_ATTEMPTS` (5) | Количество попыток скачивания модели при ошибках. |
| `github_proxies` | `bool` | `False` | Использовать списки прокси с raw-ссылок GitHub (вместо `free-proxy-server`). |
| `url_lst` | `List[str]` | `PROXY_LINK_LST` | Список raw-URL на GitHub с текстовыми файлами прокси. |
| `proxy_retries` | `int` | `NUMBER_ATTEMPTS` (5) | Количество попыток загрузки прокси по каждому URL. |
| `main_retries` | `int` | `MAIN_PROXY_ATTEMPTS` (10) | Количество повторных циклов получения рабочего прокси из GitHub. |
| `lang_lst` | `Optional[List[str]]` | `None` | Список языковых кодов (например, `["en", "ru"]`) для EasyOCR. |
| `use_gpu_for_ocr` | `bool` | `False` | Использовать GPU для OCR (EasyOCR / DeepSeek). |
| `virtual_storage` | `bool` | `False` | Включить режим виртуального хранилища – сканировать папку `virtual_storage_path`. |
| `virtual_storage_path` | `Optional[str]` | `None` | Путь к корневой папке виртуального хранилища. |
| `with_ocr` | `bool` | `False` | Включить OCR для изображений при сканировании виртуального хранилища. |
| `cloud_version` | `bool` | `False` | Использовать облачный API DeepSeek вместо локальной модели. |
| `with_deepseek` | `bool` | `True` | Использовать DeepSeek OCR; если `False` – EasyOCR. |
| `model_size` | `Literal["tiny", "small", "base", "large", "gundam"]` | `"tiny"` | Размер локальной модели DeepSeek OCR. |
| `crop_mode` | `bool` | `False` | Разбивать большие изображения на 4 части для детального распознавания (только DeepSeek). |
| `base_url` | `str` | `"https://api.siliconflow.cn/v1/chat/completions"` | URL-адрес API для облачного DeepSeek. |
| `api_key_for_deepseek_ocr` | `Optional[str]` | `None` | API-ключ для облачного DeepSeek – обязателен, если `cloud_version=True`. |
| `timeout_for_deepseek_ocr` | `Optional[int]` | `None` | Таймаут (сек) для запросов к облачному DeepSeek. Если `None`, используется случайное значение. |
| `max_rate_limit_retries` | `Optional[int]` | `NUMBER_ATTEMPTS` | Количество повторных попыток при ошибках ограничения частоты запросов (rate limit). |
| `prefer_mirror` | `bool` | `True` | Использовать зеркало Hugging Face (`hf-mirror.com`) для загрузки. |
| `editing_files` | `bool` | `False` | Включить автоматическое редактирование файлов через генерацию JSON и запись на диск. |

---

## Примечания

- Все константы (например, `MAX_TOKENS`, `NUMBER_ATTEMPTS`, `MAIN_LANGUAGE`) определены в `BiNeuron.data.constants_for_functions`.
- Перечисление `PreferenceInAI` импортируется из `BiNeuron.data.preferences_in_ai`.
- Списки моделей для языков и уровней производительности заданы в `BiNeuron.data.models_for_programming_languages` и `BiNeuron.data.models_and_file_names`.
- Логирование настраивается в `main_logger.py` – ошибки записываются в `errors.log`.

</details>

<details>
<summary>🇨🇳 中文</summary>

## 概述

`BiNeuron` 是 **biNeuron** 包的主类。它协调整个工作流程：

- **语言检测** – 从用户请求和附加文件中确定编程语言。
- **模型选择** – 根据检测到的语言和计算机性能，自动选择最合适的 GGUF 模型（特定语言或多语言）。
- **下载与缓存** – 从 Hugging Face 下载所选模型（支持代理和镜像）。
- **提示词工程** – 根据所需场景（默认、测试、解释、重构等）构建系统提示。
- **AI 推理** – 将请求发送给已加载的大语言模型并返回响应。
- **文件编辑（可选）** – 如果启用，将解析 AI 响应并直接用于修改磁盘上的文件。
- **交互式聊天** – 支持带历史记录的多轮对话。

---

## 构造函数参数

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `request` | `str` | **必需** | 用户的输入文本（问题、代码描述或任务）。 |
| `preferences_in_ai` | `PreferenceInAI` | `PreferenceInAI.DEEPSEEK` | 多语言模式下的首选 AI 模型系列：`DEEPSEEK`、`QWEN`、`MINIMAX`、`CODE_LLAMA`、`MELLUM`、`WIZARD`。 |
| `filter_for_swearing` | `bool` | `False` | 启用脏话过滤 – 如果检测到，将返回预定义的安全响应。 |
| `additional_files` | `Optional[List[str]]` | `None` | 文件路径列表，其内容将作为上下文提供给 AI。 |
| `models_dir` | `str` | `"./models"` | 缓存已下载 GGUF 模型的目录。 |
| `with_ai_orchestrator` | `bool` | `True` | 使用 AI 模型检测编程语言；否则使用启发式方法。 |
| `verbose` | `bool` | `False` | 启用 `llama-cpp-python` 引擎的详细输出。 |
| `n_ctx` | `Optional[int]` | `None` | 上下文窗口大小（以 token 计）。如果为 `None`，则使用模型的默认值。 |
| `n_gpu_layers` | `int` | `0` | 卸载到 GPU 的模型层数（`0` 表示仅使用 CPU）。 |
| `echo` | `bool` | `False` | 在响应中回显提示（遗留字符串模式）。 |
| `max_tokens` | `int` | `MAX_TOKENS` (8192) | 响应中生成的最大 token 数。 |
| `your_token_for_hf` | `Optional[str]` | `None` | 用于私有或受限模型的 Hugging Face 访问令牌。 |
| `subdomain` | `str` | `""` | 下载时添加到模型文件名前的可选前缀。 |
| `country` | `Optional[str]` | `None` | 用于代理过滤的国家代码（例如 `"ru"`）。 |
| `protocol` | `str` | `"http"` | 代理协议（`"http"` 或 `"https"`）。 |
| `max_timeout` | `int` | `MAX_TIMEOUT` (1000) | 代理可用性检查的最大超时时间（秒）。 |
| `is_working` | `bool` | `True` | 仅使用有效的（已验证的）代理。 |
| `type_computer` | `Optional[Literal["easy", "middle", "hard", "very_hard"]]` | `None` | 用于模型量化选择的预定义计算机性能级别。如果为 `None`，则通过基准测试自动检测。 |
| `auto_proxies` | `bool` | `True` | 当主主机不可达时自动启用代理回退。 |
| `writing_response_to_file` | `bool` | `False` | 将 AI 响应保存到带时间戳的文本文件。 |
| `your_proxies_dict` | `Optional[List[str]]` | `None` | 自定义代理列表（例如 `["192.168.1.1:8080"]`）。覆盖自动发现。 |
| `determinant_mode` | `Optional[Literal["lite", "full", "auto"]]` | `"lite"` | 翻译时自然语言检测的模式（传递给 `fast_langdetect`）。 |
| `accurate_translation` | `bool` | `False` | 使用 DeepL API 进行翻译（需要 `your_key_for_deepl`）而不是 Google Translate。 |
| `your_key_for_deepl` | `str` | `""` | DeepL API 密钥 – 如果 `accurate_translation=True` 则必需。 |
| `proprietary_algorithms` | `bool` | `False` | 使用内置的关键词词典进行语言检测（仅当 `with_ai_orchestrator=False` 时）。 |
| `repo_id` | `Optional[str]` | `None` | 显式 Hugging Face 仓库 ID。如果为 `None`，则使用自动选择。 |
| `filename` | `Optional[str]` | `None` | 仓库内的模型文件名（必须与 `repo_id` 一起使用）。 |
| `min_timeout_for_checking_availability` | `int` | `MIN_TIMEOUT_FOR_CHECK` (10) | 网站连接检查的最小超时时间（秒）。 |
| `max_timeout_for_checking_availability` | `int` | `MAX_TIMEOUT_FOR_CHECK` (30) | 网站连接检查的最大超时时间（秒）。 |
| `request_language` | `str` | `"en"` | 翻译的目标语言代码（例如 `"en"`、`"ru"`）。 |
| `main_prompt_mode` | `Literal["default", "testing", "explanation", "no_comments", "refactor", "debug", "code_review", "documentation", "scaffold", "security_hardening", "algorithm_strategy"]` | `"default"` | 预定义的系统提示场景。 |
| `main_prompt` | `Optional[str]` | `None` | 自定义系统提示 – 覆盖 `main_prompt_mode`。 |
| `temperature` | `float` | `0.1` | 采样温度（0.0–1.0）– 值越高越有创造性。 |
| `retries` | `int` | `NUMBER_ATTEMPTS` (5) | 出现错误时的下载尝试次数。 |
| `github_proxies` | `bool` | `False` | 从 GitHub raw URL 获取代理列表（而不是使用 `free-proxy-server`）。 |
| `url_lst` | `List[str]` | `PROXY_LINK_LST` | 包含代理列表的 GitHub raw URL 列表。 |
| `proxy_retries` | `int` | `NUMBER_ATTEMPTS` (5) | 从 GitHub 获取代理时每个 URL 的尝试次数。 |
| `main_retries` | `int` | `MAIN_PROXY_ATTEMPTS` (10) | 从 GitHub 获取有效代理的重试周期数。 |
| `lang_lst` | `Optional[List[str]]` | `None` | EasyOCR 的语言代码列表（例如 `["en", "ru"]`）。 |
| `use_gpu_for_ocr` | `bool` | `False` | 对 OCR 使用 GPU（EasyOCR / DeepSeek）。 |
| `virtual_storage` | `bool` | `False` | 启用虚拟存储模式 – 扫描 `virtual_storage_path` 中的文件夹。 |
| `virtual_storage_path` | `Optional[str]` | `None` | 虚拟存储的根文件夹路径。 |
| `with_ocr` | `bool` | `False` | 扫描虚拟存储时为图像启用 OCR。 |
| `cloud_version` | `bool` | `False` | 使用 DeepSeek 云 API 而不是本地模型。 |
| `with_deepseek` | `bool` | `True` | 使用 DeepSeek OCR；如果为 `False`，则回退到 EasyOCR。 |
| `model_size` | `Literal["tiny", "small", "base", "large", "gundam"]` | `"tiny"` | 本地 DeepSeek OCR 模型的大小。 |
| `crop_mode` | `bool` | `False` | 将大图像分割成 4 部分以进行更详细的识别（仅 DeepSeek）。 |
| `base_url` | `str` | `"https://api.siliconflow.cn/v1/chat/completions"` | DeepSeek 云的 API 端点。 |
| `api_key_for_deepseek_ocr` | `Optional[str]` | `None` | DeepSeek 云的 API 密钥 – 如果 `cloud_version=True` 则必需。 |
| `timeout_for_deepseek_ocr` | `Optional[int]` | `None` | DeepSeek 云请求的超时时间（秒）。如果为 `None`，则使用随机值。 |
| `max_rate_limit_retries` | `Optional[int]` | `NUMBER_ATTEMPTS` | 遇到 DeepSeek 云速率限制错误时的重试次数。 |
| `prefer_mirror` | `bool` | `True` | 下载时使用 Hugging Face 镜像（`hf-mirror.com`）。 |
| `editing_files` | `bool` | `False` | 启用通过 JSON 生成和磁盘写入的自动文件编辑。 |

---

## 备注

- 所有常量（例如 `MAX_TOKENS`、`NUMBER_ATTEMPTS`、`MAIN_LANGUAGE`）均在 `BiNeuron.data.constants_for_functions` 中定义。
- `PreferenceInAI` 枚举从 `BiNeuron.data.preferences_in_ai` 导入。
- 特定语言和多语言模型的映射存储在 `BiNeuron.data.models_for_programming_languages` 和 `BiNeuron.data.models_and_file_names` 中。
- 日志记录由 `main_logger.py` 配置 – 错误写入 `errors.log`。

</details>