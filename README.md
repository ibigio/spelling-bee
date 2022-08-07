# NYT Spelling Bee Game Generator

An experiment to generate [New York Times "Spelling Bee"](https://www.nytimes.com/puzzles/spelling-bee) games with tunable properties, like the number of pangrams, the number of possible words, etc.

## Overview

This project finds every possible Spelling Bee game by efficiently searching through the full Scrabble wordlist and mapping each word to its unique set of letters.

Then, I use Google Books historical word frequencies and the LexVec embedding model to train a model that classifies words into "likely" or "unlikely" to be included in a game by the NYT editors.

## The Journey

I wanted to generate Spelling Bee games, and I wanted them to be _extra_ fun games. Enter this entire shenanigan.

The NYT editors most likely create games by selecting an interesting word, of any length, made up of seven unique letters. Then, they use a program to generate all possible words (according to Scrabble) composable by any subset of those seven letters, and then hand-pick which will be included in the game (e.g. exclude the archaic and overly derogatory).

Getting the full Scrabble dictionary was simple enough. The issue is that I can't hand-pick which words to include / exclude – but maybe an ML model can? Three and half days of scraping frequenices from Google Books and 10 minutes of training later, I have a model that can classify them with 98% accuracy! Does it still include strange words? Absolutely Did it overfit? Almost certainly. Is it just passable enough to use? For sure.

## Dependencies

### LexVec Model
This project uses the `lexvec` word embeddings model (8.6Gb) downloadable from their [Github repo](https://github.com/alexandres/lexvec). This projects assumes the model will be in the following path:
```
models/lexvec.commoncrawl.ngramsubwords.300d.W.pos.bin
```
Download it with the following command:
```
curl -L "https://www.dropbox.com/s/buix0deqlks4312/lexvec.commoncrawl.ngramsubwords.300d.W.pos.bin.gz?dl=1" --output models/lexvec.commoncrawl.ngramsubwords.300d.W.pos.bin
```

## Running

It really isn't ready to run _per se_, but you can play around with it. I might document it at some point, but not today. I think `python run.py` might do something. 🤷🏽‍♂️

### Python Setup

Set up Python virtual environment and install dependencies like so:
```
python3 -m venv env
source env/bin/activate
python -m pip install -r requirements.txt
```