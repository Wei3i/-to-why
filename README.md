# 小喵咪桌宠 🐱

一个可爱温柔的AI虚拟猫咪桌宠，可以陪伴你工作和生活。

## ✨ 功能特性

### 基础功能
- 🖱️ **点击互动** - 点击桌宠触发各种反应
- 🎨 **丰富表情** - 待机、点击、睡觉等多种状态
- 📊 **数据统计** - 记录点击次数、好感度等信息

### 进阶功能
- 🤖 **AI对话** - 与大模型集成，进行自然对话
- 👀 **屏幕识别** - 识别屏幕内容并作出对应反应（可选）
- 💕 **好感系统** - 通过互动增加好感度
- 🎁 **礼物系统** - 用点击次数兑换礼物
- 💬 **主动闲聊** - 闲置时自动发起话题

## 🚀 快速开始

### 前置要求
- Python 3.8+
- 硅基流动 API Key（[免费获取](https://siliconflow.cn/)）

### 安装步骤

1. **克隆仓库**
```bash
git clone https://github.com/Wei3i/-to-why.git
cd -to-why
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置 API**
编辑 `config.py`，填入你的硅基流动 API Key：
```python
SILICONFLOW_API_KEY = "your_api_key_here"
```

4. **运行程序**
```bash
python main.py
```

## 📁 项目结构

```
├── main.py              # 程序入口 - GUI主体和事件处理
├── config.py            # 配置文件 - API密钥和参数设置
├── api_client.py        # API模块 - 与大模型通信
├── data_manager.py      # 数据模块 - 存档和数据管理
├── persona_config.py    # 人设文件 - 角色性格和对话设定
├── features.py          # 功能模块 - 好感度和礼物系统
├── assets/              # 资源文件夹 - 存放角色图片
│   ├── idle.png        # 待机状态
│   ├── tap.png         # 被点击状态
│   ├── sleep.png       # 睡眠状态
│   ├── eat.png         # 进食状态
│   └── play.png        # 玩耍状态
├── data.json            # 存档文件 - 自动生成
├── requirements.txt     # 依赖列表
└── README.md            # 本文件
```

## 🎨 美术资源

### 如何添加角色图片

1. 准备PNG格式的图片，建议尺寸为 **200x200** 像素
2. 按照以下命名规则放入 `assets/` 文件夹：
   - `idle.png` - 待机状态
   - `tap.png` - 被点击状态
   - `sleep.png` - 睡觉状态
   - `eat.png` - 吃东西状态
   - `play.png` - 玩耍状态

3. 程序启动时会自动加载这些图片

## ⚙️ 配置说明

### config.py 主要参数

```python
# API 配置
SILICONFLOW_API_KEY = "your_api_key_here"  # 硅基流动 API Key
TEXT_MODEL = "deepseek-ai/deepseek-v3"     # 文本模型
VISION_MODEL = "Qwen/Qwen-VL-Plus"         # 视觉模型

# 窗口配置
WINDOW_WIDTH = 200                          # 窗口宽度
WINDOW_HEIGHT = 200                         # 窗口高度
INITIAL_X = 1200                            # 初始X位置
INITIAL_Y = 800                             # 初始Y位置

# 行为配置
IDLE_RANDOM_CHAT_PROBABILITY = 0.3          # 闲聊触发概率
IDLE_RANDOM_CHAT_INTERVAL = 60000           # 闲聊检查间隔（毫秒）
```

### persona_config.py 人设调整

编辑此文件修改角色性格：

```python
PET_NAME = "小喵咪"                         # 宠物名字
PET_PERSONALITY = "可爱、呆萌、温柔"        # 性格标签

# 修改下面的提示词来改变角色的说话风格
PERSONALITY_DESCRIPTION = """..."""
```

## 🔧 常见问题

### Q: 运行时报错 "API 密钥配置错误"
**A:** 检查 `config.py` 中的 `SILICONFLOW_API_KEY` 是否正确设置。从[硅基流动官网](https://siliconflow.cn/)获取你的 API Key。

### Q: 为什么宠物没有说话？
**A:** 
1. 确保已正确配置 API Key
2. 检查网络连接
3. 查看控制台输出中是否有错误信息
4. 硅基流动账户是否有可用额度

### Q: 如何自定义宠物的性格？
**A:** 编辑 `persona_config.py` 文件中的 `PERSONALITY_DESCRIPTION` 部分，修改角色设定和说话风格。

### Q: 如何关闭自动闲聊功能？
**A:** 在 `config.py` 中将 `IDLE_RANDOM_CHAT_PROBABILITY` 改为 `0`。

## 📚 开发参考

### 添加新功能的步骤

1. **如果是新的系统功能** → 编辑 `features.py`
2. **如果涉及 API 调用** → 编辑 `api_client.py` 和 `persona_config.py`
3. **如果涉及 UI 界面** → 编辑 `main.py`
4. **如果需要存档数据** → 编辑 `data_manager.py`

### 多线程架构说明

项目采用多线程设计，避免 API 调用时 UI 卡顿：

```python
# API 调用在后台线程执行
api_client.chat(user_message, callback=update_ui)

# UI 在主线程更新
self.root.after(1000, self.update_display)
```

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

改进方向：
- [ ] 更多宠物表情和动画
- [ ] 声音系统集成
- [ ] 多宠物支持
- [ ] 配置UI化界面
- [ ] 更多 API 平台支持

## 📝 许可证

MIT License - 详见 [LICENSE](LICENSE)

## 🙏 致谢

特别感谢：
- 硅基流动提供的免费 API 额度
- DeepSeek、Qwen 等开源大模型
- 所有贡献者和使用者的支持

---

**Made with ❤️ by Wei3i**

如有任何问题或建议，欢迎提交 Issue！
