import requests

def fetch_github_repos(username, is_private=True, token=None):
    GITHUB_API_URL = "https://api.github.com/users/{}/repos"
    headers = {}
    if is_private and token:
        headers['Authorization'] = f'token {token}'

    response = requests.get(GITHUB_API_URL.format(username), headers=headers)

    if response.status_code == 200:
        return response.json()
    else: 
        return None