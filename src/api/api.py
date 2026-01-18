from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import onnxruntime as ort
import numpy as np
from PIL import Image
from torchvision import transforms
import io

app = FastAPI(title="交通标志识别API", description="基于ONNX Runtime的轻量级交通标志分类服务")

# 交通标志类别名称映射（43类）
TRAFFIC_SIGN_NAMES = {
    0: "限速20公里/小时",
    1: "限速30公里/小时",
    2: "限速50公里/小时",
    3: "限速60公里/小时",
    4: "限速70公里/小时",
    5: "限速80公里/小时",
    6: "限速解除80公里/小时",
    7: "限速100公里/小时",
    8: "限速120公里/小时",
    9: "禁止超车",
    10: "大型车辆禁止超车",
    11: "前方路口优先通行",
    12: "主干道先行",
    13: "让路先行",
    14: "停车让行",
    15: "禁止通行",
    16: "禁止大型车辆通行",
    17: "禁止机动车通行",
    18: "注意路况",
    19: "前方有弯道",
    20: "前方有左右连续弯道",
    21: "前方有颠簸路面",
    22: "前方有路面变窄",
    23: "前方有施工",
    24: "前方有交通信号灯",
    25: "前方有人行横道",
    26: "前方有学生行人",
    27: "前方有自行车道",
    28: "注意路面结冰",
    29: "注意野生动物",
    30: "禁止掉头",
    31: "前方有左转车道",
    32: "前方有右转车道",
    33: "前方有左右转车道",
    34: "前方有环岛",
    35: "限速解除50公里/小时",
    36: "限速解除60公里/小时",
    37: "限速解除70公里/小时",
    38: "优先车道",
    39: "限速解除20公里/小时",
    40: "限速解除30公里/小时",
    41: "限速解除40公里/小时",
    42: "限速解除50公里/小时"
}

# 加载ONNX模型
ONNX_MODEL_PATH = "./models/tsr_cnn.onnx"
sess = ort.InferenceSession(ONNX_MODEL_PATH)
input_name = sess.get_inputs()[0].name
output_name = sess.get_outputs()[0].name

# 图像预处理
transform = transforms.Compose([
    transforms.Resize((32, 32)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

@app.post("/predict", summary="预测交通标志")
async def predict(file: UploadFile = File(...)):
    """
    接收图像文件，返回交通标志的预测结果
    
    - **file**: 图像文件（支持JPEG、PNG等格式）
    - **返回**: 预测的类别ID、类别名称和置信度
    """
    try:
        # 读取文件内容
        contents = await file.read()
        
        # 打开图像
        image = Image.open(io.BytesIO(contents)).convert('RGB')
        
        # 预处理图像
        input_tensor = transform(image).unsqueeze(0).numpy()
        
        # 执行推理
        outputs = sess.run([output_name], {input_name: input_tensor})
        logits = outputs[0]
        
        # 解析结果
        predicted_class = int(np.argmax(logits, axis=1)[0])
        probabilities = np.exp(logits) / np.sum(np.exp(logits), axis=1, keepdims=True)
        confidence = float(probabilities[0][predicted_class])
        
        # 获取类别名称
        class_name = TRAFFIC_SIGN_NAMES.get(predicted_class, f"未知类别 ({predicted_class})")
        
        # 返回结果
        return JSONResponse({
            "success": True,
            "prediction": {
                "class_id": predicted_class,
                "class_name": class_name,
                "confidence": round(confidence, 4)
            },
            "message": "预测成功"
        })
        
    except Exception as e:
        return JSONResponse({
            "success": False,
            "prediction": None,
            "message": f"预测失败: {str(e)}"
        }, status_code=500)

@app.get("/health", summary="健康检查")
async def health_check():
    """
    API服务健康检查
    """
    return {
        "status": "ok",
        "message": "交通标志识别API服务正常运行",
        "model": "LightweightTSRCNN (ONNX)",
        "classes": 43
    }

@app.get("/classes", summary="获取所有类别")
async def get_classes():
    """
    获取所有交通标志类别信息
    """
    return {
        "success": True,
        "total_classes": 43,
        "classes": [
            {"id": class_id, "name": class_name}
            for class_id, class_name in TRAFFIC_SIGN_NAMES.items()
        ]
    }

if __name__ == "__main__":
    import uvicorn
    print("启动交通标志识别API服务...")
    print(f"ONNX模型路径: {ONNX_MODEL_PATH}")
    print("服务地址: http://localhost:8000")
    print("文档地址: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
