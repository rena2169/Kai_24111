import requests
import pandas as pd

print("Скачиваем 1000 реальных постов с Hacker News...")
# Берем 1000 самых популярных постов
url = "http://hn.algolia.com/api/v1/search?tags=story&hitsPerPage=1000"
response = requests.get(url)
data = response.json()['hits']

# Оставляем только нужные поля
df = pd.DataFrame(data)[['title', 'created_at', 'points', 'num_comments']]
df.to_csv("hn_real_data.csv", index=False)
print("Готово! Файл hn_real_data.csv создан.")