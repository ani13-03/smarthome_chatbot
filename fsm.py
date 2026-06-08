# FSM.py
import random
from datetime import datetime

class SmartHomeFSM:
    def __init__(self):
        self.language = 'id'
        self.state = 'IDLE'
        
        self.devices = {
            'lampu': False,
            'tv': False,
            'ac': False,
            'cctv': True
        }
        
        self.history_log = []
        
        self.responses = {
            'id': {
                'welcome': "Halo! Saya asisten Smart Home Anda. Ketik **'bantuan'** untuk melihat daftar perintah.",
                'unknown': "Maaf, saya tidak memahami perintah tersebut. Ketik **'bantuan'** untuk melihat menu.",
                'nyala_lampu': "Lampu berhasil dinyalakan. 💡",
                'mati_lampu': "Lampu berhasil dimatikan. 🌑",
                'nyala_tv': "TV berhasil dinyalakan. 📺",
                'mati_tv': "TV berhasil dimatikan. 🔌",
                'nyala_ac': "AC berhasil dinyalakan. ❄️",
                'mati_ac': "AC berhasil dimatikan. 🌡️",
                'status_cctv': "CCTV 24 Jam aktif dan memantau dengan aman. 📹",
                'mode_tidur_tanya': "Apakah Anda ingin mengaktifkan Mode Tidur otomatis? (Ya/Tidak)",
                'mode_tidur_ya': "Mode Tidur diaktifkan. Lampu & TV dimatikan, AC tetap menyala untuk kenyamanan tidur Anda. 😴",
                'mode_tidur_tidak': "Mode Tidur dibatalkan. Perangkat tetap dalam kondisi semula. 👌",
                'nyala_semua': "Semua sistem rumah (Lampu, TV, AC) telah dinyalakan! ⚡",
                'mati_semua': "Semua sistem rumah telah dimatikan (CCTV tetap menyala). 🔒",
                'ada_orang': "Selamat datang kembali! Semua sistem otomatis dinyalakan demi kenyamanan Anda. 🏡✨",
                'keluar_rumah': "Mode Keluar Rumah aktif. Semua sistem dimatikan otomatis, CCTV tetap siaga 24 jam! 🛡️",
                'banjir': "⚠️ PERINGATAN: Terdeteksi kebocoran air/banjir! Segera amankan instalasi listrik rendah!",
                'kebakaran': "🚨 ALARM BAHAYA: Terdeteksi indikasi kebakaran/asap! Sistem sprinkler bersiap!",
                'gempa': "⚠️ PERINGATAN: Guncangan gempa terdeteksi! Harap berlindung di tempat yang aman!",
                'badai': "⚠️ PERINGATAN: Cuaca buruk/badai di luar! Jendela otomatis dikunci."
            },
            'en': {
                'welcome': "Hello! I am your Smart Home assistant. Type **'help'** to see the list of commands.",
                'unknown': "Sorry, I didn't understand that command. Type **'help'** to see the menu.",
                'nyala_lampu': "Lights turned on successfully. 💡",
                'mati_lampu': "Lights turned off successfully. 🌑",
                'nyala_tv': "TV turned on successfully. 📺",
                'mati_tv': "TV turned off successfully. 🔌",
                'nyala_ac': "AC turned on successfully. ❄️",
                'mati_ac': "AC turned off successfully. 🌡️",
                'status_cctv': "CCTV 24/7 is active and monitoring safely. 📹",
                'mode_tidur_tanya': "Would you like to activate automatic Sleep Mode? (Yes/No)",
                'mode_tidur_ya': "Sleep Mode activated. Lights & TV turned off, AC stays on for your comfort. 😴",
                'mode_tidur_tidak': "Sleep Mode canceled. Devices remain as they are. 👌",
                'nyala_semua': "All home systems (Lights, TV, AC) have been turned on! ⚡",
                'mati_semua': "All home systems have been turned off (CCTV stays ON). 🔒",
                'ada_orang': "Welcome back! All systems are automatically turned on for your comfort. 🏡✨",
                'keluar_rumah': "Away Mode active. All systems turned off automatically, CCTV remains on standby 24/7! 🛡️",
                'banjir': "⚠️ WARNING: Water leak/Flood detected! Please secure low electrical installations immediately!",
                'kebakaran': "🚨 EMERGENCY ALARM: Fire/Smoke detected! Sprinkler systems standing by!",
                'gempa': "⚠️ WARNING: Earthquake tremors detected! Please seek shelter in a safe place!",
                'badai': "⚠️ WARNING: Severe weather/Storm outside! Windows locked automatically."
            }
        }

    def add_to_history(self, action_id, action_en):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.history_log.append({
            'time': timestamp,
            'id': action_id,
            'en': action_en
        })

    def get_help_menu(self, lang: str) -> str:
        if lang == 'id':
            return """
            💡 **DAFTAR PERINTAH UTAMA (BAHASA INDONESIA)**
            * **Kontrol Perangkat:** `"nyalakan lampu"`, `"matikan lampu"`, `"nyalakan tv"`, `"matikan ac"`, dll.
            * **Aksi Massal:** `"nyalakan semua"`, `"matikan semua"`.
            * **Status CCTV:** `"cek cctv"` atau `"kamera"`.
            * **Skenario Rumah:** `"ada orang"` (semua nyala) & `"keluar rumah"` (semua mati kecuali CCTV).
            * **Mode Tidur:** `"mode tidur"` (sistem akan menanyakan konfirmasi Ya/Tidak).
            * **Simulasi Bencana:** `"terjadi banjir"`, `"kebakaran"`, `"gempa bumi"`, atau `"ada badai"`.
            * **Informasi Finansial:** `"cek tagihan listrik"`.
            * **Riwayat Perangkat:** `"lihat riwayat"` atau `"history"`.
            """
        else:
            return """
            💡 **MAIN COMMANDS LIST (ENGLISH)**
            * **Device Control:** `"turn on light"`, `"turn off light"`, `"turn on tv"`, `"turn off ac"`, etc.
            * **Bulk Actions:** `"turn on all"`, `"turn off all"`.
            * **CCTV Status:** `"check cctv"` or `"camera"`.
            * **Home Scenarios:** `"someone at home"` (all ON) & `"leave home"` (all OFF except CCTV).
            * **Sleep Mode:** `"sleep mode"` (the system will ask for Yes/No confirmation).
            * **Disaster Simulation:** `"flood detected"`, `"fire alarm"`, `"earthquake"`, or `"storm warning"`.
            * **Financial Information:** `"check electricity bill"`.
            * **Device History:** `"view history"` or `"log"`.
            """

    def process_command(self, intent: str, detected_lang: str) -> str:
        self.language = detected_lang
        lang = self.language

        if intent == 'bantuan':
            return self.get_help_menu(lang)

        if intent == 'lihat_riwayat':
            if not self.history_log:
                return "Riwayat kosong. Belum ada aktivitas perangkat." if lang == 'id' else "History is empty. No device activities yet."
            
            lines = ["📋 **Smart Home Activity History:**" if lang == 'en' else "📋 **Riwayat Aktivitas Rumah Pintar:**"]
            for log in reversed(self.history_log[-10:]):
                action = log['id'] if lang == 'id' else log['en']
                lines.append(f"• `[{log['time']}]` {action}")
            return "\n".join(lines)

        if intent == 'tagihan_listrik':
            base_bill = 150000
            active_count = sum([1 for k, v in self.devices.items() if v and k != 'cctv'])
            current_bill = base_bill + (active_count * 45000) + random.randint(1500, 5000)
            if lang == 'id':
                return f"🧾 **Estimasi Tagihan Listrik Bulan Ini:** Rp {current_bill:,}\n*(Dipengaruhi oleh {active_count} perangkat aktif + CCTV 24 Jam).* "
            else:
                return f"🧾 **Estimated Electricity Bill This Month:** IDR {current_bill:,}\n*(Affected by {active_count} active devices + 24/7 CCTV).* "

        if self.state == 'WAITING_SLEEP_CONFIRM':
            if intent == 'konfirmasi_ya':
                self.state = 'IDLE'
                self.devices['lampu'] = False
                self.devices['tv'] = False
                self.devices['ac'] = True
                self.add_to_history("Mode Tidur diaktifkan (Lampu & TV OFF, AC ON)", "Sleep Mode activated (Lights & TV OFF, AC ON)")
                return self.responses[lang]['mode_tidur_ya']
            elif intent == 'konfirmasi_tidak':
                self.state = 'IDLE'
                return self.responses[lang]['mode_tidur_tidak']
            else:
                return self.responses[lang]['mode_tidur_tanya']

        if intent == 'nyala_lampu':
            self.devices['lampu'] = True
            self.add_to_history("Lampu dinyalakan", "Lights turned ON")
            return self.responses[lang]['nyala_lampu']
        elif intent == 'mati_lampu':
            self.devices['lampu'] = False
            self.add_to_history("Lampu dimatikan", "Lights turned OFF")
            return self.responses[lang]['mati_lampu']
        elif intent == 'nyala_tv':
            self.devices['tv'] = True
            self.add_to_history("TV dinyalakan", "TV turned ON")
            return self.responses[lang]['nyala_tv']
        elif intent == 'mati_tv':
            self.devices['tv'] = False
            self.add_to_history("TV dimatikan", "TV turned OFF")
            return self.responses[lang]['mati_tv']
        elif intent == 'nyala_ac':
            self.devices['ac'] = True
            self.add_to_history("AC dinyalakan", "AC turned ON")
            return self.responses[lang]['nyala_ac']
        elif intent == 'mati_ac':
            self.devices['ac'] = False
            self.add_to_history("AC dimatikan", "AC turned OFF")
            return self.responses[lang]['mati_ac']
        elif intent == 'status_cctv':
            return self.responses[lang]['status_cctv']
            
        elif intent == 'mode_tidur':
            self.state = 'WAITING_SLEEP_CONFIRM'
            return self.responses[lang]['mode_tidur_tanya']
            
        elif intent in ['nyala_semua', 'ada_orang']:
            self.devices['lampu'] = True
            self.devices['tv'] = True
            self.devices['ac'] = True
            msg = "Sistem otomatis dinyalakan (Ada orang di rumah)" if intent == 'ada_orang' else "Semua perangkat dinyalakan"
            msg_en = "Systems automatically turned ON (Someone at home)" if intent == 'ada_orang' else "All devices turned ON"
            self.add_to_history(msg, msg_en)
            return self.responses[lang][intent]
            
        elif intent in ['mati_semua', 'keluar_rumah']:
            self.devices['lampu'] = False
            self.devices['tv'] = False
            self.devices['ac'] = False
            msg = "Sistem otomatis dimatikan (Keluar rumah)" if intent == 'keluar_rumah' else "Semua perangkat dimatikan"
            msg_en = "Systems automatically turned OFF (Away mode)" if intent == 'keluar_rumah' else "All devices turned OFF"
            self.add_to_history(msg, msg_en)
            return self.responses[lang][intent]

        elif intent in ['bencana_banjir', 'bencana_kebakaran', 'bencana_gempa', 'bencana_badai']:
            key = intent.split('_')[1]
            self.add_to_history(f"Peringatan bencana {key} dipicu", f"Disaster alert for {key} triggered")
            return self.responses[lang][key]

        return self.responses[lang]['unknown']