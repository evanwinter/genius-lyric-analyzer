# Genius Lyric Analyzer



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

Import modules at the top of `main.py`.

In your terminal, run:

`python main.py`

When prompted, enter the artist or band name and the number of songs you want to analyze (or `all` for their discography).

The following will occur:

* A directory named `output/` will be created (if it doesn't already exist)
* Song lyrics will be written to a text file named `output/artistname.txt`
* Lyrics will be analyzed for word frequency, the results of which will be written to a text file named `output/artistname-analysis.txt`

## To do

* Filter out boring/extremely common words before doing data visualization (but after writing most common words to text file)
* Filter for "(Live", "[Live"
* Calculate 'word diversity'/level of difficulty of words used (can't remember what this is called) -- can be done with NLTK?
* Better data visualization -- D3.js an option?
* Get it to run in browser

## Known issues/areas for improvement

* Doesn't count selected artist's guest verses
* Counts others' guest verses
* Because each token is stripped of punctuation and transformed to lowercase, "I'll" & "ill" are both counted as "ill", etc
* Organizational terms like "verse" and "chorus," and the artist's name itself are common and usually end up high on frequency distribution
* Majority of the 50-ish most common words end up being boring words like "i," "the," "you," etc
* Ignores any song with "tracklist" or "credits" in title, might result in skipping actual songs here and there

