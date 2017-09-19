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
* a directory named `output/artistname` will be created (if it doesn't already exist)
* Song lyrics will be written to a text file named `output/artistname.txt`
* Lyrics will be analyzed for word frequency, the results of which will be written to a text file named `output/artistname-analysis.txt`

## To do

* Look up frequency of phrase
* regex used for file setup takes "A$AP Rocky" and makes it "aaprocky" -- possible to replace $'s with "S's? also "24hrs" becomes "hrs"
* ~~Filter out boring/extremely common words before doing data visualization (but after writing most common words to text file)~~
* ~~tokenize artist name and filter from analysis -- always ends up in top 50~~
* ~~Filter for "(Live", "[Live"~~
* ~~Calculate lexical diversity (unique words / all words)~~
* Better data visualization -- D3.js an option?
* Get it to run in browser
* ~~New folder for each artist's lyrics, analysis and plot i.e. `output/artistname/`~~

## Known issues/limitations/areas for improvement (probably won't fix)

* Counts featured artists'/collaborators' lyrics too
* Because each token is stripped of punctuation and transformed to lowercase, "I'll" & "ill" are both counted as "ill", etc
* Doesn't always find the right artist: User searches artist name --> program executes a search using that exact input --> target artist is whoever the top result's primary artist is... Ex: entering Slipknot when prompted for artist name will find the top result to be an XXXTentacion song &mdash; titled "slipknot" &mdash; thus using XXXTentacion as the target artist instead.

--

### Features

* Gather the lyrics to every song in an artist's catalogue (as it is on Genius.com, that is)
* With the Natural Language Toolkit, plot the words used most frequently by that artist on a frequency distribution graph. (Overly common words are ommitted from the graph)
* Calculate stats like number of songs, number of unique words, pageviews of each song and lexical diversity -- neatly outputted in a textfile.
* Get the frequency of a specific word in an artists' catalogue.
* Coming soon: Get the frequency of a phrase.