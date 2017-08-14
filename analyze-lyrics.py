import sys
import os
import re
import requests
import json
import string
from bs4 import BeautifulSoup
import config
from collections import Counter

api = "https://api.genius.com"
client_access_token = config.client_access_token
headers = {'Authorization': 'Bearer ' + client_access_token}

def setup(artist_name):
	reload(sys)
	sys.setdefaultencoding('utf8')
	if not os.path.exists("output/"):
		os.makedirs("output/")
	lyrics_output = "output/" + re.sub(r"[^A-Za-z]+", '', artist_name) + ".txt"
	return lyrics_output

def get_songs(artist_name, lyrics_output):
	search_url = api + "/search"
	data = {'q': artist_name}
	response = requests.get(search_url, data=data, headers=headers)
	response_json = response.json()

	print("Looking for a match...")
	song_info = None
	
	hits = response_json["response"]["hits"]
	num_hits = len(hits)
	if num_hits == 0:
		print("No results for: " + artist_name + ".")

	lyrics = ''
	all_lyrics = ''

	for hit in hits:
		song_info = hit
		song_api_path = song_info["result"]["api_path"]
		lyrics = get_lyrics(song_api_path).lower()
		with open(lyrics_output, 'a') as f:
			f.write(lyrics)
			all_lyrics += lyrics

	with open(lyrics_output, 'a') as f:
		f.write(str(Counter(all_lyrics.split()).most_common()))

def get_lyrics(song_api_path):
	song_url = api + song_api_path
	response = requests.get(song_url, headers=headers)
	response_json = response.json()
	path = response_json["response"]["song"]["path"]

	page_url = "http://genius.com" + path
	page = requests.get(page_url)
	html = BeautifulSoup(page.text, "html.parser")

	[h.extract() for h in html('script')]

	lyrics = html.find("div", class_="lyrics").get_text()
	return lyrics

def main():
	arguments = sys.argv[1:]
	artist_name = arguments[0].translate(None, "\'\"")
	lyrics_output = setup(artist_name)

	print('Looking for songs by ' + artist_name + '...')

	get_songs(artist_name, lyrics_output)

if __name__ == '__main__':
	main()