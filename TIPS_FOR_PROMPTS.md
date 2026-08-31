<details>
<summary>🇬🇧 English</summary>

# Guidelines for Crafting Effective Prompts for AI

To obtain the most accurate and relevant responses from AI models, it is essential to structure your prompts thoughtfully. This guide outlines proven practices and lists all file formats that AI systems can accept, helping you get the best possible results.

---

## Core Principles

### 1. Use English When Possible
Most advanced AI models are trained primarily on English-language data. Writing your prompt in English significantly improves recognition, understanding, and response quality. If English is not your native language, simple and clear English is still preferable to other languages in most cases.

### 2. Specify Programming Languages Explicitly
If your task involves code, always mention the exact programming language(s) you need. For example, state "Python 3.11" or "JavaScript (ES2022)" rather than just "code". This activates specialised AI sub‑systems tuned for those languages, resulting in more syntactically correct and idiomatic solutions.

### 3. Provide Detailed Task Descriptions
Vague requests yield vague answers. Include:
- Input and output specifications (data types, formats, examples)
- Edge cases or constraints (e.g., performance, memory limits)
- Desired behaviour under error conditions
- Any relevant business logic or domain context

**Instead of:**  
> *“Write a function to sort an array.”*

**Prefer:**  
> *“Write a Python function that takes a list of integers and returns a new list sorted in ascending order using the quicksort algorithm. Include type hints, docstrings, and handle empty lists gracefully.”*

### 4. List Your Technology Stack
If you know which frameworks, libraries, or tools will be used, state their full names and versions. For instance:
- “Use Django 4.2 with PostgreSQL 15”
- “Implement using React 18 and TypeScript 5”
- “Run on Node.js 20 with Express 4”

This allows the AI to tailor the code to your ecosystem, avoiding incompatible APIs or outdated patterns.

---

## Supported File Formats for Processing

AI can accept and process files in the following formats. They are grouped into three categories for clarity.

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
| `.tex`, `.ltx`, `.bib` | TeX / LaTeX documents and bibliographies |
| `.csv`, `.tsv` | Tabular data (comma‑/tab‑separated) |
| `.json`, `.jsonl` | JSON and JSON Lines |
| `.xml`, `.xsd`, `.xsl`, `.xslt` | XML and related schemas/transformations |
| `.yaml`, `.yml` | YAML |
| `.toml` | TOML |
| `.ini`, `.cfg`, `.conf`, `.properties` | Configuration files |
| `.env` | Environment variable files |
| `.editorconfig` | Editor configuration |
| `.gitignore` | Git ignore lists |
| `.dockerfile` | Dockerfile |
| `.makefile` | Makefile |
| `.cmake`, `.cmakelists.txt` | CMake build files |
| `.html`, `.htm`, `.xhtml` | HTML / XHTML |
| `.css`, `.scss`, `.sass`, `.less` | Stylesheets |
| `.rss`, `.atom` | Web feeds |

### Binary and Document Formats (Newer Support)

| Extension(s) | Type |
|--------------|------|
| `.pdf` | Portable Document Format |
| `.docx` (or `.word`) | Microsoft Word document |
| `.odf` | OpenDocument Format |
| `.pptx` | PowerPoint presentation |
| `.jpg`, `.jpeg`, `.png`, `.bmp`, `.gif`, `.webp`, `.tiff`, `.tif` | Raster images |

---

## Example of a Well‑Structured Prompt

**Weak prompt:**  
> *“Write code for a web scraper.”*

**Strong prompt:**  
> *“Develop a Python 3.11 script using BeautifulSoup 4 and Requests 2.31 that scrapes product names and prices from https://example.com/products. The script should accept a URL as a command‑line argument, output results as a CSV file with columns ‘name’ and ‘price’, and handle pagination by following ‘Next’ links. Include error handling for network timeouts and missing elements.”*

This prompt is specific, actionable, and includes all necessary context.

---

## Final Tips

- **Be concise but complete** – avoid irrelevant background, but do not omit crucial details.
- **Use bullet points** for complex requirements – they improve readability.
- **Specify output format** – tell the AI whether you need code only, code with comments, or a full explanation.
- **Mention constraints** – e.g., “must run on Windows”, “must be compatible with Python 3.8+”, “must not use external libraries”.

By following these guidelines, you will harness the full potential of AI assistants, saving time and receiving high‑quality, tailored solutions.

</details>

<details>
<summary>🇷🇺 Русский</summary>

# Рекомендации по составлению эффективных запросов для ИИ

Чтобы получать от ИИ-моделей наиболее точные и релевантные ответы, важно продуманно структурировать свои запросы. Данное руководство описывает проверенные практики и перечисляет все форматы файлов, которые могут обрабатывать ИИ-системы, помогая вам добиваться наилучших результатов.

---

## Основные принципы

### 1. По возможности используйте английский язык
Большинство современных ИИ-моделей обучаются преимущественно на англоязычных данных. Запрос на английском языке значительно улучшает распознавание, понимание и качество ответа. Если английский не является вашим родным языком, простой и понятный английский всё равно предпочтительнее других языков в большинстве случаев.

### 2. Чётко указывайте языки программирования
Если ваша задача связана с кодом, всегда точно называйте нужные языки программирования. Например, указывайте «Python 3.11» или «JavaScript (ES2022)», а не просто «код». Это активирует специализированные подсистемы ИИ, настроенные на эти языки, что даёт более синтаксически корректные и идиоматичные решения.

### 3. Давайте подробное описание задачи
Расплывчатые запросы приводят к расплывчатым ответам. Включайте:
- Спецификацию входных и выходных данных (типы данных, форматы, примеры)
- Краевые случаи или ограничения (например, производительность, лимиты памяти)
- Желаемое поведение при ошибках
- Любую релевантную бизнес-логику или предметную область

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

---

## Поддерживаемые форматы файлов для обработки

ИИ может принимать и обрабатывать файлы следующих форматов. Для ясности они сгруппированы в три категории.

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
| `.tex`, `.ltx`, `.bib` | Документы TeX / LaTeX и библиографии |
| `.csv`, `.tsv` | Табличные данные (разделители запятая/табуляция) |
| `.json`, `.jsonl` | JSON и JSON Lines |
| `.xml`, `.xsd`, `.xsl`, `.xslt` | XML и связанные схемы/преобразования |
| `.yaml`, `.yml` | YAML |
| `.toml` | TOML |
| `.ini`, `.cfg`, `.conf`, `.properties` | Конфигурационные файлы |
| `.env` | Файлы переменных окружения |
| `.editorconfig` | Конфигурация редактора |
| `.gitignore` | Списки игнорирования Git |
| `.dockerfile` | Dockerfile |
| `.makefile` | Makefile |
| `.cmake`, `.cmakelists.txt` | Сборочные файлы CMake |
| `.html`, `.htm`, `.xhtml` | HTML / XHTML |
| `.css`, `.scss`, `.sass`, `.less` | Таблицы стилей |
| `.rss`, `.atom` | Веб-ленты |

### Двоичные и документные форматы (более новая поддержка)

| Расширение(я) | Тип |
|--------------|------|
| `.pdf` | Переносимый формат документов |
| `.docx` (или `.word`) | Документ Microsoft Word |
| `.odf` | OpenDocument Format |
| `.pptx` | Презентация PowerPoint |
| `.jpg`, `.jpeg`, `.png`, `.bmp`, `.gif`, `.webp`, `.tiff`, `.tif` | Растровые изображения |

---

## Пример хорошо структурированного запроса

**Слабый запрос:**  
> *«Напишите код для веб-скрапера.»*

**Сильный запрос:**  
> *«Разработайте скрипт на Python 3.11 с использованием BeautifulSoup 4 и Requests 2.31, который собирает названия товаров и цены с https://example.com/products. Скрипт должен принимать URL как аргумент командной строки, выводить результаты в CSV-файл с колонками «name» и «price» и обрабатывать пагинацию, переходя по ссылкам «Next». Включите обработку ошибок для сетевых тайм-аутов и отсутствующих элементов.»*

Этот запрос конкретен, выполним и содержит весь необходимый контекст.

---

## Заключительные советы

- **Будьте кратки, но полны** – избегайте нерелевантной информации, но не упускайте важных деталей.
- **Используйте маркированные списки** для сложных требований – это улучшает читаемость.
- **Указывайте формат вывода** – скажите ИИ, нужен ли вам только код, код с комментариями или полное объяснение.
- **Упоминайте ограничения** – например, «должен работать в Windows», «должен быть совместим с Python 3.8+», «не должен использовать внешние библиотеки».

Следуя этим рекомендациям, вы полностью раскроете потенциал ИИ-помощников, сэкономите время и получите высококачественные, адаптированные решения.

</details>
