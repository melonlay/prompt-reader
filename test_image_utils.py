from utils.image_utils import get_image_prompts
from PIL import Image
import os


def test_get_image_prompts():
    # 測試目錄
    test_dir = r"D:\workspace\python\sd20250224\stable-diffusion-webui\outputs\img2img-images\2025-03-13"

    # 遍歷目錄中的所有圖片
    for filename in os.listdir(test_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(test_dir, filename)
            print(f"\n處理圖片: {filename}")

            # 打開圖片並顯示完整信息
            with Image.open(image_path) as img:
                print("圖片信息:")
                for key, value in img.info.items():
                    print(f"  {key}: {value}")

            # 獲取提示詞
            prompts = get_image_prompts(image_path)

            # 輸出結果
            if prompts:
                print(f"找到提示詞: {prompts}")
            else:
                print("未找到提示詞")


if __name__ == "__main__":
    test_get_image_prompts()
