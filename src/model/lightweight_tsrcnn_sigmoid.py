"""
LightweightTSRCNN_Sigmoid - Sigmoid激活函数消融模型
将 ReLU 替换为 Sigmoid，用于验证激活函数的选择
注意：Sigmoid 可能导致梯度消失问题
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class LightweightTSRCNN_Sigmoid(nn.Module):
    """轻量化交通标志识别网络（Sigmoid版）- 消融实验用"""

    def __init__(self, num_classes=43):
        super(LightweightTSRCNN_Sigmoid, self).__init__()

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
        # 卷积层1: Conv -> BN -> Sigmoid -> Pool
        x = self.pool1(torch.sigmoid(self.bn1(self.conv1(x))))

        # 卷积层2: Conv -> BN -> Sigmoid -> Pool
        x = self.pool2(torch.sigmoid(self.bn2(self.conv2(x))))

        # 卷积层3: Conv -> BN -> Sigmoid -> Pool
        x = self.pool3(torch.sigmoid(self.bn3(self.conv3(x))))

        # 展平
        x = x.view(-1, 128 * 4 * 4)

        # 全连接层
        x = torch.sigmoid(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)

        return x


if __name__ == "__main__":
    # 测试模型
    model = LightweightTSRCNN_Sigmoid(num_classes=43)
    print(model)

    # 测试输入
    input_tensor = torch.randn(1, 3, 32, 32)
    output = model(input_tensor)
    print(f"Input shape: {input_tensor.shape}")
    print(f"Output shape: {output.shape}")

    # 统计参数量
    total_params = sum(p.numel() for p in model.parameters())
    print(f"Total parameters: {total_params:,}")
