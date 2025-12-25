import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath('.'))

print('Python路径:', sys.executable)
print('Python版本:', sys.version)

try:
    # 导入后端应用
    from src.backend.main import app
    print('后端应用导入成功')
    
    # 测试一些核心模块
    from src.backend.services.model import ModelService
    from src.backend.models.base import SessionLocal
    
    db = SessionLocal()
    model_service = ModelService(db)
    print('ModelService实例化成功')
    
    # 测试PyTorch和CUDA
    import torch
    print('PyTorch版本:', torch.__version__)
    print('CUDA可用:', torch.cuda.is_available())
    print('CUDA设备名称:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else '无CUDA设备')
    
    print('所有测试通过！后端服务应该可以正常运行。')
    
except Exception as e:
    print('测试失败:', str(e))
    import traceback
    traceback.print_exc()
finally:
    if 'db' in locals():
        db.close()