"""
LightweightTSRCNN_LeakyReLU - LeakyReLU激活函数消融模型
将 ReLU 替换为 LeakyReLU (alpha=0.1)，用于验证激活函数的选择
"""

import torch
import torch.nn as nn


class LightweightTSRCNN_LeakyReLU(nn.Module):
    """轻量化交通标志识别网络（LeakyReLU版）- 消融实验用"""

    def __init__(self, num_classes=43, alpha=0.1):
        super(LightweightTSRCNN_LeakyReLU, self).__init__()
        self.alpha = alpha

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
        # 卷积层1: Conv -> BN -> LeakyReLU -> Pool
        x = self.pool1(nn.functional.leaky_relu(self.bn1(self.conv1(x)), self.alpha))

        # 卷积层2: Conv -> BN -> LeakyReLU -> Pool
        x = self.pool2(nn.functional.leaky_relu(self.bn2(self.conv2(x)), self.alpha))

        # 卷积层3: Conv -> BN -> LeakyReLU -> Pool
        x = self.pool3(nn.functional.leaky_relu(self.bn3(self.conv3(x)), self.alpha))

        # 展平
        x = x.view(-1, 128 * 4 * 4)

        # 全连接层
        x = nn.functional.leaky_relu(self.fc1(x), self.alpha)
        x = self.dropout(x)
        x = self.fc2(x)

        return x


if __name__ == "__main__":
    # 测试模型
    model = LightweightTSRCNN_LeakyReLU(num_classes=43)
    print(model)

    # 测试输入
    input_tensor = torch.randn(1, 3, 32, 32)
    output = model(input_tensor)
    print(f"Input shape: {input_tensor.shape}")
    print(f"Output shape: {output.shape}")

    # 统计参数量
    total_params = sum(p.numel() for p in model.parameters())
    print(f"Total parameters: {total_params:,}")
