# 轻量级交通标志分类CNN

一个基于PyTorch的轻量级CNN模型，用于GTSRB数据集的交通标志分类任务，包含完整的Python模型训练和Java Web应用。

## 特性

- ✅ 轻量级CNN模型，适合在资源受限设备上运行
- ✅ 支持Mac M1的MPS加速
- ✅ 输入统一为32×32像素
- ✅ 输出43类交通标志
- ✅ 完整的训练和测试代码
- ✅ 自动下载和解压数据集功能
- ✅ Flask推理服务，提供REST API
- ✅ Spring Boot Web应用，支持图像上传和结果展示
- ✅ 完整的前后端系统

## 环境要求

### Python环境
- Python 3.7+
- PyTorch 2.0+
- torchvision
- torchmetrics
- matplotlib
- requests
- Pillow
- numpy
- flask
- onnx
- onnxruntime

### Java环境
- JDK 11+
- Maven 3.6+
- Spring Boot 2.7+
- Spring Web
- Spring Data JPA
- H2 Database (嵌入式)

## 安装依赖

### Python依赖
```bash
pip install torch torchvision torchmetrics matplotlib requests pillow numpy flask onnx onnxruntime
```

### Java依赖
Maven会自动下载所需依赖，无需手动安装。

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

### 5. 启动Flask推理服务

```bash
python src/api/flask_api.py
```

服务地址：http://localhost:5001
- 健康检查：GET http://localhost:5001/health
- 预测端点：POST http://localhost:5001/predict

### 6. 启动Spring Boot Web应用

```bash
cd java/tsr_cnn
mvn spring-boot:run
```

应用地址：http://localhost:8080
- 主页面：http://localhost:8080
- 识别记录：http://localhost:8080/records
- 统计分析：http://localhost:8080/statistics

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
├── src/                  # Python源代码
│   ├── api/              # Flask推理服务
│   │   ├── api.py        # FastAPI服务（备用）
│   │   └── flask_api.py  # Flask推理服务
│   ├── data/             # 数据集处理
│   │   └── dataset.py    # 数据集加载器
│   ├── export/           # ONNX模型导出
│   │   └── export_onnx.py # ONNX导出脚本
│   ├── model/            # 模型定义
│   │   └── model.py      # CNN模型定义
│   ├── train/            # 训练代码
│   │   └── train.py      # 训练脚本
│   └── test/             # 测试代码
│       └── test.py       # 测试脚本
├── java/                 # Java Web应用
│   └── tsr_cnn/          # Spring Boot项目
│       ├── src/          # Java源代码
│       ├── resources/    # 资源文件
│       └── pom.xml       # Maven配置
├── models/               # 模型保存目录
├── archive/              # 数据集目录
├── main.py               # 主程序（下载+训练+测试）
├── README.md             # 项目说明
├── USAGE.md              # 使用说明
└── .gitignore            # Git忽略文件
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

## 系统集成流程

1. **训练模型**：使用Python代码训练交通标志分类模型
2. **导出ONNX**：将训练好的模型导出为ONNX格式
3. **启动Flask服务**：启动推理服务，提供REST API
4. **启动Spring Boot应用**：启动Web应用，调用Flask服务进行推理
5. **访问Web界面**：通过浏览器上传图像并查看识别结果

## 部署说明

### 本地开发环境
1. 启动Flask服务：`python src/api/flask_api.py`
2. 启动Spring Boot应用：`cd java/tsr_cnn && mvn spring-boot:run`
3. 访问：http://localhost:8080

### 生产环境部署
1. 使用Gunicorn部署Flask服务
2. 打包Spring Boot应用为jar文件：`mvn clean package`
3. 使用systemd或Docker部署应用

## 注意事项

1. 首次运行时会自动下载数据集，需要网络连接
2. 训练时间取决于设备性能（M1/M2约需30-60分钟）
3. 模型会保存在`./models`目录下，文件名包含准确率信息
4. 测试时需要指定正确的模型文件路径
5. 确保Flask服务和Spring Boot应用在同一网络环境中

## 参考

- [GTSRB数据集](http://benchmark.ini.rub.de/?section=gtsrb&subsection=dataset)
- [PyTorch文档](https://pytorch.org/docs/)
- [Flask文档](https://flask.palletsprojects.com/)
- [Spring Boot文档](https://spring.io/projects/spring-boot)

## 许可证

MIT License
