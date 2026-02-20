*This project has been created as part of the 42 curriculum by <vvan-ach>, <bsaipidi>*

#A-Maze-ing 🧩
##📌 Description

###A-Maze-ing is a Python terminal application that generates, displays, and solves mazes based on parameters provided in a configuration file.

##The program:

###Generates a maze using a depth-first search backtracking algorithm

###Optionally creates a perfect maze (no loops)

###Can add additional random wall removals (non-perfect maze)

###Solves the maze using Breadth-First Search (BFS)

###Exports the maze structure and solution path to a file

###Displays the maze interactively in the terminal with colors

###Allows regeneration using different random seeds

###If the maze is large enough, a 42 logo watermark is drawn in the center (without blocking entry/exit).

##⚙️ Requirements

###Python 3.10+

###Virtual environment (automatically created with make install)

###Dependencies listed in requirements.txt (notably pydantic)

##📂 Project Structure
```
.
├── mazegen/
│   └── a_maze_ing.py
|   |__init__.py
├── config.txt
├── requirements.txt
├── Makefile
└── README.md
|__ pyproject.toml
```
##🚀 Installation & Usage
###1️⃣ Install dependencies
```
make install
```

###This will:

####Create a virtual environment (venv/)

####Install all required packages

##2️⃣ Run the program
```
make run
```

###This runs:
```
python mazegen/a_maze_ing.py config.txt
```

##3️⃣ Debug mode
```
make debug
```
###Runs the program with Python debugger (pdb).

4️⃣ Lint & Type Checking
```
make lint
```
###Runs:
####flake8
####mypy

##5️⃣ Clean cache files
```
make clean
```
###Removes:

####__pycache__

####.mypy_cache

####.pyc files

##📝 Configuration File Format

###The program requires a configuration file as argument.

###Example config.txt:
```
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
Parameters
Parameter	Description
WIDTH	Maze width (integer > 0)
HEIGHT	Maze height (integer > 0)
ENTRY	Entry coordinates (x,y)
EXIT	Exit coordinates (x,y)
OUTPUT_FILE	Must be maze.txt
PERFECT	True → no loops
SEED	Random seed (empty = random)
```

##🧠 Algorithms Used
###🔹 Maze Generation

###Depth-First Search (DFS) with backtracking

###Optional random wall removal for non-perfect mazes

##🔹 Maze Solving

###Breadth-First Search (BFS)

####Returns shortest path from entry to exit

##📤 Output File

###The program exports:

####Maze structure encoded in hexadecimal format

####Entry coordinates

####Exit coordinates

###Solution path as directions:

####N → North

####S → South

####E → East

####W → West

###🎮 Interactive Menu

###After generation, the terminal interface allows:
```
1 - Show/Hide solution
2 - Change wall color
3 - Regenerate maze (new random seed)
4 - Exit
```
##The current seed is displayed to allow reproducibility.
```
pip install pyproject
```
###In the file: 
#### from mazegen import Parameters, Mazegenerator

## Additional
### Team roles:
#### vvan-ach was pratogonist of the project in parsing, implementation of the maze generator algorithm and
#### path finding solution algorithm. 
#### bsaipidi made general works like, makefile, optimizing the code, correction of errores, handling edge cases and project structure.

## Use of AI 
### Mostly used to understand the subject requirements. Understand the errores given by MYPY

## Resourses:
#### https://medium.com/@marcnealer/a-practical-guide-to-using-pydantic-8aafa7feebf6
#### https://es.wikipedia.org/wiki/Vuelta_atr%C3%A1s
