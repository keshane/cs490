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

    def run(self):

        # subtract least element of every row and column
        min_costs = numpy.amin(self.matrix, axis=1)
        self.matrix = self.matrix - min_costs.transpose()
        min_costs = numpy.amin(self.matrix, axis=0)
        self.matrix = self.matrix - min_costs

        for i in range(self.nrows):
            for j in range(self.ncols):
                if self.matrix[i][j] == 0 and not _is_starred(i, j):
                    self.marked[i][j] = STAR 
                    self.cols_covered[j] = True

                    # break because this row has been covered already
                    break
        _step1()

    def _is_covered(self, i, j):
        if self.rows_covered[i] or self.cols_covered[j]:
            return True
        else:
            return False

    def _star_in_row(self, i):
        for j in range(self.ncols):
            if _is_starred(i,j):
                return j
        return -1

    def _step1(self):

        for i in range(self.nrows):
            for j in range(self.ncols):
                if self.matrix[i][j] == 0 and not _is_covered(i,j):
                    self.marked[i][j] = PRIME

                    starred_col = _star_in_row(i) 

                    # -1 means there was no star in this row
                    if starred_col == -1:
                        _step2(i, j)
                        if self.finished:
                            return
                    else:
                        self.rows_covered[i] = True
                        self.cols_covered[starred_col] = False

    def _step2(self, row, col):
        i = row
        j = col
        path = []
        path.append((i,j))
        path_ended = False
        look_for = PRIME

        while not path_ended:
            # This may not exist
            i = _get_prime_in_col(j)
            if i == -1:
                path_ended = True
                break
            path.append((i,j))

            j = _get_star_in_row(i)
            path.append((i,j))

        for zero in path:
            _toggle_zero_in_sequence(*zero)

        self.rows_covered[:] = False
        self.cols_covered[:] = False

        _cover_cols_of_stars()

        if _all_cols_covered():
            finished = True

    def _step3():
        min_val = _get_smallest()

        for i in range(self.nrows):
            if rows_covered[i]:
                for j in range(self.ncols):
                    matrix[i][j] = matrix[i][j] + min_val

        for j in range(self.ncols):
            if not cols_covered[i]:
                for i in range(self.nrows):
                    matrix[i][j] = matrix[i][j] - min_val

        _step1()



    def _get_smallest(self):
        min_so_far = 0

        for i in range(self.nrows):
            for j in range(self.ncols):
                if not _is_covered(i,j) and self.matrix[i][j] < min_so_far:
                    min_so_far = self.matrix[i][j]


    def _all_cols_covered(self):
        for j in range(self.ncols):
            if not self.cols_covered[j]:
                return False

        return True

    def _cover_cols_of_stars(self):
        for j in range(self.ncols):
            for i in range(self.nrows):
                if self.marked[i][j] == STAR:
                    self.cols_covered[j] = True
                if self.marked[i][j] == PRIME:
                    self.marked[i][j] = 0


    def _toggle_zero_in_sequence(self, i, j):
        if self.marked[i][j] == STAR:
            self.marked[i][j] = 0
        else if self.marked[i][j] == PRIME:
            self.marked[i][j] = STAR
        else:
            print("impossible")

    def _get_star_in_row(self, i):
        for j in range(self.ncols):
            if self.marked[i][j] == STAR:
                return j

        print("This should never happen")
        return -1

    def _get_prime_in_col(self, j):
        for i in range(nrows):
            if self.marked[i][j] == PRIME:
                return i
        return -1




                



    def _is_starred(i, j):
        if self.marked[i][j] == STAR:
            return True
        else:
            return False

     if count == matrix.shape[1]:
        # done

    for i in range(matrix.shape[0]):
        if rows_covered[i]:
            continue
        for j in range(matrix.shape[1]):
            if cols_covered[j]:
                continue

            if matrix[i][j] == 0:
                marked[i][j] = PRIME

                has_star = False

                for k in range(matrix.shape[1]):
                    if marked[i][k] == STAR:
                        rows_covered[i] = True
                        cols_covered[j] = False
                        has_star = True
                        break

                if not has_star:
                    alternat
