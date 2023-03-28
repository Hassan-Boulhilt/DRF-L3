import requests

def client():
    
    token_h = "Token 6bfae91664369654d7074b4bdf9106aa517cc41b"
    # credentials = {
    #     "username": "admin",
    #     "password": "1973"
    # }
    # response = requests.post("http://127.0.0.1:8000/api/rest-auth/login/", data=credentials)
    
    headers = {"Authorization": token_h}
    
    response = requests.get("http://127.0.0.1:8000/api/profiles/", headers=headers)
    
    
    print("Status Code:", response.status_code)
    
    response_data = response.json()
    
    print(response_data)
    # print("Headers:", response.headers)
    # print("Content:", response.content)
    
if __name__ == "__main__":
    client()