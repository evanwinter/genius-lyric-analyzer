## song lyrics with genius api

In your command line run the following prompts:

* `git clone https://github.com/evanwinter/genius-scrape.git`

* `cd genius-scrape`

* create a [genius api client](https://genius.com/api-clients/new), create a file named `config.py` in the project root and store your access token in it.


e.g.
```
# config.py

client_access_token = 'yourclientaccesstoken'
```



`python main.py`


## to do
* ~~strip punctuation from lyrics~~
* ~~get all of artists' songs, not just top songs~~
* more data analysis and better formatting -- D3?