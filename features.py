"""
附加功能模块
包含好感度系统、礼物兑换等扩展功能
"""

from data_manager import data_manager


class AffectionSystem:
    """好感度系统"""
    
    # 好感度等级
    LEVELS = {
        0: ("陌生", "🥀"),
        20: ("疏远", "💔"),
        40: ("一般", "🤎"),
        60: ("友好", "💛"),
        80: ("亲密", "💚"),
        100: ("最亲", "💕"),
    }
    
    @staticmethod
    def get_level(affection):
        """获取好感度等级"""
        for threshold in sorted(AffectionSystem.LEVELS.keys(), reverse=True):
            if affection >= threshold:
                return AffectionSystem.LEVELS[threshold]
        return ("陌生", "🥀")
    
    @staticmethod
    def get_description(affection):
        """获取好感度描述"""
        level_name, emoji = AffectionSystem.get_level(affection)
        return f"{emoji} 好感度: {affection}/100 ({level_name})"
    
    @staticmethod
    def add_affection_for_action(action):
        """
        根据行为增加好感度
        
        Args:
            action: 行为类型
                - "tap": 点击
                - "chat": 聊天
                - "gift": 送礼物
        """
        affection_map = {
            "tap": 2,
            "chat": 5,
            "gift": 10,
        }
        
        amount = affection_map.get(action, 1)
        data_manager.add_affection(amount)


class GiftSystem:
    """礼物系统"""
    
    GIFTS = {
        "小鱼干": {
            "cost": 50,  # 消耗点击次数
            "affection": 10,
            "description": "喵喵最爱的小鱼干~",
            "reaction": "喵呜~谢谢主人！太好吃了~",
        },
        "逗猫棒": {
            "cost": 100,
            "affection": 15,
            "description": "刺激的玩具~",
            "reaction": "咪呜咪呜~太好玩了！",
        },
        "猫窝": {
            "cost": 200,
            "affection": 20,
            "description": "温暖舒适的小窝~",
            "reaction": "呼~好舒服啊，我爱死这个窝了！",
        },
        "项圈": {
            "cost": 150,
            "affection": 18,
            "description": "漂亮的项圈~",
            "reaction": "哎呀~主人你觉得小喵好看吗~",
        },
    }
    
    @staticmethod
    def can_gift(gift_name):
        """检查是否能送礼物"""
        if gift_name not in GiftSystem.GIFTS:
            return False, "没有这个礼物呢"
        
        gift = GiftSystem.GIFTS[gift_name]
        current_clicks = data_manager.get("current_clicks", 0)
        
        if current_clicks >= gift["cost"]:
            return True, "可以送礼物"
        else:
            needed = gift["cost"] - current_clicks
            return False, f"还需要 {needed} 次点击"
    
    @staticmethod
    def send_gift(gift_name):
        """送礼物"""
        can_send, msg = GiftSystem.can_gift(gift_name)
        
        if not can_send:
            return False, msg
        
        if gift_name not in GiftSystem.GIFTS:
            return False, "没有这个礼物呢"
        
        gift = GiftSystem.GIFTS[gift_name]
        
        # 扣除点击次数
        current_clicks = data_manager.get("current_clicks", 0)
        data_manager.set("current_clicks", current_clicks - gift["cost"])
        
        # 增加好感度
        data_manager.add_affection(gift["affection"])
        
        return True, gift["reaction"]
    
    @staticmethod
    def get_all_gifts():
        """获取所有礼物列表"""
        gifts_info = []
        for name, info in GiftSystem.GIFTS.items():
            can_send, msg = GiftSystem.can_gift(name)
            gifts_info.append({
                "name": name,
                "cost": info["cost"],
                "affection": info["affection"],
                "description": info["description"],
                "can_send": can_send,
                "status": msg,
            })
        return gifts_info


class StatsDisplay:
    """统计信息显示"""
    
    @staticmethod
    def get_stats_text():
        """获取统计信息文本"""
        stats = data_manager.get_stats()
        affection_desc = AffectionSystem.get_description(stats["affection"])
        
        text = f"""
╔═══════════════════╗
║ {stats['pet_name']} 的统计信息 ║
╠═══════════════════╣
║ 点击次数: {stats['total_clicks']:>5} 次
║ {affection_desc}
║ 可消耗点击: {data_manager.get('current_clicks', 0):>3} 次
╚═══════════════════╝
        """.strip()
        
        return text
    
    @staticmethod
    def get_short_stats():
        """获取简短统计信息"""
        stats = data_manager.get_stats()
        level_name, emoji = AffectionSystem.get_level(stats["affection"])
        current_clicks = data_manager.get("current_clicks", 0)
        
        return f"点击: {stats['total_clicks']} | 可消耗: {current_clicks} | 好感: {stats['affection']} {emoji}"


if __name__ == "__main__":
    print("✓ 功能模块加载成功!")
    print("✓ 好感度系统已启用")
    print("✓ 礼物系统已启用")
    print("✓ 统计信息已启用")
    print()
    print(StatsDisplay.get_stats_text())
