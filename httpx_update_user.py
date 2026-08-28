import httpx
from tools.fakers import get_random_email

create_user_payload = {
    "email": get_random_email(),
    "password": "string",
    "lastName": "string",
    "firstName": "string",
    "middleName": "string"
}
with httpx.Client(base_url="http://localhost:8000") as client:
    create_user_response = client.post("/api/v1/users", json=create_user_payload)
    create_user_response_data = create_user_response.json()
    print(f'Create user data: {create_user_response_data}')

    login_payload = {
        "email": create_user_payload["email"],
        "password": create_user_payload["password"],
    }
    login_response = client.post("/api/v1/authentication/login", json=login_payload)
    login_response_data = login_response.json()
    print(f'Login data: {login_response_data}')

    path_payload = {
        "email": get_random_email(),
        "lastName": "string",
        "firstName": "string",
        "middleName": "string"
    }
    path_user_headers = {
        "Authorization": f"Bearer {login_response_data['token']['accessToken']}"
    }
    path_response = client.patch(
        f"/api/v1/users/{create_user_response_data['user']['id']}",
        json=path_payload,
        headers=path_user_headers
    )
    print(f'Path response code: {path_response.status_code}')
