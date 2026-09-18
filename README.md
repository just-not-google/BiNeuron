<p align="center">  
  <img src="img_files/banner.png" width="100%" alt="BiNeuron Start" />  
</p>  

# BiNeuron  

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black)

<details>
<summary>🇬🇧 English</summary>

**Intelligent Code Analysis and Generation Platform**  

BiNeuron is a sophisticated software solution that bridges the gap between human intent and machine‑generated code. It unifies advanced natural language processing, optical character recognition, and adaptive model selection into a single, powerful tool designed for developers, researchers, and technical teams.  

At its core, BiNeuron automatically identifies the programming language of a given request, extracts content from a wide array of file formats—including images and documents—and then generates context‑aware, production‑ready code using best‑in‑class local or cloud‑based language models.

## Key Capabilities  

### Programming Language Detection  
- Supports over 25 programming languages, including Python, Java, C/C++, C#, JavaScript, TypeScript, Go, Rust, Swift, Kotlin, Ruby, Dart, Julia, Lua, SQL, MATLAB, R, Pascal, Assembly, Fortran, F#, Ada, Zig, PHP, Shell, Scala, and more.  
- Combines heuristic algorithms, proprietary keyword matching, and AI‑powered orchestration to achieve high detection accuracy.  
- Analyzes both user‑supplied text and the content of attached files, or even entire directories.  

### Comprehensive File Handling  
- Extracts and translates text from common document formats: PDF, Word (DOCX), ODF, and PowerPoint (PPTX).  
- Processes source code files in nearly all text‑based formats, from plain text to configuration files.  
- Integrates advanced OCR (DeepSeek OCR or EasyOCR) to read text from images, with optional GPU acceleration and automatic splitting of large images for improved recognition.  

### AI-Powered File Editing  
- **Two‑Stage Pipeline**: The primary AI model generates the code/response. A secondary, lightweight model (e.g., Qwen2.5-Coder-1.5B) then transforms the response into a strict JSON object containing absolute file paths and full new contents.  
- **Full Context Awareness**: The JSON formatter receives the complete file context (all read files, unread file names, project root, and the primary AI’s answer) to ensure accurate path generation and content mapping.  
- **Robust Retry Mechanism**: If the JSON fails validation, the system automatically re‑prompts the formatter up to `retries` times, logging each attempt until a valid JSON is produced or the maximum retries are exhausted.  
- **Safe, Whole‑File Replacements**: Only whole-file replacements are supported (no partial edits) to maintain consistency and safety.  
- **Optional File Deletion**: When `deleting_files=True` is passed to the `BiNeuron` constructor, the JSON formatter may return `null` for a file path, and the system will safely delete that file. This feature is disabled by default to prevent accidental data loss.

### Adaptive Model Selection  
- Automatically assesses the user’s hardware capabilities (CPU cores, frequency, RAM) and selects the optimal quantized version of the target model (ranging from IQ2 to F16) to balance speed and accuracy.  
- Offers a curated repository of specialised models per programming language, ensuring high‑quality, idiomatic code generation.  

### Robust Networking  
- Implements multi‑layered accessibility to Hugging Face models, including automatic fallback to hf‑mirror.com, dynamic proxy selection, and support for custom proxy lists.  
- Fetches and verifies public proxies from GitHub raw lists, with retry mechanisms and connection health checks.  

### Virtual Storage Mode  
- Allows scanning and processing of entire folders or mounted virtual directories.  
- Recursively identifies supported files, extracts their content, and incorporates it into the analysis context - perfect for large codebases or repositories.  
- **Interactive File Explorer**: In GUI mode, the virtual storage is displayed as a tree view. Double‑click any file to open it in the default system application.  

### Multilingual Translation  
- Built‑in translation engine normalises user requests to English (or any configured target language) to ensure consistent AI interactions.  
- Supports both Google Translate and DeepL, with automatic fallback when network restrictions are detected.  
- **Offline Translation**: Optional ArgosTranslate integration (`local_trans=True`, `from_code_lang='en'`) provides fully offline translation without relying on external APIs.

## Architecture  

BiNeuron is engineered with a modular, separation‑of‑concerns design:  

- **Core Engine** - orchestrates the entire pipeline: request parsing, language detection, model selection, and response generation.  
- **OCR Module** - handles text extraction from images and scanned documents via DeepSeek OCR or EasyOCR.  
- **Model Downloader** - manages downloading and caching of Hugging Face models, with built‑in mirror and proxy support.  
- **JSON Formatter Module** - uses a lightweight model (e.g., Qwen2.5-Coder-1.5B) to convert the primary model’s response into a strict JSON object for file modifications.  
- **File Editing Module** - applies JSON‑based file changes (whole-file replacements) with error handling and retry logic. Supports optional file deletion when `deleting_files=True`.  
- **Translation Service** - provides language detection and translation utilities, with optional DeepL and ArgosTranslate integration.  
- **Network Layer** - implements proxy rotation, availability checks, and GitHub proxy fetching for circumventing restrictions.  
- **Web Interface** - a feature‑rich web application built with Flask (HTML/CSS/JS).

The architecture emphasises reusability, fault tolerance, and performance, allowing each component to operate independently while seamlessly integrating with the others.  

## Graphical Interface  

<p align="center">
  <img src="img_files/gui_screenshot_2.png" width="80%" alt="BiNeuron GUI Screenshot" />
</p>

A modern web application built with Flask, offering:  
- **Intuitive Chat Interface** - message history, file attachments, and real‑time log display.  
- **Virtual Storage Explorer** - scan and navigate directories in a tree view.  
- **Comprehensive Settings Panel** - fine‑tune every aspect of the platform: network, model selection, OCR, translation, and more.  
- **Chat Management** - create, delete, download, and filter conversation history.  
- **Live Logging** - see what the AI is doing in real time.  
- **Dark Theme** - optimized for long coding sessions.  

The application is designed to be user‑friendly, allowing developers to focus on coding while the AI handles the heavy lifting of language detection, file processing, and model orchestration.

## Development  

Only the interface and the interaction with the interface were developed with the help of **DeepSeek Coder**. This includes the Flask‑based web UI, the JavaScript front‑end, and the user interaction logic. All other components - the core engine, OCR module, model downloader, JSON formatter, file editing module, translation service, network layer, and overall architecture - were designed and written independently.

- **Model Collection**: [deepseek-ai/deepseek-coder](https://huggingface.co/collections/deepseek-ai/deepseek-coder)  
- **Example Model**: [deepseek-ai/deepseek-coder-6.7b-instruct](https://huggingface.co/deepseek-ai/deepseek-coder-6.7b-instruct)

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

### Networking & Proxies  

| Library | Purpose | Repository |
|---------|---------|-----------|
| `requests` | HTTP client for REST calls and proxy checks | [github.com/psf/requests](https://github.com/psf/requests) |
| `httpx` | Async-capable HTTP client used with proxies | [github.com/encode/httpx](https://github.com/encode/httpx) |
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

BiNeuron leverages a hand‑picked collection of open‑source code generation models, each fine‑tuned for specific programming languages. The repository includes models from DeepSeek, Qwen, MiniMax, CodeLlama, Mellum, and Wizard, among others. The system automatically fetches the appropriate model based on the detected language and the user’s hardware profile, ensuring optimal performance for every session.  

> BiNeuron represents a fusion of cutting‑edge AI, robust software engineering, and practical usability - empowering developers to focus on creativity and problem‑solving while the platform handles the complexities of language detection, file processing, and model orchestration.

</details>

<details>
<summary>🇷🇺 Русский</summary>

**Интеллектуальная платформа для анализа и генерации кода**  

BiNeuron - это сложное программное решение, которое устраняет разрыв между намерениями человека и машинным кодом. Он объединяет продвинутую обработку естественного языка, оптическое распознавание символов и адаптивный выбор модели в единый мощный инструмент, предназначенный для разработчиков, исследователей и технических групп.  

По своей сути, BiNeuron автоматически определяет язык программирования для данного запроса, извлекает содержимое из широкого спектра форматов файлов, включая изображения и документы, а затем генерирует контекстно‑зависимый, готовый к работе код, используя лучшие в своем классе локальные или облачные языковые модели.

## Ключевые возможности  

### Определение языка программирования  
- Поддерживает более 25 языков программирования, включая Python, Java, C/C++, C#, JavaScript, TypeScript, Go, Rust, Swift, Kotlin, Ruby, Dart, Julia, Lua, SQL, MATLAB, R, Pascal, Assembly, Fortran, F#, Ada, Zig, PHP, Shell, Scala и другие.  
- Объединяет эвристические алгоритмы, фирменный поиск по ключевым словам и ИИ‑управляемую оркестрацию для высокой точности определения.  
- Анализирует как текст, введённый пользователем, так и содержимое прикреплённых файлов или даже целых каталогов.  

### Всесторонняя обработка файлов  
- Извлекает и преобразует текст из распространённых форматов документов: PDF, Word (DOCX), ODF и PowerPoint (PPTX).  
- Обрабатывает файлы исходного кода почти во всех текстовых форматах - от обычного текста до конфигурационных файлов.  
- Интегрирует продвинутое OCR (DeepSeek OCR или EasyOCR) для чтения текста из изображений, с опциональным ускорением на GPU и автоматическим разбиением больших изображений для улучшенного распознавания.  

### Изменение файлов с помощью ИИ  
- **Двухэтапный пайплайн**: Основная ИИ-модель генерирует код/ответ. Вторичная лёгкая модель (например, Qwen2.5-Coder-1.5B) преобразует этот ответ в строгий JSON-объект, содержащий абсолютные пути к файлам и новое полное содержимое.  
- **Полный контекст**: Форматтер JSON получает весь контекст файлов (все прочитанные файлы, имена непрочитанных файлов, корень проекта и ответ основной ИИ-модели) для точной генерации путей и содержимого.  
- **Надёжный механизм повторных попыток**: Если JSON не проходит валидацию, система автоматически перезапрашивает форматтер до `retries` раз, логируя каждую попытку, пока не будет получен валидный JSON или не будут исчерпаны все попытки.  
- **Безопасная замена целых файлов**: Поддерживается только полная замена файлов (не частичное редактирование) для обеспечения согласованности и безопасности.  
- **Опциональное удаление файлов**: При передаче `deleting_files=True` в конструктор `BiNeuron` JSON-форматтер может вернуть `null` для пути к файлу, и система безопасно удалит этот файл. По умолчанию функция отключена во избежание случайной потери данных.

### Адаптивный выбор модели  
- Автоматически оценивает аппаратные возможности пользователя (количество ядер CPU, частота, ОЗУ) и выбирает оптимальную квантизованную версию целевой модели (от IQ2 до F16) для баланса скорости и точности.  
- Предлагает специально подобранный репозиторий моделей для каждого языка программирования, обеспечивая высококачественную и идиоматичную генерацию кода.  

### Надёжные сетевые возможности  
- Реализует многоуровневый доступ к моделям Hugging Face, включая автоматическое переключение на hf‑mirror.com, динамический выбор прокси и поддержку пользовательских списков прокси.  
- Загружает и проверяет публичные прокси из списков GitHub, с повторными попытками и проверкой работоспособности соединений.  

### Режим виртуального хранилища  
- Позволяет сканировать и обрабатывать целые папки или смонтированные виртуальные директории.  
- Рекурсивно определяет поддерживаемые файлы, извлекает их содержимое и включает его в контекст анализа - идеально для больших кодовых баз или репозиториев.  
- **Интерактивный файловый менеджер**: В режиме GUI виртуальное хранилище отображается в виде дерева. Двойной клик по файлу открывает его в системном приложении по умолчанию.  

### Многоязычный перевод  
- Встроенный механизм перевода приводит запросы пользователя к английскому (или любому другому настроенному языку) для единообразного взаимодействия с ИИ.  
- Поддерживает Google Translate и DeepL с автоматическим переключением при обнаружении сетевых ограничений.  
- **Офлайн-перевод**: Опциональная интеграция ArgosTranslate (`local_trans=True`, `from_code_lang='en'`) обеспечивает полностью офлайн-перевод без обращения к внешним API.

## Архитектура  

BiNeuron спроектирован по модульному принципу с разделением ответственности:  

- **Основной движок** - управляет всем конвейером: разбор запроса, определение языка, выбор модели и генерация ответа.  
- **Модуль OCR** - обрабатывает извлечение текста из изображений и отсканированных документов через DeepSeek OCR или EasyOCR.  
- **Загрузчик моделей** - управляет загрузкой и кэшированием моделей Hugging Face со встроенной поддержкой зеркал и прокси.  
- **Модуль JSON-форматтера** - использует лёгкую модель (например, Qwen2.5-Coder-1.5B) для преобразования ответа основной модели в строгий JSON для изменения файлов.  
- **Модуль редактирования файлов** - применяет изменения на основе JSON (полная замена файлов) с обработкой ошибок и повторными попытками. Поддерживает опциональное удаление файлов при `deleting_files=True`.  
- **Сервис перевода** - предоставляет функции определения языка и перевода, с опциональной интеграцией DeepL и ArgosTranslate.  
- **Сетевой уровень** - реализует ротацию прокси, проверку доступности и получение прокси из GitHub для обхода ограничений.  
- **Веб-интерфейс** - функциональное веб-приложение на Flask (HTML/CSS/JS).

Архитектура делает упор на переиспользуемость, отказоустойчивость и производительность, позволяя каждому компоненту работать независимо, но при этом бесшовно интегрироваться с другими.  

## Графический интерфейс  

<p align="center">
  <img src="img_files/gui_screenshot_2.png" width="80%" alt="Скриншот GUI BiNeuron" />
</p>

Современное веб-приложение на Flask, предлагающее:  
- **Интуитивный чат** - история сообщений, прикрепление файлов и отображение логов в реальном времени.  
- **Обозреватель виртуального хранилища** - сканирование и навигация по директориям в виде дерева.  
- **Всеобъемлющая панель настроек** - тонкая настройка каждого аспекта платформы: сеть, выбор модели, OCR, перевод и многое другое.  
- **Управление чатами** - создание, удаление, загрузка и фильтрация истории диалогов.  
- **Live‑логи** - просмотр действий ИИ в реальном времени.  
- **Тёмная тема** - оптимизирована для длительных сессий разработки.  

Приложение разработано с упором на удобство, позволяя разработчикам сосредоточиться на коде, пока ИИ берёт на себя сложности определения языка, обработки файлов и оркестрации моделей.

## Разработка  

Только интерфейс и взаимодействие с интерфейсом были разработаны с помощью **DeepSeek Coder**. Это включает веб-интерфейс на Flask, JavaScript-фронтенд и логику взаимодействия с пользователем. Все остальные компоненты - основной движок, модуль OCR, загрузчик моделей, JSON-форматтер, модуль редактирования файлов, сервис перевода, сетевой уровень и общая архитектура - были спроектированы и написаны самостоятельно.

- **Коллекция моделей**: [deepseek-ai/deepseek-coder](https://huggingface.co/collections/deepseek-ai/deepseek-coder)  
- **Пример модели**: [deepseek-ai/deepseek-coder-6.7b-instruct](https://huggingface.co/deepseek-ai/deepseek-coder-6.7b-instruct)

## Зависимости  

Полный список библиотек, используемых в BiNeuron (ровно то, что объявлено в `requirements.txt`).

### Ядро и ИИ  

| Библиотека | Назначение | Репозиторий |
|-----------|------------|------------|
| `torch` | Тензорные вычисления и GPU-ускорение для локальных моделей | [github.com/pytorch/pytorch](https://github.com/pytorch/pytorch) |
| `transformers` | Загрузка и запуск моделей Hugging Face локально | [github.com/huggingface/transformers](https://github.com/huggingface/transformers) |
| `huggingface_hub` | Скачивание и кэширование моделей с Hugging Face | [github.com/huggingface/huggingface_hub](https://github.com/huggingface/huggingface_hub) |
| `llama-cpp-python` | Запуск GGUF-моделей через привязки llama.cpp | [github.com/abetlen/llama-cpp-python](https://github.com/abetlen/llama-cpp-python) |
| `pillow` | Загрузка и предобработка изображений для OCR и vision-моделей | [github.com/python-pillow/Pillow](https://github.com/python-pillow/Pillow) |

### OCR  

| Библиотека | Назначение | Репозиторий |
|-----------|------------|------------|
| `easyocr` | OCR-движок для извлечения текста из изображений | [github.com/JaidedAI/EasyOCR](https://github.com/JaidedAI/EasyOCR) |
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

### Перевод  

| Библиотека | Назначение | Репозиторий |
|-----------|------------|------------|
| `deep-translator` | Бесплатный перевод через Google Translate и др. | [github.com/nidhaloff/deep-translator](https://github.com/nidhaloff/deep-translator) |
| `deepl` | Официальный клиент DeepL API | [github.com/DeepLcom/deepl-python](https://github.com/DeepLcom/deepl-python) |
| `argostranslate` | Полностью офлайн-перевод через Argos Translate | [github.com/argosopentech/argos-translate](https://github.com/argosopentech/argos-translate) |
| `langdetect` | Определение языка (резервный алгоритм) | [github.com/Mimino666/langdetect](https://github.com/Mimino666/langdetect) |
| `fast-langdetect` | Быстрое определение языка (основной алгоритм) | [github.com/LlmKira/fast-langdetect](https://github.com/LlmKira/fast-langdetect) |

### Определение языка и кода  

| Библиотека | Назначение | Репозиторий |
|-----------|------------|------------|
| `codelang-detect` | Определение языка программирования по образцу кода | [pypi.org/project/codelang-detect](https://pypi.org/project/codelang-detect/) |
| `whats_that_code` | Независимое определение языка программирования | [github.com/matthewdeanmartin/whats_that_code](https://github.com/matthewdeanmartin/whats_that_code) |
| `badwords-py` | Фильтрация ненормативной лексики (импортируется как `badwords`) | [pypi.org/project/badwords-py](https://pypi.org/project/badwords-py/) |

### Сеть и прокси  

| Библиотека | Назначение | Репозиторий |
|-----------|------------|------------|
| `requests` | HTTP-клиент для REST-запросов и проверки прокси | [github.com/psf/requests](https://github.com/psf/requests) |
| `httpx` | HTTP-клиент с поддержкой async, используется с прокси | [github.com/encode/httpx](https://github.com/encode/httpx) |
| `free-proxy-server` | Получение и фильтрация списков бесплатных прокси | [pypi.org/project/free-proxy-server](https://pypi.org/project/free-proxy-server/) |

### Веб и система  

| Библиотека | Назначение | Репозиторий |
|-----------|------------|------------|
| `flask` | Веб-сервер и REST API для GUI | [github.com/pallets/flask](https://github.com/pallets/flask) |
| `psutil` | Чтение системной информации (CPU, RAM) для бенчмарка | [github.com/giampaolo/psutil](https://github.com/giampaolo/psutil) |
| `cryptography` | Шифрование чатов мастер-паролем (Fernet) | [github.com/pyca/cryptography](https://github.com/pyca/cryptography) |

### CLI, тестирование и упаковка  

| Библиотека | Назначение | Репозиторий |
|-----------|------------|------------|
| `pytest` | Запуск тестов | [github.com/pytest-dev/pytest](https://github.com/pytest-dev/pytest) |
| `pyinstaller` | Сборка standalone-исполняемых файлов | [github.com/pyinstaller/pyinstaller](https://github.com/pyinstaller/pyinstaller) |

## Репозиторий моделей  

BiNeuron использует тщательно подобранную коллекцию открытых моделей генерации кода, каждая из которых дообучена для конкретных языков программирования. В репозиторий входят модели от DeepSeek, Qwen, MiniMax, CodeLlama, Mellum, Wizard и других. Система автоматически загружает подходящую модель на основе определённого языка и аппаратного профиля пользователя, обеспечивая оптимальную производительность в каждом сеансе.  

> BiNeuron представляет собой синтез передового ИИ, надёжной инженерии и практической полезности, позволяя разработчикам сосредоточиться на творчестве и решении задач, пока платформа берёт на себя сложности определения языка, обработки файлов и оркестрации моделей.

</details>

<details>
<summary>🇨🇳 中文</summary>

**智能代码分析与生成平台**  

BiNeuron 是一个先进的软件解决方案，旨在弥合人类意图与机器生成代码之间的鸿沟。它将先进的自然语言处理、光学字符识别和自适应模型选择整合到一个功能强大的工具中，专为开发者、研究人员和技术团队设计。  

其核心功能是自动识别给定请求的编程语言，从包括图像和文档在内的多种文件格式中提取内容，然后使用一流本地或云端语言模型生成上下文感知、可用于生产的代码。

## 主要功能  

### 编程语言检测  
- 支持超过 25 种编程语言，包括 Python、Java、C/C++、C#、JavaScript、TypeScript、Go、Rust、Swift、Kotlin、Ruby、Dart、Julia、Lua、SQL、MATLAB、R、Pascal、Assembly、Fortran、F#、Ada、Zig、PHP、Shell、Scala 等。  
- 结合启发式算法、专有关键词匹配和 AI 驱动的编排，实现高检测精度。  
- 分析用户提供的文本以及附加文件内容，甚至整个目录。  

### 全面的文件处理  
- 从常见文档格式中提取和转换文本：PDF、Word（DOCX）、ODF 和 PowerPoint（PPTX）。  
- 处理几乎所有基于文本格式的源代码文件，从纯文本到配置文件。  
- 集成先进的 OCR（DeepSeek OCR 或 EasyOCR）从图像中读取文本，支持可选的 GPU 加速，并可自动分割大图像以提高识别效果。  

### AI 驱动的文件编辑  
- **两阶段流水线**：主 AI 模型生成代码/响应。随后，一个轻量级辅助模型（例如 Qwen2.5-Coder-1.5B）将该响应转换为严格的 JSON 对象，其中包含绝对文件路径和完整的新内容。  
- **完整上下文感知**：JSON 格式化器接收完整的文件上下文（所有已读文件、未读文件名、项目根目录以及主 AI 的回答），以确保准确的路径生成和内容映射。  
- **强大的重试机制**：如果 JSON 验证失败，系统会自动重新提示格式化器，最多重试 `retries` 次，并记录每次尝试，直到生成有效 JSON 或达到最大重试次数。  
- **安全的整文件替换**：仅支持整文件替换（不支持部分编辑），以保持一致性和安全性。  
- **可选文件删除**：当向 `BiNeuron` 构造函数传递 `deleting_files=True` 时，JSON 格式化器可能为文件路径返回 `null`，系统将安全删除该文件。此功能默认禁用，以防止意外数据丢失。

### 自适应模型选择  
- 自动评估用户的硬件能力（CPU 核心数、频率、RAM），并选择目标模型的最佳量化版本（从 IQ2 到 F16），以平衡速度和精度。  
- 为每种编程语言提供精选的专用模型仓库，确保生成高质量、地道的代码。  

### 强大的网络功能  
- 实现对 Hugging Face 模型的多层访问，包括自动回退到 hf‑mirror.com、动态代理选择以及自定义代理列表支持。  
- 从 GitHub 原始列表中获取并验证公共代理，具有重试机制和连接健康检查。  

### 虚拟存储模式  
- 允许扫描和处理整个文件夹或挂载的虚拟目录。  
- 递归识别支持的文件，提取其内容并将其纳入分析上下文——非常适合大型代码库或仓库。  
- **交互式文件浏览器**：在 GUI 模式下，虚拟存储以树形视图显示。双击任何文件可在默认系统应用程序中打开。  

### 多语言翻译  
- 内置翻译引擎将用户请求标准化为英语（或任何配置的目标语言），以确保一致的 AI 交互。  
- 支持 Google Translate 和 DeepL，检测到网络限制时自动回退。  
- **离线翻译**：可选的 ArgosTranslate 集成（`local_trans=True`，`from_code_lang='en'`）提供完全离线的翻译，无需依赖外部 API。

## 架构  

BiNeuron 采用模块化、关注点分离的设计：  

- **核心引擎** - 编排整个流水线：请求解析、语言检测、模型选择和响应生成。  
- **OCR 模块** - 通过 DeepSeek OCR 或 EasyOCR 处理图像和扫描文档中的文本提取。  
- **模型下载器** - 管理 Hugging Face 模型的下载和缓存，内置镜像和代理支持。  
- **JSON 格式化器模块** - 使用轻量级模型（例如 Qwen2.5-Coder-1.5B）将主模型的响应转换为严格的 JSON 对象以用于文件修改。  
- **文件编辑模块** - 应用基于 JSON 的文件更改（整文件替换），具备错误处理和重试逻辑。当 `deleting_files=True` 时支持可选的文件删除。  
- **翻译服务** - 提供语言检测和翻译工具，可选集成 DeepL 和 ArgosTranslate。  
- **网络层** - 实现代理轮换、可用性检查以及从 GitHub 获取代理以规避限制。  
- **Web 界面** - 使用 Flask（HTML/CSS/JS）构建的功能丰富的 Web 应用程序。

该架构强调可重用性、容错性和性能，允许每个组件独立运行，同时与其他组件无缝集成。  

## 图形界面  

<p align="center">
  <img src="img_files/gui_screenshot_2.png" width="80%" alt="BiNeuron GUI 截图" />
</p>

使用 Flask 构建的现代 Web 应用程序，提供：  
- **直观的聊天界面** - 消息历史、文件附件和实时日志显示。  
- **虚拟存储浏览器** - 以树形视图扫描和导航目录。  
- **全面的设置面板** - 微调平台的每个方面：网络、模型选择、OCR、翻译等。  
- **聊天管理** - 创建、删除、下载和筛选对话历史。  
- **实时日志** - 实时查看 AI 的操作。  
- **深色主题** - 针对长时间编码会话进行优化。  

该应用程序设计为易于使用，使开发人员可以专注于编码，而 AI 处理语言检测、文件处理和模型编排的繁重工作。

## 开发  

只有界面和与界面的交互是在 **DeepSeek Coder** 的帮助下开发的。这包括基于 Flask 的 Web UI、JavaScript 前端以及用户交互逻辑。所有其他组件——核心引擎、OCR 模块、模型下载器、JSON 格式化器、文件编辑模块、翻译服务、网络层以及整体架构——均为独立设计和编写。

- **模型集合**: [deepseek-ai/deepseek-coder](https://huggingface.co/collections/deepseek-ai/deepseek-coder)  
- **示例模型**: [deepseek-ai/deepseek-coder-6.7b-instruct](https://huggingface.co/deepseek-ai/deepseek-coder-6.7b-instruct)

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