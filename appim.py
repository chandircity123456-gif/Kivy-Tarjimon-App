import json
import requests
import time 
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
# from kivy.lang import Builder # Builder'ni yuklash shart emas, chunki qo'lda yuklamaymiz
from kivy.clock import Clock
from threading import Thread

# --- API MA'LUMOTLARI ---
# !!! DIQQAT !!! Bu joyga O'ZINGIZNING ISHLOVCHI API KALITINGIZNI kiriting!
GEMINI_API_KEY = "AIzaSyCAmVUvznajx7o5qcSA6hKj2gqBI035-_8"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

# Til nomlari
LANGUAGES = {
    "O'zbekcha": "uzbek",
    "Inglizcha": "english",
    "Ruscha": "russian"
}
# ------------------------


class Translatorbox(BoxLayout):
    """Kivy dizayn fayli (aitarjimon.kv) bilan bog'lanadigan asosiy sinf"""
    
    def translate_text(self, text_to_translate, source_lang_name, target_lang_name):
        
        if not text_to_translate or text_to_translate.isspace():
            self.ids.result_label.text = "Iltimos, avval tarjima uchun matn kiriting."
            return

        source_lang = source_lang_name 
        target_lang = target_lang_name 

        if source_lang == target_lang:
            self.ids.result_label.text = "Manba tili va Maqsad tili bir xil bo'lishi mumkin emas. Iltimos, boshqa tilni tanlang."
            return

        self.ids.translate_button.disabled = True
        self.ids.result_label.text = "Tarjima qilinmoqda... Iltimos kuting."

        Thread(target=self._run_translation, args=(text_to_translate, source_lang, target_lang)).start()

    def _get_translation_prompt(self, text_to_translate, source_lang_name, target_lang_name):
        prompt = (
            f"Matnni '{source_lang_name}' tilidan '{target_lang_name}' tiliga professional darajada tarjima qiling "
            f"va faqat tarjima natijasini qaytaring. Matn: \"{text_to_translate}\""
        )
        return prompt

    def _run_translation(self, text_to_translate, source_lang_name, target_lang_name):
        prompt = self._get_translation_prompt(text_to_translate, source_lang_name, target_lang_name)
        
        url_with_key = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"
        
        payload = {
            "contents": [
                {"parts": [{"text": prompt}]}
            ]
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        max_retries = 3
        delay_seconds = 1
        
        try:
            for i in range(max_retries):
                response = requests.post(url_with_key, headers=headers, data=json.dumps(payload), timeout=15)
                
                if response.status_code == 200:
                    break
                
                if i < max_retries - 1:
                    time.sleep(delay_seconds)
                    delay_seconds *= 2
                else:
                    response.raise_for_status()

            json_response = response.json()
            translated_text = self._parse_gemini_response(json_response)
            
        except requests.exceptions.RequestException as e:
            translated_text = f"Internet/API ulanish xatosi: {e}"
        except Exception as e:
            translated_text = f"Kutilmagan xato: {e}"
        
        Clock.schedule_once(lambda dt: self._update_ui_result(translated_text), 0)

    def _parse_gemini_response(self, result):
        if result and 'candidates' in result and len(result['candidates']) > 0:
            candidate = result['candidates'][0]
            
            if 'finishReason' in candidate and candidate['finishReason'] != "STOP":
                return f"Tarjima bekor qilindi. Sabab: {candidate['finishReason']}. Matn xavfsizlik qoidalariga mos kelmasligi mumkin."
            
            if 'content' in candidate and 'parts' in candidate['content'] and len(candidate['content']['parts']) > 0 and 'text' in candidate['content']['parts'][0]:
                return candidate['content']['parts'][0]['text'].strip()
            
            return "Tarjima natijasi topilmadi (Bo'sh javob)."
        
        if 'error' in result:
            return f"API xatosi: {result['error']['message']}"
        
        return "Tarjima natijasi topilmadi (Javob strukturasi kutilganidek emas)."

    def _update_ui_result(self, result_text):
        self.ids.result_label.text = result_text
        self.ids.translate_button.disabled = False


class AITarjimonApp(App):
    """Asosiy ilova sinfi"""
    def build(self):
        # Kivy faylini qo'lda yuklash olib tashlandi.
        # Kivy endi App sinfining nomiga qarab avtomatik ravishda 'aitarjimon.kv' ni izlaydi.
        return Translatorbox()

if __name__ == '__main__':
    AITarjimonApp().run()