"""
4x20 Learning Cards - 數據模型
定義了應用所需的所有數據庫模型，包括卡片和各種內容類型
"""

from datetime import datetime
from extensions import db

class Card(db.Model):
    """卡片模型
    
    屬性:
        id: 主鍵
        page_number: 頁碼（1-4）
        position: 卡片在頁面中的位置（0-19）
        background_color: 卡片背景顏色
        created_at: 創建時間
        updated_at: 最後更新時間
    """
    id = db.Column(db.Integer, primary_key=True)
    page_number = db.Column(db.Integer, nullable=False)  # 1-4頁
    position = db.Column(db.Integer, nullable=False)     # 0-19位置
    background_color = db.Column(db.String(20), default='#87CEEB')  # 預設為天藍色
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 關聯定義
    text_content = db.relationship('TextContent', backref='card', uselist=False, cascade='all, delete-orphan')
    image_content = db.relationship('ImageContent', backref='card', uselist=False, cascade='all, delete-orphan')
    audio_content = db.relationship('AudioContent', backref='card', uselist=False, cascade='all, delete-orphan')
    file_content = db.relationship('FileContent', backref='card', uselist=False, cascade='all, delete-orphan')

class TextContent(db.Model):
    """文字內容模型
    
    屬性:
        id: 主鍵
        card_id: 關聯的卡片ID
        content: 文字內容
        created_at: 創建時間
        updated_at: 最後更新時間
    """
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ImageContent(db.Model):
    """圖片內容模型
    
    屬性:
        id: 主鍵
        card_id: 關聯的卡片ID
        path: 圖片文件路徑
        created_at: 創建時間
        updated_at: 最後更新時間
    """
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'), nullable=False)
    path = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AudioContent(db.Model):
    """音頻內容模型
    
    屬性:
        id: 主鍵
        card_id: 關聯的卡片ID
        path: 音頻文件路徑
        created_at: 創建時間
        updated_at: 最後更新時間
    """
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'), nullable=False)
    path = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class FileContent(db.Model):
    """文件內容模型
    
    屬性:
        id: 主鍵
        card_id: 關聯的卡片ID
        filename: 原始文件名
        path: 文件存儲路徑
        created_at: 創建時間
        updated_at: 最後更新時間
    """
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    path = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
