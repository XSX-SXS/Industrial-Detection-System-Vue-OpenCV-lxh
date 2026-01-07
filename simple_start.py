# 这是一个简单的启动脚本，直接使用uvicorn启动应用
# 尝试绕过系统中AIDG SDK的影响

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "src.backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )