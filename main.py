import requests

url = 'https://store.steampowered.com/login/?redir=&redir_ssl=1&snr=1_4_4__global-header'  # Replace with the URL of the website you want to get cookies from

response = requests.get(url)
cookies = response.cookies

for cookie in cookies:
    print(f"Name: {cookie.name}")
    print(f"Value: {cookie.value}")
    print(f"Domain: {cookie.domain}")
    print(f"Path: {cookie.path}")
    print(f"Expires: {cookie.expires}")
    print("----")
