from flask import Flask, request, jsonify
import onnxruntime as ort
import numpy as np
from PIL import Image
from torchvision import transforms
import io

app = Flask(__name__)

# 交通标志类别名称映射
CLASS_NAMES = {
    0: 'Speed limit (20km/h)',
    1: 'Speed limit (30km/h)',
    2: 'Speed limit (50km/h)',
    3: 'Speed limit (60km/h)',
    4: 'Speed limit (70km/h)',
    5: 'Speed limit (80km/h)',
    6: 'End of speed limit (80km/h)',
    7: 'Speed limit (100km/h)',
    8: 'Speed limit (120km/h)',
    9: 'No passing',
    10: 'No passing for vehicles over 3.5 metric tons',
    11: 'Right-of-way at the next intersection',
    12: 'Priority road',
    13: 'Yield',
    14: 'Stop',
    15: 'No vehicles',
    16: 'Vehicles over 3.5 metric tons prohibited',
    17: 'No entry',
    18: 'General caution',
    19: 'Dangerous curve to the left',
    20: 'Dangerous curve to the right',
    21: 'Double curve',
    22: 'Bumpy road',
    23: 'Slippery road',
    24: 'Road narrows on the right',
    25: 'Road work',
    26: 'Traffic signals',
    27: 'Pedestrians',
    28: 'Children crossing',
    29: 'Bicycles crossing',
    30: 'Beware of ice/snow',
    31: 'Wild animals crossing',
    32: 'End of all speed and passing limits',
    33: 'Turn right ahead',
    34: 'Turn left ahead',
    35: 'Ahead only',
    36: 'Go straight or right',
    37: 'Go straight or left',
    38: 'Keep right',
    39: 'Keep left',
    40: 'Roundabout mandatory',
    41: 'End of no passing',
    42: 'End of no passing by vehicles over 3.5 metric tons'
}

# 模型路径（从项目根目录计算）
import os
# api -> src -> 项目根目录
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ONNX_MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "tsr_cnn.onnx")

# 输入尺寸
INPUT_SIZE = (32, 32)

# 加载模型
print("正在加载ONNX模型...")
sess = ort.InferenceSession(ONNX_MODEL_PATH)
input_name = sess.get_inputs()[0].name
output_name = sess.get_outputs()[0].name
print("模型加载成功！")

# 图像预处理
transform = transforms.Compose([
    transforms.Resize(INPUT_SIZE),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def preprocess_image(image_data):
    """预处理图像"""
    image = Image.open(io.BytesIO(image_data)).convert('RGB')
    image_tensor = transform(image)
    return image_tensor.unsqueeze(0).numpy()

def predict(image_data):
    """进行推理"""
    # 执行推理
    outputs = sess.run([output_name], {input_name: image_data})
    
    # 获取预测结果
    logits = outputs[0]
    predicted_class = np.argmax(logits, axis=1)[0]
    probabilities = np.exp(logits) / np.sum(np.exp(logits), axis=1, keepdims=True)
    confidence = probabilities[0][predicted_class]
    
    return predicted_class, confidence

@app.route('/predict', methods=['POST'])
def predict_endpoint():
    """预测端点"""
    try:
        print(f"请求方法: {request.method}")
        print(f"请求头: {dict(request.headers)}")
        print(f"请求参数: {dict(request.form)}")
        print(f"文件参数: {list(request.files.keys())}")
        
        # 检查是否有文件
        if 'file' not in request.files:
            return jsonify({"error": "没有提供图像文件", "available_files": list(request.files.keys())}), 400
        
        # 读取图像
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "没有选择文件"}), 400
        
        # 预处理图像
        image_data = file.read()
        print(f"图像大小: {len(image_data)} bytes")
        processed_image = preprocess_image(image_data)
        
        # 推理
        predicted_class, confidence = predict(processed_image)
        
        # 获取类别名称
        class_name = CLASS_NAMES.get(int(predicted_class), "Unknown")
        
        # 返回结果
        return jsonify({
            "success": True,
            "prediction": {
                "class_id": int(predicted_class),
                "class_name": class_name,
                "confidence": float(confidence)
            },
            "message": "预测成功"
        })
        
    except Exception as e:
        print(f"错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """健康检查端点"""
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    print("启动Flask服务...")
    print("服务地址: http://localhost:5001")
    print("API文档: http://localhost:5001/health")
    print("预测端点: POST http://localhost:5001/predict")
    app.run(host='0.0.0.0', port=5001, debug=False)
