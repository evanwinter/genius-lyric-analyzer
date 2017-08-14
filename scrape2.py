#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

base_url = "https://api.genius.com"
headers = {'Authorization': 'Bearer 4QovAN-T1mJa6hNLXvtNqTzI3J3uB73qYvQDJIyL2eQyOx-UHMtBEeNBWLhuFbW9'}

song_title = "Codeine Crazy"
artist_name = "Future"

def lyrics_from_song_api_path(song_api_path):
  song_url = base_url + song_api_path
  response = requests.get(song_url, headers=headers)
  json = response.json()
  path = json["response"]["song"]["path"]

  page_url = "http://genius.com" + path
  page = requests.get(page_url)
  html = BeautifulSoup(page.text, "html.parser")

  [h.extract() for h in html('script')]

  lyrics = html.find("div", class_="lyrics").get_text()
  print lyrics
  return lyrics

if __name__ == "__main__":
  print("Starting...")
  search_url = base_url + "/search"
  data = {'q': song_title}
  response = requests.get(search_url, data=data, headers=headers)
  print(response)
  json = response.json()
  print(json)
  song_info = None
  for hit in json["response"]["hits"]:
    if hit["result"]["primary_artist"]["name"] == artist_name:
      song_info = hit
      break
  if song_info:
    song_api_path = song_info["result"]["api_path"]
    print lyrics_from_song_api_path(song_api_path)