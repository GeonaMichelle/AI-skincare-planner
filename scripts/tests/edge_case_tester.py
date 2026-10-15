import requests
import json
import time

BASE_URL = "http://localhost:8000/api/v1"

# Utility for printing results
def print_res(name, passed, details=""):
    status = "[PASS]" if passed else "[FAIL]"
    print(f"{status} | {name} {('- ' + details) if details else ''}")
    return passed

def run_all_tests():
    print("Starting Comprehensive API & Edge Case Testing on Deployed Docker Container...\n")
    all_passed = True

    # 1. Healthcheck
    try:
        r = requests.get(f"http://localhost:8000/api/health")
        passed = r.status_code == 200
        all_passed = all_passed and print_res("System Health Check", passed)
    except Exception as e:
        all_passed = all_passed and print_res("System Health Check", False, str(e))
        print("Application might not be running. Run `docker compose up -d` first.")
        return

    # 2. Authentication - Edge Cases
    print("\n--- Authentication Edge Cases ---")
    # Missing fields
    r = requests.post(f"{BASE_URL}/auth/login", json={"email": "admin@skiniq.ai"})
    all_passed = all_passed and print_res("Login with Missing Password (422 expected)", r.status_code == 422)

    # Invalid credentials
    r = requests.post(f"{BASE_URL}/auth/login", json={"email": "admin@skiniq.ai", "password": "WrongPassword"})
    all_passed = all_passed and print_res("Login with Invalid Password (401 expected)", r.status_code == 401)

    # Valid Login
    r = requests.post(f"{BASE_URL}/auth/login", json={"email": "admin@skiniq.ai", "password": "AdminPass2026!"})
    login_success = r.status_code == 200
    all_passed = all_passed and print_res("Valid Admin Login", login_success)
    
    token = r.json().get("access_token") if login_success else ""
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Registration - Edge Cases
    print("\n--- Registration Edge Cases ---")
    # Duplicate email
    r = requests.post(f"{BASE_URL}/auth/register", json={
        "email": "admin@skiniq.ai", "password": "NewPassword123!", "full_name": "Test", "role": "USER"
    })
    all_passed = all_passed and print_res("Register with Existing Email (400 expected)", r.status_code == 400)

    # Invalid email format (assuming API validates email format, if it doesn't we might get 422 or 201 depending on pydantic schema)
    r = requests.post(f"{BASE_URL}/auth/register", json={
        "email": "invalid-email", "password": "NewPassword123!", "full_name": "Test", "role": "USER"
    })
    all_passed = all_passed and print_res("Register with Invalid Email Format", r.status_code == 422)

    # 4. Protected Endpoints (RBAC / Auth checks)
    print("\n--- Protected Route Edge Cases ---")
    # Access without token
    r = requests.get(f"{BASE_URL}/auth/me")
    all_passed = all_passed and print_res("Access protected route without token (401 expected)", r.status_code == 401)

    # Access with valid token
    if token:
        r = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        all_passed = all_passed and print_res("Access protected route with valid token", r.status_code == 200)

    # 5. Dashboards & Profiles (Data Boundaries)
    print("\n--- Dashboard & Data Boundary Cases ---")
    if token:
        # Invalid user_id format
        r = requests.get(f"{BASE_URL}/dashboard/user/invalid_id", headers=headers)
        all_passed = all_passed and print_res("Fetch dashboard with string user_id (422 expected)", r.status_code == 422)

        # Non-existent user dashboard
        r = requests.get(f"{BASE_URL}/dashboard/user/99999", headers=headers)
        all_passed = all_passed and print_res("Fetch dashboard for non-existent user", r.status_code in [200, 404])
        
        # Valid Admin Dashboard
        r = requests.get(f"{BASE_URL}/dashboard/admin", headers=headers)
        all_passed = all_passed and print_res("Fetch Admin Dashboard Data", r.status_code == 200)

    print("\n---------------------------------------------------")
    if all_passed:
        print("ALL EDGE CASES AND TESTS PASSED SUCCESSFULLY! THE DEPLOYMENT IS ROBUST.")
    else:
        print("SOME TESTS FAILED. PLEASE REVIEW THE LOGS ABOVE.")

if __name__ == "__main__":
    run_all_tests()
