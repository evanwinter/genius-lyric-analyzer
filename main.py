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

def get_artist_from_name(raw_artist_name):
	search_url = api + "/search"
	data = { 'q': raw_artist_name }
	res = requests.get(search_url, data=data, headers=headers)
	response = res.json()
	hits = response["response"]["hits"]
	
	# If the raw search yields no results at all...
	if len(hits) == 0:
		print("No results for " + raw_artist_name + ".")
		# TODO: Prompt for another search instead of exiting the program.
		return 
	
	artist_search_results = []

	for hit in hits:
		hit_id = hit["result"]["primary_artist"]["id"]
		artist_search_results.append(hit_id)
	
	# Target the primary artist responsible for the greatest number of songs yielded by the raw search.
	# e.g. A search for 'Lil' will yield songs by Wanye AND Uzi. Target artist is whoever has most songs in results.
	most_common_results = Counter(artist_search_results).most_common()
	raw_target_artist = most_common_results[0]

	# TODO make this not suck
	# format Counter results -- only want the name of the top artist
	target_artist_id = str(raw_target_artist).replace("(", "").split(",")[0] # .replace("(u'", "").replace("', ", ',').replace(")", "").split(',')[0]

	# Return the artist who matches the target artist name.
	for hit in hits:
		artist = hit["result"]["primary_artist"]
		artist_id = str(artist["id"])
		if artist_id == target_artist_id:
			return artist

def setup_output(artist):
	reload(sys)
	sys.setdefaultencoding("utf8")
	stripped_artist_name = re.sub(r"[^A-Za-z0-9$]+", "", artist["name"].lower())
	if not os.path.exists("output/"):
		os.makedirs("output/")
	if not os.path.exists("output/" + stripped_artist_name + "/"):
		os.makedirs("output/" + stripped_artist_name + "/")

	output_file = "output/" + stripped_artist_name + "/" + stripped_artist_name + "-lyrics.txt"
	return output_file

def get_all_songs(artist):

	current_page = 1
	next_page = True

	song_lyrics = ""
	all_lyrics = ""
	all_songs = []

	while next_page:

		print(str(len(all_songs)) + " songs found...")

		artist_songs_url = api + "/artists/" + str(artist["id"]) + "/songs"
		params = {
			"page": current_page,
			"sort": "popularity",
			"per_page": 50
		}
		data = {}
		res = requests.get(artist_songs_url, data=data, headers=headers, params=params)
		response = res.json()
		songs = response["response"]["songs"]

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

	songs = []

	song_lyrics = ""
	limit_lyrics = ""
	limit_songs = []

	while next_page and len(songs) < limit:

		artist_songs_url = api + "/artists/" + str(artist["id"]) + "/songs"
		params = {
			"page": current_page,
			"sort": "popularity",
			"per_page": 5
		}
		data = {}
		res = requests.get(artist_songs_url, data=data, headers=headers, params=params)
		response = res.json()
		songs = response["response"]["songs"]

		if songs:
			current_page += 1

		else:
			next_page = False

		limit_songs += songs
		count += 1

		if songs:
			print(str(len(limit_songs)) + " songs found.")

	return limit_songs
	
def get_all_lyrics(songs, artist, output_file):
	all_lyrics = ""
	all_count = 0
	count = 0
	all_songs = songs
	num_songs = len(all_songs)

	for song in all_songs:
		all_count += 1
		print(str(all_count) + " / " + str(num_songs))
		print("Title: " + str(song["title"]))
		
		if title_fits_criteria(song, artist):

			song_lyrics = get_song_lyrics(song)
			write_lyrics(song, song_lyrics, output_file)
			print("Stored lyrics for " + song["title"] + ".")

			count += 1
			print(str(count) + " songs stored.\n")

			all_lyrics += song_lyrics

	return all_lyrics

def get_song_lyrics(song):
	this_song = song
	song_lyrics_url = genius_url + this_song["path"]

	page = requests.get(song_lyrics_url)
	html = BeautifulSoup(page.text, "html.parser")
	[h.extract() for h in html("script")]

	song_lyrics = html.find("div", class_="lyrics").get_text()

	return song_lyrics

def title_fits_criteria(song, artist):
	
	passes_filter = True

	title_filterwords = [ "tracklist", "credits", "[speech", "(speech", "speech]", "speech)", "(live", "[live", "album art", "remix", "reprise)", "reprise]", "live version", "version)", "version]", "radio edit", "interview", "[hook", "[booklet", "live in", "live from", "(mix", "[mix", "mix)", "mix]" ]

	if artist["id"] != song["primary_artist"]["id"]:
		print("Not primary artist.\n")
		passes_filter = False
		return passes_filter
	for filterword in title_filterwords:
		if filterword in song["title"].lower():
			print("Tracklist, credits, remix, live version or speech ignored.")
			print("Flagged word: " + filterword + "\n")
			passes_filter = False
			return passes_filter

	return passes_filter

def format_lyrics(lyrics):
	
	formatted_lyrics = lyrics.split()
	formatted_lyrics = ["".join(c for c in s if c not in string.punctuation) for s in formatted_lyrics]
	formatted_lyrics = [s.lower() for s in formatted_lyrics if s]
	formatted_lyrics = str(formatted_lyrics).replace(", (", "").replace("',", "").replace("u'", "").replace("[", "").replace("']", "")

	return formatted_lyrics

def write_lyrics(song, lyrics, output_file):
	with open(output_file, "a") as f:
		# write song header
		f.write("------------------------------------------------------\n")
		f.write("Title: " + song["title"] + "\n")
		try:
			pageviews = song["stats"]["pageviews"]
			f.write("Pageviews: " + str(pageviews) + "\n")
		except:
			f.write("Pageview data unavailable.\n")
		f.write("------------------------------------------------------\n")

		# write lyrics
		f.write(lyrics)

def setup_analysis_output( artist, songs ):
	artist_name = artist["name"]
	stripped_artist_name = re.sub(r"[^A-Za-z0-9$]+", "", artist_name.lower())
	analysis_output_file = "output/" + stripped_artist_name + "/" + stripped_artist_name + "-analysis.txt"
	with open(analysis_output_file, "w") as f:
		# write analysis header
		f.write("\n------------------------------------------------------\n")
		f.write(artist_name + "\n")
		f.write("Number of songs: " + str(len(songs)) + "\n")
	return analysis_output_file

def analyze_lyrics( lyrics, analysis_output_file ):
	all_lyrics = lyrics
	all_tokens = nltk.word_tokenize(all_lyrics)
	
	most_common_words = Counter(all_tokens).most_common()

	num_words = len(all_tokens)
	num_unique_words = len(set(all_tokens))

	lexical_diversity = float(num_unique_words) / num_words
	lexical_diversity_percentage = lexical_diversity * 100

	with open(analysis_output_file, "a") as f:
		f.write("Total number of words: " + str(num_words) + "\n")
		f.write("Number of unique words: " + str(num_unique_words) + "\n")
		f.write("Lexical diversity: " + str(lexical_diversity_percentage) + "%\n")
		f.write('------------------------------------------------------\n')
		f.write("\nword,frequency\n----\n")
		f.write(str(most_common_words).replace("[('", "").replace("[", "").replace("]", "").replace("('", '\n').replace("),", "").replace("', ", ',').replace(")", "") + "\n")

def lookup_word_frequency( word, analysis_output_file ):

	with open(analysis_output_file, "r") as f:
		for line in f:
			split_line = line.split(",")
			this_word = split_line[0]
			if len(split_line) > 1:
				this_frequency = split_line[1].replace("\n", "")
			else:
				this_frequency = 0
			if this_word == word:
				return this_frequency
		print("\nCouldn't find that word in lyrics.")
		return 0

def plot_word_frequency( lyrics, artist ):
	print("Plotting word frequency...")
	print("Close the pop-up window to continue.")
	all_lyrics = lyrics
	all_tokens = nltk.word_tokenize(all_lyrics)

	# set up filters
	boring_words = [ "the", "i", "you", "and", "me", "a", "it", "im", "my", "to", "on", "in", "that", "wan", "na", "is", "your", "so", "of", "its", "for", "at" ]
	digits = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
	song_structure_words = [ "[intro", "[verse", "[chorus", "[hook", "[prechorus", "[bridge", "intro", "verse", "chorus", "hook", "prechorus" ]
	artist_names = nltk.word_tokenize(str(artist["name"]).lower())

	filtered_tokens = [ x for x in all_tokens if ((x not in boring_words) and (x not in song_structure_words) and (x not in digits) and (x not in artist_names)) ]

	# plot the n most common tokens - hard to see more than ~50 on a 13" display
	num_to_plot = 50

	fdist = nltk.FreqDist(filtered_tokens)
	fdist.plot(num_to_plot)

#  TODO
def print_analysis(analysis_output_file):
	with open(analysis_output_file, "r") as f:
		print(f.read())

def main():
	print("\nWelcome to the lyric analyzer!")

	quit = False

	while quit is False:

		# Get artist and collect their data
		proceed = ""
		while proceed is not "y":
			artist = None
			while artist is None:
				raw_artist_name = raw_input("Enter an artist or band name: ")
				artist = get_artist_from_name(raw_artist_name)
			artist_name = artist["name"]

			proceed = str(raw_input("\nDid you mean " + artist_name + "? (y/n) "))

		output_file = setup_output(artist)

		# Set song_limit to None to activate song limits.
		song_limit = 1
		while not song_limit:
		    try:
		        song_limit = raw_input("How many songs? (Choose a multiple of 5 or 'all' for all songs): ").lower()
		        if (song_limit == "all"):
		        	song_limit = 100000000000
		        	print('Getting all songs by ' + artist_name + '...')
		        	songs = get_all_songs(artist)
		        else:
		        	song_limit = int(song_limit)
		        	print('Getting the top ' + str(song_limit) + ' songs by ' + artist_name.upper() + '...')
		        	songs = get_limit_songs(artist, song_limit)
		    except ValueError:
	        	print("Please enter a valid number or 'all'.")
	        	song_limit = None

	 	print("Finding songs by " + artist_name + "...\n(This may take a minute)\n")
	 	songs = get_all_songs(artist)
		
		print("Found " + str(len(songs)) + " songs in total.\n")

		print("Getting lyrics...\n")
		all_lyrics = get_all_lyrics(songs, artist, output_file)

		print("Preparing lyrics for analysis...")
		formatted_lyrics = format_lyrics(all_lyrics)

		print("Setting up analysis output files...")
		analysis_output_file = setup_analysis_output(artist, songs)

		print("Analyzing lyrics...")
		analyze_lyrics(formatted_lyrics, analysis_output_file)

		#  Get user choice.
		choice = ""

		while choice != "quit":

			print("\n[" + artist_name + "] | What would you like to do?")
			print("------------------------------------------------------")
			print("(1) Look at word frequency distribution graph")
			print("(2) Look up a word frequency")
			print("(3) Print all song lyrics")
			print("(4) Print analysis file\n")
			choice = str(raw_input("Enter your choice (1-4) or 'quit': "))

			if choice == "1":
				plot_word_frequency(formatted_lyrics, artist)
			elif choice == "2":
				word = str(raw_input("Enter a word to look up: "))
				freq = lookup_word_frequency(word, analysis_output_file)
				print("\n****************")
				print("Frequency: " + str(freq))
				print("****************")
			elif choice == "3":
				print(all_lyrics)
			elif choice == "4":
				print_analysis(analysis_output_file)
			elif choice == "quit":
				break
			else:
				choice = ""

		y = ""
		while y is not "y":
			if y is "n":
				print("Goodbye.")
				sys.exit(-1)
			else:
				y = str(raw_input("Would you like to try another artist? (y/n) "))


if __name__ == "__main__":
	main()