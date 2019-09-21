import sys

"""
Usage:
Takes in initial state
And prints True if state is solvable. Else, print False

Description:
This is a helper script that checks whether given matrix
is solvable or not
If it is not solvable,
Then it becomes pointless to run the scripts to solve it
"""

class SolveChecker:
    def can_solve_or_not(self, matrix):
        arr = []
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == 0:
                    continue
                else:
                    arr.append(matrix[i][j])
                    
        inversion_count = self.get_inversion_count(arr)
        
        if inversion_count % 2 == 0:
            return True
        else:
            return False

    def get_inversion_count(self, array):
        count = 0
        for i in range(len(array)):
            for j in range(i + 1, len(array)):
                if array[i] > array[j]:
                    count += 1
        return count

# Reading file containing initial state
if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError("Wrong number of arguments!")

    try:
        matrix = open(sys.argv[1], 'r')
    except IOError:
        raise IOError("Input file(s) not found!")
    
    init_state = [[0 for i in range(3)] for j in range(3)]
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
    solve_checker = SolveChecker()
    print(solve_checker.can_solve_or_not(init_state))
    
