"""
模型注册表 - 消融实验模型集合
通过 MODEL_REGISTRY 字典统一管理所有模型
"""

from .lightweight_tsrcnn import LightweightTSRCNN
from .lightweight_tsrcnn_no_bn import LightweightTSRCNN_NoBN
from .lightweight_tsrcnn_no_dropout import LightweightTSRCNN_NoDropout
from .lightweight_tsrcnn_leaky_relu import LightweightTSRCNN_LeakyReLU
from .lightweight_tsrcnn_sigmoid import LightweightTSRCNN_Sigmoid

# 模型注册表 - 用于 train.py 和 test.py 动态加载
MODEL_REGISTRY = {
    'LightweightTSRCNN': LightweightTSRCNN,
    'LightweightTSRCNN_NoBN': LightweightTSRCNN_NoBN,
    'LightweightTSRCNN_NoDropout': LightweightTSRCNN_NoDropout,
    'LightweightTSRCNN_LeakyReLU': LightweightTSRCNN_LeakyReLU,
    'LightweightTSRCNN_Sigmoid': LightweightTSRCNN_Sigmoid,
}

__all__ = [
    'LightweightTSRCNN',
    'LightweightTSRCNN_NoBN',
    'LightweightTSRCNN_NoDropout',
    'LightweightTSRCNN_LeakyReLU',
    'LightweightTSRCNN_Sigmoid',
    'MODEL_REGISTRY',
]
