// 全局變量
let currentCardId = null;
let cardData = {};
let currentPage = 1;
let cardModal = null;
let colorModal = null;

// 初始化
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded');
    
    // 初始化Bootstrap模態框
    cardModal = new bootstrap.Modal(document.getElementById('cardModal'));
    colorModal = new bootstrap.Modal(document.getElementById('colorModal'));
    
    // 設置事件監聽器
    setupEventListeners();
    
    // 加載第一頁卡片
    loadCards();
});

// 設置事件監聽器
function setupEventListeners() {
    console.log('Setting up event listeners');
    
    // 頁面按鈕點擊
    document.querySelectorAll('#pageButtons button').forEach(button => {
        button.addEventListener('click', function() {
            const page = parseInt(this.dataset.page);
            currentPage = page;
            document.querySelectorAll('#pageButtons button').forEach(btn => {
                btn.classList.remove('active');
            });
            this.classList.add('active');
            loadCards();
        });
    });
    
    // 卡片拖放排序
    const container = document.querySelector('.cards-container');
    new Sortable(container, {
        animation: 150,
        onEnd: function(evt) {
            const cards = document.querySelectorAll('.card');
            const newOrder = Array.from(cards).map((card, index) => ({
                id: parseInt(card.dataset.cardId),
                position: index
            }));
            
            fetch('/api/cards/reorder', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(newOrder)
            });
        }
    });
    
    // 保存按鈕事件
    document.getElementById('saveCard').addEventListener('click', handleSave);
    
    // 顏色選擇器事件
    document.querySelectorAll('.color-option').forEach(option => {
        option.addEventListener('click', function() {
            const color = this.dataset.color;
            updateCardColor(currentCardId, color);
            colorModal.hide();
        });
    });
    
    // 添加刪除按鈕事件監聽器
    document.querySelectorAll('.delete-preview').forEach(button => {
        button.addEventListener('click', async function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            if (confirm('確定要刪除此內容嗎？')) {
                const type = this.dataset.type;
                try {
                    const response = await fetch(`/api/card/${currentCardId}/content/${type}`, {
                        method: 'DELETE'
                    });
                    
                    if (!response.ok) throw new Error('Failed to delete content');
                    
                    // 清除預覽
                    const previewContainer = this.closest('.preview-container');
                    previewContainer.innerHTML = '';
                    previewContainer.style.display = 'none';
                    
                    // 重新加載卡片
                    await loadCards();
                    
                } catch (error) {
                    console.error('Error deleting content:', error);
                    alert('刪除失敗：' + error.message);
                }
            }
        });
    });
    
    // 處理刪除卡片
    document.getElementById('deleteCard').addEventListener('click', function() {
        const modal = document.getElementById('cardModal');
        const cardId = modal.dataset.cardId;
        
        if (!cardId) {
            console.error('No card ID found');
            return;
        }

        if (confirm('確定要清空這張卡片的所有內容嗎？清空後將無法恢復。')) {
            fetch(`/api/card/${cardId}`, {
                method: 'DELETE'
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to clear card content');
                }
                return response.json();
            })
            .then(data => {
                if (data.message) {
                    // 關閉模態框
                    const modal = bootstrap.Modal.getInstance(document.getElementById('cardModal'));
                    modal.hide();
                    
                    // 重新加載卡片
                    loadCards();
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showError('清空卡片內容時發生錯誤：' + error.message);
            });
        }
    });
}

// 加載卡片
async function loadCards() {
    console.log('Loading cards for page:', currentPage);
    try {
        const response = await fetch(`/api/cards/${currentPage}`);
        if (!response.ok) throw new Error('Failed to load cards');
        
        const cards = await response.json();
        console.log('Loaded cards:', cards);
        
        const container = document.querySelector('.cards-container');
        container.innerHTML = '';
        
        cards.forEach(card => {
            const cardElement = createCardElement(card);
            container.appendChild(cardElement);
            cardData[card.id] = card;
        });
    } catch (error) {
        console.error('Error loading cards:', error);
        showError('Failed to load cards');
    }
}

// 創建卡片元素
function createCardElement(card) {
    const div = document.createElement('div');
    div.className = 'card';
    div.dataset.cardId = card.id;
    div.style.backgroundColor = card.background_color || '#E0FFFF';
    
    // 添加事件監聽器
    div.addEventListener('click', handleCardClick);
    div.addEventListener('dblclick', handleCardDoubleClick);
    div.addEventListener('contextmenu', handleCardRightClick);
    
    // 渲染內容
    renderCardContent(card, div);
    
    return div;
}

// 渲染卡片內容
function renderCardContent(card, element) {
    let content = '';
    
    // 顯示文字內容
    if (card.text_content) {
        // 計算字體大小倍數
        const textLength = card.text_content.length;
        let fontSize = 14; // 預設字體大小
        
        if (textLength < 8) {
            fontSize = fontSize * 3; // 少於8個字，字體放大3倍
        } else if (textLength < 20) {
            fontSize = fontSize * 2; // 少於20個字，字體放大2倍
        }
        
        content += `<div class="card-text" style="font-size: ${fontSize}px">${card.text_content}</div>`;
    }
    
    // 顯示圖片
    if (card.image_content) {
        content += `<img src="/uploads/${card.image_content}" class="card-img" alt="Card image">`;
    }
    
    // 顯示音頻
    if (card.audio_content) {
        content += `
            <audio controls class="card-audio">
                <source src="/uploads/${card.audio_content}" type="audio/mpeg">
                Your browser does not support the audio element.
            </audio>
        `;
    }
    
    // 顯示文件
    if (card.file_content) {
        content += `
            <div class="card-file">
                <a href="/uploads/${card.file_content.path}" target="_blank">
                    ${card.file_content.filename}
                </a>
            </div>
        `;
    }
    
    // 如果沒有內容，顯示提示文字
    if (!content) {
        content = '<div class="card-empty">雙擊編輯</div>';
    }
    
    element.innerHTML = content;
}

// 處理卡片點擊
function handleCardClick(event) {
    const card = event.currentTarget;
    card.classList.toggle('flipped');
}

// 處理卡片雙擊
function handleCardDoubleClick(event) {
    event.preventDefault();
    event.stopPropagation();
    
    currentCardId = parseInt(event.currentTarget.dataset.cardId);
    const cardInfo = cardData[currentCardId];
    
    // 設置模態框的cardId
    document.getElementById('cardModal').dataset.cardId = currentCardId;
    
    // 清空所有預覽
    document.getElementById('imagePreview').innerHTML = '';
    document.getElementById('audioPreview').innerHTML = '';
    document.getElementById('filePreview').innerHTML = '';
    
    // 填充文字內容
    document.getElementById('textContent').value = cardInfo.text_content || '';
    
    // 顯示現有內容預覽
    if (cardInfo.image_content) {
        document.getElementById('imagePreview').innerHTML = `
            <img src="/uploads/${cardInfo.image_content}" class="preview-img" alt="Current image">
            <button type="button" class="btn btn-danger delete-preview" data-type="image">刪除</button>
        `;
        document.getElementById('imagePreview').style.display = 'block';
    }
    
    if (cardInfo.audio_content) {
        document.getElementById('audioPreview').innerHTML = `
            <audio controls>
                <source src="/uploads/${cardInfo.audio_content}" type="audio/mpeg">
            </audio>
            <button type="button" class="btn btn-danger delete-preview" data-type="audio">刪除</button>
        `;
        document.getElementById('audioPreview').style.display = 'block';
    }
    
    if (cardInfo.file_content) {
        document.getElementById('filePreview').innerHTML = `
            <a href="/uploads/${cardInfo.file_content.path}" target="_blank">
                ${cardInfo.file_content.filename}
            </a>
            <button type="button" class="btn btn-danger delete-preview" data-type="file">刪除</button>
        `;
        document.getElementById('filePreview').style.display = 'block';
    }
    
    // 清空文件輸入
    document.getElementById('imageUpload').value = '';
    document.getElementById('audioUpload').value = '';
    document.getElementById('fileUpload').value = '';
    
    // 顯示模態框
    cardModal.show();
}

// 處理卡片右鍵點擊
function handleCardRightClick(event) {
    event.preventDefault();
    currentCardId = parseInt(event.currentTarget.dataset.cardId);
    colorModal.show();
}

// 更新卡片顏色
async function updateCardColor(cardId, color) {
    try {
        const response = await fetch(`/api/card/${cardId}/color`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ color: color })
        });
        
        if (!response.ok) throw new Error('Failed to update color');
        
        // 更新 UI
        const card = document.querySelector(`[data-card-id="${cardId}"]`);
        if (card) {
            card.style.backgroundColor = color;
        }
    } catch (error) {
        console.error('Error updating card color:', error);
        showError('Failed to update card color');
    }
}

// 處理保存
async function handleSave() {
    try {
        const formData = new FormData();
        
        // 添加文字內容
        const textContent = document.getElementById('textContent').value;
        formData.append('text_content', textContent);
        
        // 添加圖片
        const imageFile = document.getElementById('imageUpload').files[0];
        if (imageFile) {
            formData.append('image', imageFile);
        }
        
        // 添加音頻
        const audioFile = document.getElementById('audioUpload').files[0];
        if (audioFile) {
            formData.append('audio', audioFile);
        }
        
        // 添加文件
        const file = document.getElementById('fileUpload').files[0];
        if (file) {
            formData.append('file', file);
        }
        
        const response = await fetch(`/api/card/${currentCardId}/content`, {
            method: 'PUT',
            body: formData
        });
        
        if (!response.ok) throw new Error('Failed to save card');
        
        // 重新加載卡片
        await loadCards();
        
        // 關閉模態框
        cardModal.hide();
        
    } catch (error) {
        console.error('Error saving card:', error);
        showError('Failed to save card');
    }
}

// 顯示錯誤
function showError(message) {
    alert(message);
}
