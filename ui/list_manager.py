import tkinter as tk
from tkinter import ttk
import os
from .ui_components import ListFrame


class ListManager:
    def __init__(self, parent, translation_manager):
        self.translation_manager = translation_manager
        self.create_frame(parent)
        self.current_folder = ""
        self.current_txt_path = None

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

        # 添加到提示詞區域按鈕
        self.add_to_left_button = ttk.Button(
            self.input_buttons_frame,
            text="添加到提示詞",
            command=self.add_to_left
        )
        self.add_to_left_button.grid(row=0, column=0, padx=2)

        # 添加到暫存區域按鈕
        self.add_to_right_button = ttk.Button(
            self.input_buttons_frame,
            text="添加到暫存",
            command=self.add_to_right
        )
        self.add_to_right_button.grid(row=0, column=1, padx=2)

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
        print("\n=== 設置當前資料夾 ===")  # 調試信息
        print(f"新資料夾路徑：'{folder_path}'")  # 調試信息

        if not folder_path:
            print("錯誤：資料夾路徑為空")  # 調試信息
            return False

        if not os.path.exists(folder_path):
            print(f"錯誤：資料夾不存在：{folder_path}")  # 調試信息
            return False

        # 更新資料夾路徑
        self.current_folder = folder_path
        print(f"已更新資料夾路徑：'{self.current_folder}'")  # 調試信息

        # 載入暫存列表
        self.load_temp_list()

        print("=== 資料夾設置完成 ===\n")  # 調試信息
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
        """保存修改後的內容到txt文件"""
        print("\n=== 開始保存文本內容 ===")  # 調試信息
        print(f"當前文本路徑：{self.current_txt_path}")  # 調試信息
        print(f"當前資料夾路徑：{self.current_folder}")  # 調試信息

        if not self.current_txt_path:
            error_msg = self.get_text("no_txt_file")
            print(f"錯誤：{error_msg}")  # 調試信息
            self.status_label.config(text=error_msg)
            return False

        try:
            items = [self.left_list.listbox.get(
                i) for i in range(self.left_list.listbox.size())]

            if not items:
                error_msg = "沒有內容需要保存"
                print(f"錯誤：{error_msg}")  # 調試信息
                self.status_label.config(text=error_msg)
                return False

            content = ', '.join(items)
            print(f"準備保存的內容：{content}")  # 調試信息

            # 確保目標目錄存在
            save_dir = os.path.dirname(self.current_txt_path)
            os.makedirs(save_dir, exist_ok=True)
            print(f"保存目錄：{save_dir}")  # 調試信息

            with open(self.current_txt_path, 'w', encoding='utf-8') as f:
                f.write(content)

            success_msg = self.get_text("save_success")
            print(f"成功：{success_msg}")  # 調試信息
            self.status_label.config(text=success_msg)

            # 確保 current_folder 已設置
            if not self.current_folder:
                self.current_folder = save_dir
                print(f"從保存目錄更新資料夾路徑：{self.current_folder}")  # 調試信息

            # 保存完文本內容後，也保存暫存列表
            print("開始保存暫存列表...")  # 調試信息
            self.save_temp_list()
            print("=== 文本內容保存完成 ===\n")  # 調試信息
            return True

        except Exception as e:
            error_msg = f"{self.get_text('save_failed')}{str(e)}"
            print(f"錯誤：{error_msg}")  # 調試信息
            self.status_label.config(text=error_msg)
            print("=== 文本內容保存失敗 ===\n")  # 調試信息
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
        self.left_list.update_texts(self.get_text("text_content"))
        self.right_list.update_texts(self.get_text("temp_list"))
        # 清空狀態標籤
        self.status_label.config(text="")

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
