# 工业低代码计算机视觉系统 - Linux部署指南

本指南将帮助您在Linux系统上部署工业低代码计算机视觉系统。

## 一、系统要求

### 1.1 硬件要求

- CPU: 4核及以上
- 内存: 8GB及以上
- 存储: 至少20GB可用空间
- GPU: 可选（推荐用于模型训练和实时推理）

### 1.2 软件要求

- Linux发行版: Ubuntu 20.04+/CentOS 7+/Debian 10+
- Python: 3.9+
- Node.js: 16.x+
- npm: 8.x+
- Git: 2.x+

## 二、环境准备

### 2.1 系统更新

#### Ubuntu/Debian
```bash
sudo apt-get update && sudo apt-get upgrade -y
```

#### CentOS/RHEL
```bash
sudo yum update -y
```

### 2.2 安装必要依赖

#### Ubuntu/Debian
```bash
sudo apt-get install -y python3 python3-pip python3-venv git curl gnupg2
```

#### CentOS/RHEL
```bash
sudo yum install -y python3 python3-pip git curl
```

### 2.3 安装Node.js

使用NodeSource安装Node.js 16.x：

```bash
# 添加NodeSource仓库
curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -

# 安装Node.js
```

#### Ubuntu/Debian
```bash
sudo apt-get install -y nodejs
```

#### CentOS/RHEL
```bash
sudo yum install -y nodejs
```

验证安装：
```bash
node -v
npm -v
```

## 三、获取项目代码

### 3.1 克隆仓库

```bash
git clone https://github.com/XSX-SXS/Industrial-Detection-System-Vue-OpenCV-lxh.git
cd Industrial-Detection-System-Vue-OpenCV-lxh
```

### 3.2 创建Python虚拟环境

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
```

#### Ubuntu/Debian/CentOS
```bash
source venv/bin/activate
```

## 四、后端部署

### 4.1 安装Python依赖

```bash
# 升级pip
pip install --upgrade pip

# 安装项目依赖
pip install -r requirements.txt
```

### 4.2 创建必要目录

```bash
mkdir -p uploads data/models
```

### 4.3 数据库初始化

项目默认使用SQLite数据库，会自动创建。如果需要使用其他数据库（如PostgreSQL/MySQL），请参考"高级配置"部分。

### 4.4 测试后端服务

```bash
# 启动后端服务
python -m uvicorn src.backend.main:app --host 0.0.0.0 --port 8000
```

访问 `http://服务器IP:8000/docs` 验证API是否正常工作。按Ctrl+C停止服务。

## 五、前端部署

### 5.1 安装前端依赖

```bash
npm install
```

### 5.2 构建前端项目

```bash
npm run build
```

构建完成后，生成的静态文件将位于`dist`目录。

## 六、生产环境配置

### 6.1 配置systemd服务

创建systemd服务文件，使后端服务能够自动启动和管理：

```bash
sudo nano /etc/systemd/system/industrial-cv.service
```

添加以下内容：

```ini
[Unit]
Description=Industrial Low-Code Computer Vision System
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/Industrial-Detection-System-Vue-OpenCV-lxh
ExecStart=/path/to/Industrial-Detection-System-Vue-OpenCV-lxh/venv/bin/python -m uvicorn src.backend.main:app --host 0.0.0.0 --port 8000
Restart=on-failure
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

替换：
- `your_username` 为您的Linux用户名
- `/path/to/` 为项目的实际路径

### 6.2 启用并启动服务

```bash
sudo systemctl daemon-reload
sudo systemctl enable industrial-cv
sudo systemctl start industrial-cv
```

检查服务状态：
```bash
sudo systemctl status industrial-cv
```

## 七、配置Nginx反向代理

### 7.1 安装Nginx

#### Ubuntu/Debian
```bash
sudo apt-get install -y nginx
```

#### CentOS/RHEL
```bash
sudo yum install -y nginx
```

### 7.2 创建Nginx配置

```bash
sudo nano /etc/nginx/sites-available/industrial-cv
```

添加以下配置：

```nginx
server {
    listen 80;
    server_name your_domain.com;  # 替换为您的域名或服务器IP

    # 前端静态文件
    location / {
        root /path/to/Industrial-Detection-System-Vue-OpenCV-lxh/dist;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # 后端API代理
    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # WebSocket代理（如果需要）
    location /ws {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # 静态资源
    location /static {
        alias /path/to/Industrial-Detection-System-Vue-OpenCV-lxh/public;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # 文件上传下载
    location /uploads {
        alias /path/to/Industrial-Detection-System-Vue-OpenCV-lxh/uploads;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

替换：
- `your_domain.com` 为您的域名或服务器IP
- `/path/to/` 为项目的实际路径

### 7.3 启用Nginx配置

```bash
sudo ln -s /etc/nginx/sites-available/industrial-cv /etc/nginx/sites-enabled/
sudo nginx -t  # 测试配置
```

### 7.4 启动Nginx服务

```bash
sudo systemctl enable nginx
sudo systemctl start nginx
```

## 八、防火墙配置

### 8.1 Ubuntu/Debian (ufw)

```bash
sudo ufw enable
sudo ufw allow 80/tcp  # HTTP
sudo ufw allow 443/tcp  # HTTPS (如果配置了SSL)
sudo ufw status
```

### 8.2 CentOS/RHEL (firewalld)

```bash
sudo systemctl enable firewalld
sudo systemctl start firewalld
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https  # 如果配置了SSL
sudo firewall-cmd --reload
sudo firewall-cmd --list-all
```

## 九、配置SSL（可选）

如果需要HTTPS，可以使用Let's Encrypt配置SSL证书：

```bash
# 安装Certbot
sudo apt-get install certbot python3-certbot-nginx  # Ubuntu/Debian
sudo yum install certbot python3-certbot-nginx  # CentOS/RHEL

# 获取并配置证书
sudo certbot --nginx -d your_domain.com
```

按照提示完成配置，Certbot会自动更新Nginx配置以启用HTTPS。

## 十、启动与验证

1. 确保所有服务都已启动：
   ```bash
   sudo systemctl status industrial-cv nginx
   ```

2. 访问系统：
   - 使用HTTP: `http://your_domain.com`
   - 使用HTTPS: `https://your_domain.com` (如果配置了SSL)

3. 验证功能：
   - 检查实时监控页面
   - 测试图像处理功能
   - 验证模型推理

## 十一、高级配置

### 11.1 切换到PostgreSQL数据库

1. 安装PostgreSQL：
   ```bash
   sudo apt-get install postgresql postgresql-contrib  # Ubuntu/Debian
   sudo yum install postgresql-server postgresql-contrib  # CentOS/RHEL
   ```

2. 创建数据库和用户：
   ```bash
sudo -u postgres psql
CREATE DATABASE industrial_cv;
CREATE USER cv_user WITH PASSWORD 'your_strong_password';
ALTER ROLE cv_user SET client_encoding TO 'utf8';
ALTER ROLE cv_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE cv_user SET timezone TO 'Asia/Shanghai';
GRANT ALL PRIVILEGES ON DATABASE industrial_cv TO cv_user;
\q
   ```

3. 修改数据库配置（`src/backend/models/base.py`）：
   ```python
   engine = create_engine(
       'postgresql://cv_user:your_strong_password@localhost/industrial_cv',
       pool_pre_ping=True,
       pool_size=20,
       max_overflow=20,
       pool_timeout=60,
       pool_recycle=3600
   )
   ```

4. 安装PostgreSQL驱动：
   ```bash
   pip install psycopg2-binary
   ```

### 11.2 配置GPU加速

如果服务器有NVIDIA GPU，可以安装CUDA和cuDNN以加速模型推理：

1. 安装NVIDIA驱动
2. 安装CUDA Toolkit
3. 安装cuDNN
4. 确保PyTorch/TensorFlow使用GPU版本

### 11.3 配置日志

项目默认输出日志到控制台。可以配置将日志输出到文件：

1. 修改`src/backend/main.py`，添加日志配置
2. 配置日志轮转

## 十二、维护与更新

### 12.1 更新代码

```bash
# 拉取最新代码
git pull

# 更新Python依赖
pip install -r requirements.txt

# 更新前端依赖
npm install

# 重新构建前端
npm run build

# 重启服务
sudo systemctl restart industrial-cv nginx
```

### 12.2 监控服务

- 查看后端日志：
  ```bash
  sudo journalctl -u industrial-cv -f
  ```

- 查看Nginx日志：
  ```bash
  sudo tail -f /var/log/nginx/access.log
  sudo tail -f /var/log/nginx/error.log
  ```

### 12.3 备份数据

```bash
# 备份数据库
cp industrial_ocr.db industrial_ocr.db.backup

# 备份模型和数据
cp -r data/models/ data/models_backup/
cp -r uploads/ uploads_backup/
```

## 十三、故障排除

### 13.1 服务无法启动

1. 检查端口是否被占用：
   ```bash
   netstat -tulpn | grep 8000
   ```

2. 查看详细日志：
   ```bash
   sudo journalctl -u industrial-cv --no-pager
   ```

### 13.2 前端无法访问后端API

1. 检查Nginx配置是否正确
2. 确保后端服务正在运行
3. 检查CORS配置（`src/backend/main.py`中的CORSMiddleware）

### 13.3 摄像头无法检测

1. 确保摄像头驱动已安装
2. 检查用户权限（是否属于video组）
3. 查看摄像头服务日志

## 十四、安全建议

1. 使用强密码和HTTPS
2. 限制SSH访问（使用密钥认证，禁止root登录）
3. 定期更新系统和依赖
4. 配置防火墙，只开放必要端口
5. 定期备份数据
6. 监控服务状态和日志

---

部署完成后，您可以在Linux系统上稳定运行工业低代码计算机视觉系统。如果遇到问题，请参考项目文档或提交Issue。
