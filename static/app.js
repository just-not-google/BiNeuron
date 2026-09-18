window.addEventListener("error", function (e) {
  console.error("[BiNeuron]", e.error || e.message);
});

const TRANSLATIONS = {
  en: {
    lang_ok:"OK",
    settings_title:"Settings", reset_btn:"Reset", export_all_btn:"Export",
    delete_all_btn:"Delete", apply_settings_btn:"Apply",
    network_frame:"Network", country_label:"Country", protocol_label:"Protocol",
    max_timeout_label:"Max timeout", is_working_label:"Is working",
    auto_proxies_label:"Auto proxies", your_proxies_label:"Your proxies",
    min_timeout_check_label:"Min timeout check", max_timeout_check_label:"Max timeout check",
    retries_label:"Retries", github_proxies_label:"Github proxies",
    url_list_label:"URL list", proxy_retries_label:"Proxy retries",
    main_retries_label:"Main retries",
    model_frame:"Model", preferences_in_ai_label:"Preferences in AI",
    models_dir_label:"Models dir", with_ai_orchestrator_label:"AI orchestrator",
    n_ctx_label:"n_ctx", n_gpu_layers_label:"n_gpu_layers", max_tokens_label:"Max tokens",
    token_hf_label:"HF token", subdomain_label:"Subdomain", repo_id_label:"Repo ID",
    filename_label:"Filename", prefer_mirror_label:"Prefer mirror",
    main_prompt_mode_label:"Main prompt mode", main_prompt_label:"Main prompt",
    temperature_label:"Temperature",
    translator_frame:"Translator", determinant_mode_label:"Determinant mode",
    accurate_translation_label:"Accurate translation", deepl_key_label:"DeepL key",
    request_language_label:"Request language",
    ocr_frame:"OCR", languages_list_label:"Languages list", use_gpu_label:"Use GPU for OCR",
    with_ocr_label:"With OCR", cloud_version_label:"Cloud version",
    with_deepseek_label:"With DeepSeek", model_size_label:"Model size",
    crop_mode_label:"Crop mode", base_url_label:"Base URL",
    api_key_deepseek_label:"DeepSeek API key", timeout_deepseek_label:"DeepSeek timeout",
    max_rate_limit_retries_label:"Rate limit retries",
    other_frame:"Other", theme_label:"Theme", filter_swearing_label:"Filter swearing",
    verbose_label:"Verbose", echo_label:"Echo", type_computer_label:"Type computer",
    proprietary_algorithms_label:"Proprietary algorithms",
    writing_response_label:"Writing response to file", editing_files_label:"Editing files",
    master_title:"Master password", master_enable:"Enable", master_disable:"Disable",
    master_checking:"Checking...", master_enabled_unlocked:"Enabled - unlocked",
    master_enabled_locked:"Enabled - locked",
    master_disabled:"Disabled - chats are stored as plaintext",
    master_crypto_missing:"cryptography not installed (pip install cryptography)",
    chat_title:"Chat", resume_button_text:"Resume request",
    welcome_text:"Welcome to BiNeuron!<br>Type your request below to begin.",
    attached_files_label:"Attached files", request_placeholder:"Type your request...",
    drop_hint:"Drag & drop files here or click to browse",
    remove_file:"Remove", logs_title:"Logs", copy_logs:"Copy logs",
    upload_btn:"Upload", send_btn:"Send", copy_chat_btn:"Copy chat", copy_message:"Copy",
    history_title:"History", history_title_virtual:"Virtual Storage",
    virtual_storage_switch:"Virtual storage", search_placeholder:"Search...",
    storage_path_placeholder:"Storage path...",
    add_btn:"Add", delete_btn:"Del", download_btn:"Save",
    browse_btn:"Browse", refresh_btn:"Refresh",
    gguf_models_frame:"GGUF models", refresh_models_btn:"Refresh models",
    polling_retry:"Connection lost, retrying...",
    polling_fail:"Connection to server lost",
    status_phrases:["Processing request...","Thinking...","Analyzing data...",
      "Generating response...","Working on it...","Almost there...",
      "Consulting the AI...","Crunching numbers...","Reading files...","Optimizing answer..."],
    no_chats_yet:"No chats yet", empty_chat:"Empty chat",
    no_models_found:"No models found", loading:"Loading...",
    scanning:"Scanning...", enter_storage_path:"Enter a storage path and click Refresh",
    enter_storage_prompt:"Enter full path to storage directory:",
    delete_chat_confirm:"Delete this chat?",
    delete_all_chats_confirm:"Delete ALL chats? This cannot be undone.",
    reset_settings_confirm:"Reset settings to defaults?",
    settings_applied:"Settings applied", settings_reset:"Settings reset",
    chat_copied:"Chat copied", no_chat_selected:"No chat selected",
    no_chats_to_export:"No chats to export", logs_empty:"Logs are empty",
    files_attached:"{n} file(s) attached",
    unlock_title:"BiNeuron is locked", unlock_hint:"Enter your master password",
    unlock_btn:"Unlock", unlock_forgot:"Forgot password? (data will be wiped)",
    last_attempt_warning:"Last attempt! Data will be wiped.",
    attempts_remaining:"{n} attempts remaining",
    all_data_wiped:"All data has been wiped.",
    unlock_failed:"Unlock failed", network_error:"Network error",
    set_master_password:"Set a master password (min 4 chars):",
    repeat_password:"Repeat master password:",
    password_too_short:"Password too short",
    passwords_do_not_match:"Passwords do not match",
    encryption_enabled:"Encryption enabled", encryption_disabled:"Encryption disabled",
    failed_prefix:"Failed: ", unknown:"unknown",
    disable_encryption_confirm:"Disable encryption? Chats will be stored as plaintext.",
    wipe_confirm_1:"This will PERMANENTLY delete all chats and the master key. Continue?",
    wipe_confirm_2:"Are you absolutely sure? This cannot be undone."
  },
  ru: {
    lang_ok:"OK",
    settings_title:"Настройки", reset_btn:"Сброс", export_all_btn:"Экспорт",
    delete_all_btn:"Удалить", apply_settings_btn:"Применить",
    network_frame:"Сеть", country_label:"Страна", protocol_label:"Протокол",
    max_timeout_label:"Макс. таймаут", is_working_label:"Работает",
    auto_proxies_label:"Авто прокси", your_proxies_label:"Свои прокси",
    min_timeout_check_label:"Мин. таймаут проверки",
    max_timeout_check_label:"Макс. таймаут проверки",
    retries_label:"Повторы", github_proxies_label:"GitHub прокси",
    url_list_label:"Список URL", proxy_retries_label:"Повторы прокси",
    main_retries_label:"Основные повторы",
    model_frame:"Модель", preferences_in_ai_label:"Предпочтения ИИ",
    models_dir_label:"Папка моделей", with_ai_orchestrator_label:"ИИ-оркестратор",
    n_ctx_label:"n_ctx", n_gpu_layers_label:"n_gpu_layers",
    max_tokens_label:"Макс. токенов",
    token_hf_label:"Токен HF", subdomain_label:"Субдомен", repo_id_label:"ID репозитория",
    filename_label:"Имя файла", prefer_mirror_label:"Предпочитать зеркало",
    main_prompt_mode_label:"Режим промпта", main_prompt_label:"Основной промпт",
    temperature_label:"Температура",
    translator_frame:"Переводчик", determinant_mode_label:"Режим определения",
    accurate_translation_label:"Точный перевод", deepl_key_label:"Ключ DeepL",
    request_language_label:"Язык запроса",
    ocr_frame:"OCR", languages_list_label:"Список языков", use_gpu_label:"GPU для OCR",
    with_ocr_label:"Использовать OCR", cloud_version_label:"Облачная версия",
    with_deepseek_label:"С DeepSeek", model_size_label:"Размер модели",
    crop_mode_label:"Режим обрезки", base_url_label:"Базовый URL",
    api_key_deepseek_label:"API-ключ DeepSeek", timeout_deepseek_label:"Таймаут DeepSeek",
    max_rate_limit_retries_label:"Повторы при лимите",
    other_frame:"Прочее", theme_label:"Тема", filter_swearing_label:"Фильтр мата",
    verbose_label:"Подробный вывод", echo_label:"Эхо", type_computer_label:"Тип компьютера",
    proprietary_algorithms_label:"Проприетарные алгоритмы",
    writing_response_label:"Запись ответа в файл", editing_files_label:"Редактирование файлов",
    master_title:"Мастер-пароль", master_enable:"Включить", master_disable:"Отключить",
    master_checking:"Проверка...", master_enabled_unlocked:"Включено - разблокировано",
    master_enabled_locked:"Включено - заблокировано",
    master_disabled:"Отключено - чаты хранятся в открытом виде",
    master_crypto_missing:"cryptography не установлена (pip install cryptography)",
    chat_title:"Чат", resume_button_text:"Возобновить запрос",
    welcome_text:"Добро пожаловать в BiNeuron!<br>Введите запрос ниже, чтобы начать.",
    attached_files_label:"Прикреплённые файлы", request_placeholder:"Введите запрос...",
    drop_hint:"Перетащите файлы сюда или нажмите для выбора",
    remove_file:"Удалить", logs_title:"Логи", copy_logs:"Скопировать логи",
    upload_btn:"Загрузить", send_btn:"Отправить", copy_chat_btn:"Копировать чат",
    copy_message:"Копировать",
    history_title:"История", history_title_virtual:"Виртуальное хранилище",
    virtual_storage_switch:"Виртуальное хранилище", search_placeholder:"Поиск...",
    storage_path_placeholder:"Путь к хранилищу...",
    add_btn:"Добавить", delete_btn:"Удалить", download_btn:"Сохранить",
    browse_btn:"Обзор", refresh_btn:"Обновить",
    gguf_models_frame:"Модели GGUF", refresh_models_btn:"Обновить модели",
    polling_retry:"Связь потеряна, переподключение...",
    polling_fail:"Соединение с сервером потеряно",
    status_phrases:["Обработка запроса...","Думаю...","Анализ данных...",
      "Генерация ответа...","Работаю над этим...","Почти готово...",
      "Консультируюсь с ИИ...","Считаю числа...","Читаю файлы...","Оптимизирую ответ..."],
    no_chats_yet:"Пока нет чатов", empty_chat:"Пустой чат",
    no_models_found:"Модели не найдены", loading:"Загрузка...",
    scanning:"Сканирование...", enter_storage_path:"Введите путь и нажмите Обновить",
    enter_storage_prompt:"Введите полный путь к папке хранилища:",
    delete_chat_confirm:"Удалить этот чат?",
    delete_all_chats_confirm:"Удалить ВСЕ чаты? Это нельзя отменить.",
    reset_settings_confirm:"Сбросить настройки до значений по умолчанию?",
    settings_applied:"Настройки применены", settings_reset:"Настройки сброшены",
    chat_copied:"Чат скопирован", no_chat_selected:"Чат не выбран",
    no_chats_to_export:"Нечего экспортировать", logs_empty:"Логи пусты",
    files_attached:"Прикреплено файлов: {n}",
    unlock_title:"BiNeuron заблокирован", unlock_hint:"Введите мастер-пароль",
    unlock_btn:"Разблокировать",
    unlock_forgot:"Забыли пароль? (данные будут удалены)",
    last_attempt_warning:"Последняя попытка! Данные будут удалены.",
    attempts_remaining:"Осталось попыток: {n}",
    all_data_wiped:"Все данные были удалены.",
    unlock_failed:"Разблокировка не удалась", network_error:"Ошибка сети",
    set_master_password:"Задайте мастер-пароль (мин. 4 символа):",
    repeat_password:"Повторите мастер-пароль:",
    password_too_short:"Пароль слишком короткий",
    passwords_do_not_match:"Пароли не совпадают",
    encryption_enabled:"Шифрование включено", encryption_disabled:"Шифрование отключено",
    failed_prefix:"Ошибка: ", unknown:"неизвестно",
    disable_encryption_confirm:"Отключить шифрование? Чаты будут храниться в открытом виде.",
    wipe_confirm_1:"Это НАВСЕГДА удалит все чаты и мастер-ключ. Продолжить?",
    wipe_confirm_2:"Вы абсолютно уверены? Это нельзя отменить."
  },
  zh: {
    lang_ok:"确定",
    settings_title:"设置", reset_btn:"重置", export_all_btn:"导出",
    delete_all_btn:"删除", apply_settings_btn:"应用",
    network_frame:"网络", country_label:"国家", protocol_label:"协议",
    max_timeout_label:"最大超时", is_working_label:"启用中",
    auto_proxies_label:"自动代理", your_proxies_label:"自定义代理",
    min_timeout_check_label:"最小检查超时",
    max_timeout_check_label:"最大检查超时",
    retries_label:"重试次数", github_proxies_label:"GitHub 代理",
    url_list_label:"URL 列表", proxy_retries_label:"代理重试",
    main_retries_label:"主重试次数",
    model_frame:"模型", preferences_in_ai_label:"AI 偏好",
    models_dir_label:"模型目录", with_ai_orchestrator_label:"AI 编排器",
    n_ctx_label:"n_ctx", n_gpu_layers_label:"n_gpu_layers",
    max_tokens_label:"最大令牌数",
    token_hf_label:"HF 令牌", subdomain_label:"子域", repo_id_label:"仓库 ID",
    filename_label:"文件名", prefer_mirror_label:"优先使用镜像",
    main_prompt_mode_label:"主提示模式", main_prompt_label:"主提示",
    temperature_label:"温度",
    translator_frame:"翻译器", determinant_mode_label:"检测模式",
    accurate_translation_label:"精确翻译", deepl_key_label:"DeepL 密钥",
    request_language_label:"请求语言",
    ocr_frame:"OCR", languages_list_label:"语言列表", use_gpu_label:"使用 GPU 进行 OCR",
    with_ocr_label:"启用 OCR", cloud_version_label:"云版本",
    with_deepseek_label:"使用 DeepSeek", model_size_label:"模型大小",
    crop_mode_label:"裁剪模式", base_url_label:"基础 URL",
    api_key_deepseek_label:"DeepSeek API 密钥",
    timeout_deepseek_label:"DeepSeek 超时",
    max_rate_limit_retries_label:"限速重试次数",
    other_frame:"其他", theme_label:"主题", filter_swearing_label:"过滤脏话",
    verbose_label:"详细输出", echo_label:"回显", type_computer_label:"计算机类型",
    proprietary_algorithms_label:"专有算法",
    writing_response_label:"将回复写入文件", editing_files_label:"编辑文件",
    master_title:"主密码", master_enable:"启用", master_disable:"禁用",
    master_checking:"检查中...", master_enabled_unlocked:"已启用 - 已解锁",
    master_enabled_locked:"已启用 - 已锁定",
    master_disabled:"已禁用 - 聊天以明文存储",
    master_crypto_missing:"未安装 cryptography (pip install cryptography)",
    chat_title:"对话", resume_button_text:"恢复请求",
    welcome_text:"欢迎使用 BiNeuron!<br>在下方输入请求以开始。",
    attached_files_label:"已附加文件", request_placeholder:"输入您的请求...",
    drop_hint:"将文件拖放到此处，或点击浏览",
    remove_file:"移除", logs_title:"日志", copy_logs:"复制日志",
    upload_btn:"上传", send_btn:"发送", copy_chat_btn:"复制对话", copy_message:"复制",
    history_title:"历史记录", history_title_virtual:"虚拟存储",
    virtual_storage_switch:"虚拟存储", search_placeholder:"搜索...",
    storage_path_placeholder:"存储路径...",
    add_btn:"新增", delete_btn:"删除", download_btn:"保存",
    browse_btn:"浏览", refresh_btn:"刷新",
    gguf_models_frame:"GGUF 模型", refresh_models_btn:"刷新模型",
    polling_retry:"连接中断，正在重试...",
    polling_fail:"与服务器的连接已断开",
    status_phrases:["正在处理请求...","思考中...","分析数据...",
      "生成回复...","正在处理...","快完成了...",
      "正在咨询 AI...","计算数字...","读取文件...","优化回答..."],
    no_chats_yet:"暂无对话", empty_chat:"空对话",
    no_models_found:"未找到模型", loading:"加载中...",
    scanning:"扫描中...", enter_storage_path:"输入路径并点击刷新",
    enter_storage_prompt:"输入存储目录的完整路径:",
    delete_chat_confirm:"删除此对话?",
    delete_all_chats_confirm:"删除所有对话?此操作无法撤销。",
    reset_settings_confirm:"将设置重置为默认值?",
    settings_applied:"设置已应用", settings_reset:"设置已重置",
    chat_copied:"对话已复制", no_chat_selected:"未选择对话",
    no_chats_to_export:"没有可导出的对话", logs_empty:"日志为空",
    files_attached:"已附加 {n} 个文件",
    unlock_title:"BiNeuron 已锁定", unlock_hint:"请输入主密码",
    unlock_btn:"解锁", unlock_forgot:"忘记密码?(数据将被删除)",
    last_attempt_warning:"最后一次尝试!数据将被删除。",
    attempts_remaining:"剩余尝试次数: {n}",
    all_data_wiped:"所有数据已被删除。",
    unlock_failed:"解锁失败", network_error:"网络错误",
    set_master_password:"设置主密码(至少 4 个字符):",
    repeat_password:"再次输入主密码:",
    password_too_short:"密码太短",
    passwords_do_not_match:"密码不匹配",
    encryption_enabled:"加密已启用", encryption_disabled:"加密已禁用",
    failed_prefix:"失败: ", unknown:"未知",
    disable_encryption_confirm:"禁用加密?聊天将以明文存储。",
    wipe_confirm_1:"这将永久删除所有对话和主密钥。继续?",
    wipe_confirm_2:"您确定吗?此操作无法撤销。"
  }
};

const POLL_INTERVAL_MS = 700;
const POLL_TIMEOUT_MS = 20000;
const POLL_MAX_ERRORS = 15;
const LAST_TASK_KEY = "bineuron_last_task_id";
const STICK_TOLERANCE = 40;
const AVAILABLE_THEMES = [
  "midnight", "monokai", "dracula", "nord",
  "solar-flare", "github-noir", "one-dark",
  "catppuccin", "tokyo-night", "gruvbox", "ayu-mirage",
  "material-ocean", "cobalt", "synthwave", "everforest",
  "rose-pine", "kanagawa", "cyberpunk", "matrix", "vaporwave",
  "obsidian", "oceanic", "forest", "amoled",
];

const state = {
  lang: "en",
  theme: "midnight",
  meta: {},
  isBusy: false,
  taskId: null,
  pollTimer: null,
  lastLogCount: 0,
  attachedFiles: [],
  currentChatId: null,
  chats: {},
  timerStart: null,
  timerInterval: null,
  master: { enabled: false, unlocked: false, attempts_left: 3, available: false },
};

let lastLogEl = null;
let lastLogWasProgress = false;
let consecutivePollErrors = 0;
let pollingPaused = false;
let logLineCount = 0;
let fullLogBuffer = [];
let copyResetTimer = null;

const $  = function (sel, root) { return (root || document).querySelector(sel); };
const $$ = function (sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); };
const t  = function (key, vars) {
  const dict = TRANSLATIONS[state.lang] || TRANSLATIONS.en;
  let s = (dict[key] !== undefined) ? dict[key] : (TRANSLATIONS.en[key] !== undefined ? TRANSLATIONS.en[key] : key);
  if (vars && typeof s === "string") {
    s = s.replace(/\{(\w+)\}/g, function (m, k) {
      return (vars[k] !== undefined) ? vars[k] : m;
    });
  }
  return s;
};

function isAtBottom(el) {
  return (el.scrollHeight - el.scrollTop - el.clientHeight) < STICK_TOLERANCE;
}

function createStickyScroll(el) {
  const self = {
    stick: true,
    onChange: null,
    scrollBottom: function () { el.scrollTop = el.scrollHeight; },
    scrollIfSticky: function () {
      if (self.stick) el.scrollTop = el.scrollHeight;
    },
    forceScroll: function () {
      self.stick = true;
      el.scrollTop = el.scrollHeight;
    }
  };
  el.addEventListener("scroll", function () {
    const atBottom = isAtBottom(el);
    if (self.stick !== atBottom) {
      self.stick = atBottom;
      if (typeof self.onChange === "function") self.onChange(atBottom);
    }
  });
  return self;
}

const messagesWrap = $("#messagesWrap");
const logsPanel    = $("#logsPanel");
const logsBody     = $("#logsBody");
const logsToggle   = $("#logsToggle");
const logsCount    = $("#logsCount");
const logsSpinner  = $("#logsSpinner");
const logsCopy     = $("#logsCopy");
const statusBar    = $("#statusBar");
const requestInput = $("#requestInput");
const sendBtn      = $("#sendBtn");
const resumeBtn    = $("#resumeBtn");

const messagesScroll = createStickyScroll(messagesWrap);
const logsScroll     = createStickyScroll(logsBody);

function applyTheme(name) {
  const theme = AVAILABLE_THEMES.indexOf(name) >= 0 ? name : "midnight";
  document.documentElement.setAttribute("data-theme", theme);
  const sel = document.getElementById("themeSelect");
  if (sel) sel.value = theme;
  state.theme = theme;
}

function saveLastTask(tid) {
  try {
    if (tid) localStorage.setItem(LAST_TASK_KEY, tid);
    else localStorage.removeItem(LAST_TASK_KEY);
  } catch (e) {}
}
function loadLastTask() {
  try { return localStorage.getItem(LAST_TASK_KEY); }
  catch (e) { return null; }
}

function applyLanguage() {
  document.documentElement.lang = state.lang;
  document.title = "BiNeuron";
  $$("[data-i18n]").forEach(function (el) { el.innerHTML = t(el.dataset.i18n); });
  $$("[data-i18n-ph]").forEach(function (el) { el.placeholder = t(el.dataset.i18nPh); });
  $$("[data-i18n-title]").forEach(function (el) { el.title = t(el.dataset.i18nTitle); });
  const vs = $("#virtualStorage").checked;
  $("#historyTitle").textContent = vs ? t("history_title_virtual") : t("history_title");
  const lc = $("#logsCopy");
  if (lc) lc.title = t("copy_logs");
  renderFileChips();
  updateMasterUI();
  const ml = $("#modelsList");
  if (ml && ml.children.length === 1) {
    ml.firstChild.textContent = t("no_models_found");
  }
}

$("#langOk").addEventListener("click", function () {
  state.lang = $("#langSelect").value || "en";
  $("#langModal").classList.add("hidden");
  applyLanguage();
  applyTheme(state.theme);
});

$$(".spin").forEach(function (spin) {
  const input = spin.querySelector("input");
  const up    = spin.querySelector('[data-spin="up"]');
  const down  = spin.querySelector('[data-spin="down"]');
  if (!input) return;
  function step(dir) {
    const s = parseFloat(input.step) || 1;
    let v = parseFloat(input.value) || 0;
    v += dir * s;
    const dec = (String(s).split(".")[1] || "").length;
    input.value = dec > 0 ? v.toFixed(dec) : Math.round(v);
    input.dispatchEvent(new Event("input", {bubbles: true}));
  }
  if (up)   up.addEventListener("click",   function () { step(1); });
  if (down) down.addEventListener("click", function () { step(-1); });
});

function fillSelect(sel, values) {
  const el = $(sel);
  if (!el) return;
  el.innerHTML = "";
  (values || []).forEach(function (v) {
    const o = document.createElement("option");
    o.value = v; o.textContent = v;
    el.appendChild(o);
  });
}

async function loadMeta() {
  const r = await fetch("/api/meta");
  state.meta = await r.json();
  fillSelect("#protocolSelect", state.meta.protocols);
  fillSelect("#prefsSelect",    state.meta.preferences_in_ai);
  fillSelect("#detModeSelect",  state.meta.determinant_modes);
  fillSelect("#promptModeSelect", state.meta.main_prompt_modes);
  fillSelect("#modelSizeSelect", state.meta.model_sizes);
  fillSelect("#typeComputerSelect", ["auto"].concat(state.meta.types_power || []));
  if (state.meta.import_error) {
    const w = $("#importWarning");
    w.style.display = "block";
    w.textContent = "BiNeuron import failed: " + state.meta.import_error;
  }
}

function fillForm(settings) {
  $$("[data-setting]").forEach(function (el) {
    const key = el.dataset.setting;
    const v = settings[key];
    if (el.type === "checkbox") el.checked = !!v;
    else if (v === undefined || v === null) el.value = "";
    else el.value = v;
  });
  if (settings.theme) applyTheme(settings.theme);
  onVirtualStorageChanged();
}

function collectSettings() {
  const out = {};
  $$("[data-setting]").forEach(function (el) {
    const key = el.dataset.setting;
    if (el.type === "checkbox") out[key] = el.checked;
    else if (el.type === "number") {
      const n = parseFloat(el.value);
      out[key] = isNaN(n) ? 0 : n;
    } else out[key] = el.value;
  });
  out.theme = state.theme;
  return out;
}

async function loadSettings() {
  const r = await fetch("/api/settings");
  const s = await r.json();
  fillForm(s);
}

async function saveSettings() {
  await fetch("/api/settings", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(collectSettings())
  });
}

$("#btnApply").addEventListener("click", async function () {
  await saveSettings();
  toast(t("settings_applied"));
});
$("#btnReset").addEventListener("click", async function () {
  if (!confirm(t("reset_settings_confirm"))) return;
  const r = await fetch("/api/settings/reset", {method: "POST"});
  const data = await r.json();
  fillForm(data.settings);
  toast(t("settings_reset"));
});
$("#btnExport").addEventListener("click", exportAllChats);
$("#btnDelete").addEventListener("click", deleteAllChats);

document.addEventListener("change", function (e) {
  if (e.target && e.target.id === "themeSelect") {
    applyTheme(e.target.value);
    saveSettings();
  }
});

logsToggle.addEventListener("click", function (e) {
  if (e.target.closest(".logs-copy")) return;
  const nowCollapsed = logsPanel.classList.toggle("collapsed");
  if (!nowCollapsed) {
    setTimeout(function () { logsScroll.forceScroll(); }, 60);
  }
});
logsToggle.addEventListener("keydown", function (e) {
  if (e.key === "Enter" || e.key === " ") {
    e.preventDefault();
    logsToggle.click();
  }
});

function setLogsActive(active) {
  logsSpinner.hidden = !active;
}

function flashCopied() {
  if (!logsCopy) return;
  logsCopy.classList.add("copied");
  logsCopy.textContent = "OK";
  if (copyResetTimer) clearTimeout(copyResetTimer);
  copyResetTimer = setTimeout(function () {
    logsCopy.classList.remove("copied");
    logsCopy.textContent = "C";
  }, 1200);
}

if (logsCopy) {
  logsCopy.addEventListener("click", function (e) {
    e.stopPropagation();
    if (!fullLogBuffer.length) { toast(t("logs_empty")); return; }
    copyToClipboard(fullLogBuffer.join("\n"));
    flashCopied();
  });
}

function hideWelcome() {
  const el = messagesWrap.querySelector(".welcome");
  if (el && el.parentNode) el.parentNode.removeChild(el);
}

function addMessage(role, text, timestamp) {
  hideWelcome();
  const wrap = document.createElement("div");
  wrap.className = "msg " + role;
  const body = document.createElement("div");
  body.className = "text";
  body.textContent = text;
  const meta = document.createElement("div");
  meta.className = "meta";
  const time = document.createElement("span");
  time.className = "time";
  time.textContent = timestamp || nowTime();
  const copy = document.createElement("button");
  copy.className = "btn small";
  copy.textContent = t("copy_message");
  copy.addEventListener("click", function () { copyToClipboard(text); });
  meta.appendChild(time);
  meta.appendChild(copy);
  wrap.appendChild(body);
  wrap.appendChild(meta);
  messagesWrap.appendChild(wrap);
  messagesScroll.scrollIfSticky();
}

function looksLikeProgress(text) {
  if (!text) return false;
  if (/[\u2588\u2589\u258A\u258B\u258C\u258D\u258E\u258F\u2591\u2592\u2593]/.test(text)) return true;
  if (text.indexOf("█") >= 0 || text.indexOf("▊") >= 0 || text.indexOf("▉") >= 0) return true;
  if (/downloading bytes|Fetching|it\/s\]|B\/s\]/.test(text)) return true;
  if (/%\|/.test(text) && /[|<]/.test(text)) return true;
  return false;
}

function resetLogTracker() {
  lastLogEl = null;
  lastLogWasProgress = false;
}

function addLog(text) {
  const isProgress = looksLikeProgress(text);
  if (isProgress && lastLogEl && lastLogWasProgress && lastLogEl.parentNode === logsBody) {
    lastLogEl.textContent = text;
    if (fullLogBuffer.length > 0) fullLogBuffer[fullLogBuffer.length - 1] = text;
  } else {
    const div = document.createElement("div");
    div.className = "log-line" + (isProgress ? " progress" : "");
    div.textContent = text;
    logsBody.appendChild(div);
    lastLogEl = div;
    logLineCount++;
    logsCount.textContent = String(logLineCount);
    fullLogBuffer.push(text);
  }
  lastLogWasProgress = isProgress;
  if (!logsPanel.classList.contains("collapsed")) {
    logsScroll.scrollIfSticky();
  }
}

function clearLogs() {
  logsBody.innerHTML = "";
  logLineCount = 0;
  logsCount.textContent = "0";
  fullLogBuffer = [];
  resetLogTracker();
}

function clearMessages() {
  messagesWrap.innerHTML = "";
  const w = document.createElement("div");
  w.className = "welcome";
  w.innerHTML = t("welcome_text");
  messagesWrap.appendChild(w);
  resetLogTracker();
}

function nowTime() {
  const d = new Date();
  const pad = function (n) { return String(n).padStart(2, "0"); };
  return pad(d.getDate()) + "." + pad(d.getMonth() + 1) + "." + d.getFullYear() +
         " " + pad(d.getHours()) + ":" + pad(d.getMinutes()) + ":" + pad(d.getSeconds());
}
function copyToClipboard(text) {
  navigator.clipboard.writeText(text).catch(function () {
    const ta = document.createElement("textarea");
    ta.value = text;
    document.body.appendChild(ta);
    ta.select();
    document.execCommand("copy");
    ta.remove();
  });
}

function startRequestTimer() {
  state.timerStart = Date.now();
  tickStatus();
}
function tickStatus() {
  if (state.timerStart === null) return;
  const elapsed = (Date.now() - state.timerStart) / 1000;
  const m = String(Math.floor(elapsed / 60)).padStart(2, "0");
  const s = String(Math.floor(elapsed % 60)).padStart(2, "0");
  const phrases = t("status_phrases");
  const p = phrases[Math.floor(elapsed / 5) % phrases.length];
  statusBar.textContent = p + " " + m + ":" + s;
  state.timerInterval = setTimeout(tickStatus, 1000);
}
function stopRequestTimer() {
  if (state.timerInterval) clearTimeout(state.timerInterval);
  state.timerInterval = null;
  state.timerStart = null;
  statusBar.textContent = "";
}

async function ensureCurrentChat() {
  if (state.currentChatId && state.chats[state.currentChatId]) return state.currentChatId;
  const r = await fetch("/api/chats", {method: "POST"});
  if (r.status === 401) { handleLocked(); return null; }
  const data = await r.json();
  state.currentChatId = data.id;
  state.chats[data.id] = data.chat;
  renderHistoryList();
  return data.id;
}

async function persistMessage(chatId, role, content) {
  if (!chatId) return;
  const r = await fetch("/api/chats/" + chatId + "/messages", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({role: role, content: content})
  });
  if (r.status === 401) { handleLocked(); return; }
  if (state.chats[chatId]) {
    state.chats[chatId].messages.push({
      role: role, content: content, timestamp: nowTime()
    });
  }
}

async function sendMessage() {
  if (state.isBusy) return;
  const text = requestInput.value.trim();
  if (!text) return;
  const chatId = await ensureCurrentChat();
  addMessage("user", text);
  await persistMessage(chatId, "user", text);
  messagesScroll.forceScroll();
  requestInput.value = "";
  resumeBtn.classList.remove("visible");
  clearLogs();
  logsPanel.classList.remove("collapsed");
  state.isBusy = true;
  state.lastLogCount = 0;
  consecutivePollErrors = 0;
  resetLogTracker();
  setLogsActive(true);
  startRequestTimer();
  try {
    const r = await fetch("/api/chat", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        request: text,
        settings: collectSettings(),
        attached_files: state.attachedFiles.map(function (f) { return f.path; })
      })
    });
    if (!r.ok) throw new Error("HTTP " + r.status);
    const data = await r.json();
    state.taskId = data.task_id;
    saveLastTask(data.task_id);
    pollTask(data.task_id);
  } catch (e) {
    addLog("ERROR: " + e.message);
    finishTask();
  }
}

async function fetchTaskOnce(tid) {
  const controller = new AbortController();
  const timeoutId = setTimeout(function () { controller.abort(); }, POLL_TIMEOUT_MS);
  try {
    const r = await fetch("/api/chat/task/" + tid + "?since=" + state.lastLogCount, {
      signal: controller.signal,
      cache: "no-store"
    });
    if (!r.ok) throw new Error("HTTP " + r.status);
    return await r.json();
  } finally {
    clearTimeout(timeoutId);
  }
}

function pollTask(tid) {
  state.pollTimer = setTimeout(async function () {
    if (pollingPaused) { pollTask(tid); return; }
    let data;
    try {
      data = await fetchTaskOnce(tid);
      if (consecutivePollErrors > 0) {
        addLog("[web] Reconnected to server.");
        consecutivePollErrors = 0;
      }
    } catch (e) {
      consecutivePollErrors++;
      if (consecutivePollErrors === 1) {
        statusBar.textContent = t("polling_retry");
      }
      if (consecutivePollErrors >= POLL_MAX_ERRORS) {
        addLog("[web] " + t("polling_fail") + ": " + e.message);
        finishTask();
        return;
      }
      pollTask(tid);
      return;
    }
    (data.logs || []).forEach(function (l) { addLog(l); });
    state.lastLogCount = data.log_count;
    if (data.status === "done") {
      addMessage("assistant", data.answer || "(empty response)");
      const chatId = state.currentChatId;
      if (chatId) persistMessage(chatId, "assistant", data.answer || "");
      finishTask();
    } else if (data.status === "error") {
      addLog("TASK FAILED: " + (data.error || "unknown error"));
      finishTask();
    } else {
      pollTask(tid);
    }
  }, POLL_INTERVAL_MS);
}

function finishTask() {
  state.isBusy = false;
  state.taskId = null;
  consecutivePollErrors = 0;
  saveLastTask(null);
  if (state.pollTimer) clearTimeout(state.pollTimer);
  state.pollTimer = null;
  stopRequestTimer();
  setLogsActive(false);
}

async function tryResumeAfterReload() {
  const tid = loadLastTask();
  if (!tid) return false;
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(function () { controller.abort(); }, POLL_TIMEOUT_MS);
    const r = await fetch("/api/chat/task/" + tid + "?since=0", {
      signal: controller.signal,
      cache: "no-store"
    });
    clearTimeout(timeoutId);
    if (!r.ok) { saveLastTask(null); return false; }
    const data = await r.json();
    if (data.status === "running") {
      state.taskId = tid;
      state.isBusy = true;
      state.lastLogCount = 0;
      consecutivePollErrors = 0;
      logsPanel.classList.remove("collapsed");
      startRequestTimer();
      setLogsActive(true);
      addLog("[web] Resuming previous request...");
      pollTask(tid);
      return true;
    }
    saveLastTask(null);
    return false;
  } catch (e) {
    return false;
  }
}

sendBtn.addEventListener("click", sendMessage);
requestInput.addEventListener("keydown", function (e) {
  if (e.key === "Enter") sendMessage();
});
resumeBtn.addEventListener("click", function () {
  if (state.isBusy) return;
  resumeBtn.classList.remove("visible");
  sendMessage();
});

$("#copyBtn").addEventListener("click", function () {
  const lines = [];
  $$(".msg", messagesWrap).forEach(function (m) {
    const role = m.classList.contains("user") ? "User"
               : m.classList.contains("assistant") ? "Assistant"
               : "Log";
    const el = m.querySelector(".text") || m;
    lines.push(role + ": " + el.textContent.trim());
  });
  copyToClipboard(lines.join("\n"));
  toast(t("chat_copied"));
});

function renderFileChips() {
  const container = $("#fileChips");
  if (!container) return;
  container.innerHTML = "";
  state.attachedFiles.forEach(function (file, index) {
    const chip = document.createElement("span");
    chip.className = "file-chip";
    const name = document.createElement("span");
    name.className = "name";
    name.textContent = file.name;
    name.title = file.name;
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "remove";
    btn.textContent = "x";
    btn.title = t("remove_file");
    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      removeAttachedFile(index);
    });
    chip.appendChild(name);
    chip.appendChild(btn);
    container.appendChild(chip);
  });
}

function removeAttachedFile(index) {
  if (index < 0 || index >= state.attachedFiles.length) return;
  state.attachedFiles.splice(index, 1);
  renderFileChips();
}

async function uploadFiles(fileList) {
  if (!fileList || !fileList.length) return;
  const fd = new FormData();
  for (let i = 0; i < fileList.length; i++) fd.append("files", fileList[i]);
  const r = await fetch("/api/upload", {method: "POST", body: fd});
  const data = await r.json();
  const paths = (data.paths || []).slice();
  const names = Array.prototype.slice.call(fileList).map(function (f) { return f.name; });
  for (let i = 0; i < paths.length; i++) {
    state.attachedFiles.push({name: names[i] || paths[i], path: paths[i]});
  }
  renderFileChips();
  if (paths.length) toast(t("files_attached", {n: paths.length}));
}

$("#uploadBtn").addEventListener("click", function () {
  const input = document.createElement("input");
  input.type = "file";
  input.multiple = true;
  input.addEventListener("change", function () { uploadFiles(input.files); });
  input.click();
});

const dropZone = $("#dropZone");
if (dropZone) {
  function openPicker() {
    const input = document.createElement("input");
    input.type = "file";
    input.multiple = true;
    input.addEventListener("change", function () { uploadFiles(input.files); });
    input.click();
  }
  dropZone.addEventListener("click", function (e) {
    if (e.target.closest(".file-chip")) return;
    openPicker();
  });
  dropZone.addEventListener("keydown", function (e) {
    if (e.key === "Enter" || e.key === " ") { e.preventDefault(); openPicker(); }
  });
  ["dragenter", "dragover"].forEach(function (evt) {
    dropZone.addEventListener(evt, function (e) {
      e.preventDefault(); e.stopPropagation();
      dropZone.classList.add("drag-over");
    });
  });
  ["dragleave", "dragend"].forEach(function (evt) {
    dropZone.addEventListener(evt, function (e) {
      e.preventDefault(); e.stopPropagation();
      if (e.target === dropZone || !dropZone.contains(e.relatedTarget)) {
        dropZone.classList.remove("drag-over");
      }
    });
  });
  dropZone.addEventListener("drop", function (e) {
    e.preventDefault(); e.stopPropagation();
    dropZone.classList.remove("drag-over");
    const dt = e.dataTransfer;
    if (dt && dt.files && dt.files.length) uploadFiles(dt.files);
  });
  ["dragover", "drop"].forEach(function (evt) {
    window.addEventListener(evt, function (e) { e.preventDefault(); });
  });
}

const historyList = $("#historyList");
const treeView    = $("#treeView");

function renderHistoryList() {
  historyList.innerHTML = "";
  const entries = Object.entries(state.chats)
    .sort(function (a, b) { return (b[1].created_at || "").localeCompare(a[1].created_at || ""); });
  if (!entries.length) {
    historyList.innerHTML = '<div style="color:var(--fg-dark);padding:8px;">' + t("no_chats_yet") + '</div>';
    return;
  }
  entries.forEach(function (entry) {
    const id = entry[0], chat = entry[1];
    const btn = document.createElement("button");
    btn.className = "chat-item" + (id === state.currentChatId ? " active" : "");
    const first = (chat.messages || []).find(function (m) { return m.role === "user"; });
    const title = first ? first.content.slice(0, 30) : t("empty_chat");
    btn.textContent = (chat.created_at || "-") + " - " + title;
    btn.addEventListener("click", function () { loadChat(id); });
    historyList.appendChild(btn);
  });
}

async function loadChat(id) {
  const r = await fetch("/api/chats/" + id);
  if (r.status === 401) { handleLocked(); return; }
  if (!r.ok) return;
  const chat = await r.json();
  state.currentChatId = id;
  clearMessages();
  clearLogs();
  (chat.messages || []).forEach(function (m) {
    if (m.role === "user" || m.role === "assistant") addMessage(m.role, m.content, m.timestamp);
    else addLog(m.content);
  });
  messagesScroll.forceScroll();
  logsScroll.forceScroll();
  renderHistoryList();
}

async function loadChats() {
  const r = await fetch("/api/chats");
  if (r.status === 401) { handleLocked(); return; }
  state.chats = await r.json();
  const ids = Object.keys(state.chats)
    .sort(function (a, b) {
      return (state.chats[b].created_at || "").localeCompare(state.chats[a].created_at || "");
    });
  if (ids.length) {
    state.currentChatId = ids[0];
    await loadChat(ids[0]);
  } else {
    state.currentChatId = null;
    clearMessages();
    clearLogs();
  }
  renderHistoryList();
}

$("#btnAddChat").addEventListener("click", async function () {
  const r = await fetch("/api/chats", {method: "POST"});
  if (r.status === 401) { handleLocked(); return; }
  const data = await r.json();
  state.currentChatId = data.id;
  state.chats[data.id] = data.chat;
  clearMessages();
  clearLogs();
  renderHistoryList();
});

$("#btnDelChat").addEventListener("click", async function () {
  if (!state.currentChatId) return;
  if (!confirm(t("delete_chat_confirm"))) return;
  const r = await fetch("/api/chats/" + state.currentChatId, {method: "DELETE"});
  if (r.status === 401) { handleLocked(); return; }
  delete state.chats[state.currentChatId];
  state.currentChatId = null;
  const ids = Object.keys(state.chats);
  if (ids.length) await loadChat(ids[0]);
  else { clearMessages(); clearLogs(); renderHistoryList(); }
});

$("#btnDlChat").addEventListener("click", function () {
  if (!state.currentChatId || !state.chats[state.currentChatId]) {
    toast(t("no_chat_selected")); return;
  }
  const chat = state.chats[state.currentChatId];
  const text = (chat.messages || []).map(function (m) {
    return m.role.charAt(0).toUpperCase() + m.role.slice(1) + ": " + m.content;
  }).join("\n");
  const blob = new Blob([text], {type: "text/plain"});
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "chat_" + state.currentChatId + ".txt";
  a.click();
  URL.revokeObjectURL(a.href);
});

async function exportAllChats() {
  const ids = Object.keys(state.chats);
  if (!ids.length) { toast(t("no_chats_to_export")); return; }
  const lines = [];
  ids.forEach(function (id) {
    const c = state.chats[id];
    lines.push("===== " + c.created_at + " (" + id + ") =====");
    (c.messages || []).forEach(function (m) { lines.push(m.role + ": " + m.content); });
    lines.push("");
  });
  const blob = new Blob([lines.join("\n")], {type: "text/plain"});
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "bineuron_all_chats.txt";
  a.click();
  URL.revokeObjectURL(a.href);
}

async function deleteAllChats() {
  if (!Object.keys(state.chats).length) return;
  if (!confirm(t("delete_all_chats_confirm"))) return;
  for (const id of Object.keys(state.chats)) {
    const r = await fetch("/api/chats/" + id, {method: "DELETE"});
    if (r.status === 401) { handleLocked(); return; }
  }
  state.chats = {};
  state.currentChatId = null;
  clearMessages();
  clearLogs();
  renderHistoryList();
}

$("#searchChats").addEventListener("input", function (e) {
  const q = e.target.value.toLowerCase();
  $$(".chat-item", historyList).forEach(function (el) {
    el.style.display = el.textContent.toLowerCase().indexOf(q) >= 0 ? "" : "none";
  });
});

const virtualStorage  = $("#virtualStorage");
const historyControls = $("#historyControls");
const storageControls = $("#storageControls");

function onVirtualStorageChanged() {
  const on = virtualStorage.checked;
  historyControls.classList.toggle("hidden", on);
  storageControls.classList.toggle("visible", on);
  historyList.style.display = on ? "none" : "block";
  treeView.style.display    = on ? "block" : "none";
  $("#historyTitle").textContent = on ? t("history_title_virtual") : t("history_title");
  if (on) loadStorageTree();
}
virtualStorage.addEventListener("change", onVirtualStorageChanged);

async function loadStorageTree() {
  const path = $("#storagePath").value.trim();
  if (!path) {
    treeView.innerHTML = '<div style="padding:8px;color:var(--fg-dark);">' + t("enter_storage_path") + '</div>';
    return;
  }
  treeView.innerHTML = '<div style="padding:8px;color:var(--fg-dark);">' + t("scanning") + '</div>';
  const r = await fetch("/api/storage/tree", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({path: path})
  });
  const data = await r.json();
  if (!data.ok) {
    treeView.innerHTML = '<div style="padding:8px;color:#ffb0b0;">' + data.error + '</div>';
    return;
  }
  treeView.innerHTML = "";
  treeView.appendChild(renderTreeNode(data.tree));
}

function renderTreeNode(node) {
  const ul = document.createElement("ul");
  const li = document.createElement("li");
  if (node.type === "file") li.classList.add("file");
  li.textContent = node.name;
  li.dataset.path = node.path;
  if (node.type === "file") {
    li.addEventListener("dblclick", function () {
      fetch("/api/storage/open", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({path: node.path})
      });
    });
  } else if (node.children) {
    const sub = document.createElement("ul");
    node.children.forEach(function (ch) { sub.appendChild(renderTreeNode(ch)); });
    li.appendChild(sub);
  }
  ul.appendChild(li);
  return ul;
}

$("#btnBrowse").addEventListener("click", function () {
  const p = prompt(t("enter_storage_prompt"));
  if (p) { $("#storagePath").value = p; loadStorageTree(); }
});
$("#btnRefresh").addEventListener("click", loadStorageTree);

$("#refreshModels").addEventListener("click", async function () {
  const dir = $('[data-setting="models_dir"]').value.trim() || "./models";
  const list = $("#modelsList");
  list.innerHTML = '<div style="color:var(--fg-dark);">' + t("loading") + '</div>';
  const r = await fetch("/api/models?dir=" + encodeURIComponent(dir));
  const data = await r.json();
  list.innerHTML = "";
  if (!data.ok || !data.models.length) {
    list.innerHTML = '<div style="color:var(--fg-dark);">' + t("no_models_found") + '</div>';
    return;
  }
  data.models.forEach(function (name) {
    const el = document.createElement("div");
    el.textContent = name;
    el.title = name;
    list.appendChild(el);
  });
});

function toast(msg) {
  const el = document.createElement("div");
  el.textContent = msg;
  el.style.position = "fixed";
  el.style.left = "50%";
  el.style.bottom = "30px";
  el.style.transform = "translateX(-50%)";
  el.style.background = "var(--bg-frame)";
  el.style.border = "1px solid var(--border)";
  el.style.padding = "8px 14px";
  el.style.borderRadius = "6px";
  el.style.zIndex = "2000";
  el.style.boxShadow = "0 6px 20px rgba(0,0,0,.5)";
  el.style.fontSize = "13px";
  document.body.appendChild(el);
  setTimeout(function () { el.remove(); }, 2200);
}

const unlockModal    = document.getElementById("unlockModal");
const unlockPwd      = document.getElementById("unlockPassword");
const unlockOk       = document.getElementById("unlockOk");
const unlockHint     = document.getElementById("unlockHint");
const unlockAttempts = document.getElementById("unlockAttempts");
const unlockWipe     = document.getElementById("unlockWipeHint");

function updateMasterUI() {
  const box = document.getElementById("masterState");
  if (!box) return;
  const m = state.master;
  if (!m.available) {
    box.textContent = t("master_crypto_missing");
    box.className = "master-state off";
    const b1 = document.getElementById("btnMasterEnable");
    const b2 = document.getElementById("btnMasterDisable");
    if (b1) b1.disabled = true;
    if (b2) b2.disabled = true;
    return;
  }
  if (m.enabled) {
    box.textContent = m.unlocked ? t("master_enabled_unlocked") : t("master_enabled_locked");
    box.className = "master-state on";
    document.getElementById("btnMasterEnable").disabled = true;
    document.getElementById("btnMasterDisable").disabled = !m.unlocked;
  } else {
    box.textContent = t("master_disabled");
    box.className = "master-state off";
    document.getElementById("btnMasterEnable").disabled = false;
    document.getElementById("btnMasterDisable").disabled = true;
  }
}

async function refreshMasterStatus() {
  try {
    const r = await fetch("/api/master/status");
    state.master = await r.json();
    updateMasterUI();
  } catch (e) {}
}

function showUnlockModal(attemptsLeft) {
  unlockModal.classList.remove("hidden");
  unlockPwd.value = "";
  unlockPwd.focus();
  unlockHint.textContent = t("unlock_hint");
  if (attemptsLeft !== undefined && attemptsLeft !== null) {
    if (attemptsLeft <= 1) {
      unlockAttempts.classList.add("danger");
      unlockAttempts.textContent = t("last_attempt_warning");
    } else {
      unlockAttempts.classList.remove("danger");
      unlockAttempts.textContent = t("attempts_remaining", {n: attemptsLeft});
    }
  } else {
    unlockAttempts.textContent = "";
  }
}

function hideUnlockModal() {
  unlockModal.classList.add("hidden");
}

function handleLocked() {
  state.master.unlocked = false;
  showUnlockModal(state.master.attempts_left);
}

async function tryUnlock() {
  const pwd = unlockPwd.value;
  if (!pwd) return;
  unlockOk.disabled = true;
  try {
    const r = await fetch("/api/master/unlock", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({password: pwd}),
    });
    const data = await r.json();
    if (data.ok) {
      hideUnlockModal();
      state.master.unlocked = true;
      await loadChats();
      await refreshMasterStatus();
      return;
    }
    if (data.wiped) {
      unlockHint.textContent = t("all_data_wiped");
      unlockAttempts.classList.remove("danger");
      unlockAttempts.textContent = "";
      unlockOk.disabled = true;
      setTimeout(function () {
        hideUnlockModal();
        state.chats = {};
        state.currentChatId = null;
        clearMessages();
        clearLogs();
        renderHistoryList();
        refreshMasterStatus();
      }, 2500);
      return;
    }
    if (data.wrong) {
      state.master.attempts_left = data.attempts_left;
      showUnlockModal(data.attempts_left);
      unlockPwd.value = "";
    } else {
      unlockHint.textContent = data.error || t("unlock_failed");
    }
  } catch (e) {
    unlockHint.textContent = t("network_error");
  } finally {
    unlockOk.disabled = false;
  }
}

if (unlockOk) {
  unlockOk.addEventListener("click", tryUnlock);
  unlockPwd.addEventListener("keydown", function (e) {
    if (e.key === "Enter") tryUnlock();
  });
}

if (unlockWipe) {
  unlockWipe.addEventListener("click", async function () {
    if (!confirm(t("wipe_confirm_1"))) return;
    if (!confirm(t("wipe_confirm_2"))) return;
    for (let i = 0; i < 3; i++) {
      await fetch("/api/master/unlock", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({password: "__wipe__" + i}),
      });
    }
    location.reload();
  });
}

const btnMasterEnable  = document.getElementById("btnMasterEnable");
const btnMasterDisable = document.getElementById("btnMasterDisable");

if (btnMasterEnable) {
  btnMasterEnable.addEventListener("click", async function () {
    const pwd = prompt(t("set_master_password"));
    if (!pwd) return;
    if (pwd.length < 4) { toast(t("password_too_short")); return; }
    const pwd2 = prompt(t("repeat_password"));
    if (pwd !== pwd2) { toast(t("passwords_do_not_match")); return; }
    const r = await fetch("/api/master/setup", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({password: pwd}),
    });
    const data = await r.json();
    if (data.ok) {
      toast(t("encryption_enabled"));
      await refreshMasterStatus();
    } else {
      toast(t("failed_prefix") + (data.error || t("unknown")));
    }
  });
}

if (btnMasterDisable) {
  btnMasterDisable.addEventListener("click", async function () {
    if (!confirm(t("disable_encryption_confirm"))) return;
    const r = await fetch("/api/master/disable", {method: "POST"});
    const data = await r.json();
    if (data.ok) {
      toast(t("encryption_disabled"));
      await refreshMasterStatus();
    } else {
      toast(t("failed_prefix") + (data.error || t("unknown")));
    }
  });
}

document.addEventListener("visibilitychange", function () {
  pollingPaused = document.hidden;
});

(async function init() {
  try {
    applyLanguage();
    const m = await fetch("/api/master/status").then(r => r.json());
    state.master = m;
    updateMasterUI();
    if (m.enabled && !m.unlocked) {
      showUnlockModal(m.attempts_left);
      return;
    }
    await loadMeta();
    await loadSettings();
    await loadChats();
    await tryResumeAfterReload();
  } catch (e) {
    console.error("Init failed:", e);
  }
})();