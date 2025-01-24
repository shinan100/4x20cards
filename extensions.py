"""
4x20 Learning Cards - 擴展模組
定義了應用所需的Flask擴展實例，方便在不同模組間共享
"""

from flask_sqlalchemy import SQLAlchemy

# 創建SQLAlchemy實例，用於處理數據庫操作
# 這個實例將在app.py中被初始化
db = SQLAlchemy()
