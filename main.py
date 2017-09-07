import sys
import os
import re
import config
import requests
import json
from bs4 import BeautifulSoup
from collections import Counter
import string
# import nltk

api = "https://api.genius.com"
genius_url = "http://genius.com"
client_access_token = config.client_access_token
headers = { 'Authorization': 'Bearer ' + client_access_token }

def get_artist_from_name( artist_name ):
	search_url = api + "/search"
	data = { 'q': artist_name }
	res = requests.get( search_url, data=data, headers=headers )

	response = res.json()
	hits = response['response']['hits']
	
	if len(hits) == 0:
		print('No results for ' + artist_name + '.')
		sys.exit('Exiting program.')
	
	artist = hits[0]['result']['primary_artist']

	return artist

def setup_output( artist ):
	reload(sys)
	sys.setdefaultencoding('utf8')
	if not os.path.exists('output/'):
		os.makedirs('output/')
	output_file = 'output/' + re.sub(r"[^A-Za-z]+", '', artist['name'].lower()) + '.txt'
	return output_file

def get_all_songs( artist ):

	current_page = 1
	next_page = True

	song_lyrics = ''
	all_lyrics = ''
	all_songs = []

	while next_page:

		artist_songs_url = api + '/artists/' + str(artist['id']) + '/songs'
		params = {
			'page': current_page,
			'sort': 'popularity',
			'per_page': 50
		}
		data = {}
		res = requests.get(artist_songs_url, data=data, headers=headers, params=params)
		response = res.json()
		songs = response['response']['songs']

		if songs:
			current_page += 1

		else:
			next_page = False

		all_songs += songs

	return all_songs

def get_limit_songs( artist, song_limit ):

	current_page = 1
	next_page = True
	limit = song_limit
	count = 0

	song_lyrics = ''
	limit_lyrics = ''
	limit_songs = []

	while next_page and count < song_limit:

		artist_songs_url = api + '/artists/' + str(artist['id']) + '/songs'
		params = {
			'page': current_page,
			'sort': 'popularity',
			'per_page': 1
		}
		data = {}
		res = requests.get(artist_songs_url, data=data, headers=headers, params=params)
		response = res.json()
		songs = response['response']['songs']

		if songs:
			current_page += 1

		else:
			next_page = False

		limit_songs += songs
		count += 1

	return limit_songs
	
def get_all_lyrics( songs, artist, output_file ):
	all_songs = songs
	all_lyrics = ''
	count, all_count = 0

	for song in all_songs:
		all_count += 1
		print('\n' + str(all_count))		
		print('Name: ' + song['title'])
		if fits_criteria(song, artist):
			song_lyrics = get_song_lyrics( song )
			all_lyrics += song_lyrics
			count += 1
			write_lyrics( song, song_lyrics, output_file )
			print('Stored lyrics for ' + song['title'])
			print(str(count) + ' stored.')
	return all_lyrics

def get_song_lyrics( song ):
	this_song = song
	song_lyrics_url = genius_url + this_song['path']

	page = requests.get(song_lyrics_url)
	html = BeautifulSoup(page.text, "html.parser")
	[h.extract() for h in html('script')]
	song_lyrics = html.find("div", class_="lyrics").get_text()

	return song_lyrics

def fits_criteria( song, artist ):
	
	passes_filter = True

	if "tracklist" in song['title'].lower():
		print('Tracklist ignored.')
		passes_filter = False
	if artist['id'] != song['primary_artist']['id']:
		print('Not primary artist.')
		passes_filter = False
	if "credits" in song['title'].lower():
		print('Credits ignored.')
		passes_filter = False

	return passes_filter

def format_lyrics( lyrics ):
	
	formatted_lyrics = lyrics.split()
	formatted_lyrics = [''.join(c for c in s if c not in string.punctuation) for s in formatted_lyrics]
	formatted_lyrics = [s.lower() for s in formatted_lyrics if s]
	formatted_lyrics = str(formatted_lyrics).replace(', (', '\n').replace("',", '').replace("u'", '').replace("[", '').replace("']", '')

	return formatted_lyrics

def write_lyrics( song, lyrics, output_file ):
	with open(output_file, 'a') as f:
		f.write( song['title'] )
		f.write( '\n------------------------------------------------------\n------------------------------------------------------' )
		f.write(lyrics)

def analyze_lyrics( lyrics, artist ):
	# all_tokens = nltk.word_tokenize( lyrics )

	analysis_output_file = 'output/' + re.sub(r"[^A-Za-z]+", '', artist['name'].lower()) + '-analysis.txt'

	most_common_words = Counter(lyrics.split()).most_common()

	with open(analysis_output_file, 'w') as f:
		f.write(str(most_common_words).replace("[('", '').replace('[', '').replace(']', '').replace("('", '\n').replace("),", '').replace("', ", ',').replace(')', ''))

	# boring_words = [ 'the', 'i', 'you', 'and', 'me', 'a', 'it', 'im', 'my' ]

	# all_tokens = all_tokens - boring_words

	# fdist = nltk.FreqDist(all_tokens)
	# fdist.plot(50)

def main():
	print('\nWelcome to the lyric analyzer!')
	artist_name = raw_input("\nEnter an artist or band name: ")

	print('\nLooking up artist...')
	artist = get_artist_from_name( artist_name )

	print('\nSetting up output files...')
	output_file = setup_output( artist )

	song_limit = None
	while not song_limit:
	    try:
	        song_limit = raw_input("\nHow many songs? ('all' for all songs): ").lower()
	        if (song_limit == "all"):
	        	song_limit = 100000000000
	        	print('\nFinding all songs by ' + artist['name'].upper() + '...')
	        	songs = get_all_songs( artist )
	        else:
	        	song_limit = int(song_limit)
	        	print('\nFinding the top ' + str(song_limit) + ' songs by ' + artist['name'].upper() + '...')
	        	songs = get_limit_songs( artist, song_limit )
	    except ValueError:
        	print("Please enter a valid number or 'all'.")
        	song_limit = None	
	
	print('\nFound ' + str(len(songs)) + ' songs.')

	print('\nScraping lyrics for each song...')
	all_lyrics = get_all_lyrics( songs, artist, output_file )

	print('\nFormatting lyrics for analysis...')
	formatted_lyrics = format_lyrics( all_lyrics )

	print('\nAnalyzing lyrics...')
	analyze_lyrics( formatted_lyrics, artist )

if __name__ == '__main__':
	main()