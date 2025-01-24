"""
4x20 Learning Cards - 主應用文件
這個文件包含了Flask應用的主要邏輯，包括路由處理和文件上傳功能
"""

# 導入必要的模組
from flask import Flask, render_template, jsonify, request, send_from_directory  # Flask Web框架相關功能
from flask_cors import CORS  # 處理跨域請求
import os  # 操作系統功能
from datetime import datetime  # 處理日期和時間
from werkzeug.utils import secure_filename  # 安全處理文件名
from extensions import db  # 數據庫擴展
from models import Card, TextContent, ImageContent, AudioContent, FileContent  # 數據模型

# 創建Flask應用實例
app = Flask(__name__)
CORS(app)  # 啟用跨域支持

# 應用配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cards.db'  # SQLite數據庫路徑
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 關閉SQLAlchemy的修改跟踪
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')  # 上傳文件保存路徑
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 限制上傳文件大小為16MB

# 確保上傳目錄存在
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# 初始化數據庫
db.init_app(app)

# 允許的文件類型
ALLOWED_EXTENSIONS = {
    'image': {'png', 'jpg', 'jpeg', 'gif'},  # 允許的圖片格式
    'audio': {'mp3', 'wav', 'ogg'},          # 允許的音頻格式
    'file': {'pdf', 'doc', 'docx', 'txt', 'zip'}  # 允許的文件格式
}

def allowed_file(filename, file_type):
    """檢查文件類型是否允許上傳"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS[file_type]

def save_file(file, file_type):
    """保存上傳的文件，並返回唯一的文件名"""
    if file and file.filename:
        filename = secure_filename(file.filename)  # 安全化文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')  # 添加時間戳防止文件名衝突
        unique_filename = timestamp + filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        return unique_filename
    return None

@app.route('/')
def index():
    """首頁路由"""
    return render_template('index.html')

@app.route('/page/<int:page_number>')
def page(page_number):
    """頁面路由，處理1-4頁的訪問"""
    if page_number < 1 or page_number > 4:
        return redirect('/')
    return render_template('index.html')

@app.route('/api/cards/<int:page_number>')
def get_cards(page_number):
    """獲取指定頁面的所有卡片"""
    try:
        if page_number < 1 or page_number > 4:
            return jsonify({'error': 'Invalid page number'}), 400
            
        # 獲取指定頁面的所有卡片
        cards = Card.query.filter_by(page_number=page_number).order_by(Card.position).all()
        
        # 如果頁面沒有卡片，創建20張新卡片
        if not cards:
            for pos in range(20):
                new_card = Card(page_number=page_number, position=pos)
                db.session.add(new_card)
            db.session.commit()
            cards = Card.query.filter_by(page_number=page_number).order_by(Card.position).all()
        
        # 準備返回數據
        cards_data = []
        for card in cards:
            card_data = {
                'id': card.id,
                'position': card.position,
                'background_color': card.background_color,
                'text_content': card.text_content.content if card.text_content else None,
                'image_content': card.image_content.path if card.image_content else None,
                'audio_content': card.audio_content.path if card.audio_content else None,
                'file_content': {
                    'path': card.file_content.path,
                    'filename': card.file_content.filename
                } if card.file_content else None,
                'updated_at': card.updated_at.strftime('%Y%m%d') if card.updated_at else None
            }
            cards_data.append(card_data)
        
        return jsonify(cards_data)
    except Exception as e:
        print('Error in get_cards:', str(e))
        return jsonify({'error': str(e)}), 500

@app.route('/api/card/<int:card_id>', methods=['GET'])
def get_card(card_id):
    """獲取單個卡片的詳細信息"""
    try:
        card = Card.query.get_or_404(card_id)
        card_data = {
            'id': card.id,
            'position': card.position,
            'background_color': card.background_color,
            'text_content': card.text_content.content if card.text_content else None,
            'image_content': card.image_content.path if card.image_content else None,
            'audio_content': card.audio_content.path if card.audio_content else None,
            'file_content': {
                'path': card.file_content.path,
                'filename': card.file_content.filename
            } if card.file_content else None,
            'updated_at': card.updated_at.strftime('%Y%m%d') if card.updated_at else None
        }
        return jsonify(card_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/card/<int:card_id>/color', methods=['PUT'])
def update_card_color(card_id):
    """更新卡片背景顏色"""
    try:
        card = Card.query.get_or_404(card_id)
        data = request.get_json()
        
        if 'color' in data:
            card.background_color = data['color']
            db.session.commit()
            return jsonify({'success': True})
        return jsonify({'error': 'No color provided'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/card/<int:card_id>/content', methods=['PUT'])
def update_card_content(card_id):
    """更新卡片內容（文字、圖片、音頻、文件）"""
    try:
        card = Card.query.get_or_404(card_id)
        
        # 處理文字內容
        text_content = request.form.get('text_content')
        if text_content is not None:
            if card.text_content:
                card.text_content.content = text_content
            else:
                new_text = TextContent(card_id=card.id, content=text_content)
                db.session.add(new_text)
        
        # 處理圖片上傳
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file and allowed_file(image_file.filename, 'image'):
                filename = save_file(image_file, 'image')
                if filename:
                    if card.image_content:
                        # 刪除舊文件
                        old_path = os.path.join(app.config['UPLOAD_FOLDER'], card.image_content.path)
                        if os.path.exists(old_path):
                            os.remove(old_path)
                        card.image_content.path = filename
                    else:
                        new_image = ImageContent(card_id=card.id, path=filename)
                        db.session.add(new_image)
        
        # 處理音頻上傳
        if 'audio' in request.files:
            audio_file = request.files['audio']
            if audio_file and allowed_file(audio_file.filename, 'audio'):
                filename = save_file(audio_file, 'audio')
                if filename:
                    if card.audio_content:
                        # 刪除舊文件
                        old_path = os.path.join(app.config['UPLOAD_FOLDER'], card.audio_content.path)
                        if os.path.exists(old_path):
                            os.remove(old_path)
                        card.audio_content.path = filename
                    else:
                        new_audio = AudioContent(card_id=card.id, path=filename)
                        db.session.add(new_audio)
        
        # 處理文件上傳
        if 'file' in request.files:
            file = request.files['file']
            if file and allowed_file(file.filename, 'file'):
                filename = save_file(file, 'file')
                if filename:
                    if card.file_content:
                        # 刪除舊文件
                        old_path = os.path.join(app.config['UPLOAD_FOLDER'], card.file_content.path)
                        if os.path.exists(old_path):
                            os.remove(old_path)
                        card.file_content.path = filename
                        card.file_content.filename = file.filename
                    else:
                        new_file = FileContent(card_id=card.id, path=filename, filename=file.filename)
                        db.session.add(new_file)
        
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/card/<int:card_id>/content/<content_type>', methods=['DELETE'])
def delete_card_content(card_id, content_type):
    try:
        card = Card.query.get_or_404(card_id)
        
        if content_type == 'image':
            if card.image_content:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], card.image_content.path)
                if os.path.exists(file_path):
                    os.remove(file_path)
                card.image_content = None
        elif content_type == 'audio':
            if card.audio_content:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], card.audio_content.path)
                if os.path.exists(file_path):
                    os.remove(file_path)
                card.audio_content = None
        elif content_type == 'file':
            if card.file_content:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], card.file_content.path)
                if os.path.exists(file_path):
                    os.remove(file_path)
                card.file_content = None
        
        db.session.commit()
        return jsonify({'message': 'Content deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/cards/reorder', methods=['POST'])
def reorder_cards():
    """重新排序卡片"""
    try:
        data = request.get_json()
        for item in data:
            card = Card.query.get(item['id'])
            if card:
                card.position = item['position']
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    """提供上傳文件的訪問"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    # 應用啟動時初始化數據庫
    with app.app_context():
        db.create_all()
        
        # 檢查每頁的卡片數量，確保每頁都有20張卡片
        for page in range(1, 5):
            cards = Card.query.filter_by(page_number=page).all()
            if len(cards) != 20:
                Card.query.filter_by(page_number=page).delete()
                for pos in range(20):
                    new_card = Card(page_number=page, position=pos)
                    db.session.add(new_card)
        db.session.commit()
    
    # 以調試模式運行應用
    app.run(debug=True)
