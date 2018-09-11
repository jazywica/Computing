# -*- encoding: utf-8 -*-
""" Template testing suite for Project_4 - this is the TESTING SUITE, all tests are run from here """

import poc_simpletest  # imports testing engine
import _03_Project_4 as pro  # imports the algorithms we are going to test


def run_suite():
    """ Some informal testing code """
	
    def print_matrix(matrix):
        for row in matrix:
            print(row)
    suite = poc_simpletest.TestSuite()  # create a TestSuite object
    print("\nSTARTING TESTS:")


    # 1. check the basic MATRIX methods directly
    suite.run_test(pro.build_scoring_matrix({"A", "B", "C"}, 10, 4, -4)['A'], {'A': 10, 'C': 4, 'B': 4, '-': -4}, "Test #1a: 'build_scoring_matrix' method")  # due to technical reasons we only check the first key 'A"
    suite.run_test(pro.build_scoring_matrix({'A', 'C', 'T', 'G'}, 6, 2, -4)['-'], {'A': -4, 'C': -4, '-': -4, 'T': -4, 'G': -4}, "Test #1b: 'build_scoring_matrix' method")

    sc_matrix = pro.build_scoring_matrix({'A', 'C', 'T', 'G'}, 10, 2, -4)
    al_matrix = pro.compute_alignment_matrix("ACC", "TTTACACGG", sc_matrix, True)
    suite.run_test(al_matrix[-1], [-12, -6, 0, 6, 2, 6, 10, 14, 10, 6], "Test #1c: 'compute_alignment_matrix' method")  # we only need to check the last row


    # 2. check the basic ALIGNMENT methods directly
    suite.run_test(pro.compute_global_alignment("ACC", "TTTACACGG", sc_matrix, al_matrix), (6, '---AC-C--', 'TTTACACGG'), "Test #2a: 'compute_global_alignment' method")  # testing the example 1c above

    sc_matrix = {'A': {'A': 2, 'C': 1, '-': 0, 'T': 1, 'G': 1}, 'C': {'A': 1, 'C': 2, '-': 0, 'T': 1, 'G': 1}, '-': {'A': 0, 'C': 0, '-': 0, 'T': 0, 'G': 0}, 'T': {'A': 1, 'C': 1, '-': 0, 'T': 2, 'G': 1}, 'G': {'A': 1, 'C': 1, '-': 0, 'T': 1, 'G': 2}}
    al_matrix = [[0, 0, 0, 0, 0, 0], [0, 2, 2, 2, 2, 2], [0, 2, 3, 4, 4, 4], [0, 2, 3, 4, 6, 6], [0, 2, 3, 4, 6, 8], [0, 2, 3, 5, 6, 8], [0, 2, 3, 5, 7, 8]]
    suite.run_test(pro.compute_global_alignment("ACTACT", "AGCTA", sc_matrix, al_matrix),(8, 'A-CTACT', 'AGCTA--'), "Test #2b: 'compute_global_alignment' method")

    sc_matrix = pro.build_scoring_matrix({"A", "C", "G", "T"}, 10, 2, -4)
    al_matrix = pro.compute_alignment_matrix("ACC", "TTTACACGG", sc_matrix, False)
    suite.run_test(pro.compute_local_alignment("ACC", "TTTACACGG", sc_matrix, al_matrix), (26, 'AC-C', 'ACAC'), "Test #2c: 'compute_local_alignment' method")


    # 3. report number of tests and failures
    suite.report_results()


run_suite()
