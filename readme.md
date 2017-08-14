## song lyrics with genius api

* `git clone https://github.com/evanwinter/genius-scrape.git`

* `cd genius-scrape`

* create a [genius api client](https://genius.com/api-clients/new)

* create a file named `config.py` and enter your access token like so:

```
# config.py

client_access_token = 'yourclientaccesstoken'
```

## get one song's lyrics

`python get-song-lyrics.py 'songname' 'artistname'`

## get and analyze lyrics from an artist's top ten songs

`python analyze-lyrics.py 'artistname'`