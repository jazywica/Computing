# -*- encoding: utf-8 -*-
""" Construct list of binary numbers of given length. Creates natural binary numbers and Gray codes """


# 1. BINARY NUMBERS
def make_binary(length):
    """ Function that generates ordered list of binary numbers in ascending order """
    if length == 0:
        return [""]

    all_but_first = make_binary(length - 1)  # this will take us all the way to the bottom of the recursion

    answer = []  # this is a single entity that is going to be used locally to output the result further
    for bits in all_but_first:
        answer.append("0" + bits)  # in these two next loops we are going to add '0' and '1' to the original 'all_but_first' list derived from the recursion
    for bits in all_but_first:
        answer.append("1" + bits)
    return answer  # 1st round: ['0', '1'], 2nd: ['00', '01', '10', '11'], 3rd: ['000', '001', '010', '011', '100', '101', '110', '111'], 4th: ['0000', '0001', '0010', '0011', '0100', '0101', '0110', '0111', '1000', '1001', '1010', '1011', '1100', '1101', '1110', '1111']


def bin_to_dec(bin_num):
    """ Convert a binary number to decimal """
    if len(bin_num) == 0:
        return 0
    else:
        above = 2 * bin_to_dec(bin_num[:-1])  # here we call recursively smaller and smaller parts of the number to the left. on the way back we multiply each 1 by 2 as we move further to the right
        current = int(bin_num[-1])  # this is the current digit we are on at a particular call - always the last element of 'bin_num'
        result = above + current  # EX: for the 00111 on the way back we get: 0 + 0 + 1*2*2 + 1*2 + 1 = 7
        return result


# 2. GRAY CODE: after Frank Gray, is an ordering of the binary numeral system such that two successive values differ in only one bit (binary digit)
# Using a standard binary number system, the resulting n-bit number may have several incorrect bits. For example, if the value 7 was incorrectly scanned as 8, the resulting five-bit binary strings "00111" and "01000"
# would differ by 4 bits. In gray code the five-bit Gray codes corresponding to 7 and 8 are "00100" and "01100", respectively. Note that these two strings differ by exactly one bit.
def make_gray(length):
    """ Function that generates ordered list of Gray codes in ascending order """
    if length == 0:
        return [""]

    all_but_first = make_gray(length - 1)

    answer = []
    for bits in all_but_first:
        answer.append("0" + bits)

    all_but_first.reverse()  # basically what we have to do is to avoid jumps like 1111 to 10000, therefore we have to reverse the list in the middle of the process, so it doesn't end with 1111, but with 1000 and onto 10000

    for bits in all_but_first:
        answer.append("1" + bits)
    # Now lets compare the original 'make_binary' with the 'make_gray'
    # 1st round: ['0', '1'], 2nd: ['00', '01', '10', '11'], 3rd: ['000', '001', '010', '011', '100', '101', '110', '111'], 4th: ['0000', '0001', '0010', '0011', '0100', '0101', '0110', '0111', '1000', '1001', '1010', '1011', '1100', '1101', '1110', '1111']
    # 1st round: ['0', '1'], 2nd: ['00', '01', '11', '10'], 3rd: ['000', '001', '011', '010', '110', '111', '101', '100'], 4th: ['0000', '0001', '0011', '0010', '0110', '0111', '0101', '0100', '1100', '1101', '1111', '1110', '1010', '1011', '1001', '1000']
    return answer


def gray_to_bin(gray_code):
    """ Convert a Gray code to a binary number """
    if len(gray_code) <= 1:  # this function goes from the right to left and back. it turns around and rewrites the first significant figure
        return gray_code
    else:
        significant_bits = gray_to_bin(gray_code[:-1])
        last_gray = int(gray_code[-1])  # this is the level we are currently at
        last_sign = int(significant_bits[-1])  # this is the level up (in significance)
        last_bit = (last_gray + last_sign) % 2  # here we add the two above to get the current (last) bit (either 0 or 1)
        return significant_bits + str(last_bit)  # at the end we return the unchanged significant numbers plus the calculated last bit (for each recursive call)


def run_examples():
    """ print out example of Gray code representations """
    num = 5
    print()
    print("Binary numbers of length", num)
    bin_list = make_binary(num)
    print(bin_list)
    print()
    print("Decimal numbers up to", 2 ** num)
    print([bin_to_dec(binary_number) for binary_number in bin_list])
    print()
    print("Gray codes of length", num)
    gray_list = make_gray(num)
    print(gray_list)
    print()
    print("Gray codes converted to binary numbers")
    print([gray_to_bin(gray_code) for gray_code in gray_list])
    print()
    print("Gray codes converted to decimal numbers")
    print(bin_to_dec(gray_to_bin("1100")))  # this should return 8


run_examples()
