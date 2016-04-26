from fifteen import Puzzle

puzzle = Puzzle(4, 4)
print str(puzzle)
t = puzzle.lower_row_invariant(2, 2)
print t
#puzzle.set_number(0, 1, 13)
#puzzle.set_number(3, 1, 1)
puzzle.set_number(0, 0, 10)
puzzle.set_number(2, 2, 0)
print str(puzzle)
t = puzzle.lower_row_invariant(2, 2)
print t
