import requests
from agent.config import NEWSAPI_KEY

NEWSAPI_URL = "https://newsapi.org/v2/everything"

class NewsSearchError(Exception):
    pass

# Search recent news for a specific ticker or company
def search_market_news(query: str , days_back: int = 7 , page_size: int = 5) -> list[dict]:
    # If no query is passed
    if not query or not query.strip():
        raise NewsSearchError("Query cannot be empty.")
    
    params = {
        "q" : query,
        "sortBy" : "publishedAt",
        "pageSize" : page_size, 
        "language"  : "en",
        "apiKey" : NEWSAPI_KEY
    }
    
    # Query the NewsAPI for recent news articles
    try:
        response = requests.get(NEWSAPI_URL , params = params)
    except requests.exceptions.RequestException as e:
        raise NewsSearchError(f"Error while making request to NewsAPI: {e}")
    
    # Too many requests check
    if response.status_code == 429:
        raise NewsSearchError("NewsAPI rate limit exceeded — try again later")

    # Check for other HTTP errors
    if response.status_code != 200:
        raise NewsSearchError(f"NewsAPI returned status {response.status_code}: {response.text}")
    
    data = response.json()
    articles = data.get("articles", [])
    
    # Return empty list if no articles found
    if not articles:
        return []
    
    # Format the articles into a dictionary list with relevant information
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