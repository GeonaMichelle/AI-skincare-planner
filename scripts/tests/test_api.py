import requests

def get_token():
    url = "http://127.0.0.1:8000/api/v1/auth/login"
    data = {"email": "user@skiniq.ai", "password": "Password123!"}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()["access_token"]
    
    print("Login failed:", response.text)
    return None

token = get_token()
if token:
    headers = {"Authorization": f"Bearer {token}"}
    
    print("Testing /recommendations with budget 20...")
    res = requests.get("http://127.0.0.1:8000/api/v1/products/recommendations?max_budget=20", headers=headers)
    print("Recommendations Status:", res.status_code)
    if res.status_code == 200:
        data = res.json()
        print("Recommendations count:", len(data.get("recommended_products", [])))
        for r in data.get("recommended_products", []):
            print(f"- {r['product']['name']} ({r['price_estimate']}) [Alternatives: {len(r.get('alternatives', []))}]")
    
    print("\nTesting /compare...")
    res = requests.post("http://127.0.0.1:8000/api/v1/products/compare", json={"product_names": ["CeraVe Hydrating Cleanser", "Vanicream Daily Facial Moisturizer"]}, headers=headers)
    print("Compare Status:", res.status_code)
    if res.status_code == 200:
        print("Compare Result:", res.json())
    else:
        print("Compare Error:", res.text)
