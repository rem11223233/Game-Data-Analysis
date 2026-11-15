import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei'] 
plt.rcParams['axes.unicode_minus'] = False

# 读取并清洗
df = pd.read_csv('wzry_accounts.csv')
df['价格'] = df['价格'].astype(str).str.replace('¥', '').str.replace(',', '')
df['价格'] = pd.to_numeric(df['价格'], errors='coerce')
df = df.dropna(subset=['价格'])
df['皮肤数量'] = pd.to_numeric(df['皮肤数量'], errors='coerce').fillna(0)
df['贵族等级_num'] = pd.to_numeric(df['贵族等级'].astype(str).str.replace('V', ''), errors='coerce').fillna(0)

# 过滤掉贵族等级为0的普通玩家，只看V1-V10
vip_df = df[df['贵族等级_num'] > 0]
vip_profile = vip_df.groupby('贵族等级')[['皮肤数量', '价格']].mean()

# 画图
plt.figure(figsize=(8, 5))
# 画一条金色的折线
plt.plot(vip_profile.index, vip_profile['皮肤数量'], marker='o', color='gold', linewidth=3, markersize=8)
plt.title('贵族等级与平均皮肤数量的关系', fontsize=14)
plt.xlabel('贵族等级', fontsize=12)
plt.ylabel('平均皮肤数量', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()