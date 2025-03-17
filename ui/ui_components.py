import tkinter as tk
from tkinter import ttk


class ListFrame:
    def __init__(self, parent, title, delete_callback, translation_manager):
        self.translation_manager = translation_manager
        self.delete_callback = delete_callback
        self.create_frame(parent, title)

    def get_text(self, key):
        """獲取當前語言的文本"""
        return self.translation_manager.get_text(key)

    def create_frame(self, parent, title):
        """創建列表框架"""
        self.frame = ttk.Frame(parent)

        # 設置框架的行列權重
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        # 創建標題區域
        self.create_header(title)

        # 創建列表區域
        self.create_list_area()

    def create_header(self, title):
        """創建標題區域"""
        self.header_frame = ttk.Frame(self.frame)
        self.header_frame.grid(
            row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        self.header_frame.grid_columnconfigure(0, weight=1)

        # 標題標籤
        self.title_label = ttk.Label(
            self.header_frame,
            text=title,
            style='Title.TLabel'
        )
        self.title_label.grid(row=0, column=0, sticky=tk.W)

        # 刪除按鈕
        self.delete_button = ttk.Button(
            self.header_frame,
            text=self.get_text("delete"),
            command=self.delete_callback
        )
        self.delete_button.grid(row=0, column=1, sticky=tk.E)

    def create_list_area(self):
        """創建列表區域"""
        # 創建列表框和滾動條
        self.list_frame = ttk.Frame(self.frame)
        self.list_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.list_frame.grid_rowconfigure(0, weight=1)
        self.list_frame.grid_columnconfigure(0, weight=1)

        # 創建滾動條
        self.scrollbar = ttk.Scrollbar(self.list_frame)
        self.scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # 創建列表框
        self.listbox = tk.Listbox(
            self.list_frame,
            yscrollcommand=self.scrollbar.set,
            selectmode=tk.SINGLE,
            exportselection=False
        )
        self.listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 配置滾動條
        self.scrollbar.config(command=self.listbox.yview)

    def grid(self, **kwargs):
        """網格布局方法"""
        self.frame.grid(**kwargs)

    def update_texts(self, title):
        """更新界面文字"""
        self.title_label.config(text=title)
        self.delete_button.config(text=self.get_text("delete"))
