import os
import sys
import requests
import zipfile
import shutil
import argparse
from src.train.train import train_model
from src.test.test import test_model

# GTSRB数据集下载链接
download_links = {
    'train': 'https://sid.erda.dk/public/archives/daaeac0d7ce1152aea9b61d9f1e19370/GTSRB-Training_fixed.zip',
    'test': 'https://sid.erda.dk/public/archives/daaeac0d7ce1152aea9b61d9f1e19370/GTSRB_Final_Test_Images.zip',
    'test_labels': 'https://sid.erda.dk/public/archives/daaeac0d7ce1152aea9b61d9f1e19370/GTSRB_Final_Test_GT.zip'
}

def download_file(url, save_path):
    """下载文件"""
    print(f"正在下载: {url}")
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    with open(save_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    print(f"下载完成: {save_path}")

def unzip_file(zip_path, extract_path):
    """解压文件"""
    print(f"正在解压: {zip_path}")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    print(f"解压完成: {extract_path}")

def download_gtsrb_dataset(dataset_path):
    """下载并解压GTSRB数据集"""
    if os.path.exists(dataset_path):
        print(f"数据集已存在于: {dataset_path}")
        return True
    
    # 创建临时目录
    temp_dir = os.path.join(dataset_path, 'temp')
    os.makedirs(temp_dir, exist_ok=True)
    
    try:
        # 下载所有文件
        for key, url in download_links.items():
            filename = os.path.basename(url)
            zip_path = os.path.join(temp_dir, filename)
            download_file(url, zip_path)
            
            # 解压
            unzip_file(zip_path, dataset_path)
        
        # 整理文件结构
        # 训练集应该已经是正确的结构
        
        # 测试集需要将Final_Test_Images中的图像移动到Final_Test/Images
        test_images_src = os.path.join(dataset_path, 'GTSRB', 'Final_Test', 'Images')
        test_images_dst = os.path.join(dataset_path, 'Final_Test', 'Images')
        if os.path.exists(test_images_src):
            os.makedirs(test_images_dst, exist_ok=True)
            for file in os.listdir(test_images_src):
                shutil.move(os.path.join(test_images_src, file), os.path.join(test_images_dst, file))
        
        # 移动测试标签文件
        test_labels_src = os.path.join(dataset_path, 'GT-final_test.csv')
        test_labels_dst = os.path.join(dataset_path, 'GT-final_test.csv')
        if os.path.exists(os.path.join(dataset_path, 'GTSRB', 'GT-final_test.csv')):
            shutil.move(os.path.join(dataset_path, 'GTSRB', 'GT-final_test.csv'), test_labels_dst)
        
        # 清理临时文件
        shutil.rmtree(temp_dir)
        
        # 检查文件结构
        if os.path.exists(os.path.join(dataset_path, 'Training')) and os.path.exists(os.path.join(dataset_path, 'Final_Test')):
            print(f"数据集下载并整理完成: {dataset_path}")
            return True
        else:
            print("数据集结构不正确")
            return False
            
    except Exception as e:
        print(f"下载数据集时出错: {e}")
        # 清理
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        return False

def main():
    parser = argparse.ArgumentParser(description='GTSRB交通标志分类')
    parser.add_argument('--download', action='store_true', help='下载GTSRB数据集')
    parser.add_argument('--train', action='store_true', help='训练模型')
    parser.add_argument('--test', action='store_true', help='测试模型')
    parser.add_argument('--dataset_path', type=str, default='/Users/zklee/pyProject/tsr_cnn/archive', help='数据集路径')
    parser.add_argument('--model_path', type=str, default='./models/best_model.pth', help='模型路径')
    parser.add_argument('--epochs', type=int, default=50, help='训练轮次')
    parser.add_argument('--batch_size', type=int, default=64, help='批量大小')
    parser.add_argument('--lr', type=float, default=0.001, help='学习率')
    
    args = parser.parse_args()
    
    # 创建模型保存目录
    os.makedirs('./models', exist_ok=True)
    
    # 下载数据集
    if args.download:
        success = download_gtsrb_dataset(args.dataset_path)
        if not success:
            print("下载数据集失败，请手动下载。")
            return
    
    # 训练模型
    if args.train:
        print("开始训练模型...")
        train_model(
            dataset_path=args.dataset_path,
            epochs=args.epochs,
            batch_size=args.batch_size,
            learning_rate=args.lr
        )
        print("训练完成！")
    
    # 测试模型
    if args.test:
        print("开始测试模型...")
        if not os.path.exists(args.model_path):
            print(f"模型文件不存在: {args.model_path}")
            print("请先训练模型或指定正确的模型路径。")
            return
        
        test_model(args.model_path, args.dataset_path, batch_size=args.batch_size, visualize=True)
        print("测试完成！")
    
    # 如果没有指定任何操作，显示帮助信息
    if not any([args.download, args.train, args.test]):
        parser.print_help()

if __name__ == "__main__":
    main()
