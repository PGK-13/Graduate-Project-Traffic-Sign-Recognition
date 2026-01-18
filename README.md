# 轻量级交通标志分类CNN

一个基于PyTorch的轻量级CNN模型，用于GTSRB数据集的交通标志分类任务。

## 特性

- ✅ 轻量级CNN模型，适合在资源受限设备上运行
- ✅ 支持Mac M1的MPS加速
- ✅ 输入统一为32×32像素
- ✅ 输出43类交通标志
- ✅ 完整的训练和测试代码
- ✅ 自动下载和解压数据集功能

## 环境要求

- Python 3.7+
- PyTorch 2.0+
- torchvision
- torchmetrics
- matplotlib
- requests
- Pillow
- numpy

## 安装依赖

```bash
pip install torch torchvision torchmetrics matplotlib requests pillow numpy
```

## 数据集

使用GTSRB（German Traffic Sign Recognition Benchmark）数据集，包含43类交通标志：
- 训练集：约39,000张图像
- 测试集：约12,600张图像

程序支持自动下载数据集，或手动下载后放入指定目录。

## 使用方法

### 1. 自动下载数据集

```bash
python main.py --download
```

### 2. 训练模型

```bash
python main.py --train --epochs 50 --batch_size 64 --lr 0.001
```

### 3. 测试模型

```bash
python main.py --test --model_path ./models/best_model_epoch_xx_xx.xx.pth
```

### 4. 一站式操作（下载+训练+测试）

```bash
python main.py --download --train --test --epochs 50
```

## 模型结构

轻量级CNN模型结构：

1. **卷积层1**：3×32×32 → 32×32×32（5×5卷积，padding=2，BN，ReLU，MaxPool）
2. **卷积层2**：32×32×32 → 64×16×16（5×5卷积，padding=2，BN，ReLU，MaxPool）
3. **卷积层3**：64×16×16 → 128×8×8（3×3卷积，padding=1，BN，ReLU，MaxPool）
4. **全连接层1**：128×4×4 → 2048（ReLU，Dropout）
5. **全连接层2**：2048 → 43（输出43类）

## 文件结构

```
ts_r_cnn/
├── model.py           # 模型定义
├── dataset.py         # 数据集加载器
├── train.py           # 训练代码
├── test.py            # 测试代码
├── main.py            # 主程序（下载+训练+测试）
├── README.md          # 项目说明
├── models/            # 模型保存目录
└── GTSRB/             # 数据集目录
    ├── Training/      # 训练集
    └── Final_Test/    # 测试集
```

## 训练参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| epochs | 50 | 训练轮次 |
| batch_size | 64 | 批量大小 |
| learning_rate | 0.001 | 学习率 |
| save_dir | ./models | 模型保存目录 |

## 设备支持

- **Mac M1/M2**：自动使用MPS加速
- **CUDA设备**：自动使用CUDA加速
- **CPU**：所有设备兼容

## 测试评估指标

- 准确率（Accuracy）
- 精确率（Precision）
- 召回率（Recall）
- F1分数（F1 Score）
- 混淆矩阵（可视化）

## 注意事项

1. 首次运行时会自动下载数据集，需要网络连接
2. 训练时间取决于设备性能（M1/M2约需30-60分钟）
3. 模型会保存在`./models`目录下，文件名包含准确率信息
4. 测试时需要指定正确的模型文件路径

## 参考

- [GTSRB数据集](http://benchmark.ini.rub.de/?section=gtsrb&subsection=dataset)
- [PyTorch文档](https://pytorch.org/docs/)

## 许可证

MIT License
