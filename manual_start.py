import subprocess
import sys
import os

# 构建启动命令
command = [
    sys.executable,  # 使用当前Python解释器
    "-m", "uvicorn",
    "src.backend.main:app",
    "--host", "0.0.0.0",
    "--port", "8000",
    "--reload"
]

print(f"启动命令: {' '.join(command)}")
print("\n正在启动后端服务...")

# 创建一个新的环境，移除所有可能的SDK路径
env = os.environ.copy()

# 清理PATH环境变量
if 'PATH' in env:
    paths = env['PATH'].split(';')
    cleaned_paths = [p for p in paths if 'AIDG' not in p]
    env['PATH'] = ';'.join(cleaned_paths)
    print(f"\n清理后的PATH: {env['PATH']}")

# 启动进程
process = subprocess.Popen(
    command,
    env=env,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# 实时输出stdout和stderr
while True:
    output = process.stdout.readline()
    if output:
        print(output.strip())
    error = process.stderr.readline()
    if error:
        print(f"错误: {error.strip()}")
    if process.poll() is not None:
        break

# 等待进程完成
return_code = process.wait()
print(f"\n进程结束，返回码: {return_code}")