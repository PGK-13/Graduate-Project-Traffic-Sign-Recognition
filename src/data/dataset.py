import os
import csv
import torch
from torch.utils.data import Dataset
from torchvision import transforms
from PIL import Image
import numpy as np

class GTSRB(Dataset):
    def __init__(self, root_dir, train=True, transform=None):
        self.root_dir = root_dir
        self.train = train
        self.transform = transform
        self.images = []
        self.labels = []
        
        if self.train:
            # 训练集：每个类别一个文件夹
            self._load_train_data()
        else:
            # 测试集：使用GT-final_test.csv文件
            self._load_test_data()
    
    def _load_train_data(self):
        # 读取训练集标注文件
        gt_file = os.path.join(self.root_dir, 'Train.csv')
        with open(gt_file, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # 跳过表头
            for row in reader:
                img_path = os.path.join(self.root_dir, row[7])  # row[7] 是 Path 列
                label = int(row[6])  # row[6] 是 ClassId 列
                self.images.append(img_path)
                self.labels.append(label)
    
    def _load_test_data(self):
        # 读取测试集标注文件
        gt_file = os.path.join(self.root_dir, 'Test.csv')
        with open(gt_file, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # 跳过表头
            for row in reader:
                img_path = os.path.join(self.root_dir, row[7])  # row[7] 是 Path 列
                label = int(row[6])  # row[6] 是 ClassId 列
                self.images.append(img_path)
                self.labels.append(label)
    
    def __len__(self):
        return len(self.images)
    
    def __getitem__(self, idx):
        # 加载图像
        img_path = self.images[idx]
        image = Image.open(img_path).convert('RGB')
        label = self.labels[idx]
        
        # 应用变换
        if self.transform:
            image = self.transform(image)
        
        return image, label

# 数据预处理函数
def get_transforms():
    train_transforms = transforms.Compose([
        transforms.Resize((32, 32)),
        transforms.RandomRotation(15),
        transforms.RandomAffine(0, translate=(0.1, 0.1)),
        transforms.ColorJitter(brightness=0.2, contrast=0.2),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    test_transforms = transforms.Compose([
        transforms.Resize((32, 32)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    return train_transforms, test_transforms

# 测试数据集加载
if __name__ == "__main__":
    # 使用用户的archive目录
    dataset_path = "/Users/zklee/pyProject/tsr_cnn/archive"
    
    train_transforms, test_transforms = get_transforms()
    
    try:
        train_dataset = GTSRB(dataset_path, train=True, transform=train_transforms)
        test_dataset = GTSRB(dataset_path, train=False, transform=test_transforms)
        
        print(f"训练集大小: {len(train_dataset)}")
        print(f"测试集大小: {len(test_dataset)}")
        
        # 查看一个样本
        if len(train_dataset) > 0:
            img, label = train_dataset[0]
            print(f"样本图像形状: {img.shape}")
            print(f"样本标签: {label}")
            print("数据集加载成功！")
    except Exception as e:
        print(f"数据集加载失败: {e}")
        print("请确保数据集路径正确，并且数据集已经解压完成。")
        import traceback
        traceback.print_exc()
