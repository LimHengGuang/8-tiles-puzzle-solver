import os
import sys
import math
import copy
from Queue import PriorityQueue

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
        self.goal_coord = self.init_goal_coord_dic(self.goal_state)
        self.frontier = PriorityQueue()
        self.visited = set()

    def init_goal_coord_dic(self, goal_state):
        dic = {}
        for i in range(3):
            for j in range(3):
                # ignore the empty space, aka, 0
                if goal_state[i][j] == 0:
                    continue
                if goal_state[i][j] not in dic:
                    dic[goal_state[i][j]] = (i, j)
        return dic

    def solve(self):
        '''
        A* search
        using Tree Search Algorithm
        and a heuristic max(Euclidean dist offset, num of tiles out of row/col)
        If 8-tile is solvable, program prints out number of nodes explored in stdout
        Also stdout the max frontier size
        '''
        # returns an empty list of actions if start state is already the goal state
        if self.goal_test(self.init_state, self.goal_state):
            return []

        self.frontier.put((self.get_heuristic(self.init_state),\
            Node(self.clone_state(self.init_state), 0, [])))

        num_of_nodes_generated = 1
        frontier_size = 1
        max_frontier_size = 1
        while not self.frontier.empty():
            f, curr_node = self.frontier.get()
            frontier_size -= 1
            curr_state = curr_node.state

            # goal testing
            if self.goal_test(curr_state, self.goal_state):
                print("Number of nodes generated: " + str(num_of_nodes_generated))
                print("Maximum size of frontier: " + str(max_frontier_size))
                return curr_node.actions

            hashable = self.make_hashable_state(curr_state)
            self.visited.add(hashable)

            g = curr_node.g

            # don't add node into frontier if it already requires 300 moves
            # since it is meaningless to explore... assignment dictates <= 300 moves
            if g >= 300:
                continue
            empty_i, empty_j = self.find_empty_space(curr_state)
            legal_moves = self.get_legal_moves(empty_i, empty_j)

            # test the legal moves to heuristic
            for move_cmd in legal_moves:
                new_state = self.move(curr_state, move_cmd, empty_i, empty_j)

                hashable = self.make_hashable_state(new_state)
                if hashable in self.visited:
                    continue

                new_actions_lst = copy.copy(curr_node.actions)
                new_actions_lst.append(move_cmd)
                new_g = g + 1
                new_f = new_g + self.get_heuristic(new_state)  #f(n) = g(n) + h(n)

                self.frontier.put((new_f, Node(new_state, new_g, new_actions_lst)))
                num_of_nodes_generated += 1
                frontier_size += 1
                max_frontier_size = max(max_frontier_size, frontier_size)

        return ["UNSOLVABLE"]

    def make_hashable_state(self, state):
        lst = []
        for row in state:
            lst.append(tuple(row))
        return tuple(lst)

    def clone_state(self, state):
        '''Takes in a state, and returns a copied state'''
        cloned_state = []
        for row in state:
            new_row = copy.copy(row)
            cloned_state.append(new_row)
        return cloned_state


    def get_heuristic(self, state):
        return max(self.euclidean_dist_heuristic(state),\
                   self.out_of_row_col_heuristic(state))

    def euclidean_dist_heuristic(self, state):
        '''Sums up the total offset of tiles in terms of euclidean distance'''
        dist = 0
        for i in range(3):
            for j in range(3):
                # ignoring the empty space, aka, 0
                if state[i][j] == 0:
                    continue
                goal_coord_x, goal_coord_y = self.goal_coord[state[i][j]]
                dist += math.sqrt(math.pow((goal_coord_x - i), 2)\
                                  + math.pow((goal_coord_y - i), 2))
        return dist

    def out_of_row_col_heuristic(self, state):
        '''
        Count and return number of tiles out of row
        + Number of tiles out of column
        '''
        count = 0
        for i in range(3):
            for j in range(3):
                # ignoring the empty space, aka, 0
                if state[i][j] == 0:
                    continue
                goal_coord_x, goal_coord_y = self.goal_coord[state[i][j]]
                if i != goal_coord_x:
                    count += 1
                if j != goal_coord_y:
                    count += 1
        return count

    def get_legal_moves(self, i, j):
        """
        Takes in coordinate of empty space, and use it to determine the current state
        Returns a list of legal moves to take for current state
        """
        legal_moves = list()
        for action in self.action_dic.keys():
            coordinate_change = self.action_dic[action]
            new_i = coordinate_change[0] + i
            new_j = coordinate_change[1] + j
            if (new_i >= 0 and new_i < 3) and (new_j >= 0 and new_j < 3):
                legal_moves.append(self.reflection_dic[action])
        return legal_moves

    def move(self, state, move_cmd, i, j):
        """
        Takes in move_cmd, which dictates move you desire
        Takes in coordinates of empty space
        Pre-condition: move_cmd has to be valid for the current configuration
        Post-condition: returns a NEW state
        """
        new_state = self.clone_state(state)
        coordinate_change = self.action_dic[self.reflection_dic[move_cmd]]
        new_state[i][j], new_state[i + coordinate_change[0]][j + coordinate_change[1]] = \
                               new_state[i + coordinate_change[0]][j + coordinate_change[1]]\
                               , new_state[i][j]
        return new_state

    def find_empty_space(self, state):
        """Evaluates the state and returns index of empty space"""
        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    return (i, j)

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


# This class models the graph nodes within A* search
class Node:
    def __init__(self, state, g, actions):
        self.g = g
        self.state = state
        self.actions = actions

    def __str__(self):
        return str(self.g) + " " + str(self.actions)

    def __lt__(self, node_two):
        return self.g < node_two.g

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        raise IOError("Input file not found!")

    init_state = [[0 for i in range(3)] for j in range(3)]
    goal_state = [[0 for i in range(3)] for j in range(3)]
    lines = f.readlines()

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

    puzzle = Puzzle(init_state, goal_state)
    ans = puzzle.solve()

    with open(sys.argv[2], 'a') as f:
        for answer in ans:
            f.write(answer+'\n')
