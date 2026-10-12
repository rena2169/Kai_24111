from bs4 import BeautifulSoup
import requests
import csv
import time


def main():
    base_url = "https://news.ycombinator.com/"
    news = fetch_page(base_url)
    save_to_csv(news)

def fetch_page(base_url):
    news = []
    for page in range(1, 4):
        url = f"{base_url}?p={page}"
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            for item in soup.select('.titleline > a'):
                news.append({
                    "title": item.text,
                    "url": item.get("href")
                })
        time.sleep(1)
    return news

def save_to_csv(news):
    with open("news.csv", 'w', encoding="utf-8", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["title", "url"])
        for new in news:
            writer.writerow([new["title"], new["url"]])

if __name__ == "__main__":
    main()