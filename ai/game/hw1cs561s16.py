# -*- coding: utf-8 -*-
# Author : ThammeGowda Narayanaswamy
# USC ID : 2074-6694-39
# Session: Spring 2016
# Course : USC CSCI 561 Foundations of Artificial Intelligence
# Topic  : Home work 1 : Squirrel Fight Game Strategy
#
# NOTE: Refer to CS561Spring2016HW1.pdf for the game rules

from __future__ import print_function
import argparse
from os import path
from decimal import Decimal
import string


POS_INFINITY = Decimal("inf")
NEG_INFINITY = Decimal("-inf")

COL_NAMES = [i for i in string.uppercase[0:5]]
ROW_NAMES = [str(i) for i in range(1, 6)]

STATE_OUT_FILE = "next_state.txt"
LOG_OUT_FILE = "traverse_log.txt"
TRACE_OUT_FILE = "trace_state.txt"


class SquirrelProblem(object):

    '''
    Squirrel Problem stated by Home work 1 of USC CSCI 561 - Spring 2016
    '''
    def __init__(self, prob_file):

        self.board_size = 5                               # Fixed, as per description
        self.empty_cell = '*'                             # Fixed, as per description
        self.opponent = lambda piece: 'O' if piece == 'X' else 'X'

        with open(prob_file) as f:
            lines = f.readlines()
            count = 0
            self.strategy = int(lines[0].strip())
            if self.strategy < 4:
                self.my_piece = lines[1].strip()
                self.opp_piece = self.opponent(self.my_piece)
                self.cutoff = int(lines[2].strip())
                count = 3
            else:
                self.first_player = lines[1].strip()
                self.first_player_algo = int(lines[2].strip())
                self.first_player_cut_off = int(lines[3].strip())
                self.second_player = lines[4].strip()
                self.second_player_algo = int(lines[5].strip())
                self.second_player_cut_off = int(lines[6].strip())
                count = 7

            # lines are board scores
            # n x n board. each cell has value
            self.costs = [[int(j) for j in lines[count + i].strip().split()]
                          for i in range(self.board_size)]
            count += self.board_size
            # lines 8 to 12 are positions
            # # n x n board. each cell has playerSign
            self.state = [[j for j in lines[count + i].strip()]
                          for i in range(self.board_size)]


    def print_state(self, state, debug=True, fileName=None, stdOut=True):
        '''
        Prints current state of the board to console
        :return:
        '''
        out_format = lambda i, j: '  %2d|%s' % (self.costs[i][j], state[i][j])\
            if debug else self.state[i][j]
        res = ""
        for i in range(self.board_size):
            for j in range(self.board_size):
                res += out_format(i, j)
            res += "\r\n"
        if fileName:
            with open(fileName, 'w') as w:
                w.write(res)
        if stdOut:
            print(res)
        return res

    def eval_score(self, state, player):
        '''
        Evaluates the score of game at any given state.
         The game score = my score - opponent score
        :param state: state of game
        :return: game score which is an integer
        '''
        score = 0
        opp_player = self.opponent(player)
        for (i,j) in self.all_cells():
            if state[i][j] == player:
                    score += self.costs[i][j]
            elif state[i][j] == opp_player:
                score -= self.costs[i][j]
            #else it is a free node
        return score

    def determineNextStateHeuristic(self, state, player):
        """
        Determines heuristics for the next possible state of given player from any given state
        :param state: the current state
        :param player: the player who has a move
        :return: heuristic
        """

        opp_piece = self.opponent(player)
        heuristic = [[None for j in range(self.board_size)] for i in range(self.board_size)]
        # the heuristic is computed without actually making the move
        # this is done using delta with current score
        current_score = self.eval_score(state, player)
        for i, j in self.all_cells():
            if state[i][j] == self.empty_cell:  # empty cell else: it's owned by somebody
                heuristic[i][j] = current_score + self.costs[i][j]
                # checking if this can also be a raid
                # checking if this can be a raid
                adjacent_cells = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
                raid = False

                opp_loss = 0
                for x, y in adjacent_cells:
                    if 0 <= x < self.board_size and 0 <= y < self.board_size:
                        if state[x][y] == opp_piece:
                            opp_loss += self.costs[x][y]
                        elif state[x][y] == player:
                            raid = True
                if raid:
                    # for all the raids, the new score goes up by 2 times the raided cell
                    # its 2 times because the foe loses it and we gain it. Thus difference is large by 2 times
                    heuristic[i][j] += 2 * opp_loss
        return heuristic

    def all_cells(self):
        """
        Yields indices for all possibles cells in the board
        :return: (row, column) indices from top left to bottom right
        """
        for i in range(self.board_size):
            for j in range(self.board_size):
                yield (i, j)

    def all_empty_cells(self, state):
        res = []
        for i, j in self.all_cells():
            if state[i][j] == self.empty_cell:
                res.append((i, j))
        return res


    def is_terminal_state(self, state):
        """
        checks if the game state is terminal
        :param state: game state
        :return: boolean True if the game is complete, False if further moves are possible
        """
        #state is complete if all cells are occupied
        for i, j in self.all_cells():
            if state[i][j] == self.empty_cell:
                return False
        return True

    def move_to_cell(self, state, row, col, player_piece):
        '''
        Takes over a specified cell
        :param state: state
        :param row: the row number
        :param col: column number
        :param player_piece: player piece
        :return: list of triples (row, col, piece);
         NOTE return list can be used for reverting the state by undoing the moves
        '''
        oppPiece = self.opponent(player_piece)
        undoLog = []
        if state[row][col] == self.empty_cell:

            # player owns this cell now. so it is no longer empty
            self.state[row][col] = player_piece
            undoLog.append((row, col, self.empty_cell))

            # checking if this can be a raid
            adjacent_cells = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]
            raid = False
            oppCells = []
            for i, j in adjacent_cells:
                if 0 <= i < self.board_size and  0 <= j < self.board_size:
                    if state[i][j] == oppPiece:
                        oppCells.append((i, j))
                    elif state[i][j] == player_piece:
                        raid = True
            if raid:
                for x, y in oppCells:
                    state[x][y] = player_piece
                    undoLog.append((x, y, oppPiece))
        else:
            raise Exception("I don't break Game Rules! The cell is not empty")
        return undoLog


    def apply_moves(self, state, actions):
        """
        Applies a sequence of moves on a state
        :param state: the initial state
        :param actions: sequence of moves (row, col, player)
        :return:
        """
        for action in actions:
            state[action[0]][action[1]] = action[2]


    def greedy_bfs(self, player):
        '''
        Performs next move by using Greedy best first search strategy
        :return:
        '''
        heuristic = self.determineNextStateHeuristic(self.state, player)
        maxVal = NEG_INFINITY
        pos = None
        # Find greedy best first position
        for i, j in self.all_cells():
            if heuristic[i][j] != None and heuristic[i][j] > maxVal:
                maxVal = heuristic[i][j]
                pos = (i, j)
        if pos:
            return self.move_to_cell(self.state, pos[0], pos[1], player)
        #else: no available slot, die

    def mini_max(self, logfile):
        root = MiniMaxSolver(self, self.my_piece, self.opp_piece, self.cutoff, logfile)\
            .solve(self.state)
        if root.next_move:
            move = root.next_move
            self.move_to_cell(self.state, move.pos[0], move.pos[1], move.piece)

    def alpha_beta_pruning(self, logfile):
        root = AlphaBetaSolver(self, self.my_piece, self.opp_piece, self.cutoff, logfile).solve(self.state)
        if root.next_move:
            move = root.next_move
            self.move_to_cell(self.state, move.pos[0], move.pos[1], move.piece)

    def simulate(self):
        count = 0
        with open(TRACE_OUT_FILE, 'w') as out:
            while not self.is_terminal_state(self.state):
                if count % 2 == 0:
                    self.your_turn(self.first_player_algo, self.first_player, self.second_player, self.first_player_cut_off)
                else:
                    self.your_turn(self.second_player_algo, self.second_player, self.first_player, self.second_player_cut_off)
                if count > 0:
                    out.write("\r\n")
                res = self.print_state(self.state, debug=False, stdOut=False).strip()
                out.write(res)
                count += 1

    def your_turn(self, strategy, player, opponent, cutoff):
        if strategy == 1:
            self.greedy_bfs(player)
        elif strategy == 2:
            move = MiniMaxSolver(self, player, opponent, cutoff).solve(self.state).next_move
            self.move_to_cell(self.state, move.pos[0], move.pos[1], move.piece)
            pass
        elif strategy == 3:
            move = AlphaBetaSolver(self, player, opponent, cutoff).solve(self.state).next_move
            self.move_to_cell(self.state, move.pos[0], move.pos[1], move.piece)
        else:
            raise Exception("Invalid state")


    def play_game(self, algorithm):
        '''
        Makes the next move as per the algorithm
        :param algorithm: the strategy for next move
        :return:
        '''
        if algorithm == 1:
            self.greedy_bfs(self.my_piece)
        elif algorithm == 2:
            with open(LOG_OUT_FILE, 'w') as logfile:
                self.mini_max(logfile)
        elif algorithm == 3:
            with open(LOG_OUT_FILE, 'w') as logfile:
                self.alpha_beta_pruning(logfile)
        elif algorithm == 4:
            self.simulate()
        else:
            raise Exception("Algorithm %d is unknown!" % algorithm)

    def read_state_file(self, fileName, n):
        """
        Reads game state from a file
        :param fileName: path to file
        :param n: the matrix/board size
        :return: nxn matrix having game state
        """
        with open(fileName) as f:
            return [[j for j in next(f).strip()] for _ in range(n)]

    def are_states_same(self, state1, state2):
        """
        Returns True if give two states are same
        :param state1: first state
        :param state2: second state
        :return: True if states are same; false otherwise
        """
        for i, j in self.all_cells():
            if state1[i][j] != state2[i][j]:
                return False
        return True


class Node(object):

    def __init__(self, score, pos, piece, depth=0, parent=None):
        self.parent = parent
        self.children = None
        self.score = score
        self.pos = pos
        self.piece = piece
        self.depth = depth
        self.next_move = None

    def add_child(self, node):
        node.parent = self
        node.depth = self.depth + 1
        if self.children == None:
            self.children = []
        self.children.append(node)

    def pretty_print(self, prefix="", isTail=True):
        name = "%3s %s" % (self.score, self.pos)
        print(prefix + ("└── " if isTail else "├── ") + name)
        if (self.children):
            formatstring = "    " if isTail else  "│   "
            for i in range(0, len(self.children) - 1):
                self.children[i].__prettyPrint(prefix + formatstring, False)
            self.children[-1].__prettyPrint(prefix + formatstring, True)


class MiniMaxSolver(object):

    def __init__(self, problem, max_player, min_player, cutoff, logfile=None):
        self.problem = problem
        self.logfile = logfile
        self.eval = lambda state : problem.eval_score(state, max_player)
        self.max_player = max_player
        self.min_player = min_player
        self.maxdepth = cutoff

    def solve(self, state):
        # first turn is my players'. My player is maxPlayer
        if self.logfile:
            self.logfile.write("Node,Depth,Value")
        root = Node(NEG_INFINITY, (None, None), None)
        self.maximize(state, root)
        return root

    def log(self, node, alphaBeta=False):
        if self.logfile:
            self.logfile.write("\r\n" + MiniMaxSolver.format_log(node, alphaBeta))

    @staticmethod
    def format_log(node, alpha_beta=False):
        name = "root" if node.depth == 0\
            else "%s%s" % (COL_NAMES[node.pos[1]], ROW_NAMES[node.pos[0]])
        res = "%s,%s,%s" % (name, node.depth, node.score)
        if alpha_beta:
            res += ",%s,%s" % (node.alpha, node.beta)
        return res


    def maximize(self, state, parent):
        cells = self.problem.all_empty_cells(state)
        if parent.depth == self.maxdepth or not cells:
            parent.score = self.eval(state)
        else:
            self.log(parent)
            for x, (i, j) in enumerate(cells):
                moves = self.problem.move_to_cell(state, i, j, self.max_player)    # max's move
                child = Node(POS_INFINITY, (i, j), self.max_player)
                parent.add_child(child)
                child.score = self.minimize(state, child)              # turn goes to min player
                if child.score > parent.score:
                    parent.score = child.score
                    parent.next_move = child
                if x < len(cells) - 1:                                 # for all except the last one
                    self.log(parent)
                self.problem.apply_moves(state, moves)
        self.log(parent)
        return parent.score

    def minimize(self, state, parent):
        cells = self.problem.all_empty_cells(state)
        if parent.depth == self.maxdepth or not cells:
            parent.score = self.eval(state)
        else:
            self.log(parent)
            for x, (i, j) in enumerate(cells):
                moves = self.problem.move_to_cell(state, i, j, self.min_player)     # min's move
                child = Node(NEG_INFINITY, (i, j), self.min_player)
                parent.add_child(child)
                self.maximize(state, child)                             # turn goes to max, depth reduced by 1
                if child.score < parent.score:
                    parent.score = child.score
                    parent.next_move = child
                if x < len(cells) -1: # for all except the last one
                    self.log(parent)
                self.problem.apply_moves(state, moves)
        self.log(parent)
        return parent.score


class AlphaBetaSolver(MiniMaxSolver):

    def solve(self, state):
        if self.logfile:
            self.logfile.write("Node,Depth,Value,Alpha,Beta")
        root = Node(NEG_INFINITY, (None, None), None) # this node for the next move, which is maximizer
                                                 # The worst possible value for him is -Infinity
        root.alpha = NEG_INFINITY                     # Max value, we dont know yet, so -Infinity
        root.beta = POS_INFINITY                      # Min value, we dont know yet, so +Infinity
        self.maximize(state, root)
        return root

    def maximize(self, state, parent):
        cells = self.problem.all_empty_cells(state)
        if parent.depth == self.maxdepth or not cells:
            parent.score = self.eval(state)
        else:
            self.log(parent, True)
            for x, (i, j) in enumerate(cells):
                moves = self.problem.move_to_cell(state, i, j, self.max_player)    # max's move
                child = Node(POS_INFINITY, (i, j), self.max_player)     # this node is for the next move, which is minimizer
                                                                  # The worst possible value for him is +infinity
                child.alpha = parent.alpha                        # Inherit alpha beta
                child.beta = parent.beta
                parent.add_child(child)                           #dept gets incremented
                self.minimize(state, child)              # turn goes to min player
                self.problem.apply_moves(state, moves)       #undo

                if child.score > parent.score:
                    parent.score = child.score
                    parent.next_move = child
                if child.score >= parent.beta: # intuition : Min player (parent) wont let this happen
                    break
                if child.score > parent.alpha:
                    parent.alpha = child.score

                if x < len(cells) - 1:                                 # for all except the last one
                    self.log(parent, True)
        self.log(parent, True)
        return parent.score

    def minimize(self, state, parent):
        cells = self.problem.all_empty_cells(state)
        if parent.depth == self.maxdepth or not cells:
            parent.score = self.eval(state)
        else:
            self.log(parent, True)
            for x, (i, j) in enumerate(cells):
                moves = self.problem.move_to_cell(state, i, j, self.min_player)     # min's move
                child = Node(NEG_INFINITY, (i, j), self.min_player)
                child.alpha = parent.alpha
                child.beta = parent.beta
                parent.add_child(child)
                self.maximize(state, child)                             # turn goes to max, depth reduced by 1
                self.problem.apply_moves(state, moves)
                if child.score < parent.score:
                    parent.score = child.score
                    parent.next_move = child
                if child.score <= parent.alpha:
                    break
                if child.score < parent.beta:
                    parent.beta = child.score
                if x < len(cells) -1: # for all except the last one
                    self.log(parent, True)

        self.log(parent, True)
        return parent.score

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CSCI-561 - HW 1 Solutions - by Thamme Gowda N.')
    parser.add_argument('-i','--input', help='Input File', required=True)
    parser.add_argument('-t','--test', action="store_true", help='Auto detect tests in directory')
    parser.add_argument('-tf','--testfile', required = False, help='Use this test file')
    args = vars(parser.parse_args())

    prob = SquirrelProblem(args['input'])
    prob.play_game(prob.strategy)
    prob.print_state(debug=False, state=prob.state, fileName=STATE_OUT_FILE, stdOut=False)

    # below is for testing
    testfile = None
    testLogFile = None
    if args['test']: # test was requested
        tmp = path.join(path.dirname(path.abspath(args['input'])), STATE_OUT_FILE)
        if path.exists(tmp): # see if there is a test file
            testfile = tmp
        tmp = path.join(path.dirname(path.abspath(args['input'])), LOG_OUT_FILE)
        if path.exists(tmp): # see if there is a test file
            testLogFile = tmp
        #print("Score X : %s" % prob.eval_score(prob.state, player='X'))
        #print("Score O : %s" % prob.eval_score(prob.state, player='O'))
    if 'testfile' in args and args['testfile']:
        testfile = args['testfile']
    if testfile:
        terminalState = prob.read_state_file(testfile, prob.board_size)
        res = prob.are_states_same(prob.state, terminalState)
        print("Next State Same ?: %s" % res)
        if not res:
            print("Error:\n Expected state:\n")
            prob.print_state(terminalState)
            print("But actual state:\n")
            prob.print_state(prob.state)
    if 2 <= prob.strategy <= 3 and testLogFile:
        import filecmp
        res = filecmp.cmp(testLogFile, LOG_OUT_FILE)
        print("Log Matched ? %s " % res)

