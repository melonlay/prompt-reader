# Prompt Reader 提示詞管理器

[English](#english) | [繁體中文](#繁體中文)

## 繁體中文

### 簡介
Prompt Reader 是一個用於管理和編輯圖片提示詞的工具。它可以幫助用戶查看圖片、編輯相關的提示詞，並提供暫存功能以重複使用常用的提示詞。

![程式主界面](img/zh_TW.jpg)

### 環境需求
- Python 3.10 或更高版本
- tkinter
- Pillow 11.1.0（用於圖片處理）
- 作業系統：Windows、macOS 或 Linux

### 安裝說明
1. 克隆或下載此專案到本地
2. 安裝必要的 Python 套件：
   ```bash
   pip install -r requirements.txt
   ```

### 功能特點
- 圖片瀏覽功能
  - 支持瀏覽資料夾中的圖片
  - 可通過按鈕或輸入數字快速切換圖片
  - 顯示當前圖片索引和總數
- 提示詞管理
  - 自動讀取圖片中的提示詞信息
  - 支持讀取與圖片同名的 txt 文件中的提示詞
  - 自動合併並去重圖片和文本中的提示詞
  - 支持直接輸入新的提示詞
  - 防止重複添加相同的提示詞
- 暫存列表功能
  - 可將常用提示詞保存到暫存列表
  - 支持在提示詞列表和暫存列表間複製提示詞
  - 自動保存暫存列表到 temp.txt 文件
- 多語言支持
  - 支持切換界面語言（繁體中文、簡體中文、英文）
  - 所有操作提示均支持多語言顯示
- 右鍵刪除功能
  - 支持右鍵直接刪除提示詞
- 雙擊移動提示詞
  - 支持雙擊移動提示詞
- 回車快速添加提示詞
  - 支持回車快速添加提示詞
- 提示詞來源顯示
  - 顯示圖片提示詞數量
  - 顯示文本提示詞數量
  - 顯示不重複提示詞總數

### 使用說明
1. 啟動程式：運行 `prompt_reader.py`
2. 選擇資料夾：點擊「選擇資料夾」按鈕，選擇包含圖片和對應文本文件的資料夾
3. 瀏覽圖片：
   - 使用左側的圖片列表瀏覽圖片
   - 點擊圖片可在預覽區域查看大圖
   - 使用滑鼠滾輪或縮放按鈕調整圖片大小
4. 管理提示詞：
   - 程式會自動讀取圖片中的提示詞信息
   - 同時讀取與圖片同名的 txt 文件中的提示詞
   - 所有提示詞會自動合併並去重
   - 可以使用右鍵選單刪除提示詞
   - 可以雙擊將提示詞在列表間移動
5. 查看提示詞統計：
   - 狀態欄會顯示圖片提示詞數量
   - 顯示文本提示詞數量
   - 顯示不重複提示詞總數

### 檔案說明
- `prompt_reader.py`：主程式入口
- `requirements.txt`：Python 套件需求檔案
- `temp.txt`：暫存提示詞列表檔案
- `*.txt`：與圖片同名的提示詞檔案

---

## English

### Introduction
Prompt Reader is a tool for managing and editing image prompts. It helps users view images, edit related prompts, and provides a temporary storage feature for reusing common prompts.

![Main Interface](img/en.jpg)

### Requirements
- Python 3.10 or higher
- tkinter 
- Pillow 11.1.0 (for image processing)
- Operating System: Windows, macOS, or Linux

### Installation
1. Clone or download this project to your local machine
2. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

### Features
- Image Browsing
  - Browse images in selected folder
  - Switch images via buttons or number input
  - Display current image index and total count
- Prompt Management
  - Automatically read prompts from image metadata
  - Support reading prompts from corresponding txt files
  - Automatically merge and deduplicate prompts from both sources
  - Support direct input of new prompts
  - Prevent duplicate prompt entries
- Temporary List
  - Save commonly used prompts to temporary list
  - Copy prompts between prompt list and temporary list
  - Auto-save temporary list to temp.txt file
- Multi-language Support
  - Switch interface language (Traditional Chinese, Simplified Chinese, English)
  - All operation prompts support multiple languages
- Right-click Delete
  - Delete prompts directly with right-click
- Double-click Move
  - Move prompts between lists with double-click
- Quick Add with Enter
  - Add prompts quickly using Enter key
- Prompt Source Display
  - Show number of prompts from image
  - Show number of prompts from text file
  - Show total number of unique prompts

### Usage Instructions
1. Start Program: Run `prompt_reader.py`
2. Select Folder: Click "Select Folder" button to choose a folder containing images
3. Browse Images:
   - Use left side image list to browse images
   - Click image to view large image in preview area
   - Use mouse wheel or zoom buttons to adjust image size
4. Manage Prompts:
   - Program automatically reads prompts from image metadata
   - Also reads prompts from corresponding txt files
   - All prompts are automatically merged and deduplicated
   - Use right-click menu to delete prompts
   - Double-click to move prompts between lists
5. View Prompt Statistics:
   - Status bar shows number of prompts from image
   - Shows number of prompts from text file
   - Shows total number of unique prompts

### File Description
- `prompt_reader.py`: Main program entry
- `requirements.txt`: Python package requirements file
- `temp.txt`: Temporary prompt list file
- `*.txt`: Prompt files with same names as images 

## Contribution

Welcome to submit issues and pull requests!

## License

MIT License 