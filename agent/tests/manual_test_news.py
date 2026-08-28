from agent.tools.news import search_market_news, NewsSearchError

TEST_QUERIES = ["Tesla", "Rivian", "Nvidia", "Apple"]

def run():
    for query in TEST_QUERIES:
        try:
            results = search_market_news(query)
            print(f"{query}: OK, {len(results)} articles")
            if results:
                print(f"  Latest: {results[0]['title']} ({results[0]['source']})")
        except NewsSearchError as e:
            print(f"{query}: FAILED - {e}")

    # confirm error path still works inside this script
    try:
        search_market_news("")
        print("Empty query: unexpectedly succeeded — bug")
    except NewsSearchError as e:
        print(f"Empty query: correctly caught - {e}")

if __name__ == "__main__":
    run()