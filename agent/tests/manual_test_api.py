import requests

BASE_URL = "http://localhost:8000"

def test_health():
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health check: {response.status_code} - {response.json()}")

def test_chat(message: str):
    response = requests.post(
        f"{BASE_URL}/chat",
        json={"message": message}
    )
    print(f"Question: {message}")
    print(f"Status: {response.status_code}")
    print(f"Answer: {response.json()['answer']}")

if __name__ == "__main__":
    test_health()
    print()
    test_chat("What is Tesla's current RSI?")
    print()
    test_chat("Compare Tesla and Rivian on volatility, which looks riskier?")