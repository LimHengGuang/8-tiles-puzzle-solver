# 8-tiles Puzzle Solver
The 8-tiles puzzle solver takes in the state of an 8-tiles puzzle, and gives an output of moves that solves the puzzle. \
This project was done as a case study on the effects that differing heuristics may have on the run time of solving the 8-tile puzzle despite using the same search algorithm (A* search), and was undertaken as Assignment 1 of Introduction to Artificial Intelligence (CS3243). Additional helper functions in ```helper_scripts``` were written for testing and validation of inputs and outputs.

## Usage
Written in ```Python 2.6```. However, you may run the scripts with ```Python 3.7```, just change the import from ```Queue``` to ```queue```.

#### Puzzle Solving Scripts
Takes in puzzle in input_file, and writes move sequences as output into specified output_file.
```python
python 8tile_heuristic1.py input_file output_file  #to use heuristic 1
python 8tile_heuristic2.py input_file output_file  #to use heuristic 2
```
#### Check solvable
To avoid an unnecessarily long and meaningless attempt to solve a potentially unsolvable puzzle, it is best to check whether puzzle is solvable before running ```8tile_*.py``` by counting the number of inversions, using ```helper_scripts/check_solvable.py```
Prints ```True``` if puzzle in input_file is solvable. Prints ```False``` otherwise.
```python
python check_solvable.py input_file
```
#### Validate moves
Prints ```True``` if sequence of moves in moves_output solves the puzzle. Prints ```False``` otherwise.
```python
python move_executor.py input_file moves_output
```

## Input format
Takes in 3 lines of numbers, each number signifies a puzzle tile (0 signifies empty space in puzzle), and is separated by spacebar.
E.g
```
1 2 3
0 4 6
7 5 8
```
## Moves output format
An example of move output to solving the above puzzle:
```
LEFT
UP
LEFT
```

Check out the ```sample_inputs``` and ```sample_outputs``` for more clarity.

## Heuristic functions
### Heuristic 1
Sum of manhattan distance
##### Statistics
```
For input_1.txt:
Number of nodes generated: 10
Maximum size of the frontier: 6

For input_2.txt:
Number of nodes generated: 9
Maximum size of the frontier: 6

For input_3.txt:
Number of nodes generated: 10501
Maximum size of the frontier: 3721

For input_4.txt:
Not solvable
```

### Heuristic 2
Max of 2 heuristics. *h1* is the sum of Euclidean distances of the tiles from their goal positions. *h2* is the number of tiles out of row + number of tiles out of column.
##### Statistics
```
For input_1.txt:
Number of nodes generated: 36
Maximum size of the frontier: 14

For input_2.txt:
Number of nodes generated: 12
Maximum size of the frontier: 7

For input_3.txt:
Number of nodes generated: 194071
Maximum size of the frontier: 41796

For input_4.txt:
Not solvable
```

## Comparison of heuristics
Based on the statistics, heuristic 1 yields significantly better time complexity and consumes significantly less memory than heuristic 2. Overall, the performance of heuristic 1 is better than heuristic 2. \
The reason being that both *h1* and *h2* in heuristic 2 are dominated by the Manhattan distance heuristic. This can be proven by taking a closer look on how both *h1* and *h2* of heuristic 2 are dominated by heuristic 1.
