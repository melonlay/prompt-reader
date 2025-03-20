import tkinter as tk
from tkinter import ttk
from .image_viewer import ImageViewer
from .list_manager import ListManager


class MainWindow:
    def __init__(self, translation_manager):
        self.translation_manager = translation_manager
        self.root = tk.Tk()  # 創建根窗口
        self.setup_main_window()
        self.create_ui_layout()
        self.connect_components()

    def get_text(self, key):
        """獲取當前語言的文本"""
        return self.translation_manager.get_text(key)

    def setup_main_window(self):
        """初始化主視窗設置"""
        self.root.title(self.get_text("window_title"))
        self.root.geometry("1200x800")

        # 設置主視窗的行列權重
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def create_ui_layout(self):
        """創建整體UI布局"""
        self.create_main_frame()
        self.create_language_selector()

        # 創建圖片查看器
        self.image_viewer = ImageViewer(
            self.main_frame, self.translation_manager)
        self.image_viewer.frame.grid(row=1, column=0, sticky=(
            tk.W, tk.E, tk.N, tk.S), padx=(0, 10))

        # 創建列表管理器
        self.list_manager = ListManager(
            self.main_frame, self.translation_manager)
        self.list_manager.frame.grid(
            row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))

    def connect_components(self):
        """連接組件之間的功能"""
        print("正在連接組件...")  # 調試信息

        # 將列表管理器的方法連接到圖片查看器
        self.image_viewer.load_text_content = self.list_manager.load_text_content
        self.image_viewer.save_text_content = self.list_manager.save_text_content
        # 添加相互引用
        self.image_viewer.list_manager = self.list_manager
        self.list_manager.image_viewer = self.image_viewer
        print("已連接組件之間的相互引用")  # 調試信息

        # 保存原始的 select_folder 方法
        original_select_folder = self.image_viewer.select_folder

        # 創建新的 select_folder 方法
        def new_select_folder():
            print("\n=== 開始選擇資料夾 ===")  # 調試信息
            folder_path = original_select_folder()
            if folder_path:
                print(f"資料夾選擇成功：{folder_path}")  # 調試信息

                # 設置資料夾路徑（這會自動載入暫存列表）
                self.list_manager.set_current_folder(folder_path)

                # 強制更新界面
                self.list_manager.frame.update()
                print("=== 資料夾選擇完成 ===\n")  # 調試信息
            return folder_path

        # 替換 select_folder 方法
        self.image_viewer.select_folder = new_select_folder

        # 設置退出功能
        self.image_viewer.on_exit = self.on_exit
        print("組件連接完成")  # 調試信息

    def create_main_frame(self):
        """創建主框架"""
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.grid(row=0, column=0, sticky=(
            tk.W, tk.E, tk.N, tk.S), padx=20, pady=20)

        # 設置主框架的行列權重
        self.main_frame.grid_rowconfigure(1, weight=1)  # 主要內容區域可擴展
        self.main_frame.grid_columnconfigure(0, weight=2)  # 左側框架
        self.main_frame.grid_columnconfigure(1, weight=3)  # 右側框架

    def create_language_selector(self):
        """創建語言選擇器"""
        self.lang_frame = ttk.Frame(self.main_frame)
        self.lang_frame.grid(row=0, column=1, sticky=tk.NE, padx=5, pady=5)

        self.lang_label = ttk.Label(
            self.lang_frame,
            text=self.get_text("language") + ":"
        )
        self.lang_label.grid(row=0, column=0, padx=(0, 5))

        language_names = self.translation_manager.get_language_names()
        self.lang_var = tk.StringVar(
            value=self.translation_manager.get_current_language())
        self.lang_selector = ttk.Combobox(
            self.lang_frame,
            textvariable=self.lang_var,
            values=list(language_names.values()),
            width=10,
            state="readonly"
        )
        self.lang_selector.grid(row=0, column=1)
        self.lang_selector.set(
            language_names[self.translation_manager.get_current_language()])
        self.lang_selector.bind('<<ComboboxSelected>>',
                                self.on_language_change)

    def on_language_change(self, event=None):
        """處理語言變更"""
        selected_name = self.lang_selector.get()
        language_names = self.translation_manager.get_language_names()
        for code, name in language_names.items():
            if name == selected_name:
                self.translation_manager.set_language(code)
                self.update_all_texts()
                break

    def update_all_texts(self):
        """更新所有界面文字"""
        self.root.title(self.get_text("window_title"))
        self.lang_label.config(text=self.get_text("language") + ":")
        self.image_viewer.update_texts()
        self.list_manager.update_texts()

    def on_exit(self):
        """退出程序"""
        self.root.quit()

    def run(self):
        """運行應用程序"""
        self.root.mainloop()
