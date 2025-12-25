import requests
import json
import sys

BASE_URL = "http://localhost:8000/api"

def test_stop_training(model_id):
    """测试停止训练功能"""
    try:
        print(f"停止训练模型: {model_id}")
        
        # 发送停止训练请求
        response = requests.post(f"{BASE_URL}/models/{model_id}/stop-training")
        
        if response.status_code == 200:
            result = response.json()
            print(f"训练停止成功！")
            print(f"模型状态: {result['status']}")
            print(f"响应: {result}")
            return True
        else:
            print(f"训练停止失败，状态码: {response.status_code}")
            print(f"响应: {response.json()}")
            return False
            
    except Exception as e:
        print(f"发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"用法: python {sys.argv[0]} <model_id>")
        sys.exit(1)
    
    model_id = int(sys.argv[1])
    test_stop_training(model_id)