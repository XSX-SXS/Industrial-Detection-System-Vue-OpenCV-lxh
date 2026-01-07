# 工业低代码计算机视觉系统 - Colab配置指南

本指南将帮助您在Google Colab上配置并运行工业低代码计算机视觉系统。

## 一、环境准备

### 1.1 创建新的Colab笔记本

1. 访问 [Google Colab](https://colab.research.google.com/)
2. 点击"新建笔记本" → "Python 3"
3. 在菜单栏中选择"运行时" → "更改运行时类型"
4. 选择硬件加速器：**GPU** (建议使用，以加速模型推理)
5. 点击"保存"

### 1.2 克隆项目代码

在Colab单元格中运行以下命令：

```python
# 克隆项目仓库
!git clone https://github.com/XSX-SXS/Industrial-Detection-System-Vue-OpenCV-lxh.git

# 进入项目目录
%cd Industrial-Detection-System-Vue-OpenCV-lxh
```

## 二、后端配置

### 2.1 安装Python依赖

```python
# 升级pip
!pip install --upgrade pip

# 安装项目依赖
!pip install -r requirements.txt
```

### 2.2 安装额外依赖

```python
# 安装ngrok用于端口映射
!pip install pyngrok

# 安装Node.js和npm (用于前端)
!apt-get update && apt-get install -y nodejs npm
```

### 2.3 配置ngrok

需要一个ngrok账号和认证令牌。注册地址：[ngrok.com](https://ngrok.com/)

```python
from pyngrok import ngrok

# 替换为您的ngrok认证令牌
!ngrok authtoken YOUR_NGROK_AUTH_TOKEN
```

## 三、前端配置

### 3.1 安装Node.js依赖

```python
# 安装前端依赖
!npm install
```

### 3.2 构建前端项目

```python
# 构建前端项目
!npm run build
```

## 四、启动服务

### 4.1 启动后端服务

在一个新的单元格中运行：

```python
import subprocess
import threading
import time
from pyngrok import ngrok

# 创建uploads和dist目录（如果不存在）
!mkdir -p uploads dist

# 启动后端服务
backend_process = subprocess.Popen([
    'python', '-m', 'uvicorn', 'src.backend.main:app', 
    '--host', '0.0.0.0', '--port', '8000'
])

# 等待服务启动
print("正在启动后端服务...")
time.sleep(5)

# 配置ngrok隧道
http_tunnel = ngrok.connect(addr="8000", proto="http")
print(f"后端API地址: {http_tunnel.public_url}")
print(f"前端访问地址: {http_tunnel.public_url}")
```

### 4.2 检查服务状态

```python
# 查看服务是否运行
!ps aux | grep uvicorn
```

## 五、使用说明

### 5.1 访问前端界面

1. 复制上一步输出的"前端访问地址"
2. 在浏览器中打开该地址
3. 您将看到工业低代码计算机视觉系统的登录界面

### 5.2 功能演示

#### 5.2.1 实时视频流

- 在"实时监控"页面，可以查看和管理视频流
- Colab环境中可能无法访问本地摄像头，您可以：
  - 使用网络摄像头URL（如RTSP流）
  - 上传视频文件进行处理

#### 5.2.2 图像处理

- 在"图像处理"页面，可以：
  - 进行单步图像处理操作
  - 创建图像处理流水线
  - 测试和预览处理效果

#### 5.2.3 模型训练与推理

- 在"模型"页面，可以：
  - 上传数据集
  - 训练新模型
  - 调用已训练模型进行推理

#### 5.2.4 数据标注

- 在"标注"页面，可以：
  - 标注图像数据
  - 生成训练数据
  - 管理数据集

## 六、注意事项

### 6.1 资源限制

- Colab会话有时间限制（通常为12小时）
- 长时间不活动会导致会话断开
- 建议定期保存工作进度

### 6.2 摄像头访问

- Colab环境无法直接访问本地摄像头
- 可以通过以下方式替代：
  - 上传视频文件
  - 使用网络摄像头流（如IP摄像头的RTSP/HTTP URL）

### 6.3 数据持久化

- Colab的临时存储会在会话结束后清除
- 建议将重要数据保存到Google Drive：

```python
# 挂载Google Drive
from google.colab import drive
drive.mount('/content/drive')

# 复制数据到Drive
!cp -r data/ /content/drive/MyDrive/Industrial-CV-Data/
```

### 6.4 GPU使用

- 确保已选择GPU作为硬件加速器
- 可以通过以下命令检查GPU是否可用：

```python
import torch
print(f"CUDA可用: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU型号: {torch.cuda.get_device_name(0)}")
```

## 七、停止服务

```python
# 停止后端服务
backend_process.terminate()

# 关闭ngrok隧道
ngrok.kill()

print("服务已停止")
```

## 八、常见问题

### 8.1 端口冲突

如果遇到端口冲突，可以修改后端端口：

```python
# 更改端口为8001
backend_process = subprocess.Popen([
    'python', '-m', 'uvicorn', 'src.backend.main:app', 
    '--host', '0.0.0.0', '--port', '8001'
])

# 相应地更新ngrok隧道
http_tunnel = ngrok.connect(addr="8001", proto="http")
```

### 8.2 依赖安装失败

尝试单独安装失败的依赖：

```python
# 例如，单独安装opencv-python
!pip install --upgrade opencv-python
```

### 8.3 前端构建错误

如果npm构建失败，尝试清理缓存并重新安装：

```python
!npm cache clean --force
!npm install
!npm run build
```

## 九、项目结构说明

```
├── src/                # 源代码目录
│   ├── backend/        # 后端代码 (FastAPI)
│   │   ├── main.py     # 后端入口文件
│   │   ├── routers/    # API路由
│   │   ├── services/   # 业务逻辑
│   │   └── models/     # 数据库模型
│   ├── components/     # Vue组件
│   ├── views/          # Vue页面
│   └── main.js         # 前端入口文件
├── public/             # 静态资源
├── data/               # 数据目录
├── models/             # 模型文件
├── requirements.txt    # Python依赖
└── package.json        # Node.js依赖
```

## 十、技术支持

如果遇到问题，可以参考以下资源：

- 项目文档：查看README.md
- 原始文献：https://mp.weixin.qq.com/s/SHFpFBWoQCOPrXFHkTYOMg
- GitHub Issues：在项目仓库中提交问题

---

祝您在Colab上愉快地使用工业低代码计算机视觉系统！
