# engine.py
import re

class NLPEngine:
    def __init__(self):
        self.intents = {
            'bencana_banjir': r'\b(banjir|kebanjiran|flood|flooding|water leak)\b',
            'bencana_kebakaran': r'\b(kebakaran|api|asap|fire|smoke|burning)\b',
            'bencana_gempa': r'\b(gempa|earthquake|quake|guncangan)\b',
            'bencana_badai': r'\b(badai|topan|storm|hurricane|wind)\b',
            'nyala_lampu': r'\b(nyalakan|hidupkan|turn on|switch on).*lampu\b|\b(turn on|switch on).*light\b',
            'mati_lampu': r'\b(matikan|padamkan|turn off|switch off).*lampu\b|\b(turn off|switch off).*light\b',
            'nyala_tv': r'\b(nyalakan|hidupkan|turn on|switch on).*tv\b',
            'mati_tv': r'\b(matikan|padamkan|turn off|switch off).*tv\b',
            'nyala_ac': r'\b(nyalakan|hidupkan|turn on|switch on).*ac\b',
            'mati_ac': r'\b(matikan|padamkan|turn off|switch off).*ac\b',
            'status_cctv': r'\b(cctv|kamera|camera)\b',
            'mode_tidur': r'\b(mode tidur|sleep mode|tidur|sleep)\b',
            'nyala_semua': r'\b(nyalakan semua|hidupkan semua|turn on all|activate all)\b',
            'mati_semua': r'\b(matikan semua|padamkan semua|turn off all|deactivate all)\b',
            'ada_orang': r'\b(ada orang|datang|sampai rumah|i\'m home|arrived|someone at home)\b',
            'keluar_rumah': r'\b(keluar rumah|pergi|leave home|going out|leave)\b',
            'tagihan_listrik': r'\b(tagihan listrik|listrik|electricity bill|electricity|bill)\b',
            'konfirmasi_ya': r'\b(ya|yes|oke|setuju|boleh|yeah|ok|sure)\b',
            'konfirmasi_tidak': r'\b(tidak|no|jangan|batal|nope|cancel)\b',
            'bantuan': r'\b(bantuan|help|fitur|perintah|command|features|menu)\b',
            'lihat_riwayat': r'\b(riwayat|history|log|catatan)\b'
        }

    def detect_language(self, text: str) -> str:
        text = text.lower()
        en_keywords = [
            'turn on', 'turn off', 'switch', 'light', 'flood', 'fire', 'smoke', 
            'earthquake', 'storm', 'sleep', 'all', 'home', 'leave', 'bill', 'help', 'history', 'log'
        ]
        id_keywords = [
            'nyalakan', 'matikan', 'hidupkan', 'padamkan', 'lampu', 'banjir', 'kebakaran', 
            'api', 'asap', 'gempa', 'badai', 'tidur', 'semua', 'rumah', 'pergi', 'tagihan', 'bantuan', 'riwayat'
        ]
        
        en_score = sum(1 for word in en_keywords if word in text)
        id_score = sum(1 for word in id_keywords if word in text)
        
        if en_score > id_score:
            return 'en'
        return 'id'

    def detect_intent(self, text: str) -> str:
        text = text.lower()
        for intent, pattern in self.intents.items():
            if re.search(pattern, text):
                return intent
        return 'unknown'