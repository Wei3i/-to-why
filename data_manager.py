"""
数据管理模块
负责读取、保存、管理桌宠的持久化数据
"""

import json
import os
from datetime import datetime
from config import DATA_FILE, DEFAULT_DATA

class DataManager:
    """数据管理器"""
    
    def __init__(self):
        self.data = self.load_data()
    
    def load_data(self):
        """
        加载存档数据
        如果文件不存在，创建新的存档
        """
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    print(f"✓ 成功加载数据文件: {DATA_FILE}")
                    return data
            except Exception as e:
                print(f"⚠ 读取数据文件失败: {e}，创建新存档")
                return self._create_new_data()
        else:
            print(f"✓ 首次运行，创建新存档文件: {DATA_FILE}")
            return self._create_new_data()
    
    def _create_new_data(self):
        """创建新的默认存档"""
        new_data = DEFAULT_DATA.copy()
        new_data["creation_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.save_data(new_data)
        return new_data
    
    def save_data(self, data=None):
        """
        保存数据到 JSON 文件
        
        Args:
            data: 要保存的数据字典，如果为 None 则保存当前数据
        """
        if data is None:
            data = self.data
        
        try:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"✓ 数据已保存")
                return True
        except Exception as e:
            print(f"✗ 保存数据失败: {e}")
            return False
    
    def get(self, key, default=None):
        """获取数据"""
        return self.data.get(key, default)
    
    def set(self, key, value):
        """设置数据"""
        self.data[key] = value
        self.save_data()
    
    def increment_clicks(self, count=1):
        """增加点击次数"""
        self.data["total_clicks"] += count
        self.data["current_clicks"] = self.data.get("current_clicks", 0) + count
        self.save_data()
        print(f"✓ 点击次数: {self.data['total_clicks']}")
    
    def add_affection(self, amount):
        """增加好感度"""
        self.data["affection"] = min(100, self.data.get("affection", 50) + amount)
        self.save_data()
        print(f"✓ 好感度: {self.data['affection']}/100")
    
    def reduce_affection(self, amount):
        """减少好感度"""
        self.data["affection"] = max(0, self.data.get("affection", 50) - amount)
        self.save_data()
        print(f"✓ 好感度: {self.data['affection']}/100")
    
    def get_stats(self):
        """获取统计信息"""
        return {
            "total_clicks": self.data.get("total_clicks", 0),
            "affection": self.data.get("affection", 50),
            "pet_name": self.data.get("pet_name", "小喵咪"),
        }


# 全局数据管理器实例
data_manager = DataManager()


if __name__ == "__main__":
    print("✓ ��据管理模块加载成功!")
    print(f"✓ 当前数据: {data_manager.get_stats()}")
