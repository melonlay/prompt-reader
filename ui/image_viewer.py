import tkinter as tk
from tkinter import ttk, filedialog
import os
from utils.image_handler import ImageHandler
from utils.image_utils import get_image_prompts


class ImageViewer:
    def __init__(self, parent, translation_manager):
        self.translation_manager = translation_manager
        self.image_handler = ImageHandler()
        self.create_frame(parent)
        self.current_folder = ""
        self.current_txt_path = None

    def get_text(self, key):
        """獲取當前語言的文本"""
        return self.translation_manager.get_text(key)

    def create_frame(self, parent):
        """創建圖片查看器框架"""
        self.frame = ttk.Frame(parent)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        # 文件夾選擇區域
        self.create_folder_frame()

        # 圖片顯示區域
        self.create_image_frame()

        # 導航控制區域
        self.create_navigation_frame()

        # 退出按鈕
        self.exit_button = ttk.Button(
            self.frame,
            text=self.get_text("exit"),
            command=self.on_exit
        )
        self.exit_button.grid(row=3, column=0, pady=10)

    def create_folder_frame(self):
        """創建文件夾選擇區域"""
        self.folder_frame = ttk.Frame(self.frame)
        self.folder_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)
        self.folder_frame.grid_columnconfigure(1, weight=1)

        self.folder_button = ttk.Button(
            self.folder_frame,
            text=self.get_text("select_folder"),
            command=self.select_folder
        )
        self.folder_button.grid(row=0, column=0, padx=(0, 10))

        self.folder_label = ttk.Label(
            self.folder_frame,
            text=self.get_text("no_folder"),
            wraplength=250
        )
        self.folder_label.grid(row=0, column=1, sticky=(tk.W, tk.E))

    def create_image_frame(self):
        """創建圖片顯示區域"""
        self.image_frame = ttk.Frame(
            self.frame,
            width=400,
            height=400
        )
        self.image_frame.grid(row=1, column=0, sticky=(
            tk.W, tk.E, tk.N, tk.S), pady=10)
        self.image_frame.grid_propagate(False)
        self.image_frame.grid_rowconfigure(0, weight=1)
        self.image_frame.grid_columnconfigure(0, weight=1)

        self.image_label = ttk.Label(self.image_frame)
        self.image_label.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    def create_navigation_frame(self):
        """創建導航控制區域"""
        self.nav_frame = ttk.Frame(self.frame)
        self.nav_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=5)
        self.nav_frame.grid_columnconfigure(1, weight=1)

        # 上一張按鈕
        self.prev_button = ttk.Button(
            self.nav_frame,
            text=self.get_text("prev"),
            command=self.prev_image,
            state=tk.DISABLED
        )
        self.prev_button.grid(row=0, column=0, padx=5)

        # 圖片計數區域（包含輸入框）
        self.counter_frame = ttk.Frame(self.nav_frame)
        self.counter_frame.grid(row=0, column=1)

        # 當前圖片輸入框
        self.current_image_var = tk.StringVar(value="0")
        self.current_image_entry = ttk.Entry(
            self.counter_frame,
            textvariable=self.current_image_var,
            width=5,
            justify=tk.CENTER
        )
        self.current_image_entry.grid(row=0, column=0)
        self.current_image_entry.bind('<Return>', self.on_image_number_enter)
        self.current_image_entry.bind('<FocusOut>', self.validate_image_number)

        # 總數標籤
        self.total_label = ttk.Label(self.counter_frame, text="/0")
        self.total_label.grid(row=0, column=1)

        # 下一張按鈕
        self.next_button = ttk.Button(
            self.nav_frame,
            text=self.get_text("next"),
            command=self.next_image,
            state=tk.DISABLED
        )
        self.next_button.grid(row=0, column=2, padx=5)

        # 保存按鈕
        self.save_button = ttk.Button(
            self.nav_frame,
            text=self.get_text("save"),
            command=self.on_save_click,
            state=tk.DISABLED
        )
        self.save_button.grid(row=0, column=3, padx=5)

    def select_folder(self):
        """選擇文件夾並加載內容"""
        print("\n=== ImageViewer 開始選擇資料夾 ===")  # 調試信息

        folder_path = filedialog.askdirectory()
        if folder_path:
            print(f"用戶選擇的資料夾：'{folder_path}'")  # 調試信息
            self.current_folder = folder_path
            self.folder_label.config(text=folder_path)

            print("正在加載圖片...")  # 調試信息
            if self.image_handler.load_images(folder_path):
                # 調試信息
                print(f"找到 {self.image_handler.get_total_images()} 張圖片")
                self.show_image(0)
                self.update_button_states()
                self.save_button.config(state=tk.NORMAL)
                print("=== ImageViewer 資料夾選擇完成 ===\n")  # 調試信息
                return folder_path
            else:
                print("警告：資料夾中沒有找到圖片")  # 調試信息
                print("=== ImageViewer 資料夾選擇完成 ===\n")  # 調試信息
                return folder_path

        print("用戶取消選擇資料夾")  # 調試信息
        print("=== ImageViewer 資料夾選擇完成 ===\n")  # 調試信息
        return None

    def show_image(self, index):
        """顯示指定索引的圖片"""
        if self.image_handler.show_image(index, self.image_label):
            self.update_counter(
                index + 1,
                self.image_handler.get_total_images()
            )
            # 獲取當前圖片路徑
            current_image_path = self.image_handler.get_current_image_path()

            # 讀取圖片提示詞
            image_prompts = get_image_prompts(current_image_path)

            # 讀取文本文件提示詞
            txt_prompts = []
            if hasattr(self, 'load_text_content'):
                self.load_text_content(current_image_path)
                # 從左側列表獲取文本文件的提示詞，並確保是列表類型
                temp_txt_prompts = list(
                    self.list_manager.left_list.listbox.get(0, tk.END))
                # 過濾掉 no_txt_file
                if not (len(temp_txt_prompts) == 1 and temp_txt_prompts[0] == self.get_text("no_txt_file")):
                    txt_prompts = temp_txt_prompts

                # 如果沒有文本文件但有圖片提示詞，清空左側列表
                if len(txt_prompts) == 0 and image_prompts:
                    self.list_manager.left_list.listbox.delete(0, tk.END)

            # 合併提示詞並去重，並按字母順序排序
            all_prompts = sorted(list(set(image_prompts + txt_prompts)))

            if all_prompts:
                # 更新提示詞列表
                self.update_prompt_list(all_prompts)
                # 更新狀態標籤
                status_parts = []
                if image_prompts:
                    status_parts.append(
                        f"{self.get_text('image_prompts_count')}: {len(image_prompts)}")
                if txt_prompts:
                    status_parts.append(
                        f"{self.get_text('txt_prompts_count')}: {len(txt_prompts)}")
                if all_prompts:
                    status_parts.append(
                        f"{self.get_text('total_unique_prompts')}: {len(all_prompts)}")

                status_text = ", ".join(status_parts)
                self.list_manager.status_label.config(text=status_text)
            else:
                # 如果沒有任何提示詞，顯示提示信息
                self.list_manager.status_label.config(
                    text=self.get_text("no_prompts_found"))

            self.update_button_states()
            return True
        return False

    def update_counter(self, current, total):
        """更新圖片計數"""
        self.current_image_var.set(str(current))
        self.total_label.config(text=f"/{total}")

    def update_button_states(self):
        """更新按鈕狀態"""
        self.prev_button.config(
            state=tk.NORMAL if self.image_handler.can_move_prev() else tk.DISABLED)
        self.next_button.config(
            state=tk.NORMAL if self.image_handler.can_move_next() else tk.DISABLED)

    def prev_image(self):
        """顯示上一張圖片"""
        if self.image_handler.can_move_prev():
            self.show_image(self.image_handler.get_current_index() - 1)

    def next_image(self):
        """顯示下一張圖片"""
        if self.image_handler.can_move_next():
            self.show_image(self.image_handler.get_current_index() + 1)

    def on_save_click(self):
        """處理保存按鈕點擊事件"""
        print("保存按鈕被點擊")  # 調試信息
        if hasattr(self, 'save_text_content'):
            print("調用 save_text_content 方法")  # 調試信息
            self.save_text_content()
        else:
            print("錯誤：save_text_content 方法未連接")  # 調試信息

    def load_text_content(self, image_path):
        """加載文本內容"""
        # 這個方法將在 ListManager 中實現
        pass

    def on_exit(self):
        """退出程序"""
        if hasattr(self, 'frame') and self.frame.winfo_exists():
            self.frame.winfo_toplevel().quit()

    def update_texts(self):
        """更新界面文字"""
        self.folder_button.config(text=self.get_text("select_folder"))
        self.folder_label.config(text=self.get_text(
            "no_folder") if not self.current_folder else self.current_folder)
        self.prev_button.config(text=self.get_text("prev"))
        self.next_button.config(text=self.get_text("next"))
        self.save_button.config(text=self.get_text("save"))
        self.exit_button.config(text=self.get_text("exit"))

    def on_image_number_enter(self, event):
        """處理圖片編號輸入"""
        try:
            # 獲取輸入的數字
            number = int(self.current_image_var.get())
            total_images = self.image_handler.get_total_images()

            # 確保數字在有效範圍內
            if 1 <= number <= total_images:
                # 顯示對應的圖片（注意：輸入是1-based，但內部是0-based）
                self.show_image(number - 1)
            else:
                # 如果數字無效，恢復當前圖片編號
                self.validate_image_number(None)
        except ValueError:
            # 如果輸入的不是數字，恢復當前圖片編號
            self.validate_image_number(None)

    def validate_image_number(self, event):
        """驗證並修正圖片編號"""
        if self.image_handler.get_total_images() > 0:
            current = self.image_handler.get_current_index() + 1
            self.current_image_var.set(str(current))
        else:
            self.current_image_var.set("0")

    def update_prompt_list(self, prompts):
        """更新提示詞列表"""
        if hasattr(self, 'list_manager'):
            # 清空左側列表
            self.list_manager.left_list.listbox.delete(0, tk.END)
            # 添加新的提示詞
            for prompt in prompts:
                self.list_manager.left_list.listbox.insert(tk.END, prompt)
