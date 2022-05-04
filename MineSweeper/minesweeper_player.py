import numpy
import constraint
from minesweeper_common import UNKNOWN, MINE, get_neighbors

RUN_TESTS = False

class Player:
    def __init__(self, rows, columns, game, mine_prb):
        # Initialize a player for a game on a board of given size with the probability of a mine on each cell.
        self.rows = rows
        self.columns = columns
        self.game = game
        self.mine_prb = mine_prb
        self.not_mine_prb = 1 - mine_prb

        # Matrix of all neighbor cells for every cell.
        self.neighbors = get_neighbors(rows, columns)

        # Matrix of numbers of missing mines in the neighborhood of every cell.
        # -1 if a cell is unexplored.
        self.mines = numpy.full(rows*columns, -1).reshape((rows, columns))

        # Matrix of the numbers of unexplored neighborhood cells, excluding known mines.
        self.unknown = numpy.full(rows*columns, 0).reshape((rows, columns))
        for i in range(self.rows):
            for j in range(self.columns):
                self.unknown[i,j] = len(self.neighbors[i,j])

        # A set of cells for which the precomputed values self.mines and self.unknown need to be updated.
        self.invalid = set()

    def turn(self):
        # Returns the position of one cell to be explored.
        pos = self.preprocessing()
        if not pos:
            pos = self.probability_player()
        self.invalidate_with_neighbors(pos)
        return pos

    def probability_player(self):
        # Return an unexplored cell with the minimal probability of mine
        prb = self.get_each_mine_probability()
        min_prb = 1
        for i in range(self.rows):
            for j in range(self.columns):
                if self.game[i,j] == UNKNOWN:
                    if prb[i,j] > 0.9999: # Float-point arithmetics may not be exact.
                        self.game[i,j] = MINE
                        self.invalidate_with_neighbors((i,j))
                    if min_prb > prb[i,j]:
                        min_prb = prb[i,j]
                        best_position = (i,j)
        return best_position

    def invalidate_with_neighbors(self, pos):
        # Insert a given position and its neighborhood to the list of cell requiring update of precomputed information.
        self.invalid.add(pos)
        for neigh in self.neighbors[pos]:
            self.invalid.add(neigh)

    def preprocess_all(self):
        # Preprocess all cells
        self.invalid = set((i,j) for i in range(self.rows) for j in range(self.columns))
        pos = self.preprocessing()
        assert(pos == None) # Preprocessing is incomplete

    def preprocessing(self):
        """
            Update precomputed information of cells in the set self.invalid.
            Using a simple counting, check cells which have to contain a mine.
            If this simple counting finds a cell which cannot contain a mine, then returns its position.
            Otherwise, returns None.
        """
        while self.invalid:
            pos = self.invalid.pop()

            # Count the numbers of unexplored neighborhood cells, excluding known mines.
            self.unknown[pos] = sum(1 if self.game[neigh] == UNKNOWN else 0 for neigh in self.neighbors[pos])

            if self.game[pos] >= 0:
                # If the cell pos is explored, count the number of missing mines in its neighborhood.
                self.mines[pos] = self.game[pos] - sum(1 if self.game[neigh] == MINE else 0 for neigh in self.neighbors[pos])
                assert(0 <= self.mines[pos] and self.mines[pos] <= self.unknown[pos])

                if self.unknown[pos] > 0:
                    if self.mines[pos] == self.unknown[pos]:
                        # All unexplored neighbors have to contain a mine, so mark them.
                        for neigh in self.neighbors[pos]:
                            if self.game[neigh] == UNKNOWN:
                                self.game[neigh] = MINE
                                self.invalidate_with_neighbors(neigh)

                    elif self.mines[pos] == 0:
                        # All mines in the neighborhood was found, so explore the rest.
                        self.invalid.add(pos) # There may be other unexplored neighbors.
                        for neigh in self.neighbors[pos]:
                            if self.game[neigh] == UNKNOWN:
                                return neigh
                        assert(False) # There has to be at least one unexplored neighbor.

        if not RUN_TESTS:
            return None

        # If the invalid list is empty, so self.unknown and self.mines should be correct.
        # Verify it to be sure.
        for i in range(self.rows):
            for j in range(self.columns):
                assert(self.unknown[i,j] == sum(1 if self.game[neigh] == UNKNOWN else 0 for neigh in self.neighbors[i,j]))
                if self.game[i,j] >= 0:
                    assert(self.mines[i,j] == self.game[i,j] - sum(1 if self.game[neigh] == MINE else 0 for neigh in self.neighbors[i,j]))

    def find_normalized_prob_of_mine(self, square, solutions):
        prob_of_mine = 0 
        prob_of_number = 0

        for solution in solutions:
            prob_of_solution = 1 #probability that this solution is correct
            
            for v in solution.values():
                if v:
                    prob_of_solution *= self.mine_prb
                else:
                    prob_of_solution *= self.not_mine_prb
            
            if solution[square]:
                prob_of_mine += prob_of_solution #probability that this square has mine
            else:
                prob_of_number += prob_of_solution #probability that this square has not mine

        #return the normalized probability of mine
        return float(prob_of_mine) / sum([prob_of_mine, prob_of_number])

    def get_each_mine_probability(self):
        # Returns a matrix of probabilities of a mine of each cell
        problem = constraint.Problem()
        probability = numpy.zeros((self.rows,self.columns))

        for i in range(self.rows):
            for j in range(self.columns):

                if self.game[i,j] == MINE:
                    probability[i,j] = 1

                elif self.game[i,j] == UNKNOWN:
                    probability[i,j] = self.mine_prb

                else:
                    unknown_neighbors = [] #unexplored neighbors of given square

                    for n in self.neighbors[i, j]:
                        if self.game[n] == UNKNOWN:
                            unknown_neighbors.append(n)
                            
                            #add new variable: unexplored squares, that are neighbors of explored squares
                            if n not in problem._variables.keys():
                                problem.addVariable(n, [0, 1])
                    
                    #add new constraint: number of mines between unknown neighbors must be equal to self.mines
                    if unknown_neighbors:
                        problem.addConstraint(constraint.ExactSumConstraint(self.mines[i, j]), unknown_neighbors)
        
        solutions = problem.getSolutions()
        
        #find the correct normalized probability for each fringe square
        for square in problem._variables.keys():
            probability[square] = self.find_normalized_prob_of_mine(square, solutions)

        return probability
