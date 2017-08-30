import nltk

artist_name = 'osno1'

output = re.sub(r"[^A-Za-z]+", '', artist_name) + ".txt"

with open