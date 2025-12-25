# 移除导致授权错误的SDK路径
$env:PATH = ($env:PATH -split ';') | Where-Object { $_ -ne 'E:\AIDG_2.2.2_stable_20250307' } | Join-String -Separator ';'

# 启动后端服务
python -m uvicorn src.backend.main:app --reload