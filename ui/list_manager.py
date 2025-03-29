import tkinter as tk
from tkinter import ttk
import os
from .ui_components import ListFrame
from utils.gemini_interface import GeminiInterface
from PIL import Image
from typing import List, Optional, Callable


class ListManager:
    def __init__(self, parent, translation_manager):
        self.translation_manager = translation_manager
        self.create_frame(parent)
        self.current_folder = ""
        self.current_txt_path = None

        # 初始化 Gemini 接口
        api_key = os.getenv('GEMINI_API_KEY')
        if api_key:
            try:
                self.gemini = GeminiInterface(api_key)
            except Exception as e:
                print(f"Error initializing Gemini interface: {str(e)}")
                self.gemini = None
        else:
            self.gemini = None

        # 創建右鍵選單
        self.context_menu = tk.Menu(parent, tearoff=0)
        self.context_menu.add_command(label=self.get_text(
            "delete"), command=self.delete_selected_item)

    def get_text(self, key):
        """獲取當前語言的文本"""
        return self.translation_manager.get_text(key)

    def create_frame(self, parent):
        """創建列表管理器框架"""
        self.frame = ttk.Frame(parent)
        self.frame.grid_rowconfigure(2, weight=1)  # 修改權重，為輸入區域留出空間
        self.frame.grid_columnconfigure(0, weight=1)

        # 創建狀態標籤
        self.status_label = ttk.Label(self.frame, text="")
        self.status_label.grid(
            row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))

        # 創建輸入區域
        self.create_input_frame()

        # 創建列表區域
        self.lists_frame = ttk.Frame(self.frame)
        self.lists_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 設置列表框架的行列權重
        self.lists_frame.grid_rowconfigure(0, weight=1)
        self.lists_frame.grid_columnconfigure(0, weight=1)
        self.lists_frame.grid_columnconfigure(2, weight=1)

        self.setup_list_frames()

    def create_input_frame(self):
        """創建提示詞輸入區域"""
        self.input_frame = ttk.Frame(self.frame)
        self.input_frame.grid(
            row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        self.input_frame.grid_columnconfigure(0, weight=1)

        # 創建輸入框
        self.prompt_var = tk.StringVar()
        self.prompt_entry = ttk.Entry(
            self.input_frame,
            textvariable=self.prompt_var
        )
        self.prompt_entry.grid(
            row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))

        # 創建按鈕容器
        self.input_buttons_frame = ttk.Frame(self.input_frame)
        self.input_buttons_frame.grid(row=0, column=1)

        # 添加 Gemini 建議按鈕
        self.gemini_button = ttk.Button(
            self.input_buttons_frame,
            text=self.get_text("get_suggestions"),
            command=self.get_gemini_suggestions
        )
        self.gemini_button.grid(row=0, column=0, padx=2)

        # 添加到提示詞區域按鈕
        self.add_to_left_button = ttk.Button(
            self.input_buttons_frame,
            text=self.get_text("add_to_prompts"),
            command=self.add_to_left
        )
        self.add_to_left_button.grid(row=0, column=1, padx=2)

        # 添加到暫存區域按鈕
        self.add_to_right_button = ttk.Button(
            self.input_buttons_frame,
            text=self.get_text("add_to_temp"),
            command=self.add_to_right
        )
        self.add_to_right_button.grid(row=0, column=2, padx=2)

        # 綁定回車鍵事件
        self.prompt_entry.bind('<Return>', self.on_enter_press)

    def setup_list_frames(self):
        """設置列表框架"""
        # 創建左側列表
        self.left_list = ListFrame(
            self.lists_frame,
            self.get_text("text_content"),
            self.delete_left_item,
            self.translation_manager
        )
        self.left_list.grid(row=0, column=0, sticky=(
            tk.W, tk.E, tk.N, tk.S), padx=(0, 5))

        # 綁定雙擊事件
        self.left_list.listbox.bind(
            '<Double-Button-1>', self.on_left_double_click)
        # 綁定右鍵事件
        self.left_list.listbox.bind('<Button-3>', self.show_context_menu)

        # 創建傳輸按鈕
        self.create_transfer_buttons()

        # 創建右側列表
        self.right_list = ListFrame(
            self.lists_frame,
            self.get_text("temp_list"),
            self.delete_right_item,
            self.translation_manager
        )
        self.right_list.grid(row=0, column=2, sticky=(
            tk.W, tk.E, tk.N, tk.S), padx=(5, 0))

        # 綁定雙擊事件
        self.right_list.listbox.bind(
            '<Double-Button-1>', self.on_right_double_click)
        # 綁定右鍵事件
        self.right_list.listbox.bind('<Button-3>', self.show_context_menu)

    def create_transfer_buttons(self):
        """創建中間傳輸按鈕"""
        self.button_frame = ttk.Frame(self.lists_frame)
        self.button_frame.grid(row=0, column=1, sticky=(tk.N, tk.S), padx=10)

        self.buttons_container = ttk.Frame(self.button_frame)
        self.buttons_container.grid(row=0, column=0)
        self.button_frame.grid_rowconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(0, weight=1)

        self.to_right_button = ttk.Button(
            self.buttons_container, text="→", command=self.move_to_right)
        self.to_right_button.grid(row=0, column=0, pady=2)

        self.to_left_button = ttk.Button(
            self.buttons_container, text="←", command=self.move_to_left)
        self.to_left_button.grid(row=1, column=0, pady=2)

    def move_to_right(self):
        """將選中項目複製到右側列表"""
        selection = self.left_list.listbox.curselection()
        if selection:
            index = selection[0]
            item = self.left_list.listbox.get(index)
            # 檢查是否已存在於右側列表
            existing_items = self.right_list.listbox.get(0, tk.END)
            if item not in existing_items:
                self.right_list.listbox.insert(tk.END, item)

    def move_to_left(self):
        """將選中項目複製到左側列表"""
        selection = self.right_list.listbox.curselection()
        if selection:
            index = selection[0]
            item = self.right_list.listbox.get(index)
            # 檢查是否已存在於左側列表
            existing_items = self.left_list.listbox.get(0, tk.END)
            if item not in existing_items:
                self.left_list.listbox.insert(tk.END, item)

    def delete_left_item(self):
        """刪除左側列表中選中的項目"""
        selection = self.left_list.listbox.curselection()
        if selection:
            self.left_list.listbox.delete(selection[0])

    def delete_right_item(self):
        """刪除右側列表中選中的項目"""
        selection = self.right_list.listbox.curselection()
        if selection:
            self.right_list.listbox.delete(selection[0])

    def set_current_folder(self, folder_path):
        """設置當前資料夾並執行相關操作"""
        print("\n=== 設置當前資料夾 ===")
        print(f"新資料夾路徑：'{folder_path}'")

        if not folder_path:
            print("錯誤：資料夾路徑為空")
            return False

        if not os.path.exists(folder_path):
            print(f"錯誤：資料夾不存在：{folder_path}")
            return False

        # 更新資料夾路徑
        self.current_folder = folder_path
        print(f"已更新資料夾路徑：'{self.current_folder}'")

        # 載入暫存列表和收藏列表
        self.load_temp_list()
        self.load_favorites()

        print("=== 資料夾設置完成 ===\n")
        return True

    def load_temp_list(self):
        """讀取暫存列表文件"""
        print("\n=== 開始載入暫存列表 ===")  # 調試信息
        print(f"當前資料夾路徑：'{self.current_folder}'")  # 調試信息

        if not self.current_folder:
            print("錯誤：當前資料夾路徑為空")  # 調試信息
            self.status_label.config(text="錯誤：未選擇資料夾")
            return False

        # 清空右側列表
        print("清空右側列表...")  # 調試信息
        self.right_list.listbox.delete(0, tk.END)

        temp_path = os.path.join(self.current_folder, 'temp.txt')
        print(f"暫存檔案完整路徑：'{temp_path}'")  # 調試信息

        if os.path.exists(temp_path):
            try:
                with open(temp_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    items = [item.strip()
                             for item in content.split(',') if item.strip()]
                    print(f"成功讀取到 {len(items)} 個暫存提示詞")  # 調試信息
                    print(f"提示詞列表：{items}")  # 調試信息

                    # 插入項目到右側列表
                    for item in items:
                        self.right_list.listbox.insert(tk.END, item)

                    # 更新狀態標籤
                    success_msg = f"已載入 {len(items)} 個暫存提示詞"
                    self.status_label.config(text=success_msg)
                    print(f"成功：{success_msg}")  # 調試信息

                    # 強制更新界面
                    self.right_list.listbox.update()
                    print("=== 暫存列表載入完成 ===\n")  # 調試信息
                    return True
            except Exception as e:
                error_msg = f"無法讀取暫存檔案：{str(e)}"
                print(f"錯誤：{error_msg}")  # 調試信息
                self.status_label.config(text=error_msg)
                print("=== 暫存列表載入失敗 ===\n")  # 調試信息
                return False
        else:
            print(f"提示：暫存檔案不存在，這是正常的（首次使用）")  # 調試信息
            self.status_label.config(text="暫存檔案不存在（首次使用）")
            print("=== 暫存列表載入完成 ===\n")  # 調試信息
            return True

    def load_text_content(self, image_path):
        """加載與圖片對應的文本內容"""
        print("\n=== 開始載入文本內容 ===")  # 調試信息
        print(f"圖片路徑：{image_path}")  # 調試信息

        if not image_path:
            print("錯誤：圖片路徑為空")  # 調試信息
            return False

        # 更新資料夾路徑
        new_folder = os.path.dirname(image_path)
        if new_folder != self.current_folder:
            self.set_current_folder(new_folder)

        # 設置當前文本路徑
        base_path = os.path.splitext(image_path)[0]
        self.current_txt_path = base_path + '.txt'
        print(f"文本檔案路徑：{self.current_txt_path}")  # 調試信息

        # 清空左側列表
        self.left_list.listbox.delete(0, tk.END)

        if os.path.exists(self.current_txt_path):
            try:
                with open(self.current_txt_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    items = [item.strip()
                             for item in content.split(',') if item.strip()]
                    print(f"成功讀取到 {len(items)} 個提示詞")  # 調試信息
                    for item in items:
                        self.left_list.listbox.insert(tk.END, item)
                    print("=== 文本內容載入完成 ===\n")  # 調試信息
                    return True
            except Exception as e:
                error_msg = f"{self.get_text('cant_read_file')}{str(e)}"
                print(f"錯誤：{error_msg}")  # 調試信息
                self.left_list.listbox.insert(tk.END, error_msg)
                print("=== 文本內容載入失敗 ===\n")  # 調試信息
                return False
        else:
            print(f"文本檔案不存在")  # 調試信息
            self.left_list.listbox.insert(tk.END, self.get_text("no_txt_file"))
            print("=== 文本內容載入完成 ===\n")  # 調試信息
            return False

    def save_text_content(self):
        """保存文本內容到文件"""
        print("\n=== 開始保存文本內容 ===")
        print(f"當前文本路徑：{self.current_txt_path}")

        if not self.current_txt_path:
            print("錯誤：當前文本路徑為空")
            self.status_label.config(text="錯誤：未選擇文本文件")
            return False

        try:
            # 獲取左側列表的所有項目
            items = self.left_list.listbox.get(0, tk.END)
            content = ','.join(items)
            print(f"準備保存的內容：{content}")

            # 保存文本內容
            with open(self.current_txt_path, 'w', encoding='utf-8') as f:
                f.write(content)

            # 保存暫存列表
            self.save_temp_list()

            success_msg = "保存成功"
            print(f"成功：{success_msg}")
            self.status_label.config(text=success_msg)
            return True
        except Exception as e:
            error_msg = f"保存失敗：{str(e)}"
            print(f"錯誤：{error_msg}")
            self.status_label.config(text=error_msg)
            return False

    def save_temp_list(self):
        """保存暫存列表到文件"""
        print("\n=== 開始保存暫存列表 ===")  # 調試信息
        print(f"當前資料夾路徑：'{self.current_folder}'")  # 調試信息

        if not self.current_folder:
            print("錯誤：未設置當前資料夾路徑")  # 調試信息
            self.status_label.config(text="錯誤：未設置保存目錄")
            print("=== 暫存列表保存失敗 ===\n")  # 調試信息
            return False

        if not os.path.exists(self.current_folder):
            try:
                os.makedirs(self.current_folder)
                print(f"創建目錄：{self.current_folder}")  # 調試信息
            except Exception as e:
                error_msg = f"無法創建目錄：{str(e)}"
                print(f"錯誤：{error_msg}")  # 調試信息
                self.status_label.config(text=error_msg)
                print("=== 暫存列表保存失敗 ===\n")  # 調試信息
                return False

        temp_path = os.path.join(self.current_folder, 'temp.txt')
        print(f"暫存檔案完整路徑：'{temp_path}'")  # 調試信息

        try:
            items = [self.right_list.listbox.get(
                i) for i in range(self.right_list.listbox.size())]
            print(f"準備保存 {len(items)} 個提示詞")  # 調試信息
            print(f"提示詞列表：{items}")  # 調試信息

            content = ', '.join(items)
            with open(temp_path, 'w', encoding='utf-8') as f:
                f.write(content)

            success_msg = "暫存列表保存成功"
            print(f"成功：{success_msg}")  # 調試信息
            self.status_label.config(text=success_msg)
            print("=== 暫存列表保存完成 ===\n")  # 調試信息
            return True

        except Exception as e:
            error_msg = f"無法保存暫存列表：{str(e)}"
            print(f"錯誤：{error_msg}")  # 調試信息
            self.status_label.config(text=error_msg)
            print("=== 暫存列表保存失敗 ===\n")  # 調試信息
            return False

    def update_texts(self):
        """更新界面文字"""
        # 更新標題
        self.left_list.update_texts(self.get_text("text_content"))
        self.right_list.update_texts(self.get_text("temp_list"))

        # 更新按鈕文字
        self.add_to_left_button.config(text=self.get_text("add_to_prompts"))
        self.add_to_right_button.config(text=self.get_text("add_to_temp"))
        self.gemini_button.config(text=self.get_text("get_suggestions"))

        # 更新右鍵選單
        self.context_menu.entryconfigure(
            0, label=self.get_text("delete"))

    def add_to_left(self):
        """添加提示詞到左側列表"""
        prompt = self.prompt_var.get().strip()
        if prompt:
            # 檢查是否已存在
            existing_items = self.left_list.listbox.get(0, tk.END)
            if prompt not in existing_items:
                self.left_list.listbox.insert(tk.END, prompt)
                self.prompt_var.set("")  # 清空輸入框
                self.status_label.config(text="提示詞已添加到提示詞區域")
            else:
                self.status_label.config(text="提示詞已存在於提示詞區域")

    def add_to_right(self):
        """添加提示詞到右側列表"""
        prompt = self.prompt_var.get().strip()
        if prompt:
            # 檢查是否已存在
            existing_items = self.right_list.listbox.get(0, tk.END)
            if prompt not in existing_items:
                self.right_list.listbox.insert(tk.END, prompt)
                self.prompt_var.set("")  # 清空輸入框
                self.status_label.config(text="提示詞已添加到暫存區域")
            else:
                self.status_label.config(text="提示詞已存在於暫存區域")

    def on_enter_press(self, event):
        """處理回車鍵事件"""
        # 預設添加到提示詞區域
        self.add_to_left()

    def on_left_double_click(self, event):
        """處理左側列表的雙擊事件 - 將項目添加到暫存列表"""
        selection = self.left_list.listbox.curselection()
        if selection:
            index = selection[0]
            item = self.left_list.listbox.get(index)
            # 檢查是否已存在於右側列表
            existing_items = self.right_list.listbox.get(0, tk.END)
            if item not in existing_items:
                self.right_list.listbox.insert(tk.END, item)
                self.status_label.config(text=f"已添加到暫存列表：{item}")

    def on_right_double_click(self, event):
        """處理右側列表的雙擊事件 - 將項目添加到提示詞列表"""
        selection = self.right_list.listbox.curselection()
        if selection:
            index = selection[0]
            item = self.right_list.listbox.get(index)
            # 檢查是否已存在於左側列表
            existing_items = self.left_list.listbox.get(0, tk.END)
            if item not in existing_items:
                self.left_list.listbox.insert(tk.END, item)
                self.status_label.config(text=f"已添加到提示詞列表：{item}")

    def load_favorites(self):
        """從文件加載收藏列表"""
        if not self.current_folder:
            return False

        favorites_path = os.path.join(self.current_folder, 'favorites.txt')
        if os.path.exists(favorites_path):
            try:
                with open(favorites_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    self.favorite_list = [
                        item.strip() for item in content.split(',') if item.strip()]
                    self.favorite_list_frame.listbox.delete(0, tk.END)
                    for item in self.favorite_list:
                        self.favorite_list_frame.listbox.insert(tk.END, item)
                return True
            except Exception as e:
                print(f"加載收藏列表失敗：{str(e)}")
                return False
        return True

    def save_favorites(self):
        """保存收藏列表到文件"""
        if not self.current_folder:
            return False

        favorites_path = os.path.join(self.current_folder, 'favorites.txt')
        try:
            with open(favorites_path, 'w', encoding='utf-8') as f:
                f.write(','.join(self.favorite_list))
            return True
        except Exception as e:
            print(f"保存收藏列表失敗：{str(e)}")
            return False

    def show_context_menu(self, event):
        """直接刪除選中的項目"""
        # 獲取被點擊的列表
        clicked_list = event.widget
        # 確保有選中的項目
        if clicked_list.curselection():
            index = clicked_list.curselection()[0]
            item = clicked_list.get(index)
            clicked_list.delete(index)
            # 更新狀態標籤
            if clicked_list == self.left_list.listbox:
                self.status_label.config(text=f"已從提示詞列表移除：{item}")
            else:
                self.status_label.config(text=f"已從暫存列表移除：{item}")

    def delete_selected_item(self):
        """刪除選中的項目"""
        if hasattr(self, 'current_selected_list'):
            selection = self.current_selected_list.curselection()
            if selection:
                index = selection[0]
                item = self.current_selected_list.get(index)
                self.current_selected_list.delete(index)
                # 更新狀態標籤
                if self.current_selected_list == self.left_list.listbox:
                    self.status_label.config(text=f"已從提示詞列表移除：{item}")
                else:
                    self.status_label.config(text=f"已從暫存列表移除：{item}")

    def get_gemini_suggestions(self):
        """從 Gemini 獲取提示詞建議"""
        try:
            # 檢查是否已初始化 Gemini 接口
            if not self.gemini:
                api_key = os.getenv('GEMINI_API_KEY')
                if not api_key:
                    self.status_label.config(text=self.get_text("no_api_key"))
                    return
                try:
                    self.gemini = GeminiInterface(api_key)
                except Exception as e:
                    print(f"Error initializing Gemini interface: {str(e)}")
                    self.status_label.config(
                        text=self.get_text("suggestion_error"))
                    return

            # 檢查是否有選擇圖片
            if not hasattr(self, 'image_viewer') or not self.image_viewer.image_handler.current_image:
                self.status_label.config(
                    text=self.get_text("no_image_selected"))
                return

            # 獲取當前圖片路徑
            current_image_path = self.image_viewer.image_handler.image_files[
                self.image_viewer.image_handler.current_index]

            # 打開當前圖片
            with Image.open(current_image_path) as img:
                # 獲取當前暫存列表中的提示詞
                temp_prompts = list(self.right_list.listbox.get(0, tk.END))

                # 獲取建議
                suggestions = self.gemini.get_prompt_suggestions(
                    img, temp_prompts)

                if suggestions:
                    # 獲取當前左側列表中的所有項目
                    existing_items = self.left_list.listbox.get(0, tk.END)

                    # 添加建議到提示詞列表
                    added_count = 0
                    for suggestion in suggestions:
                        # 確保建議不為空且不在現有列表中
                        if suggestion and suggestion not in existing_items:
                            self.left_list.listbox.insert(tk.END, suggestion)
                            added_count += 1

                    # 更新狀態標籤
                    if added_count > 0:
                        self.status_label.config(
                            text=f"{self.get_text('suggestions_added')} ({added_count})")
                    else:
                        self.status_label.config(
                            text=self.get_text("no_new_suggestions"))
                else:
                    self.status_label.config(
                        text=self.get_text("no_suggestions"))

        except Exception as e:
            print(f"Error getting Gemini suggestions: {str(e)}")
            self.status_label.config(text=self.get_text("suggestion_error"))
