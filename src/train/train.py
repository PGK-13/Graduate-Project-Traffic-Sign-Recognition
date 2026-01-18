import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
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

def train_model(dataset_path, epochs=50, batch_size=64, learning_rate=0.001, save_dir="./models"):
    # 数据预处理
    train_transforms, test_transforms = get_transforms()
    
    # 加载数据集
    train_dataset = GTSRB(dataset_path, train=True, transform=train_transforms)
    test_dataset = GTSRB(dataset_path, train=False, transform=test_transforms)
    
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=2)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=2)
    
    # 初始化模型
    model = LightweightTSRCNN(num_classes=43).to(device)
    
    # 损失函数和优化器
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=5, factor=0.5)
    
    # 创建模型保存目录
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    # 训练循环
    best_accuracy = 0.0
    for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        
        for i, (images, labels) in enumerate(train_loader):
            # 将数据移到设备
            images = images.to(device)
            labels = labels.to(device)
            
            # 前向传播
            outputs = model(images)
            loss = criterion(outputs, labels)
            
            # 反向传播和优化
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            # 统计
            running_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            
            if (i+1) % 100 == 0:
                print(f'轮次 [{epoch+1}/{epochs}], 批次 [{i+1}/{len(train_loader)}], 损失: {running_loss/(i+1):.4f}, 准确率: {100*correct/total:.2f}%')
        
        # 计算训练集准确率
        train_accuracy = 100 * correct / total
        print(f'轮次 [{epoch+1}/{epochs}], 训练损失: {running_loss/len(train_loader):.4f}, 训练准确率: {train_accuracy:.2f}%')
        
        # 验证模型
        val_accuracy = test_model(model, test_loader, device)
        print(f'轮次 [{epoch+1}/{epochs}], 验证准确率: {val_accuracy:.2f}%')
        
        # 学习率调度
        scheduler.step(100 - val_accuracy)  # 因为ReduceLROnPlateau期望指标越小越好
        
        # 保存最佳模型
        if val_accuracy > best_accuracy:
            best_accuracy = val_accuracy
            model_path = os.path.join(save_dir, f'best_model_epoch_{epoch+1}_{best_accuracy:.2f}.pth')
            torch.save(model.state_dict(), model_path)
            print(f'保存最佳模型到: {model_path}')
    
    print(f'训练完成! 最佳验证准确率: {best_accuracy:.2f}%')
    return model

def test_model(model, test_loader, device):
    model.eval()
    correct = 0
    total = 0
    
    with torch.no_grad():
        for images, labels in test_loader:
            images = images.to(device)
            labels = labels.to(device)
            
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    
    accuracy = 100 * correct / total
    return accuracy

if __name__ == "__main__":
    # 数据集路径
    DATASET_PATH = "/Users/zklee/pyProject/tsr_cnn/archive"  # 用户的数据集路径
    
    # 训练参数
    EPOCHS = 50
    BATCH_SIZE = 64
    LEARNING_RATE = 0.001
    SAVE_DIR = "./models"
    
    try:
        train_model(DATASET_PATH, EPOCHS, BATCH_SIZE, LEARNING_RATE, SAVE_DIR)
    except Exception as e:
        print(f"训练过程中出现错误: {e}")
        print("请确保数据集路径正确，并且数据集已经解压完成。")
