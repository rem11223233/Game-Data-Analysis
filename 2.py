import pandas as pd
import matplotlib.pyplot as plt

# 解决中文显示
plt.rcParams['font.sans-serif'] = ['SimHei'] 
plt.rcParams['axes.unicode_minus'] = False

# 1. 读取与清洗（老规矩）
df = pd.read_csv('wzry_accounts.csv')
df['价格'] = df['价格'].astype(str).str.replace('¥', '').str.replace(',', '')
df['价格'] = pd.to_numeric(df['价格'], errors='coerce')
df = df.dropna(subset=['价格'])
df['皮肤数量'] = pd.to_numeric(df['皮肤数量'], errors='coerce').fillna(0)
df['贵族等级_num'] = pd.to_numeric(df['贵族等级'].astype(str).str.replace('V', ''), errors='coerce').fillna(0)

print("============ 渠道与高净值玩家分析 ============\n")

# --- 分析一：渠道差异 ---
print("--- 📱 各渠道(QQ/微信)与系统(安卓/苹果)的账号均价 ---")
channel_price = df.groupby(['账号类型', '系统版本'])['价格'].mean().unstack()
print(channel_price)

# 画图一
plt.figure(figsize=(8, 5))
channel_price.plot(kind='bar', color=['#FF9999', '#66B2FF'])
plt.title('不同渠道与系统的账号均价对比')
plt.ylabel('平均价格 (元)')
plt.xticks(rotation=0)
plt.show() # 这里会弹出第一张图，看完关掉它

# --- 分析二：高净值玩家画像 ---
print("\n--- 👑 各贵族等级的平均皮肤数与均价 ---")
vip_df = df[df['贵族等级_num'] > 0]
vip_profile = vip_df.groupby('贵族等级')['皮肤数量', '价格'].mean() if '价格' in vip_df.columns else None
# 上面这句做个兼容，直接按下面正常写
vip_profile = vip_df.groupby('贵族等级')[['皮肤数量', '价格']].mean()
print(vip_profile)

# 画图二
plt.figure(figsize=(8, 5))
plt.plot(vip_profile.index, vip_profile['皮肤数量'], marker='o', color='gold', linewidth=2)
plt.title('贵族等级与平均皮肤数量的关系')
plt.xlabel('贵族等级')
plt.ylabel('平均皮肤数量')
plt.grid(True)
plt.show() # 这里会弹出第二张图

print("\n✅ 2.py 运行完毕！")