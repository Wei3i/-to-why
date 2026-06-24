# 🐱 图片集成指南

## 📋 图片状态映射

你提供的5张猫咪图片已按以下方式映射到项目中：

| 文件名 | 状态 | 说明 | 你的图片 |
|--------|------|------|---------|
| `idle.png` | 待机 | 正常闲置状态 | 图5（呆萌表情） |
| `tap.png` | 被点击 | 被戳到的反应 | 图6（伤心表情） |
| `sleep.png` | 睡觉 | 睡眠状态 | 图7（睡觉状态） |
| `relax.png` | 放松 | 休息/放松状态 | 图8（侧躺放松） |
| `play.png` | 开心 | 玩耍/开心状态 | 图9（开心竖尾巴） |

## 📂 项目结构

```
-to-why/
├── assets/                  # 图片文件夹
│   ├── idle.png            # 待机
│   ├── tap.png             # 被点击
│   ├── sleep.png           # 睡觉
│   ├── relax.png           # 放松
│   └── play.png            # 开心
├── main.py
├── config.py
└── ... (其他文件)
```

## 🖼️ 添加你的图片到项目

### 方式1️⃣：手动添加（推荐用于测试）

1. **在项目根目录创建 `assets` 文件夹**
   ```bash
   mkdir assets
   ```

2. **将你的5张图片按以下名称放入 `assets/` 文件夹**
   - `idle.png` ← 图5（呆萌表情）
   - `tap.png` ← 图6（伤心表情）
   - `sleep.png` ← 图7（睡觉状态）
   - `relax.png` ← 图8（侧躺放松）
   - `play.png` ← 图9（开心竖尾巴）

3. **确保图片是 PNG 格式**（推荐尺寸：200x200 像素）

4. **运行程序**
   ```bash
   python main.py
   ```

### 方式2️⃣：使用 GitHub 上传

1. 打开你的仓库：https://github.com/Wei3i/-to-why
2. 点击 `Add file` → `Upload files`
3. 拖入5张图片
4. 上传到 `assets/` 文件夹

## 🎨 图片格式要求

- **格式**：PNG（支持透明背景）
- **推荐尺寸**：200x200 像素
- **文件大小**：< 100KB 每张
- **命名**：务必使用上述精确文件名

## ⚙️ 程序如何加载图片

程序在 `main.py` 中的 `load_images()` 函数会自动：

1. ✅ 检查 `assets/` 文件夹是否存在
2. ✅ 加载 5 个指定状态的 PNG 图片
3. ✅ 如果文件不存在，使用占位符（灰色圆形）
4. ✅ 根据宠物状态切换显示对应图片

```python
# 自动加载逻辑（在 main.py 中）
for state in ["idle", "tap", "sleep", "relax", "play"]:
    path = f"assets/{state}.png"
    if os.path.exists(path):
        img = Image.open(path).resize((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.images[state] = ImageTk.PhotoImage(img)
```

## 🧪 测试步骤

1. **准备图片**
   ```
   assets/
   ├── idle.png
   ├── tap.png
   ├── sleep.png
   ├── relax.png
   └── play.png
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **运行程序**
   ```bash
   python main.py
   ```

4. **测试互动**
   - 点击宠物窗口 → 应该显示 `tap.png`
   - 右键菜单选择功能 → 触发不同状态

## 📝 常见问题

### Q: 图片没有显示？
**A:** 检查以下内容：
1. ✅ 图片是否在 `assets/` 文件夹中
2. ✅ 文件名是否完全匹配（区分大小写）
3. ✅ 图片格式是否为 PNG
4. ✅ 查看控制台输出是否有错误信息

### Q: 图片显示不清晰？
**A:** 
1. 确保原图尺寸 >= 200x200 像素
2. 如果太小，会被拉伸失真
3. 使用高质量的 PNG 图片

### Q: 可以使用其他格式的图片吗？
**A:** 
- 支持格式：PNG、JPG、GIF、BMP
- 推荐：PNG（支持透明背景）
- 不支持：WebP、SVG（需要先转换）

## 🔄 动画状态流程

```
待机 (idle)
  ↓ [点击]
被点击 (tap) → 1秒后 → 返回待机
  
主动事件触发
  ↓
开心 (play) / 睡觉 (sleep) / 放松 (relax)
  ↓
自动返回待机
```

## 📦 后续优化建议

1. **添加更多表情**
   - 嗷呜（生气）
   - 吃东西（进食）
   - 摔倒（失败）

2. **动画帧**
   - 同一状态多张图片实现帧动画
   - 例如：`idle_1.png`, `idle_2.png`, `idle_3.png`

3. **背景去除**
   - 为所有图片统一使用透明背景
   - 提升视觉效果

## ✅ 完成检查清单

- [ ] 已创建 `assets/` 文件夹
- [ ] 已放入 5 张 PNG 图片
- [ ] 图片名称完全匹配
- [ ] 已安装 Pillow 依赖
- [ ] 已运行 `python main.py`
- [ ] 宠物能正常显示和互动

---

**准备好了？开始体验你的小喵咪桌宠吧！** 🐱✨
