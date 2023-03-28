import requests

def client():
    
    # token_h = "Token 6bfae91664369654d7074b4bdf9106aa517cc41b"
    data = {
        "username": "hufgtyifrt",
        "email": "testzert@test.com",
        "password1": "1973AaBbCc",
        "password2": "1973AaBbCc"
    }
    response = requests.post("http://127.0.0.1:8000/api/dj-rest-auth/registration/", data=data)
    
    # headers = {"Authorization": token_h}
    
    # response = requests.get("http://127.0.0.1:8000/api/profiles/", headers=headers)
    
    
    print("Status Code:", response.status_code)
    
    response_data = response.json()
    
    print(response_data)
    # print("Headers:", response.headers)
    # print("Content:", response.content)
    
if __name__ == "__main__":
    client()