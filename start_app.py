import sys
import os

# 打印原始的sys.path
print("Original sys.path:")
for path in sys.path:
    print(f"  - {path}")

# 移除包含'AIDG'的路径
cleaned_path = [path for path in sys.path if 'AIDG' not in path]
sys.path = cleaned_path

# 打印清理后的sys.path
print("\nCleaned sys.path:")
for path in sys.path:
    print(f"  - {path}")

# 移除环境变量中的SDK路径
if 'PATH' in os.environ:
    original_path = os.environ['PATH']
    print("\nOriginal PATH:")
    print(f"  {original_path}")
    
    # 移除包含'AIDG'的路径
    paths = original_path.split(';')
    cleaned_paths = [p for p in paths if 'AIDG' not in p]
    os.environ['PATH'] = ';'.join(cleaned_paths)
    
    print("\nCleaned PATH:")
    print(f"  {os.environ['PATH']}")

# 启动uvicorn服务器
import uvicorn
from src.backend.main import app

if __name__ == "__main__":
    print("\nStarting uvicorn server...")
    uvicorn.run("src.backend.main:app", host="0.0.0.0", port=8000, reload=True)