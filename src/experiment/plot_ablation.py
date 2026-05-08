"""
消融实验绘图脚本
读取 train.py 保存的 history.json，生成对比图
"""

import os
import json
import matplotlib.pyplot as plt
from matplotlib import font_manager

# 中文字体设置
plt.rcParams['axes.unicode_minus'] = False
font_path = "/System/Library/Fonts/PingFang.ttc"
cn_font = font_manager.FontProperties(fname=font_path)

# 实验结果目录
MODELS_DIR = "./models"


def load_history(model_name):
    """加载训练历史数据"""
    history_path = os.path.join(MODELS_DIR, f"{model_name}_history.json")
    if os.path.exists(history_path):
        with open(history_path, 'r') as f:
            return json.load(f)
    return None


def plot_ablation_study():
    """绘制消融实验对比图"""
    # 需要对比的模型
    models = {
        'LightweightTSRCNN': 'LightweightTSRCNN (完整)',
        'LightweightTSRCNN_NoBN': 'LightweightTSRCNN (无BN)',
    }

    results = {}
    for model_name, display_name in models.items():
        history = load_history(model_name)
        if history:
            results[display_name] = history
            print(f"已加载: {model_name}")

    if not results:
        print("未找到训练历史数据！请先运行训练脚本。")
        return

    # 创建图表
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    linestyles = ['-', '--', '-.', ':']

    # 子图1: Loss 曲线
    ax1 = axes[0]
    for i, (name, history) in enumerate(results.items()):
        epochs = range(1, len(history['train_loss']) + 1)
        ax1.plot(epochs, history['train_loss'],
                color=colors[i % len(colors)], linestyle='-',
                label=f'{name} - 训练', linewidth=2)
        ax1.plot(epochs, history['val_loss'],
                color=colors[i % len(colors)], linestyle='--',
                label=f'{name} - 验证', linewidth=2, alpha=0.7)

    ax1.set_xlabel('Epoch', fontsize=12)
    ax1.set_ylabel('Loss', fontsize=12)
    ax1.set_title('BN消融实验: Loss对比', fontsize=14, fontweight='bold')
    ax1.legend(loc='upper right', fontsize=9)
    ax1.grid(True, alpha=0.3)

    # 子图2: Accuracy 曲线
    ax2 = axes[1]
    for i, (name, history) in enumerate(results.items()):
        epochs = range(1, len(history['train_acc']) + 1)
        ax2.plot(epochs, history['train_acc'],
                color=colors[i % len(colors)], linestyle='-',
                label=f'{name} - 训练', linewidth=2)
        ax2.plot(epochs, history['val_acc'],
                color=colors[i % len(colors)], linestyle='--',
                label=f'{name} - 验证', linewidth=2, alpha=0.7)

    ax2.set_xlabel('Epoch', fontsize=12)
    ax2.set_ylabel('Accuracy (%)', fontsize=12)
    ax2.set_title('BN消融实验: 准确率对比', fontsize=14, fontweight='bold')
    ax2.legend(loc='lower right', fontsize=9)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(MODELS_DIR, 'ablation_bn.png'), dpi=150, bbox_inches='tight')
    print(f"图表已保存到: {MODELS_DIR}/ablation_bn.png")
    plt.show()


def plot_all_ablation():
    """绘制所有消融实验的综合对比图"""
    models_to_plot = [
        'LightweightTSRCNN',
        'LightweightTSRCNN_NoBN',
        'LightweightTSRCNN_NoDropout',
        'LightweightTSRCNN_LeakyReLU',
        'LightweightTSRCNN_Sigmoid',
    ]

    display_names = {
        'LightweightTSRCNN': '完整模型',
        'LightweightTSRCNN_NoBN': '无BN',
        'LightweightTSRCNN_NoDropout': '无Dropout',
        'LightweightTSRCNN_LeakyReLU': 'LeakyReLU',
        'LightweightTSRCNN_Sigmoid': 'Sigmoid',
    }

    results = {}
    for model_name in models_to_plot:
        history = load_history(model_name)
        if history:
            results[model_name] = history

    if not results:
        print("未找到足够的训练历史数据！")
        return

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    colors = ['#2ecc71', '#e74c3c', '#3498db', '#f39c12', '#9b59b6']

    # 子图1: 验证准确率对比
    ax1 = axes[0]
    for i, (model_name, history) in enumerate(results.items()):
        epochs = range(1, len(history['val_acc']) + 1)
        ax1.plot(epochs, history['val_acc'],
                color=colors[i % len(colors)],
                label=display_names.get(model_name, model_name),
                linewidth=2)

    ax1.set_xlabel('Epoch', fontsize=12)
    ax1.set_ylabel('验证准确率 (%)', fontsize=12)
    ax1.set_title('各模型验证准确率对比', fontsize=14, fontweight='bold')
    ax1.legend(loc='lower right', fontsize=10)
    ax1.grid(True, alpha=0.3)

    # 子图2: 最终准确率柱状图
    ax2 = axes[1]
    model_names = [display_names.get(m, m) for m in results.keys()]
    final_accs = [max(h['val_acc']) for h in results.values()]
    bars = ax2.bar(range(len(model_names)), final_accs, color=colors[:len(model_names)])

    for bar, acc in zip(bars, final_accs):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                f'{acc:.2f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax2.set_xlabel('模型', fontsize=12)
    ax2.set_ylabel('最佳验证准确率 (%)', fontsize=12)
    ax2.set_title('各模型最佳性能对比', fontsize=14, fontweight='bold')
    ax2.set_xticks(range(len(model_names)))
    ax2.set_xticklabels(model_names, rotation=15, ha='right', fontsize=10)
    ax2.set_ylim(0, 105)
    ax2.grid(True, axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(MODELS_DIR, 'ablation_all.png'), dpi=150, bbox_inches='tight')
    print(f"综合对比图已保存到: {MODELS_DIR}/ablation_all.png")
    plt.show()


def print_summary():
    """打印各模型最终结果汇总"""
    models_to_check = [
        'LightweightTSRCNN',
        'LightweightTSRCNN_NoBN',
        'LightweightTSRCNN_NoDropout',
        'LightweightTSRCNN_LeakyReLU',
        'LightweightTSRCNN_Sigmoid',
    ]

    print("\n" + "="*60)
    print("消融实验结果汇总")
    print("="*60)

    for model_name in models_to_check:
        history = load_history(model_name)
        if history:
            best_acc = max(history['val_acc'])
            final_acc = history['val_acc'][-1]
            best_loss = min(history['val_loss'])
            print(f"{model_name}:")
            print(f"  最佳验证准确率: {best_acc:.2f}%")
            print(f"  最终验证准确率: {final_acc:.2f}%")
            print(f"  最佳验证损失: {best_loss:.4f}")
            print()
        else:
            print(f"{model_name}: 未找到训练数据")
            print()


if __name__ == "__main__":
    print("消融实验绘图工具")
    print("="*40)

    # 打印结果汇总
    print_summary()

    # 绘制综合对比图
    print("\n正在生成对比图...")
    plot_all_ablation()
