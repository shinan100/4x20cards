# 4x20 Learning Cards

一個基於Flask的學習卡片管理系統，支持多媒體內容和互動功能。

## 項目結構

```
4x20cards/
│
├── app.py                 # 主應用文件，包含所有路由和應用邏輯
├── models.py             # 數據模型定義
├── extensions.py         # Flask 擴展初始化
├── requirements.txt      # 項目依賴
│
├── static/              # 靜態文件目錄
│   ├── css/
│   │   └── style.css    # 自定義樣式
│   │
│   ├── js/
│   │   └── script.js    # 前端 JavaScript 代碼
│   │
│   └── images/          # 靜態圖片資源
│
├── templates/           # HTML 模板
│   └── index.html      # 主頁面模板
│
├── uploads/            # 用戶上傳文件存儲目錄
│   ├── images/         # 上傳的圖片
│   ├── audio/          # 上傳的音頻
│   └── files/          # 上傳的其他文件
│
└── instance/           # 實例文件夾
    └── cards.db        # SQLite 數據庫文件
```

## 技術棧

- **後端框架**: Flask 2.2.5
- **數據庫**: SQLite + SQLAlchemy 1.4.23
- **前端框架**: Bootstrap 5
- **JavaScript 庫**: jQuery
- **其他依賴**: 見 requirements.txt

## 主要功能

1. **多頁面管理**
   - 支持 4 個頁面
   - 每頁 20 張卡片
   - 頁面間快速切換

2. **卡片功能**
   - 支持文字、圖片、音頻和文件
   - 卡片翻轉動畫
   - 拖拽重新排序
   - 自定義背景顏色

3. **內容管理**
   - 即時編輯和保存
   - 多媒體內容預覽
   - 文件上傳管理
   - 修改時間記錄

4. **用戶界面**
   - 響應式設計
   - 直觀的網格布局
   - 模態框編輯界面
   - 現代化的視覺效果

## 數據模型

1. **Card**
   - 基本卡片信息
   - 頁碼和位置
   - 背景顏色
   - 創建和更新時間

2. **Content Models**
   - TextContent: 文字內容
   - ImageContent: 圖片內容
   - AudioContent: 音頻內容
   - FileContent: 文件內容

## API 端點

1. **卡片操作**
   - GET /api/cards/<page_number>: 獲取指定頁面的卡片
   - GET /api/card/<card_id>: 獲取單個卡片
   - PUT /api/card/<card_id>/color: 更新卡片顏色
   - PUT /api/card/<card_id>/content: 更新卡片內容
   - DELETE /api/card/<card_id>/content/<content_type>: 刪除特定內容
   - POST /api/cards/reorder: 重新排序卡片

2. **文件訪問**
   - GET /uploads/<filename>: 訪問上傳的文件

## 安裝和運行

1. **安裝依賴**
   ```bash
   pip install -r requirements.txt
   ```

2. **運行應用**
   ```bash
   python app.py
   ```

3. **訪問應用**
   - 打開瀏覽器訪問 http://127.0.0.1:5000

## 開發指南

1. **數據庫遷移**
   - 使用 Flask-Migrate 管理數據庫架構變更
   - 遷移命令參考 Flask-Migrate 文檔

2. **文件上傳**
   - 支持的圖片格式：PNG, JPG, JPEG, GIF
   - 支持的音頻格式：MP3, WAV, OGG
   - 支持的文件格式：PDF, DOC, DOCX, TXT, ZIP
   - 文件大小限制：16MB

3. **安全考慮**
   - 文件上傳驗證
   - 安全的文件名處理
   - 數據驗證和清理

## 性能優化

1. **數據庫優化**
   - 使用適當的索引
   - 定期清理未使用的數據
   - 數據庫壓縮維護

2. **文件存儲**
   - 定期清理未使用的上傳文件
   - 圖片壓縮
   - 使用緩存減少磁盤訪問

3. **前端優化**
   - 資源壓縮和合併
   - 懶加載圖片
   - 本地存儲利用

## 注意事項

1. 這是一個開發版本，不建議在生產環境中直接使用
2. 定期備份數據庫和上傳的文件
3. 監控服務器資源使用情況
4. 根據需要調整文件大小限制

## 貢獻指南

1. Fork 本項目
2. 創建特性分支
3. 提交更改
4. 發起 Pull Request

## 許可證

MIT License
