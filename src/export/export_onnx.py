import torch
import onnx
import onnxruntime as ort
import numpy as np
from PIL import Image
from torchvision import transforms
from src.model.model import LightweightTSRCNN

# 设置设备
if torch.backends.mps.is_available():
    device = torch.device("mps")
elif torch.cuda.is_available():
    device = torch.device("cuda")
else:
    device = torch.device("cpu")

# 模型路径
PYTORCH_MODEL_PATH = "./models/best_model_epoch_1_65.93.pth"
ONNX_MODEL_PATH = "./models/tsr_cnn.onnx"

# 输入尺寸
INPUT_SIZE = (32, 32)


def export_model_to_onnx():
    """将PyTorch模型导出为ONNX格式"""
    print(f"加载PyTorch模型: {PYTORCH_MODEL_PATH}")
    
    # 加载模型
    model = LightweightTSRCNN(num_classes=43).to(device)
    model.load_state_dict(torch.load(PYTORCH_MODEL_PATH, map_location=device))
    model.eval()
    
    # 创建示例输入
    dummy_input = torch.randn(1, 3, INPUT_SIZE[0], INPUT_SIZE[1]).to(device)
    
    print(f"导出模型为ONNX格式: {ONNX_MODEL_PATH}")
    
    # 导出ONNX模型
    torch.onnx.export(
        model,
        dummy_input,
        ONNX_MODEL_PATH,
        export_params=True,
        opset_version=10,
        do_constant_folding=False,
        input_names=['input'],
        output_names=['output'],
        dynamic_axes={'input': {0: 'batch_size'}, 'output': {0: 'batch_size'}}  # 支持动态批次
    )
    
    print("验证ONNX模型")
    # 验证导出的模型
    onnx_model = onnx.load(ONNX_MODEL_PATH)
    onnx.checker.check_model(onnx_model)
    
    print(f"ONNX模型导出成功！路径: {ONNX_MODEL_PATH}")
    print(f"ONNX模型输入: {dummy_input.shape}")
    print(f"ONNX模型输出: {model(dummy_input).shape}")


class ONNXTSRInference:
    """使用ONNX Runtime进行交通标志推理"""
    
    def __init__(self, onnx_model_path):
        # 创建ONNX Runtime会话
        self.sess = ort.InferenceSession(onnx_model_path)
        
        # 获取输入输出名称
        self.input_name = self.sess.get_inputs()[0].name
        self.output_name = self.sess.get_outputs()[0].name
        
        # 图像预处理
        self.transform = transforms.Compose([
            transforms.Resize(INPUT_SIZE),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
    
    def preprocess_image(self, image_path):
        """预处理图像"""
        image = Image.open(image_path).convert('RGB')
        image_tensor = self.transform(image)
        return image_tensor.unsqueeze(0).numpy()  # 添加批次维度
    
    def predict(self, image_data):
        """进行推理"""
        # 执行推理
        outputs = self.sess.run([self.output_name], {self.input_name: image_data})
        
        # 获取预测结果
        logits = outputs[0]
        predicted_class = np.argmax(logits, axis=1)[0]
        probabilities = np.exp(logits) / np.sum(np.exp(logits), axis=1, keepdims=True)
        confidence = probabilities[0][predicted_class]
        
        return predicted_class, confidence
    
    def predict_image(self, image_path):
        """预测单张图像"""
        image_data = self.preprocess_image(image_path)
        return self.predict(image_data)


def main():
    # 导出ONNX模型
    export_model_to_onnx()
    
    # 创建推理示例
    print("\n创建ONNX推理示例")
    
    # 使用样例代码
    example_code = '''
import onnxruntime as ort
import numpy as np
from PIL import Image
from torchvision import transforms

class ONNXTSRInference:
    def __init__(self, onnx_model_path):
        self.sess = ort.InferenceSession(onnx_model_path)
        self.input_name = self.sess.get_inputs()[0].name
        self.output_name = self.sess.get_outputs()[0].name
        self.transform = transforms.Compose([
            transforms.Resize((32, 32)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
    
    def predict(self, image_path):
        # 预处理
        image = Image.open(image_path).convert('RGB')
        image_tensor = self.transform(image).unsqueeze(0).numpy()
        
        # 推理
        outputs = self.sess.run([self.output_name], {self.input_name: image_tensor})
        logits = outputs[0]
        
        # 后处理
        predicted_class = np.argmax(logits, axis=1)[0]
        probabilities = np.exp(logits) / np.sum(np.exp(logits), axis=1, keepdims=True)
        confidence = probabilities[0][predicted_class]
        
        return predicted_class, confidence

# 使用示例
if __name__ == "__main__":
    # 初始化推理器
    onnx_model_path = "./models/tsr_cnn.onnx"
    inference = ONNXTSRInference(onnx_model_path)
    
    # 预测图像（替换为你的图像路径）
    image_path = "path/to/your/image.jpg"
    predicted_class, confidence = inference.predict(image_path)
    
    print(f"预测结果: 类别 {predicted_class}")
    print(f"置信度: {confidence:.4f}")
'''
    
    # 保存示例代码
    with open("./models/onnx_inference_example.py", "w") as f:
        f.write(example_code)
    
    print(f"ONNX Runtime推理示例已保存到: ./models/onnx_inference_example.py")
    
    # 简单测试
    print("\n测试ONNX推理功能")
    try:
        # 使用训练集中的一张图像进行测试
        test_image_path = "/Users/zklee/pyProject/tsr_cnn/archive/Train/20/00020_00000_00000.png"
        
        # 初始化推理器
        inference = ONNXTSRInference(ONNX_MODEL_PATH)
        
        # 预测
        predicted_class, confidence = inference.predict_image(test_image_path)
        
        print(f"测试图像: {test_image_path}")
        print(f"预测结果: 类别 {predicted_class}")
        print(f"置信度: {confidence:.4f}")
        print("ONNX推理测试成功！")
        
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
