import pandas as pd
import matplotlib.pyplot as plt

# 解决图表中文显示为方块的问题
plt.rcParams['font.sans-serif'] = ['SimHei'] 
plt.rcParams['axes.unicode_minus'] = False

# 读取数据
df = pd.read_csv('wzry_accounts.csv')

print("============ 王者荣耀账号交易深度分析 ============\n")

# --- 数据清洗 ---
# 1. 清洗价格
df['价格'] = df['价格'].astype(str).str.replace('¥', '').str.replace(',', '')
df['价格'] = pd.to_numeric(df['价格'], errors='coerce')
df = df.dropna(subset=['价格'])

# 2. 清洗皮肤数量（关键修复！把非数字全部转成 0）
df['皮肤数量'] = pd.to_numeric(df['皮肤数量'], errors='coerce').fillna(0)

# 3. 清洗贵族等级
df['贵族等级'] = df['贵族等级'].astype(str).str.replace('V', '')
df['贵族等级'] = pd.to_numeric(df['贵族等级'], errors='coerce').fillna(0)

print(f"✅ 数据清洗完成，有效数据 {len(df)} 行\n")

# --- 数据分析 ---
avg_price = df['价格'].mean()
max_price = df['价格'].max()
print(f"💰 账号平均售价: {avg_price:.2f} 元")
print(f"💎 最贵的一个账号卖了: {max_price} 元\n")

print("--- 🏆 各段位账号的平均价格排行 (前 5 名) ---")
rank_price = df.groupby('段位')['价格'].mean().sort_values(ascending=False)
print(rank_price.head(5))

corr = df['皮肤数量'].corr(df['价格'])
print(f"\n📈 皮肤数量与价格的相关性: {corr:.3f} (越接近1，说明皮肤越影响价格)")

# --- 数据可视化 (画图) ---
print("\n正在生成图表，请稍等...")

# 画一个柱状图，展示前 5 名段位的平均价格
plt.figure(figsize=(10, 5))
# 让图表支持显示中文
plt.bar(rank_price.head(5).index, rank_price.head(5).values, color='skyblue', edgecolor='black')
plt.title('王者荣耀不同段位账号的平均交易价格')
plt.xlabel('段位')
plt.ylabel('平均价格 (元)')
for i, v in enumerate(rank_price.head(5).values):
    plt.text(i, v + 100, f"{v:.0f}", ha='center', va='bottom') # 在柱子上显示数字

plt.show()