import sys
import os
import re
import requests
import json
import string
import time
from bs4 import BeautifulSoup
import config
from collections import Counter

import nltk

api = "https://api.genius.com"
client_access_token = config.client_access_token
headers = { 'Authorization': 'Bearer ' + client_access_token }

def setup(artist_name):
	output = re.sub(r"[^A-Za-z]+", '', artist_name) + ".txt"
	return output

def analyze_lyrics(lyrics):
	analyzed_lyrics = Counter(lyrics.split()).most_common()
	return analyzed_lyrics

def format_lyrics(lyrics):
	formatted_lyrics = lyrics.split()
	formatted_lyrics = [''.join(c for c in s if c not in string.punctuation) for s in formatted_lyrics]
	formatted_lyrics = [s for s in formatted_lyrics if s]
	formatted_lyrics = str(formatted_lyrics).replace(', (', '\n').replace("',", '').replace("u'", '')
	return formatted_lyrics

def format_output(lyrics):
	analyzed_lyrics = lyrics
	formatted_output = str(analyzed_lyrics).replace("[('", '').replace("), ('", '\n').replace("',", ':')
	return formatted_output

def filter_songs( songs_list ):
	songs_list = songs_list

def fits_criteria( song, artist_id ):
	fits = True
	song = song

	if (song['primary_artist']['id'] != artist_id):
		fits = False
	if ('tracklist' in song['title'].lower().replace("[",'').replace("]",'')):
		fits = False

	return fits

def analyze(lyrics):
	# nltk.download()
	stop_words = set(nltk.corpus.stopwords.words('english'))
	stop_words.update(['.', ',', "'", '"', '?', '!', ':', ';', '(', ')', '[', ']', '{', '}', '/'])

	all_lyrics = lyrics

	all_tokens = nltk.word_tokenize(all_lyrics)

	all_tokens = [token.lower() for token in all_tokens if token.lower() not in stop_words] # if token.lower() not in stop_words
	print(all_tokens)
	fdist = nltk.FreqDist(all_tokens)
	fdist.plot(10)

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
	print('Song limit: '+str(song_limit))

	while ((next_page) and (all_count < song_limit)):

		artist_songs_url = api + "/artists/"+artist_id_string+"/songs"
		params = {
			'page': current_page,
			'sort': 'popularity',
			'per_page': 10
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
			print('Name: '+song['title'])
			all_count += 1
			song_api_path = song["api_path"]
			lyrics = get_lyrics(song_api_path).lower()

			with open(output, 'a') as f:
				if (fits_criteria(song, artist_id)):
					f.write(lyrics)
					print('Stored lyrics for ' + song['title'] + '.')
					count+=1
					print('Stored count: '+str(count))
					all_lyrics += lyrics

			print('All count: '+str(all_count))
			print('')


	print('Songs looked at: ' + str(all_count))
	print('Songs scraped: ' + str(count))
	print("Analyzing lyrics...")
	
	formatted_output = format_output(analyze_lyrics(format_lyrics(all_lyrics)))
	
	print('.')
	time.sleep(.2)
	print('..')
	time.sleep(.2)
	print('...')
	time.sleep(.2)
	print('....')
	time.sleep(.2)
	print("Done.")

	print(all_lyrics)

	analyze(all_lyrics)

	with open('analyses.txt', 'a') as af:
		af.write(formatted_output)

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
	artist_name = arguments[0]
	if len(arguments) > 1:
		limit = arguments[1]
	else:
		limit = 5
	print('Looking for artist...')
	artist_id = get_artist(artist_name)
	output = setup(artist_name)
	print('Getting lyrics to songs by ' + artist_name + '...')
	get_songs(artist_id, output, limit)

if __name__ == '__main__':
	main()