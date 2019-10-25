---
title: gamble
---

[![image](https://travis-ci.org/jpetrucciani/gamble.svg?branch=master)](https://travis-ci.org/jpetrucciani/gamble)

[![PyPI version](https://badge.fury.io/py/gamble.svg)](https://badge.fury.io/py/gamble)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

[![Python 3.6+ supported](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/release/python-360/)

[![Documentation style: archives](https://img.shields.io/badge/docstyle-archives-lightblue.svg)](https://github.com/jpetrucciani/archives)

**gamble** is a simple library that implements a collection of some
common gambling-related classes

Features
========

-   die, dice, d-notation
-   cards, decks, hands
-   poker ranks, hand comparison

Usage
=====

Installation
------------

``` {.bash}
pip install gamble
```

Basic Usage
===========

Dice
----

``` {.python}
import gamble

# create dice, defaults to 2 6-sided dice
dice = gamble.Dice()

# roll
dice.roll()
>>> 6
dice.rolls
>>> 1

# max, min
dice.max
>>> 12
dice.min
>>> 2

# d-notation for dice constructor
dice = gamble.Dice('d20+8')

# max, min
dice.max
>>> 28
dice.min
>>> 9

# parts
dice.parts
>>> [<d20 Die>, 8]

# roll_many
dice.roll_many(2)
>>> [8, 4]

# max_of, min_of
dice.max_of(3)
>>> (11, [7, 3, 11])
dice.min_of(3)
>>> (2, [2, 9, 4])
```

Cards
-----

``` {.python}
import gamble

# create a deck, defaults to the standard 52 card deck, no jokers
# the deck will be shuffled by default, unless you pass shuffle=False
deck = gamble.Deck()

deck.cards_left
>>> 52

deck.top
>>> <Card:7♠>
deck.bottom
>>> <Card:9♠>
deck.shuffle()  # you can also pass times=(int) to shuffle more than once

card = deck.draw()  # you can also pass times=(int) to draw a list of cards
>>> <Card:A♠>

# the unicode cards icons are implemented as well!
card.unicode
>>> "🂡"

# draw a poker hand, default size 5
hand = deck.draw_hand(). # you can pass size=(int) to draw a different size hand
>>> <Hand[5](straight flush) [A♠, 2♠, 3♠, 4♠, 5♠]>

hand.rank
>>> Rank(name='straight flush', value=8)

# arbitrary hand, from text notation
new_hand = gamble.Hand.get("2c,3c,4c,Kc,Kh")
>>> <Hand[5](pair) [2♣, 3♣, 4♣, K♣, K♥]>

new_hand.rank
>>> Rank(name='pair', value=1)

hand > new_hand
>>> True
```

Todo
====

-   hand equals/ge/le method
-   hand ranking when hands are very similar
