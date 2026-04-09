import requests

BASE_URL = "http://localhost:5000/blacklists"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer fixedtoken"
}

def test_post_blacklist():
    data = {
        "email": "test@example.com",
        "app_uuid": "123e4567-e89b-12d3-a456-426614174000",
        "blocked_reason": "spam"
    }
    response = requests.post(BASE_URL + "/", json=data, headers=HEADERS)
    print("POST /blacklists/:", response.status_code, response.json())

def test_get_blacklist():
    response = requests.get(BASE_URL + "/test@example.com", headers=HEADERS)
    print("GET /blacklists/test@example.com:", response.status_code, response.json())

def test_get_blacklist_not_found():
    response = requests.get(BASE_URL + "/notfound@example.com", headers=HEADERS)
    print("GET /blacklists/notfound@example.com:", response.status_code, response.json())

if __name__ == "__main__":
    test_post_blacklist()
    test_get_blacklist()
    test_get_blacklist_not_found()
