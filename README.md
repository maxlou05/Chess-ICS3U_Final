# Chess
This chess game supports both 2-player mode to play with friends and 1-player mode to play against the computer.

## Features
- All rules of chess are implemented with the exception of repeating position draws (a friendlier version is implemented instead)
- The taken pieces are drawn at the side of the board
- Ability to take back moves
- Ability to add time limits

## Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install pygame zero.
```bash
pip install pgzero
```
## Known bugs
- Choosing a depth larger than 3 will result in very long computing times for the engine (choosing 3 is still long, ~1-2 minutes)

## Suppport
Please contact the developer at mlou1@ocdsb.ca for support or feature requests.

## Sources
|Source      |Description  |
|------------|-------------|
|https://pygame-zero.readthedocs.io/_/downloads/en/stable/pdf/|Learning pygame zero basics|
|https://pygame-zero.readthedocs.io/en/1.2/learn-programming.html|Learning how to use variables in the pygame zero framework|
|https://csatlas.com/python-import-file-module/|Importing and multiple files|
|https://realpython.com/python-pass-by-reference/|Python function parameter passing|
|https://robertheaton.com/2014/02/09/pythons-pass-by-object-reference-as-explained-by-philip-k-dick/#:~:text=The%20two%20most%20widely%20known,references%20are%20passed%20by%20value.%E2%80%9D|Python function parameter passing|
|https://mathspp.com/blog/pydonts/pass-by-value-reference-and-assignment|This one is a better explanation of mutable vs immutable and function parameter passing, more details and background|
|https://en.wikipedia.org/wiki/Evaluation_function#Handcrafted_evaluation_functions|Strategies to make a chess engine|
|https://www.chessprogramming.org/Simplified_Evaluation_Function|Basic values and ideas for piece-square table based evaluation|
|http://www.talkchess.com/forum3/viewtopic.php?f=2&t=68311&start=19|The data used for tables and piece values|
|https://www.chessprogramming.org/PeSTO%27s_Evaluation_Function|Logic and pseudo code on how to use the tables|
|https://www.iconsdb.com/white-icons/stopwatch-icon.html|Image for stopwatch (white)|
|https://www.iconsdb.com/black-icons/stopwatch-icon.html|Image for stopwatch (black)|
|https://commons.wikimedia.org/wiki/Category:SVG_chess_pieces|Image for chess pieces|