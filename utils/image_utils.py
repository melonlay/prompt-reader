from PIL import Image
import json


def get_image_prompts(image_path):
    """
    從圖片中讀取提示詞信息

    Args:
        image_path (str): 圖片的路徑

    Returns:
        list: 包含提示詞的列表，如果沒有找到提示詞則返回空列表
    """
    try:
        # 打開圖片
        with Image.open(image_path) as img:
            # 獲取圖片信息
            info = img.info

            # 檢查是否有參數信息
            if 'parameters' in info:
                # 分割參數字符串，第一個部分通常是提示詞
                params = info['parameters'].split('\n')
                if params:
                    # 分割提示詞，並過濾空字符串
                    prompts = [p.strip()
                               for p in params[0].split(',') if p.strip()]
                    return prompts

            # 檢查是否有其他格式的提示詞信息
            if 'prompt' in info:
                # 如果是字符串格式
                if isinstance(info['prompt'], str):
                    prompts = [p.strip()
                               for p in info['prompt'].split(',') if p.strip()]
                    return prompts
                # 如果是 JSON 格式
                elif isinstance(info['prompt'], dict):
                    return info['prompt'].get('prompts', [])

            # 檢查是否有 PNG 特定的元數據
            if 'Description' in info:
                try:
                    # 嘗試解析 JSON 格式的描述
                    desc = json.loads(info['Description'])
                    if isinstance(desc, dict) and 'prompt' in desc:
                        prompts = [p.strip()
                                   for p in desc['prompt'].split(',') if p.strip()]
                        return prompts
                except:
                    pass

            # 檢查是否有其他常見的元數據字段
            for key in ['UserComment', 'Comment', 'ImageDescription']:
                if key in info:
                    value = info[key]
                    if isinstance(value, str):
                        # 嘗試分割字符串
                        prompts = [p.strip()
                                   for p in value.split(',') if p.strip()]
                        if prompts:
                            return prompts

    except Exception as e:
        print(f"讀取圖片提示詞時發生錯誤: {str(e)}")

    return []
