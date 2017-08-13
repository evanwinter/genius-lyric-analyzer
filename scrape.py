import requests

TOKEN = '4QovAN-T1mJa6hNLXvtNqTzI3J3uB73qYvQDJIyL2eQyOx-UHMtBEeNBWLhuFbW9'
base_url = "http://api.genius.com"

headers = {'Authorization': 'Bearer TOKEN'}
search_url = base_url + "/search"
song_title = "In the Midst of It All"
data = {'q': song_title}
response = requests.get(search_url, data=data, headers=headers)

print(data)