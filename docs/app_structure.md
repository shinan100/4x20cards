# app.py 結構文檔

## 檔案用途
主應用程式檔案，包含所有 Flask 路由和應用邏輯。

## 主要組件

### 1. 導入和配置
```python
# 導入必要的模組
from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_cors import CORS
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from extensions import db
from models import Card, TextContent, ImageContent, AudioContent, FileContent

# 應用配置
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cards.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
```

### 2. 輔助函數
```python
def allowed_file(filename, file_type)
    # 檢查文件類型是否允許上傳
    
def save_file(file, file_type)
    # 保存上傳的文件並返回唯一文件名
```

### 3. 路由處理器

#### 頁面路由
```python
@app.route('/')
def index()
    # 返回主頁

@app.route('/page/<int:page_number>')
def page(page_number)
    # 處理特定頁面的訪問
```

#### API 路由

##### 卡片操作
```python
@app.route('/api/cards/<int:page_number>')
def get_cards(page_number)
    # 獲取指定頁面的所有卡片

@app.route('/api/card/<int:card_id>')
def get_card(card_id)
    # 獲取單個卡片詳情

@app.route('/api/card/<int:card_id>/color', methods=['PUT'])
def update_card_color(card_id)
    # 更新卡片顏色

@app.route('/api/card/<int:card_id>/content', methods=['PUT'])
def update_card_content(card_id)
    # 更新卡片內容

@app.route('/api/card/<int:card_id>/content/<content_type>', methods=['DELETE'])
def delete_card_content(card_id, content_type)
    # 刪除特定類型的卡片內容

@app.route('/api/cards/reorder', methods=['POST'])
def reorder_cards()
    # 重新排序卡片
```

##### 文件處理
```python
@app.route('/uploads/<path:filename>')
def uploaded_file(filename)
    # 提供上傳文件的訪問
```

### 4. 應用入口
```python
if __name__ == '__main__':
    with app.app_context():
        # 初始化數據庫
        # 確保每頁都有20張卡片
    app.run(debug=True)
```

## 數據流

1. 客戶端請求 → Flask 路由
2. 路由處理器 → 數據庫操作
3. 數據庫返回結果 → JSON 響應
4. 文件上傳 → 保存到文件系統

## 依賴關係

- Flask: Web 框架
- SQLAlchemy: 數據庫 ORM
- Werkzeug: 文件處理
- CORS: 跨域支持

## 安全考慮

1. 文件上傳限制
   - 大小限制：16MB
   - 類型限制：特定文件格式
   
2. 文件名處理
   - 使用 secure_filename
   - 添加時間戳防止衝突

3. 錯誤處理
   - try-except 塊捕獲異常
   - 返回適當的錯誤信息
