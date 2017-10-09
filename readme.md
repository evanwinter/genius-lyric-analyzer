## What does it do?

This program takes an artist or band name and performs basic text analysis on the lyrics to all of their songs. You can look up the frequency of individual words, calculate their overall diversity of word choice, and create basic data visualizations of this information.

More specifically:

1. Gets the lyrics to every song by the target artist (the ones with lyrics on Genius.com, that is) and stores them in a text file.
2. Analyzes the lyrics and calculates the frequency of each word used as well as the artist's overall [lexical diversity](https://en.wikipedia.org/wiki/Lexical_diversity) and stores that information in a different text file.
3. Presents the user with options: (1) Plot the word frequency in a frequency distribution plot, (2) Print an individual word's frequency to the console, (3) Print all song lyrics to the console, (4) Print the analysis text file created in step 2, and (5) Populate an HTML template with this artist's information and open it in a browser.

## Usage

In your terminal, run the following commands:

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

* Formatting on HTML template.
* Javascript rewrite. Get it to run in browser
* Give context to lyrics during reverse lookup -- something along the lines of `for line in lyrics containing keyword, print line`
* Reverse lookup phrase frequency
* Output as a better webpage ~~Output as a webpage~~
* Make stats relative -- percentages etc. Need to adjust for differences in number of songs, etc 
* replace $'s with "S's - "A$AP Rocky" becomes "aaprocky" right now ~~also "24hrs" becomes "hrs"~~
* ~~Filter out boring/extremely common words before doing data visualization (but after writing most common words to text file)~~
* ~~tokenize artist name and filter from analysis -- always ends up in top 50~~
* ~~Filter for "(Live", "[Live"~~
* ~~Calculate lexical diversity (unique words / all words)~~
* Better data visualization -- D3.js an option?
* ~~New folder for each artist's lyrics, analysis and plot i.e. `output/artistname/`~~

## Known issues/limitations/areas for improvement (probably won't fix)

* Counts featured artists'/collaborators' lyrics too
* Because each token is stripped of punctuation and transformed to lowercase, "I'll" & "ill" are both counted as "ill", etc
* ~~Doesn't always find the right artist: User searches artist name --> program executes a search using that exact input --> target artist is whoever the top result's primary artist is... Ex: entering Slipknot when prompted for artist name will find the top result to be an XXXTentacion song &mdash; titled "slipknot" &mdash; thus using XXXTentacion as the target artist instead.~~

## Bugs (will fix)


* `Traceback (most recent call last):
  File "main.py", line 411, in <module>
    main()
  File "main.py", line 357, in main
    all_lyrics = get_all_lyrics(songs, artist, output_file)
  File "main.py", line 153, in get_all_lyrics
    song_lyrics = get_song_lyrics(song)
  File "main.py", line 172, in get_song_lyrics
    song_lyrics = html.find("div", class_="lyrics").get_text()
AttributeError: 'NoneType' object has no attribute 'get_text'`