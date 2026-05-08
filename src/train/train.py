import os
import json
import argparse
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from src.model import MODEL_REGISTRY
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

def train_model(dataset_path, model_name='LightweightTSRCNN', epochs=50, batch_size=64, learning_rate=0.001, save_dir="./models"):
    # 数据预处理
    train_transforms, test_transforms = get_transforms()

    # 加载数据集
    train_dataset = GTSRB(dataset_path, train=True, transform=train_transforms)
    test_dataset = GTSRB(dataset_path, train=False, transform=test_transforms)

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=0)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=0)

    # 初始化模型（从注册表获取）
    if model_name not in MODEL_REGISTRY:
        raise ValueError(f"模型 '{model_name}' 未注册！可用模型: {list(MODEL_REGISTRY.keys())}")
    model = MODEL_REGISTRY[model_name](num_classes=43).to(device)
    print(f"使用模型: {model_name}")

    # 损失函数和优化器
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=5, factor=0.5)

    # 创建模型保存目录（按模型名分类）
    model_save_dir = os.path.join(save_dir, model_name)
    if not os.path.exists(model_save_dir):
        os.makedirs(model_save_dir)

    # 训练历史记录（用于绘制曲线）
    history = {
        'train_loss': [],
        'train_acc': [],
        'val_loss': [],
        'val_acc': []
    }

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

        # 计算训练集指标
        train_loss = running_loss / len(train_loader)
        train_accuracy = 100 * correct / total
        print(f'轮次 [{epoch+1}/{epochs}], 训练损失: {train_loss:.4f}, 训练准确率: {train_accuracy:.2f}%')

        # 验证模型
        val_accuracy, val_loss = evaluate_model(model, test_loader, device, criterion)
        print(f'轮次 [{epoch+1}/{epochs}], 验证损失: {val_loss:.4f}, 验证准确率: {val_accuracy:.2f}%')

        # 记录历史
        history['train_loss'].append(train_loss)
        history['train_acc'].append(train_accuracy)
        history['val_loss'].append(val_loss)
        history['val_acc'].append(val_accuracy)

        # 学习率调度
        scheduler.step(100 - val_accuracy)  # 因为ReduceLROnPlateau期望指标越小越好

        # 保存最佳模型
        if val_accuracy > best_accuracy:
            best_accuracy = val_accuracy
            model_path = os.path.join(model_save_dir, f'{model_name}_epoch{epoch+1}_{val_accuracy:.2f}.pth')
            torch.save(model.state_dict(), model_path)
            print(f'保存最佳模型到: {model_path}')

    # 保存训练历史到 JSON
    history_path = os.path.join(model_save_dir, f'{model_name}_history.json')
    with open(history_path, 'w') as f:
        json.dump(history, f)
    print(f'训练历史已保存到: {history_path}')

    print(f'训练完成! 最佳验证准确率: {best_accuracy:.2f}%')
    return model, history

def evaluate_model(model, test_loader, device, criterion=None):
    """评估模型，返回准确率和损失"""
    model.eval()
    correct = 0
    total = 0
    total_loss = 0.0

    with torch.no_grad():
        for images, labels in test_loader:
            images = images.to(device)
            labels = labels.to(device)

            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)

            if criterion is not None:
                loss = criterion(outputs, labels)
                total_loss += loss.item()

            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    accuracy = 100 * correct / total
    avg_loss = total_loss / len(test_loader) if criterion is not None else 0.0
    return accuracy, avg_loss

def test_model(model, test_loader, device):
    """旧版测试函数，保持向后兼容"""
    accuracy, _ = evaluate_model(model, test_loader, device)
    return accuracy

if __name__ == "__main__":
    # 命令行参数解析
    parser = argparse.ArgumentParser(description='训练交通标志识别模型')
    parser.add_argument('--model', type=str, default='LightweightTSRCNN',
                        choices=list(MODEL_REGISTRY.keys()),
                        help='选择模型 (默认: LightweightTSRCNN)')
    parser.add_argument('--dataset', type=str, default="/Users/zklee/pyProject/tsr_cnn/archive",
                        help='数据集路径')
    parser.add_argument('--epochs', type=int, default=50, help='训练轮数 (默认: 50)')
    parser.add_argument('--batch_size', type=int, default=64, help='批次大小 (默认: 64)')
    parser.add_argument('--lr', type=float, default=0.001, help='学习率 (默认: 0.001)')
    parser.add_argument('--save_dir', type=str, default="./models", help='模型保存路径 (默认: ./models)')

    args = parser.parse_args()

    try:
        train_model(
            dataset_path=args.dataset,
            model_name=args.model,
            epochs=args.epochs,
            batch_size=args.batch_size,
            learning_rate=args.lr,
            save_dir=args.save_dir
        )
    except Exception as e:
        print(f"训练过程中出现错误: {e}")
        print("请确保数据集路径正确，并且数据集已经解压完成。")
