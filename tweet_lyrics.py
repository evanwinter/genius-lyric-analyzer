

import sys
import os
import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
import twitter_config
from time import sleep

auth = OAuthHandler(twitter_config.consumer_key, twitter_config.consumer_secret)
auth.set_access_token(twitter_config.access_token, twitter_config.access_secret)

api = tweepy.API(auth)

if (not api):
	print ("Can't authenticate")
	sys.exit(-1)

def get_lyrics(file_name):
	f = 'output/'+file_name.lower().replace(' ', '')+'.txt'
	if os.path.isfile(f):
		my_file = open(f, 'r')
		file_lines = my_file.readlines()
		print("Getting lyrics...")
		return file_lines
	else:
		print("No lyrics for that artist.")
		pass

def tweet(lyrics):
	for line in lyrics:
		try:
			if (line != '\n') and ('[' not in line):
				api.update_status(line)
			else:
				pass
		except tweepy.TweepError as e:
			print(e.reason)

		sleep(10)

def print_lyrics(lyrics):
	for line in lyrics:
		if (line != '\n') and ('[' not in line):
			try:
				print(line)
				if (line != '\n') and ('[' not in line):
					api.update_status(line)
				else:
					pass
			except tweepy.TweepError as e:
				print(e.reason)
		sleep(0.5)

def main():
	arguments = sys.argv[1:]
	file_name = arguments[0]
	lyrics = get_lyrics(file_name)
	if lyrics:
		tweet(lyrics)
	else:
		print("Couldn't find lyrics.")

if __name__ == '__main__':
	main()