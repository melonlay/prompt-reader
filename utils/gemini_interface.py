from google.genai import types
from PIL import Image
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch
import os
from google import genai


class GeminiInterface:
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.0-flash"

    def _gemini_sync(self, model, contents, config):
        response = self.client.models.generate_content(model=self.model,
                                                       contents=contents,
                                                       config=config)
        try:
            ret = response.text
        except ValueError:
            try:
                print(response)
                # If the response doesn't contain text, check if the prompt was blocked.
                print(response.prompt_feedback)
                # Also check the finish reason to see if the response was blocked.
                print(response.candidates[0].finish_reason)
                # If the finish reason was SAFETY, the safety ratings have more details.
                print(response.candidates[0].safety_ratings)
            except Exception as e:
                print(e)
            ret = 'blocked'
        return ret

    def get_prompt_suggestions(self, img, temp_prompts):
        """获取提示词建议"""
        command = '''looking at this image, please check the temp_prompt, and give me possible prompt in temp_prompt that is suitable for this image, 
        do not remove any underline _,
        and do not replace space with underline _ in the temp_prompt.
        input:{temp_prompts}
        Return:list[str]
        '''
        config = {
            'response_mime_type': 'application/json',
            'response_schema': list[str],
        }
        print('debug', command.format(temp_prompts=temp_prompts))
        content = [img, command.format(temp_prompts=temp_prompts)]
        response = self._gemini_sync(self.model, content, config)

        if response and response != 'blocked':
            try:
                # 尝试将响应转换为列表
                if isinstance(response, str):
                    suggestions = response.replace(
                        '"', '').replace(', ', ',').replace('[', '').replace(']', '').split(',')
                    print('debug', suggestions)
                    return suggestions
                return response
            except Exception as e:
                print(f"Error parsing Gemini response: {str(e)}")
                return []
        return []
