import streamlit as st
from engine import NLPEngine
from fsm import SmartHomeFSM

st.set_page_config(page_title="🏡 IoT Smart Home Chatbot", layout="centered")

# --- KUSTOMISASI CSS ANTI-BOCOR DARK MODE TOTAL CONTROL ---
st.markdown("""
    <style>
    /* 1. Paksa Background Aplikasi Selalu Pink Pastel */
    .stApp, .main, [data-testid="stAppViewContainer"], [data-testid="stMainBlockContainer"], [data-testid="stApp"] {
        background-color: #FFF0F5 !important;
    }
    
    div[data-testid="stVerticalBlock"], div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: transparent !important;
    }
    
    section[data-testid="stSidebar"], [data-testid="stSidebarUserContent"] {
        background-color: #FFE4E1 !important;
    }

    /* 2. Kunci Warna Semua Elemen Teks Global Agar Tetap Gelap */
    h1, h2, h3, h4, h5, h6, p, span, label, li, 
    .stMarkdown, .stMarkdown p, .stCaption p,
    [data-testid="stWidgetLabel"] p, .stChatMessage p {
        color: #4A4A4A !important;
        -webkit-text-fill-color: #4A4A4A !important;
    }
    
    /* 3. Bar Judul Utama */
    .brand-title-bar {
        background-color: #FFD1DC !important;
        padding: 20px;
        border-radius: 15px;
        border-bottom: 4px solid #FF69B4;
        box-shadow: 0px 4px 10px rgba(255, 182, 193, 0.4);
        text-align: center;
        margin-bottom: 25px;
    }
    .brand-title-bar h1 {
        color: #D11A7A !important;
        -webkit-text-fill-color: #D11A7A !important;
        margin: 0;
        font-size: 32px;
        font-weight: 800;
    }
    .brand-title-bar p {
        color: #7A4A56 !important;
        -webkit-text-fill-color: #7A4A56 !important;
        margin: 5px 0 0 0;
        font-size: 14px;
        font-style: italic;
    }

    /* 4. OVERRIDE UNTUK TAB MENU */
    div[data-testid="stTabPanel"], 
    div[data-testid="stTabsCapsule"], 
    [data-baseweb="tab-list"],
    [role="tablist"] {
        background-color: #FFF0F5 !important;
        border-bottom: 2px solid #FFB6C1 !important;
    }
    
    button[data-baseweb="tab"], [role="tab"] {
        font-size: 16px !important;
        font-weight: bold !important;
        color: #7A4A56 !important; 
        -webkit-text-fill-color: #7A4A56 !important;
        background-color: transparent !important;
        border: none !important;
    }
    
    button[data-baseweb="tab"][aria-selected="true"], [role="tab"][aria-selected="true"] {
        color: #FF1493 !important;
        -webkit-text-fill-color: #FF1493 !important;
        background-color: #FFE4E1 !important;
        border-bottom: 3px solid #FF1493 !important;
        border-radius: 8px 8px 0px 0px !important;
    }
    
    button[data-baseweb="tab"]:hover, [role="tab"]:hover {
        background-color: rgba(255, 182, 193, 0.2) !important;
    }

    /* 5. OVERRIDE INPUT CHAT UTAMA (MENGHANCURKAN WARNA DARK MODE BAWAAN STREAMLIT) */
    /* Wadah terluar pembungkus form input chat */
    div[data-testid="stChatInput"], 
    div[data-testid="stChatInputForm"], 
    form[data-testid="stChatInputForm"] {
        background-color: #FFE4E1 !important;
        border: 2px solid #FF1493 !important;
        border-radius: 12px !important;
        padding: 5px !important;
        box-shadow: none !important;
    }
    
    /* Memaksa elemen boks dalam (pembungkus textarea) agar tidak berwarna hitam/gelap */
    div[data-testid="stChatInput"] > div, 
    div[data-testid="stChatInputForm"] > div {
        background-color: #FFF0F5 !important;
        border: none !important;
    }
    
    /* Elemen teks input form/textarea boks chat */
    div[data-testid="stChatInput"] textarea, 
    [data-testid="stChatInputForm"] textarea {
        background-color: #FFF0F5 !important;
        color: #222222 !important;
        -webkit-text-fill-color: #222222 !important;
        border: none !important;
    }
    
    /* Memaksa text placeholder petunjuk ketik agar tetap terlihat gelap */
    div[data-testid="stChatInput"] textarea::placeholder, 
    [data-testid="stChatInputForm"] textarea::placeholder {
        color: #777777 !important;
        -webkit-text-fill-color: #777777 !important;
        opacity: 1 !important;
    }
    
    /* Tombol kirim panah atas di dalam boks chat */
    div[data-testid="stChatInput"] button, 
    [data-testid="stChatInputForm"] button {
        background-color: #FFB6C1 !important;
        border-radius: 8px !important;
        color: #4A4A4A !important;
    }
    
    /* 6. AREA BALON CHAT */
    div[data-testid="stChatMessage"] {
        background-color: transparent !important;
    }
    .stChatMessage[data-testid="stChatMessageUser"] > div {
        background-color: #FFB6C1 !important;
        border-radius: 15px;
        padding: 10px;
    }
    .stChatMessage[data-testid="stChatMessageAssistant"] > div {
        background-color: #FFD1DC !important;
        border-radius: 15px;
        padding: 10px;
    }
    
    /* 7. Komponen Sidebar & Kontrol */
    .status-box {
        background-color: #FFB6C1 !important;
        padding: 12px;
        border-radius: 10px;
        border-left: 5px solid #FF1493;
        margin-bottom: 10px;
        box-shadow: 1px 1px 5px rgba(0,0,0,0.05);
    }
    .status-box b, .status-box span {
        color: #4A4A4A !important;
        -webkit-text-fill-color: #4A4A4A !important;
    }
    
    .control-container {
        background-color: #FFE4E1 !important;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

if 'fsm' not in st.session_state:
    st.session_state.fsm = SmartHomeFSM()
if 'nlp' not in st.session_state:
    st.session_state.nlp = NLPEngine()
if 'messages' not in st.session_state:
    st.session_state.messages = []

def sync_lamp():
    old_state = st.session_state.fsm.devices['lampu']
    new_state = st.session_state.tg_lamp
    if old_state != new_state:
        st.session_state.fsm.devices['lampu'] = new_state
        if new_state:
            st.session_state.fsm.add_to_history("Lampu dinyalakan via Panel", "Lights turned ON via Panel")
        else:
            st.session_state.fsm.add_to_history("Lampu dimatikan via Panel", "Lights turned OFF via Panel")

def sync_tv():
    old_state = st.session_state.fsm.devices['tv']
    new_state = st.session_state.tg_tv
    if old_state != new_state:
        st.session_state.fsm.devices['tv'] = new_state
        if new_state:
            st.session_state.fsm.add_to_history("TV dinyalakan via Panel", "TV turned ON via Panel")
        else:
            st.session_state.fsm.add_to_history("TV dimatikan via Panel", "TV turned OFF via Panel")

def sync_ac():
    old_state = st.session_state.fsm.devices['ac']
    new_state = st.session_state.tg_ac
    if old_state != new_state:
        st.session_state.fsm.devices['ac'] = new_state
        if new_state:
            st.session_state.fsm.add_to_history("AC dinyalakan via Panel", "AC turned ON via Panel")
        else:
            st.session_state.fsm.add_to_history("AC dimatikan via Panel", "AC turned OFF via Panel")

HELP_TEXT_ID = """💡 **DAFTAR PERINTAH UTAMA (BAHASA INDONESIA):**
* 🔌 **Kontrol Perangkat:** `"nyalakan lampu"`, `"matikan lampu"`, `"nyalakan tv"`, `"matikan ac"`, dll.
* ⚡ **Aksi Massal:** `"nyalakan semua"`, `"matikan semua"`.
* 📹 **Status CCTV:** `"cek cctv"` atau `"kamera"`.
* 🏡 **Skenario Rumah:** `"ada orang"` *(semua nyala)* & `"keluar rumah"` *(semua mati kecuali CCTV)*.
* 💤 **Mode Tidur:** `"mode tidur"` *(sistem akan menanyakan konfirmasi Ya/Tidak)*.
* ⚠️ **Simulasi Bencana:** `"terjadi banjir"`, `"kebakaran"`, `"gempa bumi"`, atau `"ada badai"`.
* 💰 **Informasi Finansial:** `"cek tagihan listrik"`.
* 📜 **Riwayat Perangkat:** Silakan langsung buka tab **Catatan Sistem Real-time** di atas.
"""

HELP_TEXT_EN = """💡 **MAIN COMMAND LIST (ENGLISH):**
* 🔌 **Device Control:** `"turn on light"`, `"turn off light"`, `"turn on tv"`, `"turn off ac"`, etc.
* ⚡ **Bulk Action:** `"turn on all"`, `"turn off all"`.
* 📹 **CCTV Status:** `"check cctv"` or `"camera"`.
* 🏡 **Home Scenario:** `"i'm home"` *(all on)* & `"leave home"` *(all off except CCTV)*.
* 💤 **Sleep Mode:** `"sleep mode"` *(the system will ask for Yes/No confirmation)*.
* ⚠️ **Disaster Simulation:** `"flood happened"`, `"fire"`, `"earthquake"`, or `"storm"`.
* 💰 **Financial Info:** `"check bill"` or `"check electricity"`.
* 📜 **Device History:** Please view the **Real-time System Log** tab directly above.
"""

with st.sidebar:
    st.header("⚙️ Settings & Status")
    
    lang_option = st.radio(
        "🌐 Choose Language / Pilih Bahasa:",
        options=["Bahasa Indonesia", "English"],
        index=0 if st.session_state.fsm.language == 'id' else 1
    )
    
    chosen_lang_code = 'id' if lang_option == "Bahasa Indonesia" else 'en'
    
    if st.session_state.fsm.language != chosen_lang_code:
        st.session_state.fsm.language = chosen_lang_code
        st.session_state.messages = [{"role": "assistant", "content": st.session_state.fsm.responses[chosen_lang_code]['welcome']}]
        st.rerun()

    active_lang = st.session_state.fsm.language
    st.write("---")
    
    st.subheader("🏡 Status Perangkat" if active_lang == 'id' else "🏡 Device Status")
    
    def get_status_emoji(state):
        return "🟢 ON" if state else "🔴 OFF"

    devices = st.session_state.fsm.devices
    
    lamp_label = "💡 Lampu:" if active_lang == 'id' else "💡 Light:"
    tv_label = "📺 Televisi (TV):" if active_lang == 'id' else "📺 Television (TV):"
    ac_label = "❄️ Pendingin Ruangan (AC):" if active_lang == 'id' else "❄️ Air Conditioner (AC):"
    cctv_label = "📹 CCTV (24 Jam):" if active_lang == 'id' else "📹 CCTV (24 Hours):"
    cctv_sub = "(Selalu Aktif)" if active_lang == 'id' else "(Always Active)"
    
    st.markdown(f"<div class='status-box'><b>{lamp_label}</b> {get_status_emoji(devices['lampu'])}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='status-box'><b>{tv_label}</b> {get_status_emoji(devices['tv'])}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='status-box'><b>{ac_label}</b> {get_status_emoji(devices['ac'])}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='status-box'><b>{cctv_label}</b> {get_status_emoji(devices['cctv'])} {cctv_sub}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='status-box'><b>🤖 FSM State:</b> {st.session_state.fsm.state}</div>", unsafe_allow_html=True)
    
    st.write("---")
    st.markdown(HELP_TEXT_ID if active_lang == 'id' else HELP_TEXT_EN)

if not st.session_state.messages:
    st.session_state.messages.append({"role": "assistant", "content": st.session_state.fsm.responses[active_lang]['welcome']})

title_text = "🏡 Smart Home Chatbot"
subtitle_text = "Kontrol kediaman pintar Anda dengan gaya yang nyaman dan aman." if active_lang == 'id' else "Control your smart home safely and stylishly."

st.markdown(f"""
    <div class='brand-title-bar'>
        <h1>{title_text}</h1>
        <p>{subtitle_text}</p>
    </div>
""", unsafe_allow_html=True)

if active_lang == 'id':
    tab_labels = ["💬 Asisten Obrolan NLP", "🎛️ Panel Pusat Kendali", "📜 Catatan Sistem Real-time"]
else:
    tab_labels = ["💬 NLP Chat Assistant", "🎛️ Control Center Panel", "📜 Real-time System Log"]

tab_chat, tab_control, tab_log = st.tabs(tab_labels)

# --- TAB 1: NLP CHAT ASSISTANT ---
with tab_chat:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message['content'])

    placeholder_txt = "Ketik di sini (contoh: 'bantuan', 'cek listrik')..." if active_lang == 'id' else "Type here (e.g., 'help', 'check bill')...."
    if user_input := st.chat_input(placeholder_txt):
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        cleaned_input = user_input.lower().strip()
        if cleaned_input in ["bantuan", "help", "perintah", "menu"]:
            bot_response = HELP_TEXT_ID if active_lang == 'id' else HELP_TEXT_EN
        else:
            detected_intent = st.session_state.nlp.detect_intent(user_input)
            bot_response = st.session_state.fsm.process_command(detected_intent, active_lang)
        
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        st.rerun()

# --- TAB 2: CONTROL CENTER PANEL ---
with tab_control:
    ctrl_title = "🎛️ Panel Kendali Manual Perangkat" if active_lang == 'id' else "🎛️ Manual Device Control Panel"
    ctrl_desc = "Ubah status perangkat secara langsung tanpa melalui chat." if active_lang == 'id' else "Change device status directly without using chat."
    st.subheader(ctrl_title)
    st.write(ctrl_desc)
    
    toggle_lamp_txt = "💡 Sakelar Lampu Utama" if active_lang == 'id' else "💡 Main Light Switch"
    toggle_tv_txt = "📺 Sakelar Televisi (TV)" if active_lang == 'id' else "📺 Television (TV) Switch"
    toggle_ac_txt = "❄️ Sakelar Pendingin Ruangan (AC)" if active_lang == 'id' else "❄️ Air Conditioner (AC) Switch"
    
    st.markdown("<div class='control-container'>", unsafe_allow_html=True)
    st.toggle(toggle_lamp_txt, value=st.session_state.fsm.devices['lampu'], key="tg_lamp", on_change=sync_lamp)
    st.toggle(toggle_tv_txt, value=st.session_state.fsm.devices['tv'], key="tg_tv", on_change=sync_tv)
    st.toggle(toggle_ac_txt, value=st.session_state.fsm.devices['ac'], key="tg_ac", on_change=sync_ac)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.write("---")
    note_txt = "Catatan: CCTV dikunci oleh sistem FSM demi keamanan." if active_lang == 'id' else "Note: CCTV is locked by the FSM system for security."
    st.caption(note_txt)

# --- TAB 3: REAL-TIME SYSTEM LOG (HISTORY) ---
with tab_log:
    log_title = "📜 Catatan Aktivitas Perangkat Real-time" if active_lang == 'id' else "📜 Real-time Device Activity Log"
    log_desc = "Seluruh perubahan status perangkat yang terdeteksi oleh sistem FSM." if active_lang == 'id' else "All device status changes detected by the FSM system."
    st.subheader(log_title)
    st.write(log_desc)
    
    history_data = st.session_state.fsm.history_log
    
    if not history_data:
        empty_txt = "Belum ada riwayat aktivitas yang tercatat." if active_lang == 'id' else "No activity history recorded yet."
        st.info(empty_txt)
    else:
        for log in reversed(history_data):
            action_text = log['id'] if active_lang == 'id' else log['en']
            st.markdown(f"⏱️ `[{log['time']}]` &nbsp;&nbsp; {action_text}")