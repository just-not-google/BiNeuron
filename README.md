<p align="center">  
  <img src="img_files/banner_2.png" width="100%" alt="BiNeuron Start" />  
</p> 

# BiNeuron  

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black)

[![Follow on X](https://img.shields.io/badge/Follow-@BiNeuron123-000000?style=for-the-badge&logo=x&logoColor=white)](https://x.com/BiNeuron123)
[![Subscribe on YouTube](https://img.shields.io/badge/Subscribe-@bineuron-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/@bineuron)

<details>
<summary>🇬🇧 English</summary>

## Official Resources  

**WebSite**: [https://just-not-google.github.io/BiNeuron/](https://just-not-google.github.io/BiNeuron/)  
This is the official BiNeuron website. There you can download the application for Windows, macOS, and Linux, as well as view the project overview and key features.

**Hub**: [https://just-not-google.github.io/BiNeuron/website/hub.html](https://just-not-google.github.io/BiNeuron/website/hub.html)  
This is a collection of ready-to-use configurations for local AI models. Each card contains a model, an optimal system prompt, tags, and a direct link to Hugging Face. Currently, the hub has 47 configurations, including specialized models for Python, Java, and other languages.  

## Intelligent Code Analysis and Generation Platform  

BiNeuron is a sophisticated software solution that bridges the gap between human intent and machine generated code. It unifies advanced natural language processing, optical character recognition, and adaptive model selection into a single, powerful tool designed for developers, researchers, and technical teams.  

At its core, BiNeuron automatically identifies the programming language of a given request, extracts content from a wide array of file formats, including images and documents, and then generates context aware, production ready code using best in class local or cloud based language models.

## Key Capabilities  

### Programming Language Detection  
* Supports over 25 programming languages, including Python, Java, C/C++, C#, JavaScript, TypeScript, Go, Rust, Swift, Kotlin, Ruby, Dart, Julia, Lua, SQL, MATLAB, R, Pascal, Assembly, Fortran, F#, Ada, Zig, PHP, Shell, Scala, PowerShell, Solidity, OCaml, COBOL, and more.  
* Combines heuristic algorithms, proprietary keyword matching, and AI powered orchestration to achieve high detection accuracy.  
* Analyzes both user supplied text and the content of attached files, or even entire directories.  

### Comprehensive File Handling  
* Extracts and translates text from common document formats: PDF, Word (DOCX), ODF, PowerPoint (PPTX), Excel (XLSX/XLS), EPUB, MOBI, and FB2.  
* Processes source code files in nearly all text based formats, from plain text to configuration files.  
* Integrates two interchangeable OCR engines (EasyOCR and DeepSeek OCR) to read text from images, with optional GPU acceleration, language list selection, and automatic splitting of large images (`crop_mode`) for improved recognition.  
* Reads text from websites: the built in HTML scraper (`use_websites`) converts pages to clean Markdown and merges them into the request context.  

### AI Powered File Editing  
* **Two Stage Pipeline**: The primary AI model generates the code or response. A secondary, lightweight model (e.g., Qwen2.5-Coder-1.5B) then transforms the response into a strict JSON object containing absolute file paths and full new contents.  
* **Full Context Awareness**: The JSON formatter receives the complete file context (all read files, unread file names, project root, and the primary AI’s answer) to ensure accurate path generation and content mapping.  
* **Robust Retry Mechanism**: If the JSON fails validation, the system automatically re prompts the formatter up to `retries` times, logging each attempt until a valid JSON is produced or the maximum retries are exhausted.  
* **Safe, Whole File Replacements**: Only whole file replacements are supported (no partial edits) to maintain consistency and safety.  
* **Optional File Deletion**: When `deleting_files=True` is passed to the `BiNeuron` constructor, the JSON formatter may return `null` for a file path, and the system will safely delete that file. This feature is disabled by default to prevent accidental data loss.  

### Adaptive Model Selection  
* Automatically assesses the user’s hardware capabilities (CPU cores, frequency, RAM) and selects the optimal quantized version of the target model (ranging from IQ2 to F16) to balance speed and accuracy.  
* Offers a curated repository of specialised models per programming language, ensuring high quality, idiomatic code generation.  

### Robust Networking  
* Implements multi layered accessibility to Hugging Face models, including automatic fallback to hf mirror.com, dynamic proxy selection, and support for custom proxy lists.  
* Fetches and verifies public proxies from GitHub raw lists, with retry mechanisms and connection health checks.  

### Virtual Storage Mode  
* Allows scanning and processing of entire folders or mounted virtual directories.  
* Recursively identifies supported files, extracts their content, and incorporates it into the analysis context, which is perfect for large codebases or repositories.  
* **Interactive File Explorer**: In GUI mode, the virtual storage is displayed as a tree view. Double click any file to open it in the default system application.  

### Multilingual Translation  
* Built in translation engine normalises user requests to English (or any configured target language) to ensure consistent AI interactions.  
* Supports both Google Translate and DeepL, with automatic fallback when network restrictions are detected.  
* **Offline Translation**: Optional ArgosTranslate integration (`local_trans=True`, `from_code_lang='en'`) provides fully offline translation without relying on external APIs.  

### Text Enhancement and Compression  
* **Request Improvement** (`improving_user_experience=True`): A local small model (Qwen) rewrites the user’s raw request into a clear, structured prompt while preserving all technical details, including file names, code fragments, and error messages.  
* **Lossless Text Compression** (`compress_text=True`): When a large amount of file context is attached, the same small model compresses it, aggressively reducing token count while preserving every fact, number, and code fragment verbatim.  

### Privacy and Security  
* **Request Anonymization** (`anonymize_text=True`): Before being sent to translation services or AI models, the user’s request is processed through Microsoft Presidio, which detects and replaces PII (names, emails, phone numbers, addresses, credit cards, etc.) with placeholder tokens.  
* **Profanity Filter** (`filter_for_swearing=True`): Blocks requests containing aggressive language or profanity before they reach the AI.  
* **Chat Encryption**: Optionally protect all stored conversations with a master password using Fernet (AES 128 CBC + HMAC SHA256) with PBKDF2 HMAC SHA256 key derivation (200,000 iterations). After three failed unlock attempts the entire chat database and master key are permanently wiped.  

## Architecture  

BiNeuron is engineered with a modular, separation of concerns design:  

* **Core Engine** orchestrates the entire pipeline: request parsing, language detection, model selection, and response generation.  
* **OCR Module** handles text extraction from images via two interchangeable engines: EasyOCR and DeepSeek OCR (local HF Transformers or cloud API).  
* **Model Downloader** manages downloading and caching of Hugging Face models, with built in mirror and proxy support.  
* **JSON Formatter Module** uses a lightweight model (e.g., Qwen2.5-Coder-1.5B) to convert the primary model’s response into a strict JSON object for file modifications.  
* **File Editing Module** applies JSON based file changes (whole file replacements) with error handling and retry logic. Supports optional file deletion when `deleting_files=True`.  
* **Text Enhancement Module** handles request improvement (`PROMPT_FOR_IMPROVEMENT`) and lossless compression (`PROMPT_FOR_COMPRESSION`) via the same lightweight model.  
* **Translation Service** provides language detection and translation utilities, with optional DeepL and ArgosTranslate integration.  
* **Anonymization Service** integrates Microsoft Presidio for PII detection and masking.  
* **Network Layer** implements proxy rotation, availability checks, and GitHub proxy fetching for circumventing restrictions.  
* **Web Interface** is a feature rich web application built with Flask (HTML/CSS/JS), covering every configurable parameter of the nine configuration groups.  

The architecture emphasises reusability, fault tolerance, and performance, allowing each component to operate independently while seamlessly integrating with the others.  

## Graphical Interface  

<p align="center">
  <img src="img_files/gui_screenshot_2.png" width="80%" alt="BiNeuron GUI Screenshot" />
</p>

A modern web application built with Flask, offering:  
* **Intuitive Chat Interface**: message history, file attachments, and real time log display.  
* **Virtual Storage Explorer**: scan and navigate directories in a tree view.  
* **Comprehensive Settings Panel**: fine tune every aspect of the platform, including network, model selection, prompt mode, translator, OCR, file handling, safety, and more.  
* **Chat Management**: create, delete, download, and filter conversation history.  
* **Live Logging**: see what the AI is doing in real time (with spinner, deduplicated progress bars, and one click copy).  
* **Master Password Encryption**: enable or disable chat encryption directly from the UI.  
* **24 Dark Themes**: from Midnight Deep and Dracula’s Castle to Synthwave ’84, Matrix Terminal, and AMOLED Black; every theme is tuned for long coding sessions.  
* **Session Resume**: if the page is reloaded while a request is running, the client reconnects to the ongoing task automatically.  
* **Multilingual UI**: English, Russian, and Chinese.  

## Development  

Only the interface and the interaction with the interface were developed with the help of **DeepSeek Coder**. This includes the Flask based web UI, the JavaScript front end, and the user interaction logic. All other components, including the core engine, OCR module, model downloader, JSON formatter, file editing module, translation service, anonymization service, network layer, and overall architecture, were designed and written independently.  

* **Model Collection**: [deepseek-ai/deepseek-coder](https://huggingface.co/collections/deepseek-ai/deepseek-coder)  
* **Example Model**: [deepseek-ai/deepseek-coder-6.7b-instruct](https://huggingface.co/deepseek-ai/deepseek-coder-6.7b-instruct)  

## Configuration Groups  

The platform exposes nine independent configuration groups, all available from the web UI:

| Group | Purpose |
|-------|---------|
| `ModelConfig` | Model selection, cache directory, HF token, repo/filename overrides, mirror preference |
| `LLMConfig` | Context size, GPU layers, max tokens, temperature, verbose/echo flags |
| `PromptConfig` | Main prompt mode (11 pre set scenarios), custom prompt, request improvement |
| `TranslationConfig` | Determinant mode, DeepL, request language, offline Argos translation |
| `LanguageDetectionConfig` | AI orchestrator vs. proprietary keyword matching |
| `ProxyConfig` | Country, protocol, timeouts, retries, custom/GitHub proxy lists |
| `OCRConfig` | Engine selection (Easy/DeepSeek), languages, GPU, crop mode, cloud API key |
| `FileConfig` | Virtual storage, file editing, file deletion, website scraping, compression, ignored files |
| `SafetyConfig` | Profanity filter, request anonymization |

## Dependencies  

The complete list of libraries used by BiNeuron (exactly as declared in `requirements.txt`).

### Core & AI  

| Library | Purpose | Repository |
|---------|---------|-----------|
| `torch` | Tensor computation and GPU acceleration for local models | [github.com/pytorch/pytorch](https://github.com/pytorch/pytorch) |
| `transformers` | Loading and running Hugging Face models locally | [github.com/huggingface/transformers](https://github.com/huggingface/transformers) |
| `huggingface_hub` | Downloading and caching models from Hugging Face | [github.com/huggingface/huggingface_hub](https://github.com/huggingface/huggingface_hub) |
| `llama-cpp-python` | Running GGUF models via llama.cpp bindings | [github.com/abetlen/llama-cpp-python](https://github.com/abetlen/llama-cpp-python) |
| `pillow` | Image loading and preprocessing for OCR and vision models | [github.com/python-pillow/Pillow](https://github.com/python-pillow/Pillow) |

### OCR  

| Library | Purpose | Repository |
|---------|---------|-----------|
| `easyocr` | OCR engine for text extraction from images | [github.com/JaidedAI/EasyOCR](https://github.com/JaidedAI/EasyOCR) |
| `deepseek-ocr` | DeepSeek OCR client (local and cloud) | [pypi.org/project/deepseek-ocr](https://pypi.org/project/deepseek-ocr/) |

### Document Parsing  

| Library | Purpose | Repository |
|---------|---------|-----------|
| `PyMuPDF` | Reading text from PDF files | [github.com/pymupdf/PyMuPDF](https://github.com/pymupdf/PyMuPDF) |
| `docx2txt` | Extracting text from `.docx` (Microsoft Word) | [github.com/ankushshah89/python-docx2txt](https://github.com/ankushshah89/python-docx2txt) |
| `pptx2txt2` | Extracting text from `.pptx` (PowerPoint) | [pypi.org/project/pptx2txt2](https://pypi.org/project/pptx2txt2/) |
| `odfdo` | Reading OpenDocument (`.odf`) files | [github.com/jdum/odfdo](https://github.com/jdum/odfdo) |
| `markitdown` | Universal document converter (used for `.xlsx`/`.xls`) | [github.com/microsoft/markitdown](https://github.com/microsoft/markitdown) |
| `epub2txt` | Extracting text from EPUB e-books | [pypi.org/project/epub2txt](https://pypi.org/project/epub2txt/) |
| `mobi` | Extracting text from MOBI e-books | [github.com/iscc/mobi](https://github.com/iscc/mobi) |
| `fb2reader` | Reading FictionBook 2 (`.fb2`) files | [pypi.org/project/fb2reader](https://pypi.org/project/fb2reader/) |
| `html2text` | Converting HTML pages to clean Markdown | [github.com/Alir3z4/html2text](https://github.com/Alir3z4/html2text) |

### Translation  

| Library | Purpose | Repository |
|---------|---------|-----------|
| `deep-translator` | Free translation via Google Translate (and others) | [github.com/nidhaloff/deep-translator](https://github.com/nidhaloff/deep-translator) |
| `deepl` | Official DeepL API client | [github.com/DeepLcom/deepl-python](https://github.com/DeepLcom/deepl-python) |
| `argostranslate` | Fully offline translation via Argos Translate | [github.com/argosopentech/argos-translate](https://github.com/argosopentech/argos-translate) |
| `langdetect` | Language detection (fallback algorithm) | [github.com/Mimino666/langdetect](https://github.com/Mimino666/langdetect) |
| `fast-langdetect` | Fast language detection (primary algorithm) | [github.com/LlmKira/fast-langdetect](https://github.com/LlmKira/fast-langdetect) |

### Language & Code Detection  

| Library | Purpose | Repository |
|---------|---------|-----------|
| `codelang-detect` | Detecting programming language by code sample | [pypi.org/project/codelang-detect](https://pypi.org/project/codelang-detect/) |
| `whats_that_code` | Independent programming language detection | [github.com/matthewdeanmartin/whats_that_code](https://github.com/matthewdeanmartin/whats_that_code) |
| `badwords-py` | Profanity filtering (imports as `badwords`) | [pypi.org/project/badwords-py](https://pypi.org/project/badwords-py/) |

### Privacy & Anonymization  

| Library | Purpose | Repository |
|---------|---------|-----------|
| `presidio-analyzer` | PII detection engine (Microsoft Presidio) | [github.com/microsoft/presidio](https://github.com/microsoft/presidio) |
| `presidio-anonymizer` | Anonymization engine for detected PII | [github.com/microsoft/presidio](https://github.com/microsoft/presidio) |

### Networking & Proxies  

| Library | Purpose | Repository |
|---------|---------|-----------|
| `requests` | HTTP client for REST calls and proxy checks | [github.com/psf/requests](https://github.com/psf/requests) |
| `httpx` | Async capable HTTP client used with proxies | [github.com/encode/httpx](https://github.com/encode/httpx) |
| `free-proxy-server` | Fetching and filtering free proxy lists | [pypi.org/project/free-proxy-server](https://pypi.org/project/free-proxy-server/) |

### Web & System  

| Library | Purpose | Repository |
|---------|---------|-----------|
| `flask` | Web server and REST API for the GUI | [github.com/pallets/flask](https://github.com/pallets/flask) |
| `psutil` | Reading system info (CPU, RAM) for benchmarking | [github.com/giampaolo/psutil](https://github.com/giampaolo/psutil) |
| `cryptography` | Encrypting chats with a master password (Fernet) | [github.com/pyca/cryptography](https://github.com/pyca/cryptography) |

### CLI, Testing & Packaging  

| Library | Purpose | Repository |
|---------|---------|-----------|
| `pytest` | Test runner | [github.com/pytest-dev/pytest](https://github.com/pytest-dev/pytest) |
| `pyinstaller` | Building standalone executables | [github.com/pyinstaller/pyinstaller](https://github.com/pyinstaller/pyinstaller) |

## Model Repository  

BiNeuron leverages a hand picked collection of open source code generation models, each fine tuned for specific programming languages. The repository includes models from DeepSeek, Qwen, MiniMax, CodeLlama, Mellum, Wizard, and others. The system automatically fetches the appropriate model based on the detected language and the user’s hardware profile, ensuring optimal performance for every session.  

> BiNeuron represents a fusion of cutting edge AI, robust software engineering, and practical usability, empowering developers to focus on creativity and problem solving while the platform handles the complexities of language detection, file processing, and model orchestration.

</details>

<details>
<summary>🇷🇺 Русский</summary>

## Официальные ресурсы  

**ВебСайт**: [https://just-not-google.github.io/BiNeuron/](https://just-not-google.github.io/BiNeuron/)  
Это официальный сайт BiNeuron. Там можно скачать приложение для Windows, macOS и Linux, а также посмотреть обзор проекта и ключевые возможности.   

**Хаб**: [https://just-not-google.github.io/BiNeuron/website/hub.html](https://just-not-google.github.io/BiNeuron/website/hub.html)  
Это коллекция готовых конфигураций для локальных ИИ моделей. Каждая карточка содержит модель, оптимальный системный промпт, теги и прямую ссылку на Hugging Face. Сейчас в хабе 47 конфигураций, включая специализированные модели для Python, Java и других языков.  

## Интеллектуальная платформа для анализа и генерации кода

BiNeuron представляет собой сложное программное решение, которое устраняет разрыв между намерениями человека и машинным кодом. Он объединяет продвинутую обработку естественного языка, оптическое распознавание символов и адаптивный выбор модели в единый мощный инструмент, предназначенный для разработчиков, исследователей и технических групп.  

По своей сути, BiNeuron автоматически определяет язык программирования для данного запроса, извлекает содержимое из широкого спектра форматов файлов, включая изображения и документы, а затем генерирует контекстно зависимый, готовый к работе код, используя лучшие в своем классе локальные или облачные языковые модели.

## Ключевые возможности  

### Определение языка программирования  
* Поддерживает более 25 языков программирования, включая Python, Java, C/C++, C#, JavaScript, TypeScript, Go, Rust, Swift, Kotlin, Ruby, Dart, Julia, Lua, SQL, MATLAB, R, Pascal, Assembly, Fortran, F#, Ada, Zig, PHP, Shell, Scala, PowerShell, Solidity, OCaml, COBOL и другие.  
* Объединяет эвристические алгоритмы, фирменный поиск по ключевым словам и ИИ управляемую оркестрацию для высокой точности определения.  
* Анализирует как текст, введённый пользователем, так и содержимое прикреплённых файлов или даже целых каталогов.  

### Всесторонняя обработка файлов  
* Извлекает и преобразует текст из распространённых форматов документов: PDF, Word (DOCX), ODF, PowerPoint (PPTX), Excel (XLSX/XLS), EPUB, MOBI и FB2.  
* Обрабатывает файлы исходного кода почти во всех текстовых форматах, от обычного текста до конфигурационных файлов.  
* Интегрирует два взаимозаменяемых OCR движка (EasyOCR и DeepSeek OCR) для чтения текста из изображений, с опциональным ускорением на GPU, выбором списка языков и автоматическим разбиением больших изображений (`crop_mode`) для улучшенного распознавания.  
* Читает текст с сайтов: встроенный HTML скрапер (`use_websites`) конвертирует страницы в чистый Markdown и добавляет их в контекст запроса.  

### Изменение файлов с помощью ИИ  
* **Двухэтапный пайплайн**: Основная ИИ модель генерирует код или ответ. Вторичная лёгкая модель (например, Qwen2.5-Coder-1.5B) преобразует этот ответ в строгий JSON объект, содержащий абсолютные пути к файлам и новое полное содержимое.  
* **Полный контекст**: Форматтер JSON получает весь контекст файлов (все прочитанные файлы, имена непрочитанных файлов, корень проекта и ответ основной ИИ модели) для точной генерации путей и содержимого.  
* **Надёжный механизм повторных попыток**: Если JSON не проходит валидацию, система автоматически перезапрашивает форматтер до `retries` раз, логируя каждую попытку, пока не будет получен валидный JSON или не будут исчерпаны все попытки.  
* **Безопасная замена целых файлов**: Поддерживается только полная замена файлов (не частичное редактирование) для обеспечения согласованности и безопасности.  
* **Опциональное удаление файлов**: При передаче `deleting_files=True` в конструктор `BiNeuron` JSON форматтер может вернуть `null` для пути к файлу, и система безопасно удалит этот файл. По умолчанию функция отключена во избежание случайной потери данных.  

### Адаптивный выбор модели  
* Автоматически оценивает аппаратные возможности пользователя (количество ядер CPU, частота, ОЗУ) и выбирает оптимальную квантизованную версию целевой модели (от IQ2 до F16) для баланса скорости и точности.  
* Предлагает специально подобранный репозиторий моделей для каждого языка программирования, обеспечивая высококачественную и идиоматичную генерацию кода.  

### Надёжные сетевые возможности  
* Реализует многоуровневый доступ к моделям Hugging Face, включая автоматическое переключение на hf mirror.com, динамический выбор прокси и поддержку пользовательских списков прокси.  
* Загружает и проверяет публичные прокси из списков GitHub, с повторными попытками и проверкой работоспособности соединений.  

### Режим виртуального хранилища  
* Позволяет сканировать и обрабатывать целые папки или смонтированные виртуальные директории.  
* Рекурсивно определяет поддерживаемые файлы, извлекает их содержимое и включает его в контекст анализа, что идеально для больших кодовых баз или репозиториев.  
* **Интерактивный файловый менеджер**: В режиме GUI виртуальное хранилище отображается в виде дерева. Двойной клик по файлу открывает его в системном приложении по умолчанию.  

### Многоязычный перевод  
* Встроенный механизм перевода приводит запросы пользователя к английскому (или любому другому настроенному языку) для единообразного взаимодействия с ИИ.  
* Поддерживает Google Translate и DeepL с автоматическим переключением при обнаружении сетевых ограничений.  
* **Офлайн перевод**: Опциональная интеграция ArgosTranslate (`local_trans=True`, `from_code_lang='en'`) обеспечивает полностью офлайн перевод без обращения к внешним API.  

### Улучшение и сжатие текста  
* **Улучшение запроса** (`improving_user_experience=True`): Локальная малая модель (Qwen) переписывает исходный запрос пользователя в чёткий структурированный промпт, сохраняя все технические детали, включая имена файлов, фрагменты кода, сообщения об ошибках.  
* **Без потерь сжатие текста** (`compress_text=True`): Когда к запросу прикреплено много файлов, та же малая модель агрессивно сокращает их объём, сохраняя каждый факт, число и фрагмент кода дословно.  

### Приватность и безопасность  
* **Анонимизация запроса** (`anonymize_text=True`): Перед отправкой в сервисы перевода или ИИ модели запрос пользователя проходит через Microsoft Presidio, который находит и заменяет PII (имена, email, телефоны, адреса, банковские карты и т. д.) на токены заглушки.  
* **Фильтр ненормативной лексики** (`filter_for_swearing=True`): Блокирует запросы, содержащие агрессию или мат, до их попадания в ИИ.  
* **Шифрование чатов**: Возможность защитить все сохранённые беседы мастер паролем с использованием Fernet (AES 128 CBC + HMAC SHA256) и PBKDF2 HMAC SHA256 (200 000 итераций). После трёх неудачных попыток разблокировки база чатов и мастер ключ безвозвратно удаляются.  

## Архитектура  

BiNeuron спроектирован по модульному принципу с разделением ответственности:  

* **Основной движок** управляет всем конвейером: разбор запроса, определение языка, выбор модели и генерация ответа.  
* **Модуль OCR** обрабатывает извлечение текста из изображений через два взаимозаменяемых движка: EasyOCR и DeepSeek OCR (локальные HF Transformers или облачный API).  
* **Загрузчик моделей** управляет загрузкой и кэшированием моделей Hugging Face со встроенной поддержкой зеркал и прокси.  
* **Модуль JSON форматтера** использует лёгкую модель (например, Qwen2.5-Coder-1.5B) для преобразования ответа основной модели в строгий JSON для изменения файлов.  
* **Модуль редактирования файлов** применяет изменения на основе JSON (полная замена файлов) с обработкой ошибок и повторными попытками. Поддерживает опциональное удаление файлов при `deleting_files=True`.  
* **Модуль улучшения текста** выполняет улучшение запроса (`PROMPT_FOR_IMPROVEMENT`) и сжатие без потерь (`PROMPT_FOR_COMPRESSION`) той же лёгкой моделью.  
* **Сервис перевода** предоставляет функции определения языка и перевода, с опциональной интеграцией DeepL и ArgosTranslate.  
* **Сервис анонимизации** интегрирует Microsoft Presidio для обнаружения и маскирования PII.  
* **Сетевой уровень** реализует ротацию прокси, проверку доступности и получение прокси из GitHub для обхода ограничений.  
* **Веб интерфейс** это функциональное веб приложение на Flask (HTML/CSS/JS), охватывающее каждый настраиваемый параметр из девяти групп конфигурации.  

Архитектура делает упор на переиспользуемость, отказоустойчивость и производительность, позволяя каждому компоненту работать независимо, но при этом бесшовно интегрироваться с другими.  

## Графический интерфейс  

<p align="center">
  <img src="img_files/gui_screenshot_2.png" width="80%" alt="Скриншот GUI BiNeuron" />
</p>

Современное веб приложение на Flask, предлагающее:  
* **Интуитивный чат**: история сообщений, прикрепление файлов и отображение логов в реальном времени.  
* **Обозреватель виртуального хранилища**: сканирование и навигация по директориям в виде дерева.  
* **Всеобъемлющая панель настроек**: тонкая настройка каждого аспекта платформы, включая сеть, выбор модели, режим промпта, переводчик, OCR, файлы, безопасность и многое другое.  
* **Управление чатами**: создание, удаление, загрузка и фильтрация истории диалогов.  
* **Live логи**: просмотр действий ИИ в реальном времени (со спиннером, дедуплицированными прогресс барами и копированием в один клик).  
* **Шифрование мастер паролем**: включение или отключение шифрования чатов прямо из UI.  
* **24 тёмные темы**: от Midnight Deep и Dracula’s Castle до Synthwave ’84, Matrix Terminal и AMOLED Black; каждая тема оптимизирована для длительных сессий разработки.  
* **Возобновление сессии**: при перезагрузке страницы во время выполнения запроса клиент автоматически переподключается к текущей задаче.  
* **Мультиязычный интерфейс**: English, Русский, 中文.  

## Разработка  

Только интерфейс и взаимодействие с интерфейсом были разработаны с помощью **DeepSeek Coder**. Это включает веб интерфейс на Flask, JavaScript фронтенд и логику взаимодействия с пользователем. Все остальные компоненты, включая основной движок, модуль OCR, загрузчик моделей, JSON форматтер, модуль редактирования файлов, сервис перевода, сервис анонимизации, сетевой уровень и общую архитектуру, были спроектированы и написаны самостоятельно.  

* **Коллекция моделей**: [deepseek-ai/deepseek-coder](https://huggingface.co/collections/deepseek-ai/deepseek-coder)  
* **Пример модели**: [deepseek-ai/deepseek-coder-6.7b-instruct](https://huggingface.co/deepseek-ai/deepseek-coder-6.7b-instruct)  

## Группы конфигурации  

Платформа предоставляет девять независимых групп конфигурации, все доступны из веб интерфейса:

| Группа | Назначение |
|--------|-----------|
| `ModelConfig` | Выбор модели, папка кэша, HF токен, переопределение repo/filename, зеркало |
| `LLMConfig` | Размер контекста, слои GPU, макс. токенов, температура, verbose/echo |
| `PromptConfig` | Режим основного промпта (11 сценариев), пользовательский промпт, улучшение запроса |
| `TranslationConfig` | Режим определения, DeepL, язык запроса, офлайн перевод Argos |
| `LanguageDetectionConfig` | ИИ оркестратор vs. проприетарный поиск по ключевым словам |
| `ProxyConfig` | Страна, протокол, таймауты, повторы, свои/GitHub списки прокси |
| `OCRConfig` | Движок (Easy/DeepSeek), языки, GPU, crop mode, API ключ облака |
| `FileConfig` | Виртуальное хранилище, редактирование/удаление файлов, скрапинг сайтов, сжатие, игнорируемые файлы |
| `SafetyConfig` | Фильтр ненормативной лексики, анонимизация запроса |

## Зависимости  

Полный список библиотек, используемых в BiNeuron (ровно то, что объявлено в `requirements.txt`).

### Ядро и ИИ  

| Библиотека | Назначение | Репозиторий |
|-----------|------------|------------|
| `torch` | Тензорные вычисления и GPU ускорение для локальных моделей | [github.com/pytorch/pytorch](https://github.com/pytorch/pytorch) |
| `transformers` | Загрузка и запуск моделей Hugging Face локально | [github.com/huggingface/transformers](https://github.com/huggingface/transformers) |
| `huggingface_hub` | Скачивание и кэширование моделей с Hugging Face | [github.com/huggingface/huggingface_hub](https://github.com/huggingface/huggingface_hub) |
| `llama-cpp-python` | Запуск GGUF моделей через привязки llama.cpp | [github.com/abetlen/llama-cpp-python](https://github.com/abetlen/llama-cpp-python) |
| `pillow` | Загрузка и предобработка изображений для OCR и vision моделей | [github.com/python-pillow/Pillow](https://github.com/python-pillow/Pillow) |

### OCR  

| Библиотека | Назначение | Репозиторий |
|-----------|------------|------------|
| `easyocr` | OCR движок для извлечения текста из изображений | [github.com/JaidedAI/EasyOCR](https://github.com/JaidedAI/EasyOCR) |
| `deepseek-ocr` | Клиент DeepSeek OCR (локально и в облаке) | [pypi.org/project/deepseek-ocr](https://pypi.org/project/deepseek-ocr/) |

### Парсинг документов  

| Библиотека | Назначение | Репозиторий |
|-----------|------------|------------|
| `PyMuPDF` | Чтение текста из PDF | [github.com/pymupdf/PyMuPDF](https://github.com/pymupdf/PyMuPDF) |
| `docx2txt` | Извлечение текста из `.docx` (Microsoft Word) | [github.com/ankushshah89/python-docx2txt](https://github.com/ankushshah89/python-docx2txt) |
| `pptx2txt2` | Извлечение текста из `.pptx` (PowerPoint) | [pypi.org/project/pptx2txt2](https://pypi.org/project/pptx2txt2/) |
| `odfdo` | Чтение OpenDocument (`.odf`) | [github.com/jdum/odfdo](https://github.com/jdum/odfdo) |
| `markitdown` | Универсальный конвертер документов (для `.xlsx`/`.xls`) | [github.com/microsoft/markitdown](https://github.com/microsoft/markitdown) |
| `epub2txt` | Извлечение текста из EPUB | [pypi.org/project/epub2txt](https://pypi.org/project/epub2txt/) |
| `mobi` | Извлечение текста из MOBI | [github.com/iscc/mobi](https://github.com/iscc/mobi) |
| `fb2reader` | Чтение FictionBook 2 (`.fb2`) | [pypi.org/project/fb2reader](https://pypi.org/project/fb2reader/) |
| `html2text` | Конвертация HTML страниц в чистый Markdown | [github.com/Alir3z4/html2text](https://github.com/Alir3z4/html2text) |

### Перевод  

| Библиотека | Назначение | Репозиторий |
|-----------|------------|------------|
| `deep-translator` | Бесплатный перевод через Google Translate и др. | [github.com/nidhaloff/deep-translator](https://github.com/nidhaloff/deep-translator) |
| `deepl` | Официальный клиент DeepL API | [github.com/DeepLcom/deepl-python](https://github.com/DeepLcom/deepl-python) |
| `argostranslate` | Полностью офлайн перевод через Argos Translate | [github.com/argosopentech/argos-translate](https://github.com/argosopentech/argos-translate) |
| `langdetect` | Определение языка (резервный алгоритм) | [github.com/Mimino666/langdetect](https://github.com/Mimino666/langdetect) |
| `fast-langdetect` | Быстрое определение языка (основной алгоритм) | [github.com/LlmKira/fast-langdetect](https://github.com/LlmKira/fast-langdetect) |

### Определение языка и кода  

| Библиотека | Назначение | Репозиторий |
|-----------|------------|------------|
| `codelang-detect` | Определение языка программирования по образцу кода | [pypi.org/project/codelang-detect](https://pypi.org/project/codelang-detect/) |
| `whats_that_code` | Независимое определение языка программирования | [github.com/matthewdeanmartin/whats_that_code](https://github.com/matthewdeanmartin/whats_that_code) |
| `badwords-py` | Фильтрация ненормативной лексики (импортируется как `badwords`) | [pypi.org/project/badwords-py](https://pypi.org/project/badwords-py/) |

### Приватность и анонимизация  

| Библиотека | Назначение | Репозиторий |
|-----------|------------|------------|
| `presidio-analyzer` | Движок обнаружения PII (Microsoft Presidio) | [github.com/microsoft/presidio](https://github.com/microsoft/presidio) |
| `presidio-anonymizer` | Движок анонимизации обнаруженных PII | [github.com/microsoft/presidio](https://github.com/microsoft/presidio) |

### Сеть и прокси  

| Библиотека | Назначение | Репозиторий |
|-----------|------------|------------|
| `requests` | HTTP клиент для REST запросов и проверки прокси | [github.com/psf/requests](https://github.com/psf/requests) |
| `httpx` | HTTP клиент с поддержкой async, используется с прокси | [github.com/encode/httpx](https://github.com/encode/httpx) |
| `free-proxy-server` | Получение и фильтрация списков бесплатных прокси | [pypi.org/project/free-proxy-server](https://pypi.org/project/free-proxy-server/) |

### Веб и система  

| Библиотека | Назначение | Репозиторий |
|-----------|------------|------------|
| `flask` | Веб сервер и REST API для GUI | [github.com/pallets/flask](https://github.com/pallets/flask) |
| `psutil` | Чтение системной информации (CPU, RAM) для бенчмарка | [github.com/giampaolo/psutil](https://github.com/giampaolo/psutil) |
| `cryptography` | Шифрование чатов мастер паролем (Fernet) | [github.com/pyca/cryptography](https://github.com/pyca/cryptography) |

### CLI, тестирование и упаковка  

| Библиотека | Назначение | Репозиторий |
|-----------|------------|------------|
| `pytest` | Запуск тестов | [github.com/pytest-dev/pytest](https://github.com/pytest-dev/pytest) |
| `pyinstaller` | Сборка standalone исполняемых файлов | [github.com/pyinstaller/pyinstaller](https://github.com/pyinstaller/pyinstaller) |

## Репозиторий моделей  

BiNeuron использует тщательно подобранную коллекцию открытых моделей генерации кода, каждая из которых дообучена для конкретных языков программирования. В репозиторий входят модели от DeepSeek, Qwen, MiniMax, CodeLlama, Mellum, Wizard и других. Система автоматически загружает подходящую модель на основе определённого языка и аппаратного профиля пользователя, обеспечивая оптимальную производительность в каждом сеансе.  

> BiNeuron представляет собой синтез передового ИИ, надёжной инженерии и практической полезности, позволяя разработчикам сосредоточиться на творчестве и решении задач, пока платформа берёт на себя сложности определения языка, обработки файлов и оркестрации моделей.

</details>

<details>
<summary>🇨🇳 中文</summary>

## 官方资源  

**网站**：[https://just-not-google.github.io/BiNeuron/](https://just-not-google.github.io/BiNeuron/)  
这是 BiNeuron 的官方网站。您可以在此下载适用于 Windows、macOS 和 Linux 的应用程序，并查看项目概述和主要功能。  

**枢纽**：[https://just-not-google.github.io/BiNeuron/website/hub.html](https://just-not-google.github.io/BiNeuron/website/hub.html)  
这是本地 AI 模型的即用型配置集合。每张卡片包含一个模型、最佳系统提示、标签以及指向 Hugging Face 的直接链接。目前中心有 47 个配置，包括针对 Python、Java 和其他语言的专用模型。  

## 智能代码分析与生成平台

BiNeuron 是一个先进的软件解决方案，旨在弥合人类意图与机器生成代码之间的鸿沟。它将先进的自然语言处理、光学字符识别和自适应模型选择整合到一个功能强大的工具中，专为开发者、研究人员和技术团队设计。  

其核心功能是自动识别给定请求的编程语言，从包括图像和文档在内的多种文件格式中提取内容，然后使用一流本地或云端语言模型生成上下文感知、可用于生产的代码。

## 主要功能  

### 编程语言检测  
* 支持超过 25 种编程语言，包括 Python、Java、C/C++、C#、JavaScript、TypeScript、Go、Rust、Swift、Kotlin、Ruby、Dart、Julia、Lua、SQL、MATLAB、R、Pascal、Assembly、Fortran、F#、Ada、Zig、PHP、Shell、Scala、PowerShell、Solidity、OCaml、COBOL 等。  
* 结合启发式算法、专有关键词匹配和 AI 驱动的编排，实现高检测精度。  
* 分析用户提供的文本以及附加文件内容，甚至整个目录。  

### 全面的文件处理  
* 从常见文档格式中提取和转换文本：PDF、Word（DOCX）、ODF、PowerPoint（PPTX）、Excel（XLSX/XLS）、EPUB、MOBI 和 FB2。  
* 处理几乎所有基于文本格式的源代码文件，从纯文本到配置文件。  
* 集成两个可互换的 OCR 引擎（EasyOCR 和 DeepSeek OCR）从图像中读取文本，支持可选的 GPU 加速、语言列表选择，并可自动分割大图像（`crop_mode`）以提高识别效果。  
* 读取网站文本：内置 HTML 抓取器（`use_websites`）将页面转换为干净的 Markdown 并合并到请求上下文中。  

### AI 驱动的文件编辑  
* **两阶段流水线**：主 AI 模型生成代码或响应。随后，一个轻量级辅助模型（例如 Qwen2.5-Coder-1.5B）将该响应转换为严格的 JSON 对象，其中包含绝对文件路径和完整的新内容。  
* **完整上下文感知**：JSON 格式化器接收完整的文件上下文（所有已读文件、未读文件名、项目根目录以及主 AI 的回答），以确保准确的路径生成和内容映射。  
* **强大的重试机制**：如果 JSON 验证失败，系统会自动重新提示格式化器，最多重试 `retries` 次，并记录每次尝试，直到生成有效 JSON 或达到最大重试次数。  
* **安全的整文件替换**：仅支持整文件替换（不支持部分编辑），以保持一致性和安全性。  
* **可选文件删除**：当向 `BiNeuron` 构造函数传递 `deleting_files=True` 时，JSON 格式化器可能为文件路径返回 `null`，系统将安全删除该文件。此功能默认禁用，以防止意外数据丢失。  

### 自适应模型选择  
* 自动评估用户的硬件能力（CPU 核心数、频率、RAM），并选择目标模型的最佳量化版本（从 IQ2 到 F16），以平衡速度和精度。  
* 为每种编程语言提供精选的专用模型仓库，确保生成高质量、地道的代码。  

### 强大的网络功能  
* 实现对 Hugging Face 模型的多层访问，包括自动回退到 hf mirror.com、动态代理选择以及自定义代理列表支持。  
* 从 GitHub 原始列表中获取并验证公共代理，具有重试机制和连接健康检查。  

### 虚拟存储模式  
* 允许扫描和处理整个文件夹或挂载的虚拟目录。  
* 递归识别支持的文件，提取其内容并将其纳入分析上下文，这非常适合大型代码库或仓库。  
* **交互式文件浏览器**：在 GUI 模式下，虚拟存储以树形视图显示。双击任何文件可在默认系统应用程序中打开。  

### 多语言翻译  
* 内置翻译引擎将用户请求标准化为英语（或任何配置的目标语言），以确保一致的 AI 交互。  
* 支持 Google Translate 和 DeepL，检测到网络限制时自动回退。  
* **离线翻译**：可选的 ArgosTranslate 集成（`local_trans=True`，`from_code_lang='en'`）提供完全离线的翻译，无需依赖外部 API。  

### 文本增强与压缩  
* **请求改进**（`improving_user_experience=True`）：本地小型模型（Qwen）将用户的原始请求重写为清晰、结构化的提示，同时保留所有技术细节，包括文件名、代码片段、错误消息。  
* **无损文本压缩**（`compress_text=True`）：当附加大量文件上下文时，同一个轻量模型会对其进行压缩，在逐字保留每个事实、数字和代码片段的同时大幅减少 token 数量。  

### 隐私与安全  
* **请求匿名化**（`anonymize_text=True`）：在发送到翻译服务或 AI 模型之前，用户请求会经过 Microsoft Presidio 处理，该工具会检测并将 PII（姓名、电子邮件、电话号码、地址、信用卡等）替换为占位符标记。  
* **脏话过滤器**（`filter_for_swearing=True`）：在请求到达 AI 之前阻止包含攻击性语言或脏话的请求。  
* **对话加密**：可选择使用主密码保护所有存储的对话，使用 Fernet（AES 128 CBC + HMAC SHA256）和 PBKDF2 HMAC SHA256（200,000 次迭代）。三次解锁失败后，整个对话数据库和主密钥将被永久删除。  

## 架构  

BiNeuron 采用模块化、关注点分离的设计：  

* **核心引擎**负责编排整个流水线：请求解析、语言检测、模型选择和响应生成。  
* **OCR 模块**通过两个可互换引擎处理图像中的文本提取：EasyOCR 和 DeepSeek OCR（本地 HF Transformers 或云端 API）。  
* **模型下载器**管理 Hugging Face 模型的下载和缓存，内置镜像和代理支持。  
* **JSON 格式化器模块**使用轻量级模型（例如 Qwen2.5-Coder-1.5B）将主模型的响应转换为严格的 JSON 对象以用于文件修改。  
* **文件编辑模块**应用基于 JSON 的文件更改（整文件替换），具备错误处理和重试逻辑。当 `deleting_files=True` 时支持可选的文件删除。  
* **文本增强模块**通过同一个轻量模型进行请求改进（`PROMPT_FOR_IMPROVEMENT`）和无损压缩（`PROMPT_FOR_COMPRESSION`）。  
* **翻译服务**提供语言检测和翻译工具，可选集成 DeepL 和 ArgosTranslate。  
* **匿名化服务**集成 Microsoft Presidio 进行 PII 检测和屏蔽。  
* **网络层**实现代理轮换、可用性检查以及从 GitHub 获取代理以规避限制。  
* **Web 界面**是使用 Flask（HTML/CSS/JS）构建的功能丰富的 Web 应用程序，涵盖九个配置组中的每一个可配置参数。  

该架构强调可重用性、容错性和性能，允许每个组件独立运行，同时与其他组件无缝集成。  

## 图形界面  

<p align="center">
  <img src="img_files/gui_screenshot_2.png" width="80%" alt="BiNeuron GUI 截图" />
</p>

使用 Flask 构建的现代 Web 应用程序，提供：  
* **直观的聊天界面**：消息历史、文件附件和实时日志显示。  
* **虚拟存储浏览器**：以树形视图扫描和导航目录。  
* **全面的设置面板**：微调平台的每个方面，包括网络、模型选择、提示模式、翻译器、OCR、文件、安全等。  
* **聊天管理**：创建、删除、下载和筛选对话历史。  
* **实时日志**：实时查看 AI 的操作（带加载动画、去重的进度条和一键复制）。  
* **主密码加密**：可直接从 UI 启用或禁用对话加密。  
* **24 个深色主题**：从 Midnight Deep 和 Dracula’s Castle 到 Synthwave ’84、Matrix Terminal 和 AMOLED Black；每个主题都针对长时间编码会话进行了优化。  
* **会话恢复**：如果在请求运行期间重新加载页面，客户端会自动重新连接到正在进行的任务。  
* **多语言界面**：English、Русский、中文。  

## 开发  

只有界面和与界面的交互是在 **DeepSeek Coder** 的帮助下开发的。这包括基于 Flask 的 Web UI、JavaScript 前端以及用户交互逻辑。所有其他组件，包括核心引擎、OCR 模块、模型下载器、JSON 格式化器、文件编辑模块、翻译服务、匿名化服务、网络层以及整体架构，均为独立设计和编写。  

* **模型集合**: [deepseek-ai/deepseek-coder](https://huggingface.co/collections/deepseek-ai/deepseek-coder)  
* **示例模型**: [deepseek-ai/deepseek-coder-6.7b-instruct](https://huggingface.co/deepseek-ai/deepseek-coder-6.7b-instruct)  

## 配置组  

平台提供九个独立的配置组，均可从 Web 界面访问：

| 组 | 用途 |
|----|------|
| `ModelConfig` | 模型选择、缓存目录、HF 令牌、repo/filename 覆盖、镜像偏好 |
| `LLMConfig` | 上下文大小、GPU 层数、最大 token、温度、verbose/echo |
| `PromptConfig` | 主提示模式（11 个预设场景）、自定义提示、请求改进 |
| `TranslationConfig` | 检测模式、DeepL、请求语言、离线 Argos 翻译 |
| `LanguageDetectionConfig` | AI 编排器 vs. 专有关键词匹配 |
| `ProxyConfig` | 国家、协议、超时、重试、自定义/GitHub 代理列表 |
| `OCRConfig` | 引擎选择（Easy/DeepSeek）、语言、GPU、裁剪模式、云 API 密钥 |
| `FileConfig` | 虚拟存储、文件编辑/删除、网站抓取、压缩、忽略文件 |
| `SafetyConfig` | 脏话过滤、请求匿名化 |

## 依赖项  

BiNeuron 使用的完整库列表（与 `requirements.txt` 中声明的完全一致）。

### 核心与 AI  

| 库 | 用途 | 仓库 |
|----|------|------|
| `torch` | 本地模型的张量计算与 GPU 加速 | [github.com/pytorch/pytorch](https://github.com/pytorch/pytorch) |
| `transformers` | 本地加载和运行 Hugging Face 模型 | [github.com/huggingface/transformers](https://github.com/huggingface/transformers) |
| `huggingface_hub` | 从 Hugging Face 下载和缓存模型 | [github.com/huggingface/huggingface_hub](https://github.com/huggingface/huggingface_hub) |
| `llama-cpp-python` | 通过 llama.cpp 绑定运行 GGUF 模型 | [github.com/abetlen/llama-cpp-python](https://github.com/abetlen/llama-cpp-python) |
| `pillow` | OCR 和视觉模型的图像加载与预处理 | [github.com/python-pillow/Pillow](https://github.com/python-pillow/Pillow) |

### OCR  

| 库 | 用途 | 仓库 |
|----|------|------|
| `easyocr` | 从图像中提取文本的 OCR 引擎 | [github.com/JaidedAI/EasyOCR](https://github.com/JaidedAI/EasyOCR) |
| `deepseek-ocr` | DeepSeek OCR 客户端（本地和云端） | [pypi.org/project/deepseek-ocr](https://pypi.org/project/deepseek-ocr/) |

### 文档解析  

| 库 | 用途 | 仓库 |
|----|------|------|
| `PyMuPDF` | 从 PDF 中读取文本 | [github.com/pymupdf/PyMuPDF](https://github.com/pymupdf/PyMuPDF) |
| `docx2txt` | 从 `.docx`（Microsoft Word）中提取文本 | [github.com/ankushshah89/python-docx2txt](https://github.com/ankushshah89/python-docx2txt) |
| `pptx2txt2` | 从 `.pptx`（PowerPoint）中提取文本 | [pypi.org/project/pptx2txt2](https://pypi.org/project/pptx2txt2/) |
| `odfdo` | 读取 OpenDocument (`.odf`) | [github.com/jdum/odfdo](https://github.com/jdum/odfdo) |
| `markitdown` | 通用文档转换器（用于 `.xlsx`/`.xls`） | [github.com/microsoft/markitdown](https://github.com/microsoft/markitdown) |
| `epub2txt` | 从 EPUB 电子书中提取文本 | [pypi.org/project/epub2txt](https://pypi.org/project/epub2txt/) |
| `mobi` | 从 MOBI 电子书中提取文本 | [github.com/iscc/mobi](https://github.com/iscc/mobi) |
| `fb2reader` | 读取 FictionBook 2 (`.fb2`) | [pypi.org/project/fb2reader](https://pypi.org/project/fb2reader/) |
| `html2text` | 将 HTML 页面转换为干净的 Markdown | [github.com/Alir3z4/html2text](https://github.com/Alir3z4/html2text) |

### 翻译  

| 库 | 用途 | 仓库 |
|----|------|------|
| `deep-translator` | 通过 Google Translate 等免费翻译 | [github.com/nidhaloff/deep-translator](https://github.com/nidhaloff/deep-translator) |
| `deepl` | 官方 DeepL API 客户端 | [github.com/DeepLcom/deepl-python](https://github.com/DeepLcom/deepl-python) |
| `argostranslate` | 通过 Argos Translate 进行完全离线翻译 | [github.com/argosopentech/argos-translate](https://github.com/argosopentech/argos-translate) |
| `langdetect` | 语言检测（备用算法） | [github.com/Mimino666/langdetect](https://github.com/Mimino666/langdetect) |
| `fast-langdetect` | 快速语言检测（主要算法） | [github.com/LlmKira/fast-langdetect](https://github.com/LlmKira/fast-langdetect) |

### 语言与代码检测  

| 库 | 用途 | 仓库 |
|----|------|------|
| `codelang-detect` | 从代码样本检测编程语言 | [pypi.org/project/codelang-detect](https://pypi.org/project/codelang-detect/) |
| `whats_that_code` | 独立的编程语言检测 | [github.com/matthewdeanmartin/whats_that_code](https://github.com/matthewdeanmartin/whats_that_code) |
| `badwords-py` | 脏话过滤（导入为 `badwords`） | [pypi.org/project/badwords-py](https://pypi.org/project/badwords-py/) |

### 隐私与匿名化  

| 库 | 用途 | 仓库 |
|----|------|------|
| `presidio-analyzer` | PII 检测引擎（Microsoft Presidio） | [github.com/microsoft/presidio](https://github.com/microsoft/presidio) |
| `presidio-anonymizer` | 检测到的 PII 的匿名化引擎 | [github.com/microsoft/presidio](https://github.com/microsoft/presidio) |

### 网络与代理  

| 库 | 用途 | 仓库 |
|----|------|------|
| `requests` | 用于 REST 调用和代理检查的 HTTP 客户端 | [github.com/psf/requests](https://github.com/psf/requests) |
| `httpx` | 支持异步的 HTTP 客户端，用于代理 | [github.com/encode/httpx](https://github.com/encode/httpx) |
| `free-proxy-server` | 获取和过滤免费代理列表 | [pypi.org/project/free-proxy-server](https://pypi.org/project/free-proxy-server/) |

### Web 与系统  

| 库 | 用途 | 仓库 |
|----|------|------|
| `flask` | GUI 的 Web 服务器和 REST API | [github.com/pallets/flask](https://github.com/pallets/flask) |
| `psutil` | 读取系统信息（CPU、RAM）以进行基准测试 | [github.com/giampaolo/psutil](https://github.com/giampaolo/psutil) |
| `cryptography` | 使用主密码加密对话（Fernet） | [github.com/pyca/cryptography](https://github.com/pyca/cryptography) |

### CLI、测试与打包  

| 库 | 用途 | 仓库 |
|----|------|------|
| `pytest` | 测试运行器 | [github.com/pytest-dev/pytest](https://github.com/pytest-dev/pytest) |
| `pyinstaller` | 构建独立可执行文件 | [github.com/pyinstaller/pyinstaller](https://github.com/pyinstaller/pyinstaller) |

## 模型仓库  

BiNeuron 利用精心挑选的开源代码生成模型集合，每个模型针对特定编程语言进行了微调。仓库包含来自 DeepSeek、Qwen、MiniMax、CodeLlama、Mellum 和 Wizard 等的模型。系统根据检测到的语言和用户的硬件配置自动获取合适的模型，确保每次会话都能获得最佳性能。  

> BiNeuron 融合了前沿 AI、稳健软件工程和实用性，使开发人员能够专注于创造力和解决问题，而平台则处理语言检测、文件处理和模型编排的复杂性。

</details>
