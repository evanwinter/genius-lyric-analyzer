import sys
import os
import re
import config
import requests
import json
from bs4 import BeautifulSoup
from collections import Counter
import string
import nltk

api = "https://api.genius.com"
genius_url = "http://genius.com"
CLIENT_ACCESS_TOKEN = config.client_access_token
headers = { 'Authorization': 'Bearer ' + CLIENT_ACCESS_TOKEN }

def get_artist_from_name(artist_name):
	search_url = api + "/search"
	data = { 'q': artist_name }
	res = requests.get(search_url, data=data, headers=headers)

	response = res.json()
	hits = response['response']['hits']
	
	if len(hits) == 0:
		print('No results for ' + artist_name + '.')
		sys.exit('Exiting program.')
	
	artist = hits[0]['result']['primary_artist']

	return artist

def setup_output(artist):
	reload(sys)
	sys.setdefaultencoding('utf8')
	artist_name = re.sub(r"[^A-Za-z]+", '', artist['name'].lower())
	if not os.path.exists('output/'):
		os.makedirs('output/')
	if not os.path.exists('output/' + artist_name + '/'):
		os.makedirs('output/' + artist_name + '/')

	output_file = 'output/' + artist_name + '/' + artist_name + '-lyrics.txt'
	return output_file

def get_all_songs(artist):

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

def get_limit_songs(artist, song_limit):

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
	
def get_all_lyrics(songs, artist, output_file):
	all_songs = songs
	num_songs = len(all_songs)
	all_lyrics = ''
	count = 0
	all_count = 0

	for song in all_songs:
		all_count += 1
		print(str(all_count) + ' / ' + str(num_songs))		
		print('Name: ' + str(song['title']))
		if fits_criteria(song, artist):
			song_lyrics = get_song_lyrics(song)
			all_lyrics += song_lyrics
			count += 1
			write_lyrics(song, song_lyrics, output_file)
			print('Stored lyrics for ' + song['title'] + ' at ' + str(output_file))
			print(str(count) + ' songs stored.\n')

	return all_lyrics

def get_song_lyrics(song):
	this_song = song
	song_lyrics_url = genius_url + this_song['path']

	page = requests.get(song_lyrics_url)
	html = BeautifulSoup(page.text, "html.parser")
	[h.extract() for h in html('script')]

	song_lyrics = html.find("div", class_="lyrics").get_text()

	return song_lyrics

def fits_criteria(song, artist):
	
	passes_filter = True

	title_filterwords = [ "tracklist", "credits", "[speech", "(speech", "speech]", "speech)", "(live", "[live", "album art", "remix", "reprise)", "reprise]", "live version", "version)", "version]", "radio edit", "interview", "[hook", "[booklet" ]

	if artist['id'] != song['primary_artist']['id']:
		print('Not primary artist.\n')
		passes_filter = False
		return passes_filter
	for filterword in title_filterwords:
		if filterword in song['title'].lower():
			print('Tracklist, credits, remix, live version or speech ignored.')
			print('Flagged word: ' + filterword + '\n')
			passes_filter = False
			return passes_filter

	return passes_filter

def format_lyrics(lyrics):
	
	formatted_lyrics = lyrics.split()
	formatted_lyrics = [''.join(c for c in s if c not in string.punctuation) for s in formatted_lyrics]
	formatted_lyrics = [s.lower() for s in formatted_lyrics if s]
	formatted_lyrics = str(formatted_lyrics).replace(', (', '\n').replace("',", '').replace("u'", '').replace("[", '').replace("']", '')

	return formatted_lyrics

def write_lyrics(song, lyrics, output_file):
	with open(output_file, 'a') as f:
		f.write('------------------------------------------------------\n')
		f.write('Title: ' + song['title'] + '\n')
		try:
			pageviews = song['stats']['pageviews']
			f.write('Pageviews: ' + str(pageviews) + '\n')
		except:
			f.write('Pageview data unavailable.\n')
		f.write('------------------------------------------------------\n')
		f.write(lyrics)

def setup_analysis_output( artist, songs ):
	artist_name = re.sub(r"[^A-Za-z]+", '', artist['name'].lower())
	analysis_output_file = 'output/' + artist_name + '/' + artist_name + '-analysis.txt'
	with open(analysis_output_file, 'w') as f:
		f.write('------------------------------------------------------\n')
		f.write(artist['name'] + '\n')
		f.write('Number of songs: ' + str(len(songs)))
	return analysis_output_file

def analyze_lyrics( lyrics, analysis_output_file ):
	all_lyrics = lyrics
	all_tokens = nltk.word_tokenize(all_lyrics)
	
	most_common_words = Counter(all_tokens).most_common()

	num_words = len(all_tokens)
	num_unique_words = len(set(all_tokens))

	lexical_diversity = float(num_unique_words) / num_words
	lexical_diversity_percentage = lexical_diversity * 100

	with open(analysis_output_file, 'a') as f:
		f.write('Total number of words: ' + str(num_words) + '\n')
		f.write('Number of unique words: ' + str(num_unique_words) + '\n')
		f.write('Lexical diversity: ' + str(lexical_diversity_percentage) + '%\n')
		f.write('------------------------------------------------------\n')
		f.write(str(most_common_words).replace("[('", '').replace('[', '').replace(']', '').replace("('", '\n').replace("),", '').replace("', ", ',').replace(')', ''))

#  TODO
def lookup_word( word ):
	print('Looking up the frequency of "' + word + '"...\n')

def plot_word_frequency( lyrics, artist ):
	print("Plotting word frequency...")
	print("Close the pop-up window to continue.\n")
	all_lyrics = lyrics
	all_tokens = nltk.word_tokenize(all_lyrics)

	# set up filters
	boring_words = [ 'the', 'i', 'you', 'and', 'me', 'a', 'it', 'im', 'my', 'to', 'on', 'in', 'that', 'wan', 'na', 'is', 'your', 'so', 'of', 'its', 'for', 'at' ]
	digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
	song_structure_words = [ '[intro', '[verse', '[chorus', '[hook', '[prechorus', '[bridge', 'intro', 'verse', 'chorus', 'hook', 'prechorus' ]
	artist_names = nltk.word_tokenize(str(artist['name']).lower())

	filtered_tokens = [ x for x in all_tokens if ((x not in boring_words) and (x not in song_structure_words) and (x not in digits) and (x not in artist_names)) ]

	# plot the n most common tokens - hard to see more than ~50 on a 13" display
	num_to_plot = 50

	fdist = nltk.FreqDist(filtered_tokens)
	fdist.plot(num_to_plot)

#  TODO
def print_lyrics():
	print("Printing lyrics...\n")

#  TODO
def open_analysis():
	print("Open analysis\n")


def main():
	print('\nWelcome to the lyric analyzer!\n')

	# Get artist and collect their data
	artist_name = raw_input("Enter an artist or band name: ")

	print('\nLooking up artist...\n')
	artist = get_artist_from_name(artist_name)

	print('Setting up output files...\n')
	output_file = setup_output(artist)

	song_limit = None
	while not song_limit:
	    try:
	        song_limit = raw_input("How many songs? ('all' for all songs): ").lower()
	        if (song_limit == "all"):
	        	song_limit = 100000000000
	        	print('\nFinding all songs by ' + artist['name'].upper() + '...\n')
	        	songs = get_all_songs(artist)
	        else:
	        	song_limit = int(song_limit)
	        	print('\nFinding the top ' + str(song_limit) + ' songs by ' + artist['name'].upper() + '...\n')
	        	songs = get_limit_songs(artist, song_limit)
	    except ValueError:
        	print("Please enter a valid number or 'all'.\n")
        	song_limit = None
	
	print('Found ' + str(len(songs)) + ' songs.\n')

	print('Scraping lyrics for each song...\n')
	all_lyrics = get_all_lyrics(songs, artist, output_file)

	print('Formatting lyrics for analysis...\n')
	formatted_lyrics = format_lyrics(all_lyrics)

	print("Setting up analysis output files...\n")
	analysis_output_file = setup_analysis_output(artist, songs)

	print("Pre-analyzing...\n")
	analyze_lyrics(formatted_lyrics, analysis_output_file)

	#  Get user choice.
	print('What would you like to do?')
	print('------------------------------------------------------')
	print("(1) Look at word frequency distribution graph")
	print("(2) Look up a word or phrase frequency")
	print("(3) Print all song lyrics")
	print("(4) Open analysis file")
	print('------------------------------------------------------')
	choice = str(raw_input("Enter your choice (1-4) or 'quit': "))
	target = ''
	quit = False

	while choice != 'quit':
		if choice == "1":
			plot_word_frequency(formatted_lyrics, artist)
		elif choice == "2":
			word = str(raw_input("What word would you like to look up? "))
			lookup_word( word )
		elif choice == "3":
			print(all_lyrics)
		elif choice == "4":
			open_analysis()
		else:
			choice = str(raw_input("Invalid input.\nEnter your choice (1-4): "))
		print('------------------------------------------------------')
		print("(1) Look at word frequency distribution graph")
		print("(2) Look up a word or phrase frequency")
		print("(3) Print all song lyrics")
		print("(4) Open analysis file")
		print('------------------------------------------------------')
		choice = str(raw_input("Enter another choice (1-4) or 'quit': "))

	sys.exit(-1)

if __name__ == '__main__':
	main()