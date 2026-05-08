"""
LightweightTSRCNN - 完整的交通标志识别模型
包含所有组件：卷积 + BN + ReLU + Pool + Dropout + FC
作为消融实验的基准模型
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class LightweightTSRCNN(nn.Module):
    """轻量化交通标志识别网络（完整版）"""

    def __init__(self, num_classes=43):
        super(LightweightTSRCNN, self).__init__()

        # 卷积层1: 3x32x32 -> 32x32x32
        self.conv1 = nn.Conv2d(3, 32, kernel_size=5, padding=2)
        self.bn1 = nn.BatchNorm2d(32)
        self.pool1 = nn.MaxPool2d(2, 2)  # 32x32x32 -> 32x16x16

        # 卷积层2: 32x16x16 -> 64x16x16
        self.conv2 = nn.Conv2d(32, 64, kernel_size=5, padding=2)
        self.bn2 = nn.BatchNorm2d(64)
        self.pool2 = nn.MaxPool2d(2, 2)  # 64x16x16 -> 64x8x8

        # 卷积层3: 64x8x8 -> 128x8x8
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.bn3 = nn.BatchNorm2d(128)
        self.pool3 = nn.MaxPool2d(2, 2)  # 128x8x8 -> 128x4x4

        # 全连接层
        self.fc1 = nn.Linear(128 * 4 * 4, 2048)
        self.dropout = nn.Dropout(0.5)
        self.fc2 = nn.Linear(2048, num_classes)

    def forward(self, x):
        # 卷积层1: Conv -> BN -> ReLU -> Pool
        x = self.pool1(F.relu(self.bn1(self.conv1(x))))

        # 卷积层2: Conv -> BN -> ReLU -> Pool
        x = self.pool2(F.relu(self.bn2(self.conv2(x))))

        # 卷积层3: Conv -> BN -> ReLU -> Pool
        x = self.pool3(F.relu(self.bn3(self.conv3(x))))

        # 展平
        x = x.view(-1, 128 * 4 * 4)

        # 全连接层
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)

        return x


if __name__ == "__main__":
    # 测试模型
    model = LightweightTSRCNN(num_classes=43)
    print(model)

    # 测试输入
    input_tensor = torch.randn(1, 3, 32, 32)
    output = model(input_tensor)
    print(f"Input shape: {input_tensor.shape}")
    print(f"Output shape: {output.shape}")

    # 统计参数量
    total_params = sum(p.numel() for p in model.parameters())
    print(f"Total parameters: {total_params:,}")
