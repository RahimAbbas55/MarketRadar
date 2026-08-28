import requests
from agent.config import NEWSAPI_KEY

NEWSAPI_URL = "https://newsapi.org/v2/everything"

# Search recent news for a specific ticker or company
def search_market_news(query: str , days_back: int = 7 , page_size: int = 5) -> list[dict]:
    params = {
        "q" : query,
        "sortBy" : "publishedAt",
        "pageSize" : page_size, 
        "language"  : "en",
        "apiKey" : NEWSAPI_KEY
    }
    response = requests.get(NEWSAPI_URL , params = params)
    data = response.json()
    articles = data.get("articles", [])
    results = []
    for article in articles:
        results.append({
            "title" : article.get("title" , ""),
            "source" : article.get("source" , {}).get("name"),
            "published_at" : article.get("publishedAt"),
            "url" : article.get("url"),
            "description" : article.get("description"),
        })
    return results