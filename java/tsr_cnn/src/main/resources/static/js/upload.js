document.addEventListener('DOMContentLoaded', function() {
    const dropArea = document.getElementById('drop-area');
    const fileInput = document.getElementById('file-input');
    const browseBtn = document.getElementById('browse-btn');
    const resultSection = document.getElementById('result-section');
    const previewImage = document.getElementById('preview-image');
    const predictedClass = document.getElementById('predicted-class');
    const className = document.getElementById('class-name');
    const confidence = document.getElementById('confidence');
    const newUpload = document.getElementById('new-upload');
    
    // 浏览按钮点击事件
    browseBtn.addEventListener('click', function() {
        fileInput.click();
    });
    
    // 文件选择事件
    fileInput.addEventListener('change', function() {
        if (this.files.length > 0) {
            uploadFile(this.files[0]);
        }
    });
    
    // 拖拽事件
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
    });
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    // 拖拽样式
    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, highlight, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, unhighlight, false);
    });
    
    function highlight() {
        dropArea.classList.add('dragover');
    }
    
    function unhighlight() {
        dropArea.classList.remove('dragover');
    }
    
    // 拖拽上传
    dropArea.addEventListener('drop', handleDrop, false);
    
    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        
        if (files.length > 0) {
            uploadFile(files[0]);
        }
    }
    
    // 上传文件
    function uploadFile(file) {
        console.log('开始上传文件:', file.name, file.type);
        
        const formData = new FormData();
        formData.append('file', file);
        
        // 显示加载状态
        dropArea.innerHTML = '<div style="text-align: center;"><p>正在上传和识别...</p></div>';
        
        // 发送请求
        fetch('/api/image/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            console.log('响应状态:', response.status, response.statusText);
            return response.json();
        })
        .then(data => {
            console.log('响应数据:', data);
            if (data.success) {
                // 显示结果
                showResult(data.data);
            } else {
                // 显示错误
                alert('上传失败: ' + data.error);
                resetUploadArea();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('上传失败: 服务器错误');
            resetUploadArea();
        });
    }
    
    // 显示结果
    function showResult(result) {
        // 隐藏上传区域
        document.querySelector('.upload-section').style.display = 'none';
        
        // 显示结果区域
        resultSection.style.display = 'block';
        
        // 设置预览图像
        previewImage.src = '/' + result.imagePath;
        
        // 设置识别结果
        predictedClass.textContent = result.predictedClass;
        className.textContent = result.className;
        confidence.textContent = (result.confidence * 100).toFixed(2) + '%';
    }
    
    // 重置上传区域
    function resetUploadArea() {
        dropArea.innerHTML = `
            <div class="drop-content">
                <svg class="upload-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 2L2 7l10 5 10-5-10-5z"/>
                    <path d="M2 17l10 5 10-5"/>
                    <path d="M2 12l10 5 10-5"/>
                </svg>
                <p>点击或拖拽图像到此处上传</p>
                <input type="file" id="file-input" accept="image/*" style="display: none;">
                <button id="browse-btn" class="btn">浏览文件</button>
            </div>
        `;
        
        // 重新绑定事件
        const newFileInput = document.getElementById('file-input');
        const newBrowseBtn = document.getElementById('browse-btn');
        
        newBrowseBtn.addEventListener('click', function() {
            newFileInput.click();
        });
        
        newFileInput.addEventListener('change', function() {
            if (this.files.length > 0) {
                uploadFile(this.files[0]);
            }
        });
    }
    
    // 重新上传按钮
    newUpload.addEventListener('click', function() {
        // 显示上传区域
        document.querySelector('.upload-section').style.display = 'block';
        
        // 隐藏结果区域
        resultSection.style.display = 'none';
        
        // 重置上传区域
        resetUploadArea();
    });
});
