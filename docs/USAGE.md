# 交通标志分类模型使用说明

## 1. 数据集状态

✅ 数据集已成功加载！
- 训练集大小: 39209 张图像
- 测试集大小: 12630 张图像
- 类别数量: 43 类

## 2. 快速开始

### 训练模型

由于代码结构已整理，直接运行 `python3 train.py` 不再适用。您可以使用以下两种方式训练模型：

#### 方式1：使用 main.py 主程序（推荐）
```bash
# 使用默认参数训练
python3 main.py --train

# 自定义参数训练
python3 main.py --train --epochs 10 --batch_size 32 --lr 0.0005
```

#### 方式2：直接运行训练模块
```bash
# 直接运行训练代码
python3 src/train/train.py
```

### 测试模型

训练完成后，会在 `./models/` 目录下生成模型文件，文件名格式为 `best_model_epoch_X_XX.XX.pth`。

#### 方式1：使用 main.py 主程序（推荐）
```bash
# 测试模型（替换为实际生成的模型文件名）
python3 main.py --test --model_path ./models/best_model_epoch_1_65.93.pth
```

#### 方式2：直接运行测试模块
```bash
# 直接运行测试代码
python3 src/test/test.py --model_path ./models/best_model_epoch_1_65.93.pth
```

## 3. 设备支持

程序会自动检测并使用最佳设备：
- ✅ Mac M1/M2: 自动使用 MPS 加速
- ✅ CUDA 设备: 自动使用 CUDA 加速
- ✅ CPU: 所有设备兼容

### ONNX模型导出

您可以将PyTorch模型导出为ONNX格式，用于部署到其他平台或使用ONNX Runtime加速：

```bash
# 导出ONNX模型
python3 src/export/export_onnx.py
```

导出的ONNX模型将保存到 `./models/tsr_cnn.onnx`。

### API服务使用

您可以启动FastAPI服务，通过HTTP请求进行交通标志识别：

```bash
# 启动API服务
python3 src/api/api.py
```

服务启动后：
- 服务地址: http://localhost:8000
- API文档: http://localhost:8000/docs

使用API的示例：

```bash
# 使用curl测试API
curl -X POST "http://localhost:8000/predict" -F "file=@/path/to/your/image.jpg"

# 健康检查
curl http://localhost:8000/health
```

## 4. 模型结构

轻量级 CNN 模型：
- **输入**: 32×32×3 像素图像
- **输出**: 43 类交通标志
- **参数量**: 约 1.5M（非常轻量）

## 5. 训练参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| epochs | 50 | 训练轮次 |
| batch_size | 64 | 批量大小 |
| learning_rate | 0.001 | 学习率 |
| save_dir | ./models | 模型保存目录 |

## 6. 输出文件

- `./models/`: 保存训练好的模型
- `confusion_matrix.png`: 混淆矩阵可视化（测试时生成）
- 训练过程中的输出日志

## 7. 常见问题

### 问题1: 模型训练速度慢
- 解决方案: 确保 MPS 或 CUDA 已启用（程序会自动检测）

### 问题2: 模型文件找不到
- 解决方案: 检查 `./models/` 目录，文件名包含训练轮次和准确率

### 问题3: 测试时提示模型路径错误
- 解决方案: 替换为实际生成的模型文件名，例如：
  ```bash
  python3 test.py --model_path ./models/best_model_epoch_25_98.50.pth
  ```

## 8. 示例命令

```bash
# 训练10轮快速测试
python3 main.py --train --epochs 10

# 测试（替换为实际模型文件名）
python3 main.py --test --model_path ./models/best_model_epoch_10_85.23.pth
```
