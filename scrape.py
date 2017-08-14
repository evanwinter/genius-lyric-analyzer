import sys
import urllib2
import json
import os
import re
import codecs
import socket
import csv
from socket import AF_INET, SOCK_DGRAM

import config

api = 'https://api.genius.com'

client_access_token = config.client_access_token

def setup(search_term):
	reload(sys)
	sys.setdefaultencoding('utf8')
	if not os.path.exists("output/"):
		os.makedirs("output/")
	outputfilename = "output/output-" + re.sub(r"[^A-Za-z]+", '', search_term) + ".json"
	return outputfilename


def search(search_term,outputfilename,client_access_token):

	with codecs.open(outputfilename, 'ab', encoding='utf8') as outputfile:
		page = 1
		while True:
			querystring = api + "/search?q=" + urllib2.quote(search_term) + "&page=" + str(page)
			request = urllib2.Request(querystring)
			request.add_header("Authorization", "Bearer " + client_access_token)
			request.add_header("User-Agent", "curl/7.9.8  (i686-pc-linux-gnu) libcurl 7.9.8 (OpenSSL 0.9.6b) (ipv6 enabled)")
			while True:
				try:
					response = urllib2.urlopen(request, timeout=4)
					raw = response.read()
				except socket.timeout:
					print("Timeout raised and caught")
					continue
				break
			json_obj = json.loads(raw)
			
			outputfile.write(json.dumps(json_obj, indent=4, sort_keys=True) + '\n')
			
			body = json_obj["response"]["hits"]

			num_hits = len(body)
			
			if num_hits == 0:
				if page == 1:
					print("No results for: " + search_term)
				break
			
			print("page {0}; num hits {1}".format(page, num_hits))	

			# for result in body:
			#     result_id = result["result"]["id"]
			#     title = result["result"]["title"]
			#     url = result["result"]["url"]
			#     path = result["result"]["path"]
			#     header_image_url = result["result"]["header_image_url"]
			#     annotation_count = result["result"]["annotation_count"]
			#     pyongs_count = result["result"]["pyongs_count"]
			#     primaryartist_id = result["result"]["primary_artist"]["id"]
			#     primaryartist_name = result["result"]["primary_artist"]["name"]
			#     primaryartist_url = result["result"]["primary_artist"]["url"]
			#     primaryartist_imageurl = result["result"]["primary_artist"]["image_url"]
			#     row=[page,result_id,title,url,path,header_image_url,annotation_count,pyongs_count,primaryartist_id,primaryartist_name,primaryartist_url,primaryartist_imageurl]

			page += 1

def main():
	arguments = sys.argv[1:]
	search_term = arguments[0].translate(None, "\'\"")
	outputfilename = setup(search_term)
	search(search_term,outputfilename,client_access_token)

if __name__ == '__main__':
	main()