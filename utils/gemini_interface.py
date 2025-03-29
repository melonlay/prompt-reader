from google.genai import types
from PIL import Image
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch
import os
from google import genai
from typing import List, Optional, Dict, Any


class GeminiInterface:
    """
    Gemini AI 介面類，用於與 Google 的 Gemini AI 模型進行互動。
    主要功能包括：
    1. 初始化 Gemini API 客戶端
    2. 同步調用 Gemini API 生成內容
    3. 基於圖片和現有提示詞生成新的提示詞建議
    """

    def __init__(self, api_key: str) -> None:
        """
        初始化 GeminiInterface 類

        Args:
            api_key (str): Gemini API 密鑰，用於認證 API 請求
        """
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.0-flash"  # 使用 Gemini 2.0 Flash 模型

    def _gemini_sync(self, model: Any, contents: List[Any], config: Dict[str, Any]) -> Optional[str]:
        """
        同步調用 Gemini API 生成內容

        Args:
            model (Any): Gemini 模型實例
            contents (List[Any]): 輸入內容列表，可以包含文字和圖片
            config (Dict[str, Any]): 生成配置參數

        Returns:
            Optional[str]: 生成的文字內容，如果發生錯誤則返回 None
        """
        response = self.client.models.generate_content(model=self.model,
                                                       contents=contents,
                                                       config=config)
        try:
            return response.text
        except Exception as e:
            print(f"Error in Gemini API call: {e}")
            return None

    def get_prompt_suggestions(self, img: Image.Image, temp_prompts: List[str]) -> List[str]:
        """
        基於當前圖片和臨時提示詞列表生成新的提示詞建議

        Args:
            img (Image.Image): 當前圖片物件
            temp_prompts (List[str]): 臨時提示詞列表

        Returns:
            List[str]: 生成的提示詞建議列表，最多返回5個建議
        """
        try:
            # 準備提示詞
            prompt = f"""請根據以下提示詞生成更多相關的提示詞建議（最多5個）：
{', '.join(temp_prompts)}

請只返回新的提示詞，每行一個，不要包含任何其他文字。"""

            # 配置生成參數
            config = {
                "temperature": 0.7,  # 控制輸出的隨機性
                "top_p": 0.8,        # 控制輸出的多樣性
                "top_k": 40,         # 控制每次選擇的範圍
                "max_output_tokens": 1024,  # 最大輸出長度
            }

            # 調用 API
            response = self._gemini_sync(self.model, [prompt, img], config)

            if response:
                # 處理返回結果
                suggestions = [line.strip()
                               for line in response.split('\n') if line.strip()]
                return suggestions[:5]  # 最多返回5個建議
            return []
        except Exception as e:
            print(f"Error getting prompt suggestions: {e}")
            return []
