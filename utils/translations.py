from typing import Dict, List, Optional
import json
import os


class TranslationManager:
    def __init__(self) -> None:
        self.current_lang = "zh_TW"  # 預設繁體中文
        self.translations: Dict[str, Dict[str, str]] = {}
        self.language_names = {
            "zh_CN": "简体中文",
            "zh_TW": "繁體中文",
            "en": "English"
        }
        self.setup_translations()

    def setup_translations(self) -> None:
        """設置翻譯字典"""
        self.translations = {}
        self.language_names = {
            "zh_CN": "简体中文",
            "zh_TW": "繁體中文",
            "en": "English"
        }

        # 從 JSON 文件加載翻譯
        translations_dir = os.path.join(os.path.dirname(
            os.path.dirname(__file__)), 'translations')
        for lang_code in self.language_names.keys():
            json_path = os.path.join(
                translations_dir, f'{lang_code.lower()}.json')
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    self.translations[lang_code] = json.load(f)
            except Exception as e:
                print(f"無法加載 {lang_code} 的翻譯文件：{str(e)}")
                # 如果加載失敗，使用空字典
                self.translations[lang_code] = {}

    def get_text(self, key: str) -> str:
        """獲取當前語言的文本"""
        return self.translations[self.current_lang].get(key, key)

    def get_language_names(self) -> List[str]:
        """獲取語言名稱映射"""
        return list(self.language_names.keys())

    def set_language(self, lang_code: str) -> None:
        """設置當前語言"""
        if lang_code in self.translations:
            self.current_lang = lang_code
            return True
        return False

    def get_current_language(self) -> str:
        """獲取當前語言代碼"""
        return self.current_lang
