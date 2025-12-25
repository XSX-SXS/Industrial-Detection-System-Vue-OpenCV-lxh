import requests
import json
import sys

BASE_URL = "http://localhost:8000/api"

def test_start_training():
    """测试开始训练功能"""
    try:
        # 首先获取所有模型
        models_response = requests.get(f"{BASE_URL}/models/")
        models = models_response.json()
        
        if not models:
            print("没有找到模型，请先创建一个模型")
            return False
        
        # 选择第一个模型
        model = models[0]
        model_id = model["id"]
        
        print(f"选择模型: {model_id} - {model['name']}")
        
        # 发送训练请求
        response = requests.post(f"{BASE_URL}/models/{model_id}/train")
        
        if response.status_code == 200:
            result = response.json()
            print(f"训练启动成功！")
            print(f"模型状态: {result['status']}")
            print(f"响应: {result}")
            return True
        else:
            print(f"训练启动失败，状态码: {response.status_code}")
            print(f"响应: {response.json()}")
            return False
            
    except Exception as e:
        print(f"发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("测试模型训练功能...")
    success = test_start_training()
    if success:
        print("\n训练测试成功！")
        sys.exit(0)
    else:
        print("\n训练测试失败！")
        sys.exit(1)