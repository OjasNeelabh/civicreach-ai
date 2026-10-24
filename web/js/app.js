/**
 * CivicReach AI Frontend Application Controller
 * Handles multilingual switching, voice input/output, legal search, notice decryption, and Section 12 screening.
 */

const state = {
  lang: 'en',
  mode: 'standard',
  activeTab: 'laws',
  isSpeaking: false,
  isListening: false
};

const langSpeechMap = {
  en: 'en-IN',
  hi: 'hi-IN',
  bn: 'bn-IN',
  mr: 'mr-IN',
  ta: 'ta-IN'
};

document.addEventListener('DOMContentLoaded', () => {
  initLanguageSelector();
  fetchLaws('');
  updateUIStrings();
  setupVoiceRecognition();
});

// A11y live announcer
function announceA11y(text) {
  const log = document.getElementById('a11y-log');
  if (log) log.textContent = `"${text}"`;

  if (state.isSpeaking && 'speechSynthesis' in window) {
    window.speechSynthesis.cancel();
    const utter = new SpeechSynthesisUtterance(text);
    utter.lang = langSpeechMap[state.lang] || 'en-IN';
    utter.rate = 0.95;
    window.speechSynthesis.speak(utter);
  }
}

// Language selector initialization
function initLanguageSelector() {
  const select = document.getElementById('lang-select');
  if (!select) return;
  select.value = state.lang;
  select.addEventListener('change', (e) => {
    state.lang = e.target.value;
    updateUIStrings();
    fetchLaws(document.getElementById('search-input')?.value || '');
    announceA11y(`Language switched to ${state.lang.toUpperCase()}`);
  });
}

// Fetch localized strings from API
async function updateUIStrings() {
  try {
    const res = await fetch(`/api/i18n?lang=${state.lang}`);
    const data = await res.json();
    const msgs = data.messages;

    document.getElementById('portal-tagline').textContent = msgs.tagline;
    document.getElementById('article-39a-banner').innerHTML = msgs.article_39a_banner;
    document.getElementById('search-input').placeholder = msgs.search_placeholder;
    document.getElementById('search-btn-text').textContent = msgs.search_btn;

    document.getElementById('tab-btn-laws').textContent = `⚖️ ${msgs.tab_laws}`;
    document.getElementById('tab-btn-decrypt').textContent = `📜 ${msgs.tab_decrypt}`;
    document.getElementById('tab-btn-nalsa').textContent = `🛡️ ${msgs.tab_nalsa}`;
    document.getElementById('tab-btn-telelaw').textContent = `📞 ${msgs.tab_telelaw}`;

    document.getElementById('btn-mode-contrast').textContent = `👁️ ${msgs.high_contrast_btn}`;
    document.getElementById('btn-mode-easyread').textContent = `📖 ${msgs.easy_read_btn}`;
    document.getElementById('audio-label').textContent = msgs.listen_btn;
  } catch (err) {
    console.error("Failed to load i18n messages", err);
  }
}

// Tab navigation
function switchTab(tabId) {
  state.activeTab = tabId;
  const tabs = ['laws', 'decrypt', 'nalsa', 'telelaw'];
  tabs.forEach(t => {
    const tabEl = document.getElementById(`tab-content-${t}`);
    const btnEl = document.getElementById(`tab-btn-${t}`);
    if (t === tabId) {
      tabEl?.classList.remove('hidden');
      btnEl?.classList.add('border-blue-600', 'bg-blue-50', 'dark:bg-blue-950/40', 'text-blue-700', 'dark:text-blue-300', 'font-bold');
      btnEl?.setAttribute('aria-selected', 'true');
    } else {
      tabEl?.classList.add('hidden');
      btnEl?.classList.remove('border-blue-600', 'bg-blue-50', 'dark:bg-blue-950/40', 'text-blue-700', 'dark:text-blue-300', 'font-bold');
      btnEl?.setAttribute('aria-selected', 'false');
    }
  });
  announceA11y(`Switched to tab: ${tabId}`);
}

// Display Mode: Standard, High-Contrast, Easy-Read
function setDisplayMode(mode) {
  state.mode = mode;
  const body = document.body;
  body.classList.remove('theme-high-contrast', 'theme-easy-read');

  if (mode === 'contrast') {
    body.classList.add('theme-high-contrast');
    announceA11y("High Contrast OLED Mode Enabled (7:1+ Contrast Ratio)");
  } else if (mode === 'easyread') {
    body.classList.add('theme-easy-read');
    announceA11y("Easy Read & Dyslexia Mode Enabled");
  } else {
    announceA11y("Standard Mode Restored");
  }
}

// Toggle voice guidance
function toggleVoiceAudio() {
  state.isSpeaking = !state.isSpeaking;
  const btn = document.getElementById('btn-toggle-audio');
  const label = document.getElementById('audio-label');
  if (state.isSpeaking) {
    btn.classList.add('bg-emerald-600', 'text-white');
    label.textContent = "Voice Active";
    announceA11y("Voice guidance is now active. Screen updates will be spoken aloud.");
  } else {
    btn.classList.remove('bg-emerald-600', 'text-white');
    label.textContent = "Listen (Voice)";
    if ('speechSynthesis' in window) window.speechSynthesis.cancel();
    announceA11y("Voice guidance paused.");
  }
}

// Web Speech Recognition setup
function setupVoiceRecognition() {
  const micBtn = document.getElementById('btn-mic-search');
  if (!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
    if (micBtn) micBtn.style.display = 'none';
    return;
  }

  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  const recognition = new SpeechRecognition();
  recognition.continuous = false;
  recognition.interimResults = false;

  micBtn.addEventListener('click', () => {
    recognition.lang = langSpeechMap[state.lang] || 'en-IN';
    if (!state.isListening) {
      recognition.start();
      state.isListening = true;
      micBtn.classList.add('bg-red-600', 'text-white', 'animate-pulse');
      announceA11y("Listening to your voice... Speak now.");
    } else {
      recognition.stop();
      state.isListening = false;
      micBtn.classList.remove('bg-red-600', 'text-white', 'animate-pulse');
    }
  });

  recognition.onresult = (event) => {
    const text = event.results[0][0].transcript;
    document.getElementById('search-input').value = text;
    micBtn.classList.remove('bg-red-600', 'text-white', 'animate-pulse');
    state.isListening = false;
    fetchLaws(text);
    announceA11y(`Searching for: ${text}`);
  };

  recognition.onerror = () => {
    micBtn.classList.remove('bg-red-600', 'text-white', 'animate-pulse');
    state.isListening = false;
  };
}

// Fetch laws from API
async function fetchLaws(query = '') {
  const container = document.getElementById('laws-results-list');
  if (!container) return;
  container.innerHTML = `<div class="p-8 text-center text-sm text-[var(--muted-foreground)]">Loading Indian Laws and Penal Codes...</div>`;

  try {
    const res = await fetch(`/api/laws?q=${encodeURIComponent(query)}&lang=${state.lang}`);
    const data = await res.json();
    const laws = data.results || [];

    if (laws.length === 0) {
      container.innerHTML = `<div class="p-8 text-center text-sm text-[var(--muted-foreground)]">No matching legal records found. Try searching for 'cheating', 'land', 'bail', or 'violence'.</div>`;
      return;
    }

    container.innerHTML = laws.map(law => `
      <article class="p-6 rounded-2xl border border-[var(--border)] bg-[var(--card)] space-y-4 hover:border-blue-500 transition shadow-sm a11y-card">
        <div class="flex flex-wrap items-center justify-between gap-2">
          <div class="space-y-0.5">
            <span class="text-xs font-bold px-2.5 py-1 rounded bg-blue-100 text-blue-800 dark:bg-blue-950 dark:text-blue-200 border border-blue-500/20">
              ${law.act}
            </span>
            <h3 class="text-lg font-black pt-1">${law.section}: ${law.title}</h3>
            ${law.legacy_ref ? `<p class="text-xs text-[var(--muted-foreground)] a11y-text-muted">Legacy Equivalent: <strong>${law.legacy_ref}</strong></p>` : ''}
          </div>
          ${law.free_legal_aid_applicable ? `
            <span class="text-xs font-extrabold px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300 border border-emerald-500/30 flex items-center gap-1.5 a11y-badge">
              <span>⚖️</span> Free Legal Aid Guaranteed (Sec 12)
            </span>
          ` : ''}
        </div>

        <div class="p-4 rounded-xl bg-blue-50/60 dark:bg-blue-950/20 border border-blue-200/50 dark:border-blue-900/40 space-y-1">
          <div class="text-xs font-bold text-blue-800 dark:text-blue-300 uppercase tracking-wide">Plain-Language Meaning (कक्षा 4 स्तर)</div>
          <p class="text-sm font-medium leading-relaxed">${law.plain_language}</p>
        </div>

        <div class="space-y-1">
          <div class="text-xs font-bold text-[var(--muted-foreground)] a11y-text-muted uppercase tracking-wide">Immediate Citizen Action & Rights</div>
          <p class="text-xs leading-relaxed font-normal">${law.rights_and_actions}</p>
        </div>

        <div class="flex items-center justify-between pt-2 border-t border-[var(--border)] text-xs">
          <span class="text-[var(--muted-foreground)] a11y-text-muted">Category: ${law.category}</span>
          <button onclick="readAloudText('${encodeURIComponent(law.title + '. ' + law.plain_language)}')" class="font-bold text-blue-600 dark:text-blue-400 hover:underline flex items-center gap-1">
            <span>🔊</span> Listen
          </button>
        </div>
      </article>
    `).join('');

    announceA11y(`Found ${laws.length} Indian legal records.`);
  } catch (err) {
    container.innerHTML = `<div class="p-8 text-center text-sm text-red-600">Failed to connect to local legal engine.</div>`;
  }
}

function readAloudText(encoded) {
  const text = decodeURIComponent(encoded);
  announceA11y(text);
}

// Notice Decryption
async function decryptNoticeText(sampleType = null) {
  let text = '';
  if (sampleType === 'summons') {
    text = "न्यायालय अनुमंडल दंडाधिकारी, वाद संख्या 412/2026: बमुताबिक धारा 145 दंड प्रक्रिया संहिता (CrPC) / BNSS, प्रतिवादी को एतद द्वारा सूचित किया जाता है कि मौजा-रामपुर खाता सं. 42 खेसरा 108 बाबत भूमि विवाद में दिनांक 14 नवंबर को पूर्वाह्न 10:30 बजे सशरीर उपस्थित हों अन्यथा एकतरफा आदेश पारित कर दिया जाएगा।";
    document.getElementById('decrypt-input').value = text;
  } else if (sampleType === 'hospital') {
    text = "HOSPITAL BILLING MEMO: ADMISSION UNDER PM-JAY DENIED CITING NON-COVERAGE OF RETINOPATHY SURGICAL PACKAGE S110001. ADVANCE MANDATORY DEPOSIT OF ₹45,000 REQUIRED PRIOR TO INTERVENTION.";
    document.getElementById('decrypt-input').value = text;
  } else {
    text = document.getElementById('decrypt-input').value;
  }

  if (!text.trim()) {
    alert("Please enter or paste the text from your notice.");
    return;
  }

  const resultBox = document.getElementById('decrypt-result-box');
  resultBox.classList.remove('hidden');
  resultBox.innerHTML = `<div class="p-6 text-center text-sm text-[var(--muted-foreground)]">Analyzing with Indian Statutory RAG Engine...</div>`;

  try {
    const res = await fetch('/api/decrypt-notice', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, lang: state.lang })
    });
    const data = await res.json();

    resultBox.innerHTML = `
      <div class="p-6 rounded-2xl border-2 border-emerald-500/40 bg-emerald-50/40 dark:bg-emerald-950/20 space-y-4 a11y-card">
        <div class="flex flex-wrap items-center justify-between gap-2">
          <span class="text-xs font-bold px-3 py-1 rounded bg-emerald-100 text-emerald-800 dark:bg-emerald-900/60 font-semibold">
            ${data.detected_type}
          </span>
          <span class="text-xs text-[var(--muted-foreground)] a11y-text-muted">Governing Law: ${data.relevant_statute}</span>
        </div>

        <div class="p-3 rounded-lg bg-emerald-100/70 dark:bg-emerald-900/40 text-emerald-900 dark:text-emerald-200 text-sm font-bold flex items-center gap-2">
          <span class="text-lg">🛡️</span>
          <span>${data.panic_reduction}</span>
        </div>

        <div class="space-y-1">
          <div class="text-xs font-bold uppercase text-[var(--muted-foreground)] a11y-text-muted">Plain English / Regional Meaning</div>
          <p class="text-base font-semibold leading-relaxed">${data.plain_meaning}</p>
        </div>

        <div class="space-y-1">
          <div class="text-xs font-bold uppercase text-[var(--muted-foreground)] a11y-text-muted">What You Must Do Next</div>
          <p class="text-sm leading-relaxed">${data.action_steps}</p>
        </div>

        <div class="pt-3 border-t border-emerald-200 dark:border-emerald-900 flex flex-wrap items-center justify-between gap-2">
          <button onclick="switchTab('nalsa')" class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-lg text-xs shadow-sm min-h-[40px]">
            Claim Free DLSA Lawyer for this Notice →
          </button>
          <button onclick="readAloudText('${encodeURIComponent(data.panic_reduction + '. ' + data.plain_meaning + '. ' + data.action_steps)}')" class="font-bold text-emerald-700 dark:text-emerald-300 hover:underline text-xs flex items-center gap-1">
            <span>🔊</span> Listen
          </button>
        </div>
      </div>
    `;

    announceA11y(`${data.panic_reduction}. ${data.plain_meaning}`);
  } catch (err) {
    resultBox.innerHTML = `<div class="p-6 text-center text-sm text-red-600">Notice decryption failed.</div>`;
  }
}

// Section 12 NALSA Screener
async function runNALSAScreener() {
  const is_woman_or_child = document.getElementById('scr-woman').checked;
  const is_sc_st = document.getElementById('scr-scst').checked;
  const is_pwd = document.getElementById('scr-pwd').checked;
  const is_custody = document.getElementById('scr-custody').checked;
  const annual_income = parseFloat(document.getElementById('scr-income').value) || 0;
  const stateVal = document.getElementById('scr-state').value;

  const payload = {
    is_woman_or_child,
    is_sc_st,
    is_pwd,
    is_custody,
    annual_income,
    state: stateVal,
    lang: state.lang
  };

  const certBox = document.getElementById('nalsa-certificate-box');
  certBox.classList.remove('hidden');
  certBox.innerHTML = `<div class="p-6 text-center text-sm text-[var(--muted-foreground)]">Evaluating against Section 12 criteria...</div>`;

  try {
    const res = await fetch('/api/nalsa-screener', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();

    certBox.innerHTML = `
      <div class="p-6 rounded-2xl border-2 ${data.eligible ? 'border-emerald-500 bg-emerald-50/50 dark:bg-emerald-950/20' : 'border-amber-500 bg-amber-50/50 dark:bg-amber-950/20'} space-y-4 a11y-card">
        <div class="flex flex-wrap items-center justify-between gap-2 border-b border-[var(--border)] pb-3">
          <div>
            <span class="text-xs font-bold uppercase tracking-wider text-[var(--muted-foreground)]">NALSA Legal Aid Determination</span>
            <h4 class="text-xl font-extrabold text-[var(--foreground)]">${data.status}</h4>
          </div>
          <div class="text-right">
            <span class="text-xs font-mono px-2.5 py-1 rounded bg-[var(--card)] border border-[var(--border)] font-bold">
              ${data.certificate_id}
            </span>
          </div>
        </div>

        <p class="text-sm font-semibold leading-relaxed">${data.summary}</p>

        ${data.clauses && data.clauses.length > 0 ? `
          <div class="p-3 rounded-lg bg-[var(--card)] border border-[var(--border)] text-xs space-y-1">
            <div class="font-bold text-[var(--muted-foreground)]">Statutory Grounds of Entitlement:</div>
            <ul class="list-disc list-inside space-y-0.5">
              ${data.clauses.map(c => `<li><strong>${c}</strong></li>`).join('')}
            </ul>
          </div>
        ` : ''}

        <div class="space-y-1">
          <div class="text-xs font-bold uppercase text-[var(--muted-foreground)]">Action to Claim Representation:</div>
          <p class="text-xs leading-relaxed">${data.action}</p>
        </div>

        <div class="flex flex-wrap items-center justify-between gap-3 pt-3 border-t border-[var(--border)]">
          <button onclick="window.print()" class="px-5 py-2.5 rounded-xl bg-blue-600 text-white font-bold text-xs hover:bg-blue-700 transition shadow-sm min-h-[44px]">
            🖨️ Print / Save Official Certificate
          </button>
          <a href="tel:15100" class="px-5 py-2.5 rounded-xl border border-emerald-500 text-emerald-700 dark:text-emerald-300 font-bold text-xs hover:bg-emerald-50 transition min-h-[44px] flex items-center gap-1.5">
            📞 Dial NALSA Helpline (15100)
          </a>
        </div>
      </div>
    `;

    announceA11y(`${data.status}. ${data.summary}`);
  } catch (err) {
    certBox.innerHTML = `<div class="p-6 text-center text-sm text-red-600">Screener evaluation failed.</div>`;
  }
}
