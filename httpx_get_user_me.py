import httpx

login_payload = {
    "email": "user@example.com",
    "password": "string"
}

with httpx.Client(base_url="http://localhost:8000") as client:
    login_response = client.post("/api/v1/authentication/login", json=login_payload)
    login_response.raise_for_status()
    login_data = login_response.json()

    access_token = login_data["token"]["accessToken"]
    print(f"Login response: {login_data}")
    print("Status code:", login_response.status_code)

    headers = {"Authorization": f"Bearer {access_token}"}
    me_response = client.get("/api/v1/users/me", headers=headers)

    print(f"Me response: {me_response.json()}")
    print("Status code:", me_response.status_code)
