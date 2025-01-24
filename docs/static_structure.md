# static/ 目錄結構文檔

## 目錄用途
存放應用的靜態資源文件，包括 CSS 樣式、JavaScript 腳本和圖片等。

## 目錄結構
```
static/
├── css/
│   └── style.css    # 主要樣式文件
├── js/
│   └── script.js    # 主要JavaScript文件
└── images/          # 靜態圖片資源
```

## 主要組件

### 1. style.css
```css
/* 卡片容器樣式 */
.card-container {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 1rem;
    padding: 1rem;
}

/* 卡片樣式 */
.card {
    perspective: 1000px;
    height: 200px;
}

/* 卡片翻轉效果 */
.card-inner {
    position: relative;
    width: 100%;
    height: 100%;
    transform-style: preserve-3d;
    transition: transform 0.6s;
}

/* 卡片正面和背面 */
.card-front,
.card-back {
    position: absolute;
    width: 100%;
    height: 100%;
    backface-visibility: hidden;
}

/* 模態框樣式 */
.modal-content {
    max-width: 500px;
    margin: auto;
}

/* 響應式設計 */
@media (max-width: 768px) {
    .card-container {
        grid-template-columns: repeat(2, 1fr);
    }
}
```

### 2. script.js
```javascript
// 主要功能模塊
const CardManager = {
    // 初始化
    init() {
        this.bindEvents();
        this.loadCards();
    },
    
    // 事件綁定
    bindEvents() {
        // 卡片點擊
        // 拖放排序
        // 顏色選擇
        // 內容編輯
    },
    
    // 卡片加載
    loadCards() {
        // AJAX請求獲取卡片數據
        // 渲染卡片
    },
    
    // 卡片更新
    updateCard() {
        // 保存修改
        // 更新UI
    }
};

// 模態框管理
const ModalManager = {
    // 打開模態框
    // 關閉模態框
    // 保存更改
};

// 文件上傳管理
const FileUploader = {
    // 處理文件選擇
    // 上傳文件
    // 預覽文件
};

// 工具函數
const Utils = {
    // 格式化日期
    // 驗證文件
    // 錯誤處理
};
```

## 資源管理

### 1. CSS 組織
- 使用 BEM 命名約定
- 模塊化樣式
- 響應式設計
- 動畫效果

### 2. JavaScript 組織
- 模塊化設計
- 事件委託
- 錯誤處理
- 異步操作

### 3. 圖片管理
- 優化大小
- 使用適當格式
- 延遲加載

## 性能優化

1. 資源壓縮
   - 最小化 CSS 和 JS
   - 壓縮圖片
   
2. 加載優化
   - 使用 CDN
   - 資源緩存
   - 延遲加載
   
3. 執行優化
   - 避免阻塞渲染
   - 減少重排重繪
   - 使用節流和防抖

## 瀏覽器兼容性

1. CSS
   - 使用前綴
   - 降級方案
   - 媒體查詢
   
2. JavaScript
   - 特性檢測
   - Polyfill
   - 錯誤處理
