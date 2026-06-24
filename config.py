# API 配置文件
# 硅基流动平台配置

# ==================== 大模型 API 配置 ====================
# 硅基流动官方文档: https://docs.siliconflow.cn/

# API 密钥 (从硅基流动获取)
SILICONFLOW_API_KEY = "sk-dpfqdhzzclabhycetrjvutmygdvfrluhdqbrrriskachojrz"

# 接口地址
SILICONFLOW_API_URL = "https://api.siliconflow.cn/v1"

# 使用的文本对话模型
TEXT_MODEL = "deepseek-ai/deepseek-v3"  # 用于对话和碎碎念
# 可选: "meta-llama/Meta-Llama-3.1-405B-Instruct" 等

# 使用的多模态模型（屏幕识别）
VISION_MODEL = "Qwen/Qwen-VL-Plus"  # 用于屏幕内容识别

# ==================== 桌宠基础配置 ====================
WINDOW_WIDTH = 200
WINDOW_HEIGHT = 200
WINDOW_ALPHA = 0.95  # 窗口透明度 (0-1)

# 初始窗口位置 (屏幕右下角)
INITIAL_X = 1200
INITIAL_Y = 800

# ==================== 性能配置 ====================
API_TIMEOUT = 30  # API 请求超时时间（秒）
IDLE_ANIMATION_INTERVAL = 200  # 待机动画更新间隔（毫秒）
IDLE_RANDOM_CHAT_INTERVAL = 60000  # 闲置闲聊检查间隔（毫秒）
IDLE_RANDOM_CHAT_PROBABILITY = 0.3  # 闲置闲聊触发概率 (0-1)

# ==================== 数据文件 ====================
DATA_FILE = "data.json"

# 初始数据结构
DEFAULT_DATA = {
    "total_clicks": 0,
    "current_clicks": 0,
    "affection": 50,  # 初始好感度
    "pet_name": "小喵咪",
    "creation_date": None,
}
