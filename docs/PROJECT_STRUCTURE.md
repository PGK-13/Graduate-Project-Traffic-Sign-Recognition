# 交通标志识别项目结构

## 项目概述

这是一个基于PyTorch和ONNX的轻量级交通标志识别系统，包含模型训练、测试、ONNX导出和API服务等完整功能。

## 目录结构

```
ts_r_cnn/
├── archive/              # GTSRB数据集
│   ├── Train/           # 训练集图像
│   ├── Test/            # 测试集图像
│   ├── Train.csv        # 训练集标注
│   └── Test.csv         # 测试集标注
├── docs/                # 文档目录
│   └── PROJECT_STRUCTURE.md  # 项目结构说明
├── models/              # 模型保存目录
│   ├── tsr_cnn.onnx     # ONNX模型文件
│   └── best_model_epoch_X_XX.XX.pth  # PyTorch模型文件
├── src/                 # 源代码目录
│   ├── data/            # 数据处理模块
│   │   └── dataset.py   # 数据集加载和预处理
│   ├── model/           # 模型定义模块
│   │   └── model.py     # CNN模型定义
│   ├── train/           # 训练模块
│   │   └── train.py     # 模型训练代码
│   ├── test/            # 测试模块
│   │   └── test.py      # 模型测试代码
│   ├── export/          # 导出模块
│   │   └── export_onnx.py  # ONNX模型导出
│   └── api/             # API服务模块
│       └── api.py       # FastAPI服务
├── main.py              # 主程序入口
├── USAGE.md             # 使用说明
├── README.md            # 项目说明
└── requirements.txt     # 项目依赖
```

## 模块说明

### 1. 数据处理模块 (src/data/)
- **dataset.py**: GTSRB数据集的加载、预处理和数据增强

### 2. 模型定义模块 (src/model/)
- **model.py**: 轻量级CNN模型的定义，输入32×32，输出43类

### 3. 训练模块 (src/train/)
- **train.py**: 模型训练代码，支持M1的MPS/CPU/CUDA设备

### 4. 测试模块 (src/test/)
- **test.py**: 模型测试代码，包含准确率、精确率、召回率和混淆矩阵

### 5. 导出模块 (src/export/)
- **export_onnx.py**: 将PyTorch模型导出为ONNX格式

### 6. API服务模块 (src/api/)
- **api.py**: FastAPI服务，提供交通标志识别的RESTful API

## 使用示例

### 训练模型
```bash
python main.py --train
```

### 测试模型
```bash
python main.py --test --model_path ./models/best_model_epoch_X_XX.XX.pth
```

### 导出ONNX模型
```bash
python src/export/export_onnx.py
```

### 启动API服务
```bash
python src/api/api.py
```

## 注意事项

1. **路径问题**: 所有模块之间的导入都使用绝对路径，确保在项目根目录下运行
2. **依赖安装**: 运行前请安装requirements.txt中的依赖
3. **数据集**: 确保archive目录下有完整的GTSRB数据集
