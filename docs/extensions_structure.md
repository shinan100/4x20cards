# extensions.py 結構文檔

## 檔案用途
初始化和配置 Flask 擴展，使其可以在不同模組間共享。

## 主要組件

### 1. 導入
```python
from flask_sqlalchemy import SQLAlchemy
```

### 2. 擴展實例
```python
db = SQLAlchemy()  # 創建數據庫實例
```

## 使用說明

1. 在其他模組中導入
```python
from extensions import db
```

2. 在應用中初始化
```python
db.init_app(app)
```

## 擴展功能

### SQLAlchemy
- 提供 ORM 功能
- 管理數據庫連接
- 處理數據庫會話
- 提供模型基類

## 依賴關係

- Flask-SQLAlchemy: 提供 SQLAlchemy 整合
- SQLAlchemy: 底層 ORM 引擎

## 最佳實踐

1. 延遲初始化
   - 創建時不傳入 app
   - 使用 init_app 方法初始化
   
2. 單例模式
   - 確保只有一個數據庫實例
   - 在所有模組間共享

3. 配置管理
   - 在 app.py 中設置配置
   - 使用環境變量管理敏感信息
