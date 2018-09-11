# -*- encoding: utf-8 -*-
""" Project #4 - Dynamic Programming: Similarity of the substrings """


def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    """ The function returns a dictionary of dictionaries whose entries are indexed by pairs of characters in 'alphabet' plus ’-’ """
    alphabet = set(alphabet) | set('-')  # first we have to add the missing "-" value
    scoring_matrix = {}  # this is where we are going to put our dictionaries

    for row in alphabet:
        scoring_matrix[row] = {}  # this is how we create a dictionary of dictionaries
        for col in alphabet:  # based on what type of character we encounter, we assign the appropriate value
            if row == '-' or col == '-':  # we execute this condition first, as we want a score of -4 for a pair ('-', '-'), not 6
                scoring_matrix[row][col] = dash_score
            elif row == col:
                scoring_matrix[row][col] = diag_score
            else:
                scoring_matrix[row][col] = off_diag_score

    return scoring_matrix  # we have the dictionary ready now , we can access it by: scoring_matrix[row_char][col_char]


def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):  # 'global_flag' is to determine whether it is a global or local alignment matrix
    """ The function computes and returns the alignment matrix for 'seq_x' and 'seq_y' for either global or local alignment """
    len_x = len(seq_x)
    len_y = len(seq_y)
    s_matrix = [[None for dummy_j in range(len_y + 1)] for dummy_i in range(len_x + 1)]  # 'S' matrix is one row and one column bigger than m x n matrix, because of the extra '-' lines telling us how much does it cost to insert '-' in the sequence
    s_matrix[0][0] = 0

    # Now we are going to start the iterations. We are operating on two sets of indices, S matrix is always grater from X and Y by 1
    for idx_i in range(1, len_x + 1):  # this will fill in the first column with the increasing costs of replacing Y element with '-'
        s_matrix[idx_i][0] = s_matrix[idx_i - 1][0] + scoring_matrix[seq_x[idx_i - 1]]['-']  # S[i - 1][0] refers to the element ABOVE and M refers to the actual letter in X
        if global_flag == False and s_matrix[idx_i][0] < 0:  # for local alignments we are going to replace negative numbers with zeroes
            s_matrix[idx_i][0] = 0

    for idx_j in range(1, len_y + 1):  # this will fill in the first row with the increasing costs of replacing X element with '-'
        s_matrix[0][idx_j] = s_matrix[0][idx_j - 1] + scoring_matrix['-'][seq_y[idx_j - 1]]  # S[0][j - 1] refers to the element TO LEFT and M refers to the actual letter in Y
        if global_flag == False and s_matrix[0][idx_j] < 0:
            s_matrix[0][idx_j] = 0

    for idx_i in range(1, len_x + 1):  # based on the ready-made rows and columns, we can calculate the inside of the matrix
        for idx_j in range(1, len_y + 1):
            score_xy = scoring_matrix[seq_x[idx_i - 1]][seq_y[idx_j - 1]]  # score from the M matrix for the current elements of X and Y
            replace_y = scoring_matrix[seq_x[idx_i - 1]]['-']  # score from the M matrix for replacing Y element with '-'
            replace_x = scoring_matrix['-'][seq_y[idx_j - 1]]  # score from the M matrix for replacing Y element with '-'
            s_matrix[idx_i][idx_j] = max(s_matrix[idx_i - 1][idx_j - 1] + score_xy, s_matrix[idx_i - 1][idx_j] + replace_y, s_matrix[idx_i][idx_j - 1] + replace_x)

            if global_flag == False and s_matrix[idx_i][idx_j] < 0:
                s_matrix[idx_i][idx_j] = 0

    return s_matrix


def compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """ This function computes a global alignment of 'seq_x' and 'seq_y', it returns a tuple of the form (score, align_x, align_y) where 'score' is the score of the global alignment align_x and align_y """
    aligned_x = ""
    aligned_y = ""
    idx_i = len(seq_x)  # for global alignments the backtracking starts from the last element in the alignment matrix
    idx_j = len(seq_y)

    while idx_i != 0 and idx_j != 0:  # we start backtracking now, and try to find out how we go to the final score (the last entry in the matrix)
        if alignment_matrix[idx_i][idx_j] == alignment_matrix[idx_i - 1][idx_j - 1] + scoring_matrix[seq_x[idx_i - 1]][seq_y[idx_j - 1]]:  # the diagonal move always comes before the lateral moves
            aligned_x = seq_x[idx_i - 1] + aligned_x
            aligned_y = seq_y[idx_j - 1] + aligned_y
            idx_i -= 1
            idx_j -= 1
        else:
            if alignment_matrix[idx_i][idx_j] == alignment_matrix[idx_i - 1][idx_j] + scoring_matrix[seq_x[idx_i - 1]]['-']:
                aligned_x = seq_x[idx_i - 1] + aligned_x
                aligned_y = "-" + aligned_y
                idx_i -= 1
            else:
                aligned_x = "-" + aligned_x
                aligned_y = seq_y[idx_j - 1] + aligned_y
                idx_j -= 1

    while idx_i != 0:  # for the global alignment, if there are any i or j elements left, we pick them up replacing the missing letters with '-'
        aligned_x = seq_x[idx_i - 1] + aligned_x
        aligned_y = "-" + aligned_y
        idx_i -= 1
    while idx_j != 0:
        aligned_x = "-" + aligned_x
        aligned_y = seq_y[idx_j - 1] + aligned_y
        idx_j -= 1

    return (alignment_matrix[-1][-1], aligned_x, aligned_y)  # the final score in the global alignment is always the last element in the alignment matrix


def compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """ This function computes a local alignment of 'seq_x' and 'seq_y', it returns a tuple of the form (score, align_x, align_y) where 'score' is the score of the optimal local alignment align_x and align_y """
    aligned_x = ""
    aligned_y = ""
    max_val = float('-inf')
    idx = (0, 0)
    for row in range(len(seq_x) + 1):
        for col in range(len(seq_y) + 1):
            if alignment_matrix[row][col] > max_val:
                max_val = alignment_matrix[row][col]  # for local alignments the backtracking starts from the biggest element in the matrix. the matrix itself is without negative numbers
                idx = (row, col)
    idx_i, idx_j = idx

    while idx_i != 0 and idx_j != 0:  # we start backtracking now, and try to find out how we go to the final score (the last entry in the matrix) until we reach the row or col = 0
        if alignment_matrix[idx_i][idx_j] == 0:  # for the local alignment we go on until we come across '0', we are not gluing '-' neither in front nor in the end of the letters
            return (max_val, aligned_x, aligned_y)

        if alignment_matrix[idx_i][idx_j] == alignment_matrix[idx_i - 1][idx_j - 1] + scoring_matrix[seq_x[idx_i - 1]][seq_y[idx_j - 1]]:  # the diagonal move always comes before the lateral moves
            aligned_x = seq_x[idx_i - 1] + aligned_x
            aligned_y = seq_y[idx_j - 1] + aligned_y
            idx_i -= 1
            idx_j -= 1
        else:
            if alignment_matrix[idx_i][idx_j] == alignment_matrix[idx_i - 1][idx_j] + scoring_matrix[seq_x[idx_i - 1]]['-']:
                aligned_x = seq_x[idx_i - 1] + aligned_x
                aligned_y = "-" + aligned_y
                idx_i -= 1
            else:
                aligned_x = "-" + aligned_x
                aligned_y = seq_y[idx_j - 1] + aligned_y
                idx_j -= 1

    return (max_val, aligned_x, aligned_y)  # the final score in the local alignment is always the biggest element in the alignment matrix
