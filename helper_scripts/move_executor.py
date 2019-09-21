import sys

"""
This is a helper script to do testing
Takes in init_state and moves as input
Prints True if the moves solves the puzzle
Else, prints False
"""
class Puzzle(object):
    def __init__(self, init_state, goal_state):
        self.init_state = init_state
        self.goal_state = goal_state
        self.action_dic = {"UP": (-1, 0),
                           "DOWN": (1, 0),
                           "LEFT": (0, -1),
                           "RIGHT": (0, 1)}
        self.reflection_dic = {"UP": "DOWN",
                               "DOWN": "UP",
                               "LEFT": "RIGHT",
                               "RIGHT": "LEFT"}
        
    def trace_moves(self, moves):
        """
        Modifies the initial state based on moves
        Returns True if it reaches the goal state (Solved the puzzle)
        Return False otherwise.
        """
        for move_cmd in moves:
            if not self.move(move_cmd):
                print("THERE'S ILLEGAL MOVES IN YOUR MOVE SEQUENCE")
                return False
        return self.goal_test(self.init_state, self.goal_state)
    
    def move(self, move_cmd):
        """
        If move_cmd is valid, execute the move and return True.
        Else, return False.
        """
        i, j = self.find_empty_space(self.init_state)
        
        legal_moves = self.get_legal_moves(i, j)
        
        if move_cmd not in legal_moves:
            return False
        
        coordinate_change = self.action_dic[self.reflection_dic[move_cmd]]
        self.init_state[i][j], self.init_state[i + coordinate_change[0]][j + coordinate_change[1]] = \
                               self.init_state[i + coordinate_change[0]][j + coordinate_change[1]]\
                               , self.init_state[i][j]
        return True
        
    def find_empty_space(self, state):
        """Evaluates the state and returns index of empty space"""
        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    return (i, j)
                
    def get_legal_moves(self, i, j):
        """
        Takes in coordinate of empty space, and use it to determine the current state
        Returns a list of legal moves to take for current state
        """
        legal_moves = []
        for action in self.action_dic.keys():
            coordinate_change = self.action_dic[action]
            new_i = coordinate_change[0] + i
            new_j = coordinate_change[1] + j
            if (new_i >= 0 and new_i < 3) and (new_j >= 0 and new_j < 3):
                legal_moves.append(self.reflection_dic[action])
        return legal_moves
    
        
    def goal_test(self, state, goal_state):
        """
        Compares the current state and the goal
        Return True if current state is same as goal state
        Return False otherwise
        """
        for i in range(3):
            for j in range(3):
                if state[i][j] != goal_state[i][j]:
                    return False
        return True


# Reading inputs
if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise ValueError("Wrong number of arguments!")

    try:
        matrix = open(sys.argv[1], 'r')
        moves = open(sys.argv[2], 'r')
    except IOError:
        raise IOError("Input file(s) not found!")
    
    init_state = [[0 for i in range(3)] for j in range(3)]
    goal_state = [[0 for i in range(3)] for j in range(3)]
    lines = matrix.readlines()

    # set up of init_state matrix
    i,j = 0, 0
    for line in lines:
        for number in line:
            if '0'<= number <= '8':
                init_state[i][j] = int(number)
                j += 1
                if j == 3:
                    i += 1
                    j = 0

    for i in range(1, 9):
        goal_state[(i-1)//3][(i-1)%3] = i
    goal_state[2][2] = 0

    # processing input of list of moves
    move_lst = []
    for move in moves:
        move = str.rstrip(move)
        move_lst.append(move)
        
    puzzle = Puzzle(init_state, goal_state)
    print(puzzle.trace_moves(move_lst))
