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

def get_artist_songs(artist_id, output):
	return output


def main():
	arguments = sys.argv[1:]
	artist_name = arguments[0].translate(None, "\'\"")
	output = setup(artist_name)

	print('Looking for songs by ' + artist_name + '...')

if __name__ == '__main__':
	main()