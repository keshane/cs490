import numpy

class Hungarian(object):
    """
    Performs the Hungarian algorithm according to the Munkres paper
    
    Complexity of O(n^3)
    """
    STAR = 1
    PRIME = 2

    def __init__(self, cost_matrix):
        self.matrix = cost_matrix
        self.nrows = cost_matrix.shape[0]
        self.ncols = cost_matrix.shape[1]
        self.cols_covered = [False for i in range(self.ncols)]
        self.rows_covered = [False for i in range(self.nrows)]

        self.finished = False

        self.marked = numpy.empty_like(cost_matrix)
        self.marked.fill(0)
        self.state = 0

    def run(self):

        # subtract least element of every row and column
        min_costs = numpy.amin(self.matrix, axis=1)
        min_costs = min_costs[None].transpose()
        self.matrix = self.matrix - min_costs
        min_costs = numpy.amin(self.matrix, axis=0)
        self.matrix = self.matrix - min_costs

        for i in range(self.nrows):
            for j in range(self.ncols):
                if self.matrix[i][j] == 0 and not self._is_starred(i, j):
                    self.marked[i][j] = self.STAR 
                    self.cols_covered[j] = True

                    # break because this row has been covered already
                    break

        self.state = 1 

        states = {1: self._step1, 2 : self._step2, 3: self._step3}

        while not self.state == 4:
            if self.state == 2:
                states[self.state](*(ret_val))
            else:
                ret_val = states[self.state]()

        return self.marked

    def _is_starred(self, i, j):
        if self.marked[i][j] == self.STAR:
            return True
        else:
            return False

    def _is_covered(self, i, j):
        if self.rows_covered[i] or self.cols_covered[j]:
            return True
        else:
            return False

    def _star_in_row(self, i):
        for j in range(self.ncols):
            if self._is_starred(i,j):
                return j
        return -1

    def _step1(self):

        for i in range(self.nrows):
            for j in range(self.ncols):
                if self.matrix[i][j] == 0 and not self._is_covered(i,j):
                    self.marked[i][j] = self.PRIME

                    starred_col = self._star_in_row(i) 

                    # -1 means there was no star in this row
                    if starred_col == -1:
                        self.state = 2
                        return (i, j)
                    else:
                        self.rows_covered[i] = True
                        self.cols_covered[starred_col] = False

        self.state = 3

    def _step2(self, row, col):
        i = row
        j = col
        path = []
        path.append((i,j))
        path_ended = False

        while not path_ended:
            # This may not exist
            i = self._get_star_in_col(i, j)
            if i == -1:
                path_ended = True
                break
            path.append((i,j))

            j = self._get_prime_in_row(i, j)
            path.append((i,j))

        for zero in path:
            self._toggle_zero_in_sequence(*zero)

        self.rows_covered[:] = [False for _ in range(self.nrows)]
        self.cols_covered[:] = [False for _ in range(self.ncols)]

        self._cover_cols_of_stars()

        if self._all_cols_covered():
            finished = True
            self.state = 4
        else:
            self.state = 1

    def _step3(self):
        min_val = self._get_smallest()

        for i in range(self.nrows):
            if self.rows_covered[i]:
                for j in range(self.ncols):
                    self.matrix[i][j] = self.matrix[i][j] + min_val

        for j in range(self.ncols):
            if not self.cols_covered[j]:
                for i in range(self.nrows):
                    self.matrix[i][j] = self.matrix[i][j] - min_val

        self.state = 1


    def _get_smallest(self):
        min_so_far = 1000000

        for i in range(self.nrows):
            for j in range(self.ncols):
                if not self._is_covered(i,j) and self.matrix[i][j] < min_so_far:
                    min_so_far = self.matrix[i][j]

        return min_so_far


    def _all_cols_covered(self):
        for j in range(self.ncols):
            if not self.cols_covered[j]:
                return False

        return True

    def _cover_cols_of_stars(self):
        for j in range(self.ncols):
            for i in range(self.nrows):
                if self.marked[i][j] == self.STAR:
                    self.cols_covered[j] = True
                if self.marked[i][j] == self.PRIME:
                    self.marked[i][j] = 0


    def _toggle_zero_in_sequence(self, i, j):
        if self.marked[i][j] == self.STAR:
            self.marked[i][j] = 0
        elif self.marked[i][j] == self.PRIME:
            self.marked[i][j] = self.STAR
        else:
            print("impossible")

    def _get_prime_in_row(self, i, col_of_prime):
        for j in range(self.ncols):
            if self.marked[i][j] == self.PRIME and col_of_prime != j:
                return j

        print("This should never happen")
        return -1

    def _get_star_in_col(self, row_of_star, j):
        for i in range(self.nrows):
            if self.marked[i][j] == self.STAR and row_of_star != i:
                return i
        return -1


