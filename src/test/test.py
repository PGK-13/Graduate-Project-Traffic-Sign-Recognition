import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchmetrics import Accuracy, Precision, Recall, F1Score
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager
from src.model.model import LightweightTSRCNN
from src.data.dataset import GTSRB, get_transforms

# 设置设备
if torch.backends.mps.is_available():
    device = torch.device("mps")
    print("使用 MPS 设备")
elif torch.cuda.is_available():
    device = torch.device("cuda")
    print("使用 CUDA 设备")
else:
    device = torch.device("cpu")
    print("使用 CPU 设备")

def test_model(model_path, dataset_path, batch_size=64, visualize=False):
    # 数据预处理
    _, test_transforms = get_transforms()
    
    # 加载测试数据集
    test_dataset = GTSRB(dataset_path, train=False, transform=test_transforms)
    # 避免 macOS 上多进程共享内存权限问题
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=0)
    
    # 加载模型
    model = LightweightTSRCNN(num_classes=43).to(device)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()
    
    # 初始化评估指标
    accuracy = Accuracy(task='multiclass', num_classes=43).to(device)
    precision = Precision(task='multiclass', num_classes=43, average='macro').to(device)
    recall = Recall(task='multiclass', num_classes=43, average='macro').to(device)
    f1 = F1Score(task='multiclass', num_classes=43, average='macro').to(device)
    
    # 混淆矩阵
    confusion_matrix = np.zeros((43, 43), dtype=int)
    
    # 测试循环
    correct = 0
    total = 0
    
    with torch.no_grad():
        for images, labels in test_loader:
            images = images.to(device)
            labels = labels.to(device)
            
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            
            # 更新指标
            accuracy.update(predicted, labels)
            precision.update(predicted, labels)
            recall.update(predicted, labels)
            f1.update(predicted, labels)
            
            # 计算混淆矩阵
            for t, p in zip(labels.view(-1), predicted.view(-1)):
                confusion_matrix[t.long(), p.long()] += 1
            
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    
    # 计算最终指标
    acc = accuracy.compute().item() * 100
    prec = precision.compute().item() * 100
    rec = recall.compute().item() * 100
    f1_score = f1.compute().item() * 100
    
    # 打印结果
    print("\n=== 模型测试结果 ===")
    print(f"准确率: {acc:.2f}%")
    print(f"精确率 (macro): {prec:.2f}%")
    print(f"召回率 (macro): {rec:.2f}%")
    print(f"F1分数 (macro): {f1_score:.2f}%")
    print(f"测试样本总数: {total}")
    print(f"正确分类数: {correct}")
    
    # 可视化混淆矩阵的前几个类别（可选）
    if visualize:
        visualize_confusion_matrix(confusion_matrix, top_n=10)
    
    return {
        'accuracy': acc,
        'precision': prec,
        'recall': rec,
        'f1_score': f1_score,
        'confusion_matrix': confusion_matrix
    }

def visualize_confusion_matrix(confusion_matrix, top_n=10):
    """可视化混淆矩阵的前top_n个类别"""
    # 兼容中文显示（显式指定系统字体文件，避免字体回退失败）
    font_path = "/System/Library/Fonts/PingFang.ttc"
    cn_font = font_manager.FontProperties(fname=font_path)
    plt.rcParams['axes.unicode_minus'] = False
    # 只显示前top_n个类别
    cm_subset = confusion_matrix[:top_n, :top_n]
    
    plt.figure(figsize=(12, 10))
    plt.imshow(cm_subset, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title(f'混淆矩阵（前{top_n}个类别）', fontproperties=cn_font)
    plt.colorbar()
    
    classes = [str(i) for i in range(top_n)]
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45, fontproperties=cn_font)
    plt.yticks(tick_marks, classes, fontproperties=cn_font)
    
    # 在矩阵中显示数值
    fmt = 'd'
    thresh = cm_subset.max() / 2.
    for i in range(cm_subset.shape[0]):
        for j in range(cm_subset.shape[1]):
            plt.text(j, i, format(cm_subset[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm_subset[i, j] > thresh else "black")
    
    plt.ylabel('真实标签', fontproperties=cn_font)
    plt.xlabel('预测标签', fontproperties=cn_font)
    plt.tight_layout()
    plt.savefig('confusion_matrix.png')
    print(f"混淆矩阵已保存到 confusion_matrix.png")

def predict_single_image(image_path, model_path, transform=None):
    """预测单张图像"""
    from PIL import Image
    
    # 默认变换
    if transform is None:
        from torchvision import transforms
        transform = transforms.Compose([
            transforms.Resize((32, 32)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
    
    # 加载图像
    image = Image.open(image_path).convert('RGB')
    image_tensor = transform(image).unsqueeze(0).to(device)
    
    # 加载模型
    model = LightweightTSRCNN(num_classes=43).to(device)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()
    
    # 预测
    with torch.no_grad():
        output = model(image_tensor)
        _, predicted = torch.max(output, 1)
        probabilities = torch.softmax(output, dim=1)
        confidence = probabilities[0][predicted].item()
    
    return predicted.item(), confidence

if __name__ == "__main__":
    # 测试参数
    MODEL_PATH = "/Users/zklee/pyProject/tsr_cnn/models/best_model_epoch_10_97.01.pth"  # 用户指定的模型路径
    DATASET_PATH = "/Users/zklee/pyProject/tsr_cnn/archive"  # 用户的数据集路径
    BATCH_SIZE = 64
    
    try:
        # 测试整个测试集
        results = test_model(MODEL_PATH, DATASET_PATH, BATCH_SIZE, visualize=True)
        
        # 示例：预测单张图像
        # single_image_path = "path/to/test_image.jpg"
        # predicted_class, confidence = predict_single_image(single_image_path, MODEL_PATH)
        # print(f"单张图像预测结果: 类别 {predicted_class}, 置信度: {confidence:.4f}")
        
    except Exception as e:
        print(f"测试过程中出现错误: {e}")
        print("请确保模型路径和数据集路径正确。")
