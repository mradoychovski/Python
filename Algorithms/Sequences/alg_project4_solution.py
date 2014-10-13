"""
    Project 4 - Computing alignments of sequences
"""


def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    """
    Takes as input a set of characters alphabet and three scores diag_score,
    off_diag_score, and dash_score. The function returns a dictionary of
    dictionaries whose entries are indexed by pairs of characters in alphabet
    plus '-'. The score for any entry indexed by one or more dashes is
    dash_score. The score for the remaining diagonal entries is diag_score.
    Finally, the score for the remaining off-diagonal entries is off_diag_score.
    """
    scoring_matrix = {i: {j: 0 for j in alphabet} for i in alphabet}
    for row in alphabet:
        for col in alphabet:
            if row == '-' or col == '-':
                scoring_matrix[row][col] = dash_score
            elif row == col:
                scoring_matrix[row][col] = diag_score
            else:
                scoring_matrix[row][col] = off_diag_score
    return scoring_matrix


def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):
    """
    Takes as input two sequences seq_x and seq_y whose elements share a common
    alphabet with the scoring matrix scoring_matrix.
    """
    m_len_x, n_len_y = len(seq_x), len(seq_y)
    alignment_matrix = [[0]]
    for item in range(1, m_len_x+1):
        alignment_matrix.append(
            [alignment_matrix[item-1][0] + scoring_matrix[seq_x[item-1]]['-']])
        if (not global_flag) and alignment_matrix[item][0] < 0:
            alignment_matrix[item][0] = 0
    for jtem in range(1, n_len_y+1):
        alignment_matrix[0].append(
            alignment_matrix[0][jtem-1] + scoring_matrix['-'][seq_y[jtem-1]])
        if (not global_flag) and alignment_matrix[0][jtem] < 0:
            alignment_matrix[0][jtem] = 0
    for item in range(1, m_len_x+1):
        for jtem in range(1, n_len_y+1):
            alignment_matrix[item].append(
                max(alignment_matrix[item-1][jtem-1] +
                scoring_matrix[seq_x[item-1]][seq_y[jtem-1]],
                alignment_matrix[item-1][jtem] +
                scoring_matrix[seq_x[item-1]]['-'],
                alignment_matrix[item][jtem-1] +
                scoring_matrix['-'][seq_y[jtem-1]]))
            if (not global_flag) and alignment_matrix[item][jtem] < 0:
                alignment_matrix[item][jtem] = 0

    return alignment_matrix


def compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    Takes as input two sequences seq_x and seq_y whose elements share
    a common alphabet with the scoring matrix scoring_matrix.
    This function computes a global alignment of seq_x and seq_y
    using the global alignment matrix alignment_matrix.
    """
    ith, jth = len(seq_x), len(seq_y)
    x_prime, y_prime = '', ''
    while ith != 0 and jth != 0:
        if alignment_matrix[ith][jth] == \
            alignment_matrix[ith-1][jth-1] + \
            scoring_matrix[seq_x[ith-1]][seq_y[jth-1]]:
            x_prime = seq_x[ith-1] + x_prime
            y_prime = seq_y[jth-1] + y_prime
            ith -= 1
            jth -= 1
        else:
            if alignment_matrix[ith][jth] == \
                alignment_matrix[ith-1][jth] + \
                scoring_matrix[seq_x[ith-1]]['-']:
                x_prime = seq_x[ith-1] + x_prime
                y_prime = '-' + y_prime
                ith -= 1
            else:
                x_prime = '-' + x_prime
                y_prime = seq_y[jth-1] + y_prime
                jth -= 1

    while ith != 0:
        x_prime = seq_x[ith-1] + x_prime
        y_prime = '-' + y_prime
        ith -= 1

    while jth != 0:
        x_prime = '-' + x_prime
        y_prime = seq_y[jth-1] + y_prime
        jth -= 1

    score = alignment_matrix[len(seq_x)][len(seq_y)]
    return (score, x_prime, y_prime)


def compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    Takes as input two sequences seq_x and seq_y whose elements share a common
    alphabet with the scoring matrix scoring_matrix. This function computes
    a local alignment of seq_x and seq_y using the local alignment matrix
    alignment_matrix.
    """
    ith = len(seq_x)
    max_pos = alignment_matrix[ith].index(max(alignment_matrix[ith]))
    jth = max_pos
    x_prime, y_prime = '', ''
    while alignment_matrix[ith][jth] != 0:

        if alignment_matrix[ith][jth] == \
            alignment_matrix[ith-1][jth-1] + \
            scoring_matrix[seq_x[ith-1]][seq_y[jth-1]]:
            x_prime = seq_x[ith-1] + x_prime
            y_prime = seq_y[jth-1] + y_prime
            ith -= 1
            jth -= 1

        elif alignment_matrix[ith][jth] == \
            alignment_matrix[ith][jth-1] + \
            scoring_matrix['-'][seq_y[jth-1]]:
            x_prime = '-' + x_prime
            y_prime = seq_y[jth-1] + y_prime
            jth -= 1

        elif alignment_matrix[ith][jth] == \
            alignment_matrix[ith-1][jth] + \
            scoring_matrix[seq_x[ith-1]]['-']:
            x_prime = seq_x[ith-1] + x_prime
            y_prime = '-' + y_prime
            ith -= 1

    align_matrix = \
        compute_alignment_matrix(x_prime, y_prime, scoring_matrix, True)
    (score, align_x, align_y) = compute_global_alignment(
        x_prime, y_prime, scoring_matrix, align_matrix)

    return (score, align_x, align_y)


def global_alignment(seq_x, seq_y, scoring_matrix):
    """
    Input:
        Two sequences seq_x and seq_y
        scoring_matrix
    Return:
        Tuple of global alinment score and aligned sequences align_x and align_y
    """
    alignment_matrix = \
        compute_alignment_matrix(seq_x, seq_y, scoring_matrix, True)

    (score, align_x, align_y) = \
        compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix)

    return (score, align_x, align_y)


def local_alignment(seq_x, seq_y, scoring_matrix):
    """
    Input:
        Two sequences seq_x and seq_y
        scoring_matrix
    Return:
        Tuple of local alignment score and aligned sequences align_x and align_y
    """
    alignment_matrix = \
        compute_alignment_matrix(seq_x, seq_y, scoring_matrix, False)

    (score, align_x, align_y) = \
        compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix)

    return (score, align_x, align_y)
