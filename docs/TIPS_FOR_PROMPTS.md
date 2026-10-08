<details>
<summary>🇬🇧 English</summary>

# Guidelines for Crafting Effective Prompts for AI

To obtain the most accurate and relevant responses from AI models inside BiNeuron, it is essential to structure your prompts thoughtfully. This guide outlines proven practices and lists all file formats that BiNeuron can accept, helping you get the best possible results.

---

## Core Principles

### 1. Use English When Possible
Most advanced AI models are trained primarily on English language data. Writing your prompt in English significantly improves recognition, understanding, and response quality. If English is not your native language, simple and clear English is still preferable to other languages in most cases.

### 2. Specify Programming Languages Explicitly
BiNeuron detects the programming language of your request and attaches a specialised model tuned for that language. To make the most of this, always mention the exact programming language you need. For example, state "Python 3.11" or "JavaScript (ES2022)" rather than just "code". This activates the language specific subsystem (`MODELS_DICT`) and routes your prompt to the model that was fine tuned for that language.

### 3. Provide Detailed Task Descriptions
Vague requests yield vague answers. Include:
- Input and output specifications (data types, formats, examples)
- Edge cases or constraints (performance, memory limits)
- Desired behaviour under error conditions
- Any relevant business logic or domain context

**Instead of:**  
> *"Write a function to sort an array."*

**Prefer:**  
> *"Write a Python function that takes a list of integers and returns a new list sorted in ascending order using the quicksort algorithm. Include type hints, docstrings, and handle empty lists gracefully."*

### 4. List Your Technology Stack
If you know which frameworks, libraries, or tools will be used, state their full names and versions. For instance:
- "Use Django 4.2 with PostgreSQL 15"
- "Implement using React 18 and TypeScript 5"
- "Run on Node.js 20 with Express 4"

This allows the AI to tailor the code to your ecosystem, avoiding incompatible APIs or outdated patterns.

### 5. Attach Relevant Files When You Can
BiNeuron can read the content of attached files and merge it into the request context. If your task depends on existing source code, configuration files, or documentation, attach them instead of pasting fragments into the prompt. The virtual storage mode also lets you point BiNeuron at an entire folder, so the full project structure becomes part of the context.

### 6. Choose the Right Prompt Mode
BiNeuron ships with several pre built system prompt scenarios (`default`, `testing`, `explanation`, `no_comments`, `refactor`, `debug`, `code_review`, `documentation`, `scaffold`, `security_hardening`, `algorithm_strategy`). Pick the mode that matches your goal, or provide a custom system prompt if none of the presets fits.

### 7. Enable Request Improvement and Compression When Useful
If your prompt is short and chaotic, enable `improving_user_experience` so a local small model restructures it before it reaches the main AI. If you attach a lot of files, enable `compress_text` so the assembled context is compressed without losing technical facts, numbers, or code fragments.

### 8. Consider Privacy Settings
If your request contains personal data, enable `anonymize_text` so Microsoft Presidio replaces names, emails, phone numbers, and other PII before the request reaches translation services or the AI. If you want to block aggressive language, enable `filter_for_swearing`.

---

## Supported File Formats for Processing

BiNeuron accepts and processes files in the following formats. They are grouped into three categories for clarity.

> **Note on extensions:** the lists below reflect the extensions actually recognised by the runtime. Some code file extensions that are not listed in the primary router (for example exotic or framework specific ones) are still opened as plain text, but they are **not** considered first class supported formats.

### Programming Language Files

| Extension(s) | Language / Purpose |
|--------------|-------------------|
| `.py`, `.pyw`, `.pyi`, `.pyx` | Python |
| `.java` | Java |
| `.c`, `.h` | C |
| `.cpp`, `.cc`, `.cxx`, `.c++`, `.hpp`, `.hh`, `.hxx`, `.ipp` | C++ |
| `.cs` | C# |
| `.js`, `.mjs`, `.cjs` | JavaScript |
| `.ts`, `.tsx` | TypeScript |
| `.go` | Go |
| `.rs` | Rust |
| `.swift` | Swift |
| `.kt`, `.kts` | Kotlin |
| `.php`, `.php3`, `.php4`, `.php5`, `.phtml` | PHP |
| `.rb`, `.rbw`, `.rake`, `.gemspec` | Ruby |
| `.dart` | Dart |
| `.r`, `.R`, `.Rmd` | R |
| `.jl` | Julia |
| `.lua` | Lua |
| `.sql` | SQL |
| `.scala`, `.sc` | Scala |
| `.pl`, `.pm`, `.t` | Perl |
| `.hs`, `.lhs` | Haskell |
| `.erl`, `.hrl` | Erlang |
| `.ex`, `.exs` | Elixir |
| `.clj`, `.cljs`, `.cljc` | Clojure |
| `.groovy`, `.gvy` | Groovy |
| `.vb`, `.vbs` | Visual Basic |
| `.sh`, `.bash`, `.zsh`, `.ksh`, `.csh`, `.fish` | Shell scripts |
| `.ps1`, `.psm1`, `.psd1` | PowerShell |
| `.bat`, `.cmd` | Windows batch files |

### Text, Configuration, and Markup Formats

| Extension(s) | Purpose |
|--------------|---------|
| `.txt`, `.log` | Plain text and log files |
| `.md`, `.markdown`, `.rst` | Documentation (Markdown, reStructuredText) |
| `.tex`, `.ltx`, `.bib` | TeX and LaTeX documents and bibliographies |
| `.csv`, `.tsv` | Tabular data (comma or tab separated) |
| `.json`, `.jsonl` | JSON and JSON Lines |
| `.xml`, `.xsd`, `.xsl`, `.xslt` | XML and related schemas and transformations |
| `.yaml`, `.yml` | YAML |
| `.toml` | TOML |
| `.ini`, `.cfg`, `.conf`, `.properties` | Configuration files |
| `.env` | Environment variable files |
| `.editorconfig` | Editor configuration |
| `.gitignore` | Git ignore lists |
| `.dockerfile` | Dockerfile |
| `.makefile` | Makefile |
| `.cmake`, `.cmakelists.txt` | CMake build files |
| `.html`, `.htm`, `.xhtml` | HTML and XHTML |
| `.css`, `.scss`, `.sass`, `.less` | Stylesheets |
| `.rss`, `.atom` | Web feeds |

### Binary and Document Formats

All formats in this section are **actually parsed** by the runtime. Each has a dedicated extractor in `getting_text_from_files.py`.

| Extension(s) | Type | Extractor |
|--------------|------|-----------|
| `.pdf` | Portable Document Format | PyMuPDF |
| `.docx` | Microsoft Word (Office Open XML) | `docx2txt` |
| `.word` | Legacy alias, treated as plain text | plain read |
| `.odf` | OpenDocument Format | `odfdo` |
| `.pptx` | PowerPoint presentation | `pptx2txt2` |
| `.xlsx`, `.xls` | Microsoft Excel spreadsheets | MarkItDown |
| `.epub` | EPUB e book | `epub2txt` |
| `.mobi` | Mobipocket e book | `mobi` |
| `.fb2` | FictionBook 2 | `fb2reader` |

### Image Formats (OCR)

Images are processed through the OCR pipeline. BiNeuron supports two interchangeable engines: EasyOCR and DeepSeek OCR. You can pick the engine, the language list, and whether to use GPU acceleration or crop mode for large images.

| Extension(s) | Type |
|--------------|------|
| `.jpg`, `.jpeg`, `.png`, `.bmp`, `.gif`, `.webp`, `.tiff`, `.tif` | Raster images |

### Website Sources

If `use_websites` is enabled, BiNeuron can fetch text from any URL you provide in the settings and merge it into the context. The scraper uses an HTML to text conversion so the AI receives clean Markdown instead of raw markup.

---

## Example of a Well Structured Prompt

**Weak prompt:**  
> *"Write code for a web scraper."*

**Strong prompt:**  
> *"Develop a Python 3.11 script using BeautifulSoup 4 and Requests 2.31 that scrapes product names and prices from https://example.com/products. The script should accept a URL as a command line argument, output results as a CSV file with columns 'name' and 'price', and handle pagination by following 'Next' links. Include error handling for network timeouts and missing elements."*

This prompt is specific, actionable, and includes all necessary context.

---

## Working With Automatic File Editing

If you enable `editing_files` in the settings, BiNeuron uses a two stage pipeline: the primary AI generates the answer, then a lightweight JSON formatter converts that answer into a strict object that maps absolute file paths to new file contents. To get the best results:

- Always provide the project root path in your prompt or via virtual storage so the AI can build correct absolute paths.
- Mention the exact file names you want to create or modify.
- Expect whole file replacements only. Partial edits are not supported for safety reasons.
- If you also enable `deleting_files`, the AI can mark a file with a `null` value to request safe deletion.

---

## Final Tips

- **Be concise but complete**: avoid irrelevant background, but do not omit crucial details.
- **Use bullet points** for complex requirements: they improve readability.
- **Specify output format**: tell the AI whether you need code only, code with comments, or a full explanation.
- **Mention constraints**: for example, "must run on Windows", "must be compatible with Python 3.8 or newer", "must not use external libraries".
- **Preview before sending**: use the Preview Request button in the Cloud AI settings group to inspect the exact system prompt, translated request, file context, and attached file list that will be sent to the AI.

By following these guidelines, you will harness the full potential of BiNeuron, saving time and receiving high quality, tailored solutions.

</details>

<details>
<summary>🇷🇺 Русский</summary>

# Рекомендации по составлению эффективных запросов для ИИ

Чтобы получать от ИИ моделей внутри BiNeuron наиболее точные и релевантные ответы, важно продуманно структурировать свои запросы. Данное руководство описывает проверенные практики и перечисляет все форматы файлов, которые BiNeuron может обрабатывать, помогая вам добиваться наилучших результатов.

---

## Основные принципы

### 1. По возможности используйте английский язык
Большинство современных ИИ моделей обучаются преимущественно на англоязычных данных. Запрос на английском языке значительно улучшает распознавание, понимание и качество ответа. Если английский не является вашим родным языком, простой и понятный английский всё равно предпочтительнее других языков в большинстве случаев.

### 2. Чётко указывайте языки программирования
BiNeuron определяет язык программирования вашего запроса и подключает специализированную модель, настроенную на этот язык. Чтобы использовать это максимально эффективно, всегда точно называйте нужный язык программирования. Например, указывайте «Python 3.11» или «JavaScript (ES2022)», а не просто «код». Это активирует подсистему конкретного языка (`MODELS_DICT`) и направит запрос в модель, которая была дообучена под этот язык.

### 3. Давайте подробное описание задачи
Расплывчатые запросы приводят к расплывчатым ответам. Включайте:
- Спецификацию входных и выходных данных (типы данных, форматы, примеры)
- Краевые случаи или ограничения (производительность, лимиты памяти)
- Желаемое поведение при ошибках
- Любую релевантную бизнес логику или предметную область

**Вместо:**  
> *«Напишите функцию для сортировки массива.»*

**Лучше:**  
> *«Напишите функцию на Python, которая принимает список целых чисел и возвращает новый список, отсортированный по возрастанию с использованием алгоритма быстрой сортировки. Включите аннотации типов, строки документации и корректно обрабатывайте пустые списки.»*

### 4. Перечисляйте ваш технологический стек
Если вы знаете, какие фреймворки, библиотеки или инструменты будут использоваться, укажите их полные названия и версии. Например:
- «Использовать Django 4.2 с PostgreSQL 15»
- «Реализовать на React 18 и TypeScript 5»
- «Запускать на Node.js 20 с Express 4»

Это позволит ИИ адаптировать код под вашу экосистему, избегая несовместимых API или устаревших шаблонов.

### 5. Прикрепляйте релевантные файлы
BiNeuron умеет читать содержимое прикреплённых файлов и добавлять его в контекст запроса. Если ваша задача зависит от существующего исходного кода, конфигураций или документации, прикрепляйте их вместо вставки фрагментов прямо в текст. Режим виртуального хранилища позволяет указать целую папку, и структура проекта целиком становится частью контекста.

### 6. Выбирайте правильный режим промпта
BiNeuron содержит несколько готовых сценариев системного промпта (`default`, `testing`, `explanation`, `no_comments`, `refactor`, `debug`, `code_review`, `documentation`, `scaffold`, `security_hardening`, `algorithm_strategy`). Выбирайте режим, соответствующий вашей цели, или задайте собственный системный промпт, если ни один из пресетов не подходит.

### 7. Включайте улучшение и сжатие запроса при необходимости
Если ваш запрос короткий и неструктурированный, включите `improving_user_experience`, чтобы локальная малая модель переписала его перед отправкой основной ИИ. Если вы прикрепляете много файлов, включите `compress_text`, чтобы собранный контекст был сжат без потери технических фактов, чисел и фрагментов кода.

### 8. Учитывайте настройки приватности
Если запрос содержит персональные данные, включите `anonymize_text`, чтобы Microsoft Presidio заменил имена, email, телефоны и другие PII перед отправкой в сервисы перевода или ИИ. Если нужно заблокировать агрессивную лексику, включите `filter_for_swearing`.

---

## Поддерживаемые форматы файлов для обработки

BiNeuron принимает и обрабатывает файлы следующих форматов. Для ясности они сгруппированы в три категории.

> **Примечание о расширениях:** списки ниже отражают расширения, которые реально распознаются во время работы. Некоторые расширения кода, не указанные в основном маршрутизаторе (экзотические или специфичные для фреймворков), всё равно открываются как обычный текст, но они **не** считаются полноценно поддерживаемыми форматами.

### Файлы языков программирования

| Расширение(я) | Язык / Назначение |
|--------------|-------------------|
| `.py`, `.pyw`, `.pyi`, `.pyx` | Python |
| `.java` | Java |
| `.c`, `.h` | C |
| `.cpp`, `.cc`, `.cxx`, `.c++`, `.hpp`, `.hh`, `.hxx`, `.ipp` | C++ |
| `.cs` | C# |
| `.js`, `.mjs`, `.cjs` | JavaScript |
| `.ts`, `.tsx` | TypeScript |
| `.go` | Go |
| `.rs` | Rust |
| `.swift` | Swift |
| `.kt`, `.kts` | Kotlin |
| `.php`, `.php3`, `.php4`, `.php5`, `.phtml` | PHP |
| `.rb`, `.rbw`, `.rake`, `.gemspec` | Ruby |
| `.dart` | Dart |
| `.r`, `.R`, `.Rmd` | R |
| `.jl` | Julia |
| `.lua` | Lua |
| `.sql` | SQL |
| `.scala`, `.sc` | Scala |
| `.pl`, `.pm`, `.t` | Perl |
| `.hs`, `.lhs` | Haskell |
| `.erl`, `.hrl` | Erlang |
| `.ex`, `.exs` | Elixir |
| `.clj`, `.cljs`, `.cljc` | Clojure |
| `.groovy`, `.gvy` | Groovy |
| `.vb`, `.vbs` | Visual Basic |
| `.sh`, `.bash`, `.zsh`, `.ksh`, `.csh`, `.fish` | Скрипты оболочки |
| `.ps1`, `.psm1`, `.psd1` | PowerShell |
| `.bat`, `.cmd` | Пакетные файлы Windows |

### Текстовые, конфигурационные и разметочные форматы

| Расширение(я) | Назначение |
|--------------|---------|
| `.txt`, `.log` | Простые текстовые и журнальные файлы |
| `.md`, `.markdown`, `.rst` | Документация (Markdown, reStructuredText) |
| `.tex`, `.ltx`, `.bib` | Документы TeX и LaTeX, библиографии |
| `.csv`, `.tsv` | Табличные данные (разделители запятая или табуляция) |
| `.json`, `.jsonl` | JSON и JSON Lines |
| `.xml`, `.xsd`, `.xsl`, `.xslt` | XML и связанные схемы и преобразования |
| `.yaml`, `.yml` | YAML |
| `.toml` | TOML |
| `.ini`, `.cfg`, `.conf`, `.properties` | Конфигурационные файлы |
| `.env` | Файлы переменных окружения |
| `.editorconfig` | Конфигурация редактора |
| `.gitignore` | Списки игнорирования Git |
| `.dockerfile` | Dockerfile |
| `.makefile` | Makefile |
| `.cmake`, `.cmakelists.txt` | Сборочные файлы CMake |
| `.html`, `.htm`, `.xhtml` | HTML и XHTML |
| `.css`, `.scss`, `.sass`, `.less` | Таблицы стилей |
| `.rss`, `.atom` | Веб ленты |

### Двоичные и документные форматы

Все форматы в этом разделе **реально парсятся** во время работы. Для каждого есть отдельный экстрактор в `getting_text_from_files.py`.

| Расширение(я) | Тип | Экстрактор |
|--------------|------|-----------|
| `.pdf` | Переносимый формат документов | PyMuPDF |
| `.docx` | Microsoft Word (Office Open XML) | `docx2txt` |
| `.word` | Legacy алиас, открывается как обычный текст | plain read |
| `.odf` | OpenDocument Format | `odfdo` |
| `.pptx` | Презентация PowerPoint | `pptx2txt2` |
| `.xlsx`, `.xls` | Электронные таблицы Microsoft Excel | MarkItDown |
| `.epub` | Электронная книга EPUB | `epub2txt` |
| `.mobi` | Электронная книга Mobipocket | `mobi` |
| `.fb2` | FictionBook 2 | `fb2reader` |

### Форматы изображений (OCR)

Изображения обрабатываются через OCR конвейер. BiNeuron поддерживает два взаимозаменяемых движка: EasyOCR и DeepSeek OCR. Можно выбрать движок, список языков, а также использовать ли GPU ускорение и режим обрезки для больших изображений.

| Расширение(я) | Тип |
|--------------|------|
| `.jpg`, `.jpeg`, `.png`, `.bmp`, `.gif`, `.webp`, `.tiff`, `.tif` | Растровые изображения |

### Веб источники

Если включён параметр `use_websites`, BiNeuron может загружать текст с любого URL, указанного в настройках, и добавлять его в контекст. Скрапер использует преобразование HTML в текст, поэтому ИИ получает чистый Markdown вместо сырой разметки.

---

## Пример хорошо структурированного запроса

**Слабый запрос:**  
> *«Напишите код для веб скрапера.»*

**Сильный запрос:**  
> *«Разработайте скрипт на Python 3.11 с использованием BeautifulSoup 4 и Requests 2.31, который собирает названия товаров и цены с https://example.com/products. Скрипт должен принимать URL как аргумент командной строки, выводить результаты в CSV файл с колонками "name" и "price" и обрабатывать пагинацию, переходя по ссылкам "Next". Включите обработку ошибок для сетевых таймаутов и отсутствующих элементов.»*

Этот запрос конкретен, выполним и содержит весь необходимый контекст.

---

## Работа с автоматическим редактированием файлов

Если вы включите `editing_files` в настройках, BiNeuron использует двухэтапный пайплайн: основная ИИ модель генерирует ответ, затем лёгкий JSON форматтер преобразует этот ответ в строгий объект, сопоставляющий абсолютные пути к файлам и новое содержимое. Для наилучших результатов:

- Всегда указывайте корневой путь проекта в запросе или через виртуальное хранилище, чтобы ИИ мог построить корректные абсолютные пути.
- Называйте точные имена файлов, которые нужно создать или изменить.
- Помните, что поддерживается только полная замена файлов. Частичное редактирование не поддерживается в целях безопасности.
- Если вы также включите `deleting_files`, ИИ может пометить файл значением `null`, чтобы запросить безопасное удаление.

---

## Заключительные советы

- **Будьте кратки, но полны**: избегайте нерелевантной информации, но не упускайте важных деталей.
- **Используйте маркированные списки** для сложных требований: это улучшает читаемость.
- **Указывайте формат вывода**: скажите ИИ, нужен ли вам только код, код с комментариями или полное объяснение.
- **Упоминайте ограничения**: например, «должен работать в Windows», «должен быть совместим с Python 3.8 или новее», «не должен использовать внешние библиотеки».
- **Проверяйте перед отправкой**: используйте кнопку предпросмотра запроса в группе настроек Cloud AI, чтобы увидеть точный системный промпт, переведённый запрос, контекст файлов и список прикреплённых файлов, которые будут отправлены в ИИ.

Следуя этим рекомендациям, вы полностью раскроете потенциал BiNeuron, сэкономите время и получите высококачественные, адаптированные решения.

</details>

<details>
<summary>🇨🇳 中文</summary>

# 为AI编写有效提示词的指南

为了从BiNeuron中的AI模型获得最准确和相关的回答，精心构建您的提示词至关重要。本指南概述了行之有效的实践方法，并列出了BiNeuron可以接受的所有文件格式，帮助您获得最佳效果。

---

## 核心原则

### 1. 尽可能使用英语
大多数先进的AI模型主要基于英语数据进行训练。用英语编写提示词可以显著提高识别、理解和回答质量。如果英语不是您的母语，简单清晰的英语在大多数情况下仍然优于其他语言。

### 2. 明确指定编程语言
BiNeuron会检测您请求中的编程语言，并连接为该语言专门调整的模型。为了充分利用这一点，请始终明确说明所需的确切编程语言。例如，说明"Python 3.11"或"JavaScript (ES2022)"，而不仅仅是"代码"。这样可以激活特定语言子系统（`MODELS_DICT`），并将您的请求路由到为该语言微调的模型。

### 3. 提供详细的任务描述
模糊的请求会导致模糊的答案。请包括：
- 输入和输出规范（数据类型、格式、示例）
- 边缘情况或约束（性能、内存限制）
- 错误情况下的预期行为
- 任何相关的业务逻辑或领域背景

**不应这样写：**  
> *"编写一个排序数组的函数。"*

**应该这样写：**  
> *"编写一个Python函数，接受一个整数列表，使用快速排序算法返回一个按升序排列的新列表。包括类型提示、文档字符串，并优雅地处理空列表。"*

### 4. 列出您的技术栈
如果您知道将要使用的框架、库或工具，请说明其完整名称和版本。例如：
- "使用 Django 4.2 和 PostgreSQL 15"
- "使用 React 18 和 TypeScript 5 实现"
- "在 Node.js 20 和 Express 4 上运行"

这使AI能够根据您的生态系统定制代码，避免不兼容的API或过时的模式。

### 5. 尽可能附加相关文件
BiNeuron可以读取附加文件的内容并将其合并到请求上下文中。如果您的任务依赖于现有的源代码、配置文件或文档，请附加它们，而不是将片段粘贴到提示词中。虚拟存储模式还允许您将BiNeuron指向整个文件夹，因此整个项目结构会成为上下文的一部分。

### 6. 选择合适的提示模式
BiNeuron内置了几种预构建的系统提示场景（`default`、`testing`、`explanation`、`no_comments`、`refactor`、`debug`、`code_review`、`documentation`、`scaffold`、`security_hardening`、`algorithm_strategy`）。选择与您目标匹配的模式，如果预设都不合适，也可以提供自定义系统提示。

### 7. 在有用时启用请求改进和压缩
如果您的提示词简短而混乱，请启用 `improving_user_experience`，让本地小型模型在发送给主AI之前对其进行结构化。如果您附加了大量文件，请启用 `compress_text`，以便在不丢失技术事实、数字或代码片段的情况下压缩组装的上下文。

### 8. 考虑隐私设置
如果您的请求包含个人数据，请启用 `anonymize_text`，让 Microsoft Presidio 在请求到达翻译服务或AI之前替换姓名、电子邮件、电话号码和其他 PII。如果要屏蔽攻击性语言，请启用 `filter_for_swearing`。

---

## 支持处理的文件格式

BiNeuron可以接受并处理以下格式的文件。为清晰起见，它们分为三类。

> **关于扩展名的说明：** 下列列表反映运行时实际识别的扩展名。某些未在主路由器中列出的代码扩展名（例如小众或框架专用的扩展名）仍会以纯文本方式打开，但它们**不**被视为一等支持的格式。

### 编程语言文件

| 扩展名 | 语言 / 用途 |
|--------|------------|
| `.py`, `.pyw`, `.pyi`, `.pyx` | Python |
| `.java` | Java |
| `.c`, `.h` | C |
| `.cpp`, `.cc`, `.cxx`, `.c++`, `.hpp`, `.hh`, `.hxx`, `.ipp` | C++ |
| `.cs` | C# |
| `.js`, `.mjs`, `.cjs` | JavaScript |
| `.ts`, `.tsx` | TypeScript |
| `.go` | Go |
| `.rs` | Rust |
| `.swift` | Swift |
| `.kt`, `.kts` | Kotlin |
| `.php`, `.php3`, `.php4`, `.php5`, `.phtml` | PHP |
| `.rb`, `.rbw`, `.rake`, `.gemspec` | Ruby |
| `.dart` | Dart |
| `.r`, `.R`, `.Rmd` | R |
| `.jl` | Julia |
| `.lua` | Lua |
| `.sql` | SQL |
| `.scala`, `.sc` | Scala |
| `.pl`, `.pm`, `.t` | Perl |
| `.hs`, `.lhs` | Haskell |
| `.erl`, `.hrl` | Erlang |
| `.ex`, `.exs` | Elixir |
| `.clj`, `.cljs`, `.cljc` | Clojure |
| `.groovy`, `.gvy` | Groovy |
| `.vb`, `.vbs` | Visual Basic |
| `.sh`, `.bash`, `.zsh`, `.ksh`, `.csh`, `.fish` | Shell脚本 |
| `.ps1`, `.psm1`, `.psd1` | PowerShell |
| `.bat`, `.cmd` | Windows批处理文件 |

### 文本、配置和标记格式

| 扩展名 | 用途 |
|--------|------|
| `.txt`, `.log` | 纯文本和日志文件 |
| `.md`, `.markdown`, `.rst` | 文档（Markdown、reStructuredText） |
| `.tex`, `.ltx`, `.bib` | TeX 和 LaTeX 文档及参考文献 |
| `.csv`, `.tsv` | 表格数据（逗号或制表符分隔） |
| `.json`, `.jsonl` | JSON 和 JSON Lines |
| `.xml`, `.xsd`, `.xsl`, `.xslt` | XML 及相关模式和转换 |
| `.yaml`, `.yml` | YAML |
| `.toml` | TOML |
| `.ini`, `.cfg`, `.conf`, `.properties` | 配置文件 |
| `.env` | 环境变量文件 |
| `.editorconfig` | 编辑器配置 |
| `.gitignore` | Git忽略列表 |
| `.dockerfile` | Dockerfile |
| `.makefile` | Makefile |
| `.cmake`, `.cmakelists.txt` | CMake构建文件 |
| `.html`, `.htm`, `.xhtml` | HTML 和 XHTML |
| `.css`, `.scss`, `.sass`, `.less` | 样式表 |
| `.rss`, `.atom` | Web订阅源 |

### 二进制和文档格式

本节中的所有格式在运行时**都会实际被解析**。每个格式在 `getting_text_from_files.py` 中都有专用的提取器。

| 扩展名 | 类型 | 提取器 |
|--------|------|--------|
| `.pdf` | 便携式文档格式 | PyMuPDF |
| `.docx` | Microsoft Word（Office Open XML） | `docx2txt` |
| `.word` | 遗留别名，作为纯文本打开 | plain read |
| `.odf` | OpenDocument格式 | `odfdo` |
| `.pptx` | PowerPoint演示文稿 | `pptx2txt2` |
| `.xlsx`, `.xls` | Microsoft Excel 电子表格 | MarkItDown |
| `.epub` | EPUB 电子书 | `epub2txt` |
| `.mobi` | Mobipocket 电子书 | `mobi` |
| `.fb2` | FictionBook 2 | `fb2reader` |

### 图像格式（OCR）

图像通过 OCR 流水线处理。BiNeuron 支持两个可互换的引擎：EasyOCR 和 DeepSeek OCR。您可以选择引擎、语言列表，以及是否使用 GPU 加速或为大型图像启用裁剪模式。

| 扩展名 | 类型 |
|--------|------|
| `.jpg`, `.jpeg`, `.png`, `.bmp`, `.gif`, `.webp`, `.tiff`, `.tif` | 栅格图像 |

### 网站来源

如果启用 `use_websites`，BiNeuron 可以从设置中提供的任意 URL 抓取文本并将其合并到上下文中。抓取器使用 HTML 到文本的转换，因此 AI 会收到干净的 Markdown 而不是原始标记。

---

## 结构良好的提示词示例

**弱提示词：**  
> *"为网页爬虫编写代码。"*

**强提示词：**  
> *"开发一个 Python 3.11 脚本，使用 BeautifulSoup 4 和 Requests 2.31，从 https://example.com/products 抓取产品名称和价格。脚本应接受 URL 作为命令行参数，将结果输出为包含 'name' 和 'price' 列的 CSV 文件，并通过跟随 'Next' 链接处理分页。包括对网络超时和缺失元素的错误处理。"*

这个提示词具体、可操作，并包含所有必要的上下文。

---

## 使用自动文件编辑功能

如果在设置中启用 `editing_files`，BiNeuron 会使用两阶段流水线：主 AI 生成答案，然后轻量级 JSON 格式化器将该答案转换为一个严格的对象，将绝对文件路径映射到新的文件内容。为了获得最佳结果：

- 始终在提示词中或通过虚拟存储提供项目根路径，以便 AI 能构建正确的绝对路径。
- 明确说明要创建或修改的确切文件名。
- 请记住仅支持整文件替换。出于安全原因，不支持部分编辑。
- 如果同时启用 `deleting_files`，AI 可以将文件标记为 `null` 值以请求安全删除。

---

## 最后建议

- **简洁而完整**：避免无关背景，但不要遗漏关键细节。
- **对复杂要求使用项目符号**：这可以提高可读性。
- **指定输出格式**：告诉AI您是需要纯代码、带注释的代码，还是完整的解释。
- **提及约束条件**：例如，"必须在Windows上运行"、"必须兼容Python 3.8或更新版本"、"不得使用外部库"。
- **发送前预览**：使用 Cloud AI 设置组中的请求预览按钮，查看将发送到 AI 的确切系统提示、翻译后的请求、文件上下文和附加文件列表。

遵循这些指南，您将充分利用BiNeuron的潜力，节省时间并获得高质量、量身定制的解决方案。

</details>