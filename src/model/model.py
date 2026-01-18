import torch
import torch.nn as nn
import torch.nn.functional as F

class LightweightTSRCNN(nn.Module):
    def __init__(self, num_classes=43):
        super(LightweightTSRCNN, self).__init__()
        
        # 卷积层1: 3x32x32 -> 32x32x32 (padding=2保持尺寸)
        self.conv1 = nn.Conv2d(3, 32, kernel_size=5, padding=2)
        self.bn1 = nn.BatchNorm2d(32)
        self.pool1 = nn.MaxPool2d(2, 2)  # 32x32x32 -> 32x16x16
        
        # 卷积层2: 32x16x16 -> 64x16x16 (padding=2保持尺寸)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=5, padding=2)
        self.bn2 = nn.BatchNorm2d(64)
        self.pool2 = nn.MaxPool2d(2, 2)  # 64x16x16 -> 64x8x8
        
        # 卷积层3: 64x8x8 -> 128x8x8 (padding=1保持尺寸)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.bn3 = nn.BatchNorm2d(128)
        self.pool3 = nn.MaxPool2d(2, 2)  # 128x8x8 -> 128x4x4
        
        # 全连接层
        self.fc1 = nn.Linear(128 * 4 * 4, 2048)
        self.dropout = nn.Dropout(0.5)
        self.fc2 = nn.Linear(2048, num_classes)
    
    def forward(self, x):
        # 卷积层1
        x = self.pool1(F.relu(self.bn1(self.conv1(x))))
        
        # 卷积层2
        x = self.pool2(F.relu(self.bn2(self.conv2(x))))
        
        # 卷积层3
        x = self.pool3(F.relu(self.bn3(self.conv3(x))))
        
        # 展平
        x = x.view(-1, 128 * 4 * 4)
        
        # 全连接层
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        
        return x

# 测试模型
if __name__ == "__main__":
    model = LightweightTSRCNN()
    print(model)
    
    # 测试输入尺寸
    input = torch.randn(1, 3, 32, 32)
    output = model(input)
    print(f"Input shape: {input.shape}")
    print(f"Output shape: {output.shape}")
    
    # 计算模型参数数量
    total_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"Total parameters: {total_params}")
