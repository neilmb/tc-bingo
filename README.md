# TC Bingo

This is a Python script for generating random bingo cards from a collection
of possible text items. It is for text rather than pictures and you should have
at least 25 possible items.

## Usage

Install the dependencies and set up a virtualenv using `pipenv install`.

Create a configuration file `config.py` according to the format below.

Call the `bingo_cards.py` script with the name of the config file:

```shell
pipenv run ./bingo_cards.py config.py
```

The generated PDF file is called `bingo_cards.pdf`.

If you want more than the default of 25 cards, there is a `--num-cards` option.

## Configuration

The configuration of the text to appear on the cards is in a Python module
with three variables that must exist.

### `TITLE`

This is the title that appears at the top of every card.

### `FREE`

This is the text that appears in the middle space of the card. Either choose
an item that is certain to appear, or use the word "FREE" to give everyone that
space automatically.

### `TEXTS`

This is a list of strings that will form the random selections in the remaining
24 spaces. It can have as many entries as you want, but you need to have at least 
24 items there so that the cards can be filled in.
