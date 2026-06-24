"""
猫咪图片处理脚本
将图片转换为项目可用的格式
"""

from PIL import Image
import os

def create_placeholder_images():
    """
    创建占位符图片（用于测试）
    实际使用时将被真实图片替换
    """
    
    # 创建 assets 文件夹
    os.makedirs("assets", exist_ok=True)
    
    from PIL import Image, ImageDraw
    
    # 定义每个状态的颜色和描述
    states = {
        "idle": ("待机", (200, 200, 200)),
        "tap": ("被点击", (255, 200, 200)),
        "sleep": ("睡觉", (200, 220, 255)),
        "relax": ("放松", (220, 200, 255)),
        "play": ("开心", (255, 240, 200)),
    }
    
    for state, (label, color) in states.items():
        # 创建简单的占位符图片
        img = Image.new('RGBA', (200, 200), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        
        # 画一个简单的圆形
        draw.ellipse([50, 50, 150, 150], fill=color, outline='black', width=3)
        # 画眼睛
        draw.ellipse([70, 80, 85, 95], fill='black')
        draw.ellipse([115, 80, 130, 95], fill='black')
        # 画嘴巴
        draw.arc([80, 100, 120, 120], 0, 180, fill='black', width=2)
        
        # 保存
        path = f"assets/{state}.png"
        img.save(path)
        print(f"✓ 已创建占位符: {path}")

if __name__ == "__main__":
    print("创建占位符图片...")
    create_placeholder_images()
    print("✓ 完成！")
