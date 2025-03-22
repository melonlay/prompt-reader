import os
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk


class ImageHandler:
    def __init__(self):
        self.current_index = -1
        self.image_files = []
        self.photo = None
        self.current_image = None
        # 設置固定的顯示區域尺寸
        self.display_width = 400
        self.display_height = 400

    def load_images(self, folder_path):
        """加載資料夾中的圖片"""
        self.image_files = []
        for file in os.listdir(folder_path):
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                self.image_files.append(os.path.join(folder_path, file))
        self.image_files.sort()  # 按文件名排序
        if self.image_files:
            self.current_index = 0
            self.current_image = Image.open(self.image_files[0])
        return bool(self.image_files)

    def resize_image(self, image):
        """按比例調整圖片大小以適應固定的顯示區域"""
        # 獲取原始圖片尺寸
        w, h = image.size

        # 計算縮放比例
        width_ratio = self.display_width / w
        height_ratio = self.display_height / h
        ratio = min(width_ratio, height_ratio)

        # 計算新的尺寸
        new_width = int(w * ratio)
        new_height = int(h * ratio)

        # 調整圖片大小
        resized_image = image.resize(
            (new_width, new_height), Image.Resampling.LANCZOS)

        # 創建一個固定大小的白色背景
        background = Image.new(
            'RGB', (self.display_width, self.display_height), 'white')

        # 將調整後的圖片居中放置在背景上
        x = (self.display_width - new_width) // 2
        y = (self.display_height - new_height) // 2
        background.paste(resized_image, (x, y))

        return background

    def show_image(self, index, image_label):
        """顯示指定索引的圖片"""
        if 0 <= index < len(self.image_files):
            self.current_index = index
            try:
                # 打開並調整圖片大小
                image = Image.open(self.image_files[index])
                resized_image = self.resize_image(image)

                # 創建 PhotoImage 對象
                self.photo = ImageTk.PhotoImage(resized_image)

                # 更新標籤
                image_label.configure(image=self.photo)
                return True
            except Exception as e:
                print(f"無法載入圖片: {str(e)}")
                return False
        return False

    def get_current_image_path(self):
        """獲取當前圖片路徑"""
        if 0 <= self.current_index < len(self.image_files):
            return self.image_files[self.current_index]
        return None

    def get_total_images(self):
        """獲取圖片總數"""
        return len(self.image_files)

    def get_current_index(self):
        """獲取當前圖片索引"""
        return self.current_index

    def can_move_prev(self):
        """檢查是否可以顯示上一張圖片"""
        return self.current_index > 0

    def can_move_next(self):
        """檢查是否可以顯示下一張圖片"""
        return self.current_index < len(self.image_files) - 1

    def set_current_image(self, index):
        """設置當前圖片"""
        if 0 <= index < len(self.image_files):
            self.current_index = index
            self.current_image = Image.open(self.image_files[index])
            return True
        return False
