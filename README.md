# nonogram-solver v1

This concludes version one of the nonogram solver. I've been playing a lot of picross recently, and thought "how do I show I've truly mastered the game? I solve it automatically!" Thus, this program is my way of showing I've "mastered" picross, and a way to experiment with several tools I've wanted to use (such as pytest and GUIs in Python).

This version solves simple nonograms, using the Nonogram and Solver classes. This version was written "blind".  That is, I wrote it using only my knowledge of nonograms, without referring to solution steps on, say, Wikipedia. 

Near the end of the development of this version, I got lazy with the tests as the solution techniques began to become overly complex. There were many
techniques for solving that I tried that seemed overly specific, such as the function I wrote that fills from the edges. There were also many cases that I was unsure how to apply without being overly specific. Reviewing the Wikipedia on nonograms, many of the techniques I applied can be generalized. The next step will be to implement these techniques, as described in the wikipedia.

Overall, I am very happy with the Nonogram class (with a few minor changes I would like to make).  The solver class is, as I expected it to become, a mess.

## Future steps

Next version:

1. Solver class that solves in steps, rather than all at once (i.e., call s.step() to get the next action, or s.solve() to do all steps)
1. Solver methods as helper functions that act on a provided nonogram, rather than adding the nonogram to a solver class (both functions that apply rules to all rows/columns, and ones that apply to a single row)
1. Implementations and tests for each of the generalized techniques listed on Wikipedia (minus contradictions, for now)

Future versions:

1. Contradictions solving technique
1. File input methods
1. Command-line tool to solve a nonogram in a file
1. GUI for output
1. GUI for input
