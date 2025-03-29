#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import traceback
from dotenv import load_dotenv
from utils.translations import TranslationManager
from ui.main_window import MainWindow
from typing import Optional
import tkinter as tk
from tkinter import ttk

# 加载环境变量
load_dotenv()


def setup_style(root: tk.Tk) -> None:
    """設置應用程序樣式"""
    style = ttk.Style()
    style.theme_use("clam")

    # 設置字體
    default_font = ("Microsoft JhengHei", 10)
    style.configure(".", font=default_font)

    # 設置按鈕樣式
    style.configure("TButton", padding=5)

    # 設置標籤樣式
    style.configure("TLabel", padding=5)

    # 設置輸入框樣式
    style.configure("TEntry", padding=5)

    # 設置列表框樣式
    style.configure("TListbox", padding=5)


def main() -> None:
    """主函數"""
    # 創建翻譯管理器
    translation_manager = TranslationManager()

    # 創建主窗口
    app = MainWindow(translation_manager)

    # 設置樣式
    setup_style(app.root)

    # 運行應用程序
    app.run()


if __name__ == "__main__":
    # 確保在正確的工作目錄中運行
    if getattr(sys, 'frozen', False):
        # 如果是打包後的可執行文件
        os.chdir(os.path.dirname(sys.executable))
    else:
        # 如果是直接運行 Python 腳本
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        print(f"工作目錄設置為：{os.getcwd()}")

    # 運行主程序
    sys.exit(main())
