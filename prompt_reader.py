#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import traceback
from dotenv import load_dotenv
from utils.translations import TranslationManager
from ui.main_window import MainWindow

# 加载环境变量
load_dotenv()


def setup_style(root):
    """設置應用程序樣式"""
    import tkinter.ttk as ttk
    style = ttk.Style(root)

    # 設置標題標籤樣式
    style.configure('Title.TLabel', font=('Arial', 10, 'bold'))

    # 設置按鈕樣式
    style.configure('TButton', padding=3)

    return style


def main():
    """主程序入口點"""
    try:
        print("正在初始化翻譯管理器...")
        # 初始化翻譯管理器
        translation_manager = TranslationManager()
        translation_manager.set_language('zh_TW')  # 設置默認語言為繁體中文

        print("正在創建主窗口...")
        # 創建主窗口
        main_window = MainWindow(translation_manager)

        print("正在設置樣式...")
        # 設置樣式
        style = setup_style(main_window.root)

        print("啟動應用程序...")
        # 運行應用程序
        main_window.run()
    except Exception as e:
        print(f"程序運行出錯：{str(e)}", file=sys.stderr)
        print("詳細錯誤信息：", file=sys.stderr)
        traceback.print_exc()
        return 1

    return 0


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
