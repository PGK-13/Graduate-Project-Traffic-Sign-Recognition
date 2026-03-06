import onnx
from onnx import version_converter

# 输入和输出路径
INPUT_MODEL_PATH = "./models/tsr_cnn.onnx"
OUTPUT_MODEL_PATH = "./models/tsr_cnn_v9.onnx"

# 加载模型
print(f"加载模型: {INPUT_MODEL_PATH}")
model = onnx.load(INPUT_MODEL_PATH)
print(f"当前IR版本: {model.ir_version}")

# 转换版本
print("转换模型版本到9...")
try:
    converted_model = version_converter.convert_version(model, 9)
    print("转换成功！")
    
    # 保存转换后的模型
    onnx.save(converted_model, OUTPUT_MODEL_PATH)
    print(f"转换后的模型已保存到: {OUTPUT_MODEL_PATH}")
    
    # 验证转换后的模型
    print("验证转换后的模型...")
    onnx.checker.check_model(converted_model)
    print("模型验证通过！")
    
    # 检查转换后的版本
    converted_model_loaded = onnx.load(OUTPUT_MODEL_PATH)
    print(f"转换后的IR版本: {converted_model_loaded.ir_version}")
    
    print("模型版本转换完成！")
    print(f"请使用 {OUTPUT_MODEL_PATH} 作为Spring Boot项目中的模型文件")
    
except Exception as e:
    print(f"转换失败: {e}")
    import traceback
    traceback.print_exc()
