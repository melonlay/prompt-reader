class TranslationManager:
    def __init__(self):
        self.current_lang = "zh_tw"  # 預設繁體中文
        self.setup_translations()

    def setup_translations(self):
        """設置翻譯字典"""
        self.translations = {
            "zh_cn": {
                "window_title": "提示词编辑器",
                "select_folder": "选择文件夹",
                "no_folder": "未选择文件夹",
                "text_content": "提示词内容：",
                "temp_list": "常用提示词：",
                "delete": "删除",
                "prev": "上一张",
                "next": "下一张",
                "save": "保存提示词",
                "exit": "退出",
                "save_success": "提示词保存成功！",
                "save_failed": "提示词保存失败：",
                "temp_save_failed": "常用提示词保存失败：",
                "no_txt_file": "未找到对应的提示词文件",
                "no_file": "提示词内容：无对应文件",
                "loaded": "已加载",
                "load_failed": "读取失败",
                "saved": "已保存",
                "cant_read_file": "无法读取提示词文件：",
                "cant_read_temp": "无法读取常用提示词：",
                "save_status": "保存状态",
                "confirm": "确定",
                "language": "语言",
                "duplicate_prompt": "提示词已存在",
            },
            "zh_tw": {
                "window_title": "提示詞編輯器",
                "select_folder": "選擇資料夾",
                "no_folder": "未選擇資料夾",
                "text_content": "提示詞內容：",
                "temp_list": "常用提示詞：",
                "delete": "刪除",
                "prev": "上一張",
                "next": "下一張",
                "save": "儲存提示詞",
                "exit": "退出",
                "save_success": "提示詞儲存成功！",
                "save_failed": "提示詞儲存失敗：",
                "temp_save_failed": "常用提示詞儲存失敗：",
                "no_txt_file": "未找到對應的提示詞檔案",
                "no_file": "提示詞內容：無對應檔案",
                "loaded": "已載入",
                "load_failed": "讀取失敗",
                "saved": "已儲存",
                "cant_read_file": "無法讀取提示詞檔案：",
                "cant_read_temp": "無法讀取常用提示詞：",
                "save_status": "儲存狀態",
                "confirm": "確定",
                "language": "語言",
                "duplicate_prompt": "提示詞已存在",
            },
            "en": {
                "window_title": "Prompt Editor",
                "select_folder": "Select Folder",
                "no_folder": "No Folder Selected",
                "text_content": "Prompt Content: ",
                "temp_list": "Common Prompts: ",
                "delete": "Delete",
                "prev": "Previous",
                "next": "Next",
                "save": "Save Prompt",
                "exit": "Exit",
                "save_success": "Prompt Saved Successfully!",
                "save_failed": "Failed to Save Prompt: ",
                "temp_save_failed": "Failed to Save Common Prompts: ",
                "no_txt_file": "No corresponding prompt file found",
                "no_file": "Prompt Content: No File",
                "loaded": "Loaded",
                "load_failed": "Load Failed",
                "saved": "Saved",
                "cant_read_file": "Cannot read prompt file: ",
                "cant_read_temp": "Cannot read common prompts: ",
                "save_status": "Save Status",
                "confirm": "OK",
                "language": "Language",
                "duplicate_prompt": "Prompt already exists",
            }
        }

        # 語言顯示名稱映射
        self.language_names = {
            "zh_cn": "简体中文",
            "zh_tw": "繁體中文",
            "en": "English"
        }

    def get_text(self, key):
        """獲取當前語言的文本"""
        return self.translations[self.current_lang].get(key, key)

    def get_language_names(self):
        """獲取語言名稱映射"""
        return self.language_names

    def set_language(self, lang_code):
        """設置當前語言"""
        if lang_code in self.translations:
            self.current_lang = lang_code
            return True
        return False

    def get_current_language(self):
        """獲取當前語言代碼"""
        return self.current_lang
