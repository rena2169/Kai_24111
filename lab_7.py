import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Загрузка данных
print("Загрузка данных...")
df = pd.read_csv("hn_real_data.csv")
df['created_at'] = pd.to_datetime(df['created_at'])
df = df.dropna() # чистим пропуски

# 2. Вопрос 1: Топ слов
print("Считаем слова...")
words = (df['title'].str.lower()
         .str.replace(r'[^\w\s]', '', regex=True)
         .str.split()
         .explode()
         .value_counts()
         .head(10))

plt.figure(figsize=(10, 4))
sns.barplot(x=words.values, y=words.index, palette="viridis", hue=words.index, legend=False)
plt.title("Топ-10 слов в популярных постах")
plt.tight_layout()
plt.show()  # <--- Окно 1

# 3. Вопрос 2: Время публикации
print("Считаем время...")
df['hour'] = df['created_at'].dt.hour
hourly_scores = df.groupby('hour')['points'].mean()

plt.figure(figsize=(10, 4))
sns.lineplot(x=hourly_scores.index, y=hourly_scores.values, marker='o', color='orange')
plt.title("Средний рейтинг постов по часам (UTC)")
plt.xticks(range(0, 24))
plt.grid(True)
plt.tight_layout()
plt.show()  # <--- Окно 2

# 4. Вопрос 3: Связь комментов и рейтинга
correlation = df['num_comments'].corr(df['points'])
print(f"\n--- Коэффициент корреляции: {correlation:.2f} ---\n")

plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x='num_comments', y='points', alpha=0.5)
plt.title("Зависимость рейтинга от количества комментариев")
plt.tight_layout()
plt.show()  # <--- Окно 3

print("Готово!")