"""
桌宠主程序
整合所有模块，实现完整的桌宠功能
"""

import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import threading
import time
import random
import os
from datetime import datetime

from config import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    WINDOW_ALPHA,
    INITIAL_X,
    INITIAL_Y,
    IDLE_ANIMATION_INTERVAL,
    IDLE_RANDOM_CHAT_INTERVAL,
    IDLE_RANDOM_CHAT_PROBABILITY,
)
from data_manager import data_manager
from api_client import api_client
from features import AffectionSystem, GiftSystem, StatsDisplay
from persona_config import INTERACTION_RESPONSES, CATCHPHRASES, PET_NAME


class DesktopPet:
    """桌面宠物主类"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("小喵咪")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{INITIAL_X}+{INITIAL_Y}")
        self.root.attributes('-topmost', True)  # 始终在最前
        self.root.attributes('-alpha', WINDOW_ALPHA)  # 透明度
        self.root.attributes('-toolwindow', True)  # 工具栏风格
        
        # 移除窗口装饰
        self.root.overrideredirect(False)
        
        # 状态变量
        self.is_dragging = False
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.current_state = "idle"  # idle, tap, sleep, eat, play
        self.is_talking = False
        self.idle_animation_state = 0
        self.idle_animation_max = 3
        
        # 创建主容器
        self.canvas = tk.Canvas(
            self.root,
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT,
            bg="white",
            highlightthickness=0,
            cursor="hand2"
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # 绑定事件
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<Button-3>", self.on_right_click)  # 右键菜单
        
        # 加载图片（暂时使用纯色方块作为占位符）
        self.load_images()
        
        # 显示初始状态
        self.update_display()
        
        # 启动动画循环
        self.animation_loop()
        
        # 启动闲置聊天检查
        self.idle_chat_timer()
        
        print("✓ 桌宠初始化完成!")
    
    def load_images(self):
        """加载角色图片"""
        self.images = {}
        
        # 如果 assets 目录中有图片，则加载；否则使用占位符
        if os.path.exists("assets"):
            try:
                for state in ["idle", "tap", "sleep", "eat", "play"]:
                    path = f"assets/{state}.png"
                    if os.path.exists(path):
                        img = Image.open(path).resize((WINDOW_WIDTH, WINDOW_HEIGHT))
                        self.images[state] = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"⚠ 图片加载失败: {e}")
        
        # 如果没有图片，创建占位符
        if not self.images:
            self.create_placeholder_image()
    
    def create_placeholder_image(self):
        """创建占位符图片"""
        from PIL import Image, ImageDraw
        
        # 创建简单的白色背景图片
        img = Image.new('RGB', (WINDOW_WIDTH, WINDOW_HEIGHT), 'white')
        draw = ImageDraw.Draw(img)
        
        # 画简单的圆形表示猫咪
        draw.ellipse([50, 50, 150, 150], fill='gray', outline='black', width=2)
        # 画眼睛
        draw.ellipse([70, 80, 80, 90], fill='black')
        draw.ellipse([120, 80, 130, 90], fill='black')
        # 画嘴巴
        draw.arc([80, 100, 120, 120], 0, 180, fill='black', width=2)
        
        for state in ["idle", "tap", "sleep", "eat", "play"]:
            self.images[state] = ImageTk.PhotoImage(img)
    
    def update_display(self):
        """更新显示"""
        self.canvas.delete("all")
        
        # 显示图片
        if self.current_state in self.images:
            self.canvas.create_image(
                WINDOW_WIDTH // 2,
                WINDOW_HEIGHT // 2,
                image=self.images[self.current_state],
                tags="pet_image"
            )
        
        # 显示文字
        if self.is_talking:
            self.canvas.create_text(
                WINDOW_WIDTH // 2,
                WINDOW_HEIGHT - 20,
                text="正在思考...",
                fill="black",
                font=("Arial", 8),
                tags="talk_text"
            )
    
    def animation_loop(self):
        """动画循环"""
        if self.current_state == "idle":
            # 闲置时循环播放待机动画
            self.idle_animation_state = (self.idle_animation_state + 1) % self.idle_animation_max
            self.update_display()
        
        self.root.after(IDLE_ANIMATION_INTERVAL, self.animation_loop)
    
    def on_click(self, event):
        """鼠标点击事件"""
        data_manager.increment_clicks()
        self.current_state = "tap"
        self.update_display()
        
        # 随机回复
        reply = random.choice(INTERACTION_RESPONSES["tap_reaction"])
        self.show_dialog(reply)
        
        # 1秒后恢复待机
        self.root.after(1000, lambda: self.reset_to_idle())
    
    def on_drag(self, event):
        """拖拽事件"""
        if not self.is_dragging:
            self.is_dragging = True
            self.drag_start_x = event.x
            self.drag_start_y = event.y
        
        dx = event.x_root - event.x - self.root.winfo_x()
        dy = event.y_root - event.y - self.root.winfo_y()
        
        self.root.geometry(f"+{dx}+{dy}")
    
    def on_release(self, event):
        """释放鼠标事件"""
        self.is_dragging = False
    
    def on_right_click(self, event):
        """右键菜单"""
        menu = tk.Menu(self.root, tearoff=False)
        menu.add_command(label="查看数据", command=self.show_stats)
        menu.add_command(label="好感度", command=self.show_affection)
        menu.add_command(label="送礼物", command=self.show_gifts)
        menu.add_separator()
        menu.add_command(label="关于", command=self.show_about)
        menu.add_command(label="退出", command=self.close_app)
        
        menu.post(event.x_root, event.y_root)
    
    def show_dialog(self, text):
        """显示对话框"""
        self.is_talking = True
        self.update_display()
        
        # 创建对话框窗口
        dialog = tk.Toplevel(self.root)
        dialog.title(PET_NAME)
        dialog.geometry("300x100")
        dialog.attributes('-topmost', True)
        
        label = tk.Label(dialog, text=text, wraplength=280, justify=tk.LEFT, font=("Arial", 10))
        label.pack(pady=10)
        
        button = tk.Button(dialog, text="关闭", command=lambda: self.close_dialog(dialog))
        button.pack(pady=5)
        
        self.root.after(5000, lambda: self.close_dialog(dialog) if dialog.winfo_exists() else None)
    
    def close_dialog(self, dialog):
        """关闭对话框"""
        try:
            dialog.destroy()
            self.is_talking = False
            self.reset_to_idle()
        except:
            pass
    
    def reset_to_idle(self):
        """恢复待机状态"""
        if self.current_state != "idle":
            self.current_state = "idle"
            self.update_display()
    
    def show_stats(self):
        """显示统计信息"""
        stats_text = StatsDisplay.get_stats_text()
        messagebox.showinfo("统计信息", stats_text)
    
    def show_affection(self):
        """显示好感度信息"""
        stats = data_manager.get_stats()
        affection_desc = AffectionSystem.get_description(stats["affection"])
        messagebox.showinfo("好感度", affection_desc)
    
    def show_gifts(self):
        """显示礼物列表"""
        gifts = GiftSystem.get_all_gifts()
        gift_text = "\n".join([f"{'✓' if gift['can_send'] else '✗'} {gift['name']} ({gift['cost']} 点)"
                               for gift in gifts])
        messagebox.showinfo("礼物列表", gift_text)
    
    def show_about(self):
        """显示关于信息"""
        about_text = f"""小喵咪桌宠 v1.0
        
一只可爱温柔的虚拟猫咪
        
功能：
- 点击互动
- 屏幕识别
- AI聊天
- 好感系统
        """
        messagebox.showinfo("关于", about_text)
    
    def idle_chat_timer(self):
        """闲置聊天定时器"""
        if random.random() < IDLE_RANDOM_CHAT_PROBABILITY:
            # 触发闲置自言自语
            self.idle_chat()
        
        self.root.after(IDLE_RANDOM_CHAT_INTERVAL, self.idle_chat_timer)
    
    def idle_chat(self):
        """闲置时的自言自语"""
        def callback(reply):
            if reply:
                self.show_dialog(reply)
        
        # 调用 API
        api_client.idle_chat(callback=callback)
    
    def close_app(self):
        """关闭程序"""
        data_manager.save_data()
        self.root.destroy()


def main():
    """主函数"""
    root = tk.Tk()
    pet = DesktopPet(root)
    root.mainloop()


if __name__ == "__main__":
    print("""\n╔═══════════════════════════════════╗
║     小喵咪桌宠 v1.0              ║
║  一只可爱温柔的虚拟猫咪        ║
╚═══════════════════════════════════╝\n""")
    main()
