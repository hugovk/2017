# *Pride, Prejudice*

## Generated output

* [output.txt](output.txt): 103,038 words
* [output2.txt](output2.txt): 51,142 words


## What it does

The problem isn't generating over 50,000 words. The problem is existing books 
are too long. *Pride and Prejudice* is 130,000 words, *Moby Dick* is 215,136 
words (or [215,136 meows](https://github.com/hugovk/meow.py)). And we all know 
50,000 is the gold standard for a novel! So how can we reduce the word count? 

* Remove Project Gutenberg boilerplate
* Use contractions everywhere: "won't" instead of "will not", "t'" instead of "the"
* Replace "and" with a comma, "or" with a slash
* Delete parenthetical "however", "indeed" and "I dare say"
* Remove honorifics (Mr., Mrs., Miss, Dr.)
* ['Substitute ‘damn’ every time you’re inclined to write ‘very’; your editor will delete it and the writing will be just as it should be.'](https://quoteinvestigator.com/2012/08/29/substitute-damn/)
* Replace redundant phrases like "whether or not" with just "whether"

These tactics reduce *Pride and Prejudice* by about 15% to 111,000 words. 

Next we work out the ratio of words we have to 50k, count how many sentences 
we have, and work out how many sentences we want to approach 50k and use a text 
summariser to chop out the dead wood.


## How to do it

Run:

```bash
pip install -r requirements.txt

python reducifier.py
```

Example:
```bash
python reducifier.py
open
word count: 130,000
word count: 126,936	diff: 97.643%	deboilerplatify
word count: 125,438	diff: 96.491%	remove_quote_things
word count: 121,549	diff: 93.499%	deveryify
word count: 121,018	diff: 93.091%	decontractify
word count: 111,633	diff: 85.872%	dehonorify
Ratio (words/50k):	 3
Number of sentences:	 4588
Number to keep:		 1529
word count: 54,273	diff: 41.748%	summarise
```

This produces output.txt before the summariser, and output2.txt after the summariser.

Works at least with macOS High Sierra with Python 3.6.3.
