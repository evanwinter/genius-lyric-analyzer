## song lyrics with genius api

In your command line run the following prompts:

* `git clone https://github.com/evanwinter/genius-scrape.git`

* `cd genius-scrape`

Create a [Genius API Client](https://genius.com/api-clients/new) and copy your access token.

Create a file named `config.py` in the project root, and store your access token in it.

e.g.
```
# config.py

client_access_token = 'yourclientaccesstoken'
```

In your command line run:

`python main.py`

When prompted, enter the artist or band name and the number of songs you want to analyze (or `all` for their discography).



## to do
* ~~strip punctuation from lyrics~~
* ~~get all of artists' songs, not just top songs~~
* more data analysis and better formatting -- D3?