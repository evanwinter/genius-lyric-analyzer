## song lyrics with genius api

* `git clone https://github.com/evanwinter/genius-scrape.git`

* `cd genius-scrape`

* create a [genius api client](https://genius.com/api-clients/new)

* create a file named `config.py` and enter your access token like so:

```
# config.py

client_access_token = 'yourclientaccesstoken'
```

## collect and analyze lyrics from an artist's discography

`python main.py 'artistname'`


## to do
* build UI, make this usable
* ~~strip punctuation from lyrics~~
* ~~get all of artists' songs, not just top songs~~
* more data analysis and better formatting -- D3?