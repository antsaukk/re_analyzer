# Round eliminator analyzer
Command line tool for generation, execution on round-eliminator and analysis of results for star-cover problems on d-regular graphs expressed in bipartite edge-labelling formalism.


### *Usage:* 
python3.8 reanalyzer.py --file_name file.txt --iterations iterations --star_size star_size


### *or* 

python3.8 reanalyzer.py -h 

for instructions.

# Example: 
```
python3.8 reanalyzer.py --file_name tp.txt --iterations 12 --star_size 3
Problems in canonical form are formulated, do you want to display the input? [Y/N]: N
Continue with round-eliminating? [Y/N]: Y

LAUNCHING RE WITH 12 ITERATIONS ON 3-REGULAR GRAPH

ROUND-ELIMINATING PROBLEM: 1
Done. Output collected.
ROUND-ELIMINATING PROBLEM: 2
Done. Output collected.
ROUND-ELIMINATING PROBLEM: 3
Done. Output collected.
ROUND-ELIMINATING PROBLEM: 4
Done. Output collected.
ROUND-ELIMINATING PROBLEM: 5
Done. Output collected.
ROUND-ELIMINATING PROBLEM: 6
Done. Output collected.
ROUND-ELIMINATING PROBLEM: 7
Done. Output collected.
---Checking approximate convergence---
1: Covering problem of the 3 regular graph with stars of sizes [1] possibly converges.
2: Covering problem of the 3 regular graph with stars of sizes [2] possibly converges.
3: Covering problem of the 3 regular graph with stars of sizes [3] possibly converges.
4: Covering problem of the 3 regular graph with stars of sizes [1, 2] most probably diverges.
5: Covering problem of the 3 regular graph with stars of sizes [1, 3] possibly converges.
6: Covering problem of the 3 regular graph with stars of sizes [2, 3] most probably diverges.
7: Covering problem of the 3 regular graph with stars of sizes [1, 2, 3] most probably diverges.
Display divergent non-fixed point problems? [Y/N]: N
Relax divergent problems? [Y/N]: Y
Problems are relaxed. Display relaxations? [Y/N]: N
Continue with round-eliminating? [Y/N]: Y

LAUNCHING RE WITH 12 ITERATIONS AND STAR SIZE 3 

ROUND-ELIMINATING PROBLEM: 1
Done. Output collected.
ROUND-ELIMINATING PROBLEM: 2
Done. Output collected.
---Checking approximate convergence---
1: Covering problem of the 3 regular graph with stars of sizes [2, 3] possibly converges.
2: Covering problem of the 3 regular graph with stars of sizes [1, 2] possibly converges.
```

*Important: consider computational time. Problems in original form will take longer time on graphs with degree > 6. Relaxations are slower on degree > 5.*

