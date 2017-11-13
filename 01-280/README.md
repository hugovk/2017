# 280

<p align="center">
<a href="https://twitter.com/survivorevan/status/928041592207818752"><img src="https://github.com/hugovk/NaNoGenMo-2017/blob/master/01-280/tweet.png?raw=true" width="75%" height="75%"></a>
</p>

## Generated output

* [280.html](https://hugovk.github.io/NaNoGenMo-2017/01-280/280.html) - short and long tweets
* [280-short.html](https://hugovk.github.io/NaNoGenMo-2017/01-280/280-short.html) - only short tweets
* [280-long.html](https://hugovk.github.io/NaNoGenMo-2017/01-280/280-long.html) - only long tweets

## What it does

Searches Twitter for "280" and outputs one short tweet of 140 characters or less, then long tweet one over 140, then repeats until 56,000 words (280 * 200). Or can only output short tweets. Or can only output long tweets.

## How to do it

Get [Twitter app keys and secrets](https://apps.twitter.com/) and put them in 280.yaml:

```
consumer_key: TODO_ENTER_YOURS
consumer_secret: TODO_ENTER_YOURS
access_token: TODO_ENTER_YOURS
access_token_secret: TODO_ENTER_YOURS
```

Then run:

```bash
pip install pyyaml twitter
# then
python 280.py > 280.html
# or
python 280.py --toggle short > 280-short.html
# or
python 280.py --toggle long > 280-long.html
```

Works at least with macOS High Sierra with Python 3.6.3. Should work with Python 2.7.
