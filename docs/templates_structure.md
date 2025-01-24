# templates/ 目錄結構文檔

## 目錄用途
存放 Flask 應用的 HTML 模板文件。

## 目錄結構
```
templates/
└── index.html    # 主頁面模板
```

## 主要組件

### index.html
```html
<!DOCTYPE html>
<html lang="zh">
<head>
    <!-- 元信息 -->
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>4x20 Learning Cards</title>
    
    <!-- 樣式表 -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.x.x/dist/css/bootstrap.min.css">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <!-- 導航欄 -->
    <nav class="navbar navbar-expand-lg">
        <!-- 頁面切換按鈕 -->
    </nav>
    
    <!-- 主要內容 -->
    <main class="container">
        <!-- 卡片網格 -->
        <div class="card-container">
            <!-- 卡片模板 -->
        </div>
    </main>
    
    <!-- 模態框 -->
    <!-- 編輯卡片內容 -->
    <div class="modal fade" id="editCardModal">
        <!-- 表單內容 -->
    </div>
    
    <!-- 顏色選擇器 -->
    <div class="modal fade" id="colorPickerModal">
        <!-- 顏色選擇器內容 -->
    </div>
    
    <!-- 腳本 -->
    <script src="https://cdn.jsdelivr.net/npm/jquery@3.x.x/dist/jquery.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.x.x/dist/js/bootstrap.bundle.min.js"></script>
    <script src="{{ url_for('static', filename='js/script.js') }}"></script>
</body>
</html>
```

## 模板結構

### 1. 頁面布局
- 響應式導航欄
- 網格式卡片容器
- 模態框組件

### 2. 卡片組件
```html
<!-- 卡片模板 -->
<div class="card" data-id="{{ card.id }}">
    <div class="card-inner">
        <!-- 卡片正面 -->
        <div class="card-front">
            <!-- 預覽內容 -->
        </div>
        
        <!-- 卡片背面 -->
        <div class="card-back">
            <!-- 詳細內容 -->
        </div>
    </div>
</div>
```

### 3. 模態框
```html
<!-- 編輯模態框 -->
<div class="modal-dialog">
    <div class="modal-content">
        <!-- 標題 -->
        <div class="modal-header">
            <h5 class="modal-title">編輯卡片</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>
        
        <!-- 內容 -->
        <div class="modal-body">
            <!-- 文字輸入 -->
            <div class="form-group">
                <textarea class="form-control"></textarea>
            </div>
            
            <!-- 文件上傳 -->
            <div class="form-group">
                <input type="file" class="form-control">
            </div>
        </div>
        
        <!-- 按鈕 -->
        <div class="modal-footer">
            <button type="button" class="btn btn-primary">保存</button>
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">取消</button>
        </div>
    </div>
</div>
```

## 交互功能

### 1. 卡片操作
- 點擊翻轉
- 雙擊編輯
- 拖放排序
- 右鍵菜單

### 2. 內容編輯
- 文字輸入
- 文件上傳
- 預覽功能
- 自動保存

### 3. 用戶反饋
- 加載動畫
- 錯誤提示
- 操作確認
- 狀態更新

## 最佳實踐

1. 性能優化
   - 延遲加載
   - 資源壓縮
   - 緩存策略
   
2. 可訪問性
   - ARIA 標籤
   - 鍵盤導航
   - 高對比度
   
3. 用戶體驗
   - 響應式設計
   - 直觀操作
   - 錯誤處理
   
4. 代碼維護
   - 模塊化結構
   - 清晰註釋
   - 一致的命名
