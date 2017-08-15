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
	output = "output/" + re.sub(r"[^A-Za-z]+", '', artist_name) + ".txt"
	return output

def get_songs(artist_id, output, limit):

	current_page = 1
	next_page = True
	songs_array = []

	lyrics = ''
	all_lyrics = ''
	artist_id_string = str(artist_id)
	count = 0
	all_count = 0
	song_limit = limit

	while (next_page and all_count < song_limit):

		artist_songs_url = api + "/artists/"+artist_id_string+"/songs"
		params = {
			'page': current_page,
			'sort': 'popularity',
			'per_page': 50
		}
		data = {}
		response = requests.get(artist_songs_url, data=data, headers=headers, params=params)
		response_json = response.json()
		songs_list = response_json["response"]["songs"]

		if songs_list:
			songs_array += songs_list
			print('Trying page ' + str(current_page))
			current_page += 1
		else:
			next_page = False

		for song in songs_list:
			all_count += 1
			song_api_path = song["api_path"]
			if (song["primary_artist"]["id"] == artist_id):
				if ('tracklist' not in song["title"].lower()):
					print('Stored lyrics for ' + song["title"] + '.')
					count += 1
					lyrics = get_lyrics(song_api_path).lower()

					all_lyrics += lyrics
					with open(output, 'a') as f:
						f.write(lyrics)
				else:
					print("Tracklist ignored.")
			else:
				print('Not primary artist on ' + song["title"])

	print("Analyzing lyrics...")
	with open(output, 'a') as f:
		f.write(str(Counter(all_lyrics.split()).most_common()).replace(', (', '\n'))
	
	print('Songs looked at: ' + str(all_count))
	print('Songs scraped: ' + str(count))

	return output

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

def get_artist(artist_name):

	search_url = api + "/search"
	data = {'q': artist_name}
	response = requests.get(search_url, data=data, headers=headers)
	
	response_json = response.json()

	song_info = None
	
	hits = response_json["response"]["hits"]
	num_hits = len(hits)
	if num_hits == 0:
		print("No results for: " + artist_name + ".")
	
	top_artist_id = response_json["response"]["hits"][0]["result"]["primary_artist"]["id"]

	return top_artist_id


def main():
	arguments = sys.argv[1:]
	artist_name = arguments[0].translate(None, "\'\"")
	if arguments[1]:
		limit = arguments[1].translate(None, "\'\"")
	else:
		limit = 10000000
	print('Looking for artist...')
	artist_id = get_artist(artist_name)
	output = setup(artist_name)
	print('Getting lyrics to songs by ' + artist_name + '...')
	get_songs(artist_id, output, limit)

if __name__ == '__main__':
	main()