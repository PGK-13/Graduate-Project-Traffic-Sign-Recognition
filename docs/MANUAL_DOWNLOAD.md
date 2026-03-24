# GTSRB数据集手动下载指南

如果自动下载功能失败，您可以按照以下步骤手动下载和整理GTSRB数据集。

## 1. 数据集下载链接

访问GTSRB官方网站下载数据集：

[GTSRB官方下载页面](http://benchmark.ini.rub.de/?section=gtsrb&subsection=dataset#Downloads)

需要下载的文件：

1. **训练集**：
   - 文件名：`GTSRB-Training_fixed.zip`
   - 大小：约263 MB

2. **测试集图像**：
   - 文件名：`GTSRB_Final_Test_Images.zip`
   - 大小：约81 MB

3. **测试集标签**：
   - 文件名：`GTSRB_Final_Test_GT.zip`
   - 大小：约1 MB

## 2. 数据集总大小

- 未压缩：约1.2 GB
- 压缩后：约345 MB

## 3. 文件结构整理

下载完成后，需要将文件整理成以下结构：

```
ts_r_cnn/
├── GTSRB/                     # 数据集根目录
│   ├── Training/              # 训练集目录
│   │   ├── 00000/            # 类别0的图像
│   │   │   ├── GT-00000.csv   # 类别0的标注
│   │   │   └── *.ppm         # 类别0的图像文件
│   │   ├── 00001/            # 类别1的图像
│   │   ├── ...
│   │   └── 00042/            # 类别42的图像
│   ├── Final_Test/            # 测试集目录
│   │   ├── Images/           # 测试集图像
│   │   │   └── *.ppm         # 测试集图像文件
│   └── GT-final_test.csv     # 测试集标注文件
├── model.py
├── dataset.py
├── train.py
└── ...
```

## 4. 手动整理步骤

### 步骤1：创建数据集目录

```bash
mkdir -p /Users/zklee/pyProject/tsr_cnn/GTSRB/Training
mkdir -p /Users/zklee/pyProject/tsr_cnn/GTSRB/Final_Test/Images
```

### 步骤2：解压训练集

将`GTSRB-Training_fixed.zip`解压到`GTSRB/Training`目录下。
解压后，每个类别会自动生成一个形如`00000`的文件夹，包含该类别的图像和GT-*.csv标注文件。

### 步骤3：解压测试集图像

将`GTSRB_Final_Test_Images.zip`解压，然后将其中的图像文件移动到`GTSRB/Final_Test/Images`目录下。

### 步骤4：解压测试集标签

将`GTSRB_Final_Test_GT.zip`解压，得到`GT-final_test.csv`文件，将其移动到`GTSRB/`目录下。

### 步骤5：验证文件结构

确保文件结构与上述一致，特别是：
- `GTSRB/Training/`目录下有43个子目录（00000到00042）
- `GTSRB/Final_Test/Images/`目录下有测试图像
- `GTSRB/GT-final_test.csv`文件存在

## 5. 验证数据集

完成整理后，可以运行以下命令验证数据集加载是否成功：

```bash
python -c "
from dataset import GTSRB, get_transforms
import os

# 测试数据集加载
dataset_path = './GTSRB'
if os.path.exists(dataset_path):
    train_transforms, test_transforms = get_transforms()
    train_dataset = GTSRB(dataset_path, train=True, transform=train_transforms)
    test_dataset = GTSRB(dataset_path, train=False, transform=test_transforms)
    print(f'训练集大小: {len(train_dataset)}')
    print(f'测试集大小: {len(test_dataset)}')
    if len(train_dataset) > 0 and len(test_dataset) > 0:
        print('✅ 数据集加载成功！')
    else:
        print('❌ 数据集大小异常！')
else:
    print('❌ 数据集目录不存在！')
"
```

## 6. 开始使用

数据集准备完成后，即可开始训练和测试：

```bash
# 训练模型
python main.py --train --dataset_path ./GTSRB

# 测试模型
python main.py --test --dataset_path ./GTSRB --model_path ./models/best_model.pth
```

## 7. 常见问题

### 问题1：图像格式错误
解决：确保所有图像都是PPM格式，且文件路径正确。

### 问题2：标注文件格式错误
解决：检查GT-*.csv文件是否使用分号分隔符，且包含正确的列。

### 问题3：类别数量错误
解决：确保Training目录下有43个子目录（00000-00042）。

如果遇到其他问题，请检查文件结构是否与上述要求一致。
