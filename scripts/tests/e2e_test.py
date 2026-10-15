import requests
import sys

BASE_URL = "http://localhost:8000"
API_URL = f"{BASE_URL}/api/v1"

def test_health():
    res = requests.get(f"{BASE_URL}/api/health")
    assert res.status_code == 200, f"Healthcheck failed: {res.status_code}"
    print("Healthcheck passed")
    # Check security headers
    headers = res.headers
    assert headers.get("X-Content-Type-Options") == "nosniff", "Missing Security Header: nosniff"
    assert headers.get("X-Frame-Options") == "DENY", "Missing Security Header: DENY"
    print("Security Headers present")

def test_frontend_serving():
    res = requests.get(f"{BASE_URL}/")
    assert res.status_code == 200, "Frontend serving failed"
    assert "html" in res.headers.get("Content-Type", ""), "Not serving HTML"
    print("Frontend serving passed")

def run_tests():
    try:
        test_health()
        test_frontend_serving()
        print("All E2E tests passed successfully.")
    except Exception as e:
        print(f"E2E testing failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_tests()
