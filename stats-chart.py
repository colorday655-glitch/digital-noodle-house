#!/usr/bin/env python3
import random
from datetime import datetime, timedelta
from collections import Counter

def generate_mock_data():
    """生成模拟订单数据"""
    timestamps = []
    now = datetime.now()
    
    # 模拟一周的订单数据
    for day in range(7):
        date = now - timedelta(days=6-day)
        
        # 模拟高峰时段：11-13点，18-20点，22-2点
        for hour in range(24):
            if hour in [11, 12, 13]:  # 午餐高峰
                orders = random.randint(8, 15)
            elif hour in [18, 19, 20]:  # 晚餐高峰
                orders = random.randint(10, 18)
            elif hour in [22, 23, 0, 1]:  # 深夜高峰
                orders = random.randint(5, 12)
            else:
                orders = random.randint(0, 3)
            
            for _ in range(orders):
                ts = date.replace(hour=hour, minute=random.randint(0, 59)).timestamp()
                timestamps.append(int(ts))
    
    return timestamps

def generate_chart(timestamps):
    # 按小时统计
    hours = [datetime.fromtimestamp(ts).hour for ts in timestamps]
    hour_counts = Counter(hours)
    
    # 生成24小时数据
    data = {h: hour_counts.get(h, 0) for h in range(24)}
    
    # 找出高峰时段
    peak_hour = max(data, key=data.get)
    peak_count = data[peak_hour]
    
    # 生成ASCII图表
    print("\n" + "="*60)
    print("🍜 张大爷无人面馆 · 本周订单高峰时段统计")
    print("="*60)
    print(f"📅 统计周期: 最近7天")
    print(f"📦 总订单数: {len(timestamps)} 单")
    print(f"🔥 高峰时段: {peak_hour}:00 - {peak_hour+1}:00 ({peak_count} 单)")
    print("="*60)
    
    # 绘制柱状图
    max_count = max(data.values()) if data.values() else 1
    bar_width = 35
    
    print("\n📊 24小时订单分布:")
    print("-"*60)
    
    for hour in range(24):
        count = data[hour]
        bar_len = int((count / max_count) * bar_width) if max_count > 0 else 0
        bar = "█" * bar_len
        time_label = f"{hour:02d}:00"
        
        # 标记高峰时段
        if count == peak_count and count > 0:
            marker = " 🔥"
        elif count >= peak_count * 0.8 and count > 0:
            marker = " ⭐"
        else:
            marker = ""
        
        print(f"{time_label} | {bar:<35} {count:>3}单{marker}")
    
    print("-"*60)
    
    # 分析高峰时段
    print("\n🎯 高峰时段分析:")
    print("  • 午餐高峰: 11:00-13:00 (上班族点餐)")
    print("  • 晚餐高峰: 18:00-20:00 (下班回家)")
    print("  • 深夜高峰: 22:00-02:00 (夜宵时刻) 🌙")
    
    print("\n💡 运营建议:")
    print("  • 午餐/晚餐时段确保食材充足")
    print("  • 深夜是特色时段，可推出限定套餐")
    print("  • 凌晨2-6点订单最少，可作为备餐时间")
    
    print("\n" + "="*60)
    print("📊 实时监控: http://jackbaba.cn/digital-noodle-house/dashboard.html")
    print("="*60)
    print()

if __name__ == '__main__':
    # 使用mock数据
    print("使用模拟数据生成统计图...\n")
    mock_timestamps = generate_mock_data()
    generate_chart(mock_timestamps)