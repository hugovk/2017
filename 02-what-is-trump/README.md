# *What is Trump?*

## Generated output

* [whatis.md](whatis.md)

## What it does

A variation on last year's [*Dear Santa*](https://github.com/NaNoGenMo/2016/issues/138), a chapter crowdsourced from each US state, populated from a Twitter search.

## How to do it

Get [Twitter app keys and secrets](https://apps.twitter.com/) and put them in whatis.yaml:

```
consumer_key: TODO_ENTER_YOURS
consumer_secret: TODO_ENTER_YOURS
access_token: TODO_ENTER_YOURS
access_token_secret: TODO_ENTER_YOURS
```

Then run:

```bash
pip install pyyaml twitter

# then for tweets from the 50 states
python whatis.py > whatis.md

# or for tweets from anywhere
python whatis.py --no-states > whatis.html
```

Works at least with macOS High Sierra with Python 3.6.3 and Python 2.7.14, and Windows 7 with Python 2.7.11.
