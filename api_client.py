"""
大模型 API 调用模块
与硅基流动平台通信，实现对话和屏幕识别
"""

import requests
import json
import threading
from config import (
    SILICONFLOW_API_KEY,
    SILICONFLOW_API_URL,
    TEXT_MODEL,
    VISION_MODEL,
    API_TIMEOUT,
)
from persona_config import SYSTEM_PROMPT, IDLE_CHAT_PROMPT, SCREEN_RECOGNITION_PROMPT


class APIClient:
    """API 客户端"""
    
    def __init__(self):
        self.api_key = SILICONFLOW_API_KEY
        self.api_url = SILICONFLOW_API_URL
        self.text_model = TEXT_MODEL
        self.vision_model = VISION_MODEL
        self.timeout = API_TIMEOUT
        
        # 检查 API Key 是否配置
        if self.api_key == "your_api_key_here":
            print("⚠ 警告: 请在 config.py 中配置 SILICONFLOW_API_KEY")
    
    def _get_headers(self):
        """获取请求头"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
    
    def chat(self, user_message, system_prompt=None, callback=None):
        """
        文本对话接口（异步）
        
        Args:
            user_message: 用户输入的消息
            system_prompt: 系统提示词，默认使用角色人设
            callback: 回调函数，返回结果
        """
        if system_prompt is None:
            system_prompt = SYSTEM_PROMPT
        
        # 在后台线程执行 API 调用
        thread = threading.Thread(
            target=self._chat_sync,
            args=(user_message, system_prompt, callback)
        )
        thread.daemon = True
        thread.start()
    
    def _chat_sync(self, user_message, system_prompt, callback):
        """
        同步的文本对话实现
        """
        try:
            print(f"🔄 调用 API: {user_message[:50]}...")
            
            payload = {
                "model": self.text_model,
                "messages": [
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ],
                "temperature": 0.8,  # 创意度
                "max_tokens": 150,
                "top_p": 0.95,
            }
            
            response = requests.post(
                f"{self.api_url}/chat/completions",
                headers=self._get_headers(),
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                reply = result["choices"][0]["message"]["content"]
                print(f"✓ API 回复: {reply}")
                if callback:
                    callback(reply)
                return reply
            else:
                error_msg = f"API 错误: {response.status_code}"
                print(f"✗ {error_msg}")
                if callback:
                    callback(f"喵~好像出了点问题...")
                return None
                
        except requests.Timeout:
            print("✗ API 请求超时")
            if callback:
                callback("喵~网络有点慢呢...")
        except Exception as e:
            print(f"✗ API 调用异常: {e}")
            if callback:
                callback("喵~小喵有点累了...")
    
    def idle_chat(self, callback=None):
        """
        闲置时的自言自语
        
        Args:
            callback: 回调函数
        """
        prompt = "请生成一句闲置自言自语"
        self.chat(prompt, system_prompt=IDLE_CHAT_PROMPT, callback=callback)
    
    def recognize_screen(self, image_path, callback=None):
        """
        屏幕内容识别（多模态模型）
        
        Args:
            image_path: 截图文件路径
            callback: 回调函数
        """
        thread = threading.Thread(
            target=self._recognize_screen_sync,
            args=(image_path, callback)
        )
        thread.daemon = True
        thread.start()
    
    def _recognize_screen_sync(self, image_path, callback):
        """
        同步的屏幕识别实现
        """
        try:
            print(f"🔄 识别屏幕内容...")
            
            # 读取图片
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            import base64
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            
            payload = {
                "model": self.vision_model,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "image": image_base64,
                            },
                            {
                                "type": "text",
                                "text": SCREEN_RECOGNITION_PROMPT
                            }
                        ]
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 100,
            }
            
            response = requests.post(
                f"{self.api_url}/chat/completions",
                headers=self._get_headers(),
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                reply = result["choices"][0]["message"]["content"]
                print(f"✓ 屏幕识别回复: {reply}")
                if callback:
                    callback(reply)
                return reply
            else:
                print(f"✗ 屏幕识别 API 错误: {response.status_code}")
                if callback:
                    callback("喵~看不太清呢...")
                
        except Exception as e:
            print(f"✗ 屏幕识别异常: {e}")
            if callback:
                callback("喵~小喵的眼睛有点花...")


# 全局 API 客户端实例
api_client = APIClient()


if __name__ == "__main__":
    print("✓ API 客户端加载成功!")
    
    # 测试文本对话
    def test_callback(reply):
        print(f"回调结果: {reply}")
    
    # api_client.chat("你好，请介绍一下自���", callback=test_callback)
    print("✓ 如需测试，请在 config.py 中配置 API Key 后注释上面的测试行")
