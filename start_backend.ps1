# 移除导致授权错误的SDK路径
$env:PATH = ($env:PATH -split ';') -ne 'E:\AIDG_2.2.2_stable_20250307' -join ';'

# 直接使用系统Python安装依赖（如果没有安装）
python -m pip install fastapi uvicorn opencv-python numpy

# 启动后端服务
python -m uvicorn src.backend.main:app --reload