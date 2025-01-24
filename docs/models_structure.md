# models.py 結構文檔

## 檔案用途
定義應用的數據模型，使用 SQLAlchemy ORM 進行數據庫映射。

## 主要組件

### 1. 導入
```python
from datetime import datetime
from extensions import db
```

### 2. 數據模型

#### Card 模型
```python
class Card(db.Model):
    """卡片的主要數據模型"""
    
    # 基本屬性
    id = db.Column(db.Integer, primary_key=True)
    page_number = db.Column(db.Integer, nullable=False)
    position = db.Column(db.Integer, nullable=False)
    background_color = db.Column(db.String(20), default='#87CEEB')
    
    # 時間戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 關聯
    text_content = db.relationship('TextContent', backref='card', uselist=False, cascade='all, delete-orphan')
    image_content = db.relationship('ImageContent', backref='card', uselist=False, cascade='all, delete-orphan')
    audio_content = db.relationship('AudioContent', backref='card', uselist=False, cascade='all, delete-orphan')
    file_content = db.relationship('FileContent', backref='card', uselist=False, cascade='all, delete-orphan')
```

#### 內容模型

##### TextContent
```python
class TextContent(db.Model):
    """文字內容模型"""
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

##### ImageContent
```python
class ImageContent(db.Model):
    """圖片內容模型"""
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'), nullable=False)
    path = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

##### AudioContent
```python
class AudioContent(db.Model):
    """音頻內容模型"""
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'), nullable=False)
    path = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

##### FileContent
```python
class FileContent(db.Model):
    """文件內容模型"""
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    path = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

## 數據關係

1. Card (1) ←→ (0/1) TextContent
2. Card (1) ←→ (0/1) ImageContent
3. Card (1) ←→ (0/1) AudioContent
4. Card (1) ←→ (0/1) FileContent

## 字段說明

### Card
- id: 主鍵
- page_number: 頁碼 (1-4)
- position: 卡片位置 (0-19)
- background_color: 背景顏色 (預設: #87CEEB)
- created_at: 創建時間
- updated_at: 更新時間

### Content Models 共同字段
- id: 主鍵
- card_id: 關聯的卡片ID
- created_at: 創建時間
- updated_at: 更新時間

### 特殊字段
- TextContent.content: 文字內容
- ImageContent.path: 圖片文件路徑
- AudioContent.path: 音頻文件路徑
- FileContent.path: 文件路徑
- FileContent.filename: 原始文件名

## 數據完整性

1. 外鍵約束
   - 所有內容模型通過 card_id 關聯到 Card
   - 使用 cascade 確保刪除卡片時清理相關內容

2. 非空約束
   - page_number 和 position 必須提供
   - 內容字段（content, path, filename）不能為空

3. 時間戳
   - 自動記錄創建時間
   - 自動更新修改時間
