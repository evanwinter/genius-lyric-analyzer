import sys
import os
import re
import requests
import json
from bs4 import BeautifulSoup
import config

api = "https://api.genius.com"
client_access_token = config.client_access_token
headers = {'Authorization': 'Bearer ' + client_access_token}


def setup(artist_name, song_title):
	reload(sys)
	sys.setdefaultencoding('utf8')
	if not os.path.exists("output/"):
		os.makedirs("output/")
	outputfilename = "output/" + re.sub(r"[^A-Za-z]+", '', artist_name) + "-" + re.sub(r"[^A-Za-z]+", '', song_title) + ".txt"
	return outputfilename

def get_song(artist_name, song_title, outputfilename):
	search_url = api + "/search"
	data = {'q': song_title}
	response = requests.get(search_url, data=data, headers=headers)
	response_json = response.json()

	print("Looking for a match...")
	song_info = None
	
	hits = response_json["response"]["hits"]
	num_hits = len(hits)
	print(json.dumps(hits, indent=4, sort_keys=True))
	if num_hits == 0:
		print("No results for: " + song_title + " by " + artist_name + ".")

	for hit in hits:
		if hit["result"]["primary_artist"]["name"].lower() == artist_name.lower():
			print("Match found.")
			song_info = hit
			break

	if song_info:
		song_api_path = song_info["result"]["api_path"]
		lyrics = get_lyrics(song_api_path)
		with open(outputfilename, 'a') as f:
			f.write(lyrics)
	else:
		print("No match found.")	

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
	print lyrics
	return lyrics

def main():
	arguments = sys.argv[1:]
	song_title = arguments[0].translate(None, "\'\"")
	artist_name = arguments[1].translate(None, "\'\"")
	outputfilename = setup(artist_name, song_title)

	print('Looking for ' + song_title + ' by ' + artist_name + '...')

	get_song(artist_name, song_title, outputfilename)

if __name__ == '__main__':
	main()