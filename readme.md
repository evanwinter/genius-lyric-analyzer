## Usage

In your terminal, run the following prompts:

* `git clone https://github.com/evanwinter/genius-scrape.git`

* `cd genius-scrape`


Create a [Genius API Client](https://genius.com/api-clients/new) and copy your access token.


Create a file named `config.py` in the project root, and store your access token in it.


e.g.
```
# config.py

client_access_token = 'yourclientaccesstoken'
```


In your terminal, run:


`python main.py`


When prompted, enter the artist or band name and the number of songs you want to analyze (or `all` for their discography).


The following will occur:

* A directory named `output/` will be created (if it doesn't already exist)
* Song lyrics will be written to a text file named `artistname.txt`
* Lyrics will be analyzed for word frequency, the results of which will be written to a text file named `artistname-analysis.txt`