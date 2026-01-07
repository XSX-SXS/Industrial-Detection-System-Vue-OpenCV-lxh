import requests
import json
import sys

BASE_URL = "http://localhost:8000/api"

def test_create_model():
    """测试创建新模型"""
    try:
        # 创建模型请求
        model_data = {
            "name": "测试模型",
            "architecture": "yolo_v8",
            "dataset_id": 1,
            "parameters": {
                "epochs": 10,
                "batch_size": 8,
                "img_size": 640
            }
        }
        
        response = requests.post(f"{BASE_URL}/models/", json=model_data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"模型创建成功！")
            print(f"模型ID: {result['id']}")
            print(f"响应: {result}")
            return result['id']
        else:
            print(f"模型创建失败，状态码: {response.status_code}")
            print(f"响应: {response.json()}")
            return None
            
    except Exception as e:
        print(f"发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def test_start_training(model_id):
    """测试开始训练功能"""
    try:
        print(f"开始训练模型: {model_id}")
        
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
    print("测试创建新模型并开始训练...")
    
    # 创建新模型
    model_id = test_create_model()
    
    if model_id:
        # 开始训练
        success = test_start_training(model_id)
        
        if success:
            print("\n训练测试成功！")
            sys.exit(0)
        else:
            print("\n训练测试失败！")
            sys.exit(1)
    else:
        print("\n模型创建失败！")
        sys.exit(1)