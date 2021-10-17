# name: golan matuf
# date: 20211007
import this
NUMBER_OF_DIGITS = 5


def check_functions():
    assert (check_numbers('12345')) is True
    assert (check_numbers('abcde')) is False
    assert (check_numbers('123')) is False
    assert (check_numbers('')) is False
    assert (check_numbers('0000000000')) is False
    assert (check_numbers('a')) is False
    assert (check_numbers('1234O')) is False


def check_numbers(num):
    """
    check if the user input is
    :param num: a string that needs checking if it's length equal NUMBER_OF_DIGITS,
                and check that it is a decimal number that we can sum
    :return:
    """
    if len(num) != NUMBER_OF_DIGITS or not num.isdecimal():
        return False
    return True


def make_magic(num):
    """
    :param num: a number that we need to process, initially a five digit number
    :return: digits_str: a string of the number digit separated by ','.
             digits_sum: the digits sum.
    """
    # convert num to list of strings
    digits_list = list(num)
    # join the digit to a single string with ',' in between
    digits_str = ','.join(digits_list)
    # convert each digit to integer -> sum the ints
    digits_sum = sum(int(i) for i in digits_list)
    # returns:
    return digits_str, digits_sum


def main():
    check_functions()
    five_digits = input("please enter a five digit number: ")
    while not check_numbers(five_digits):
        five_digits = input("please enter a five digit number: ")
    digits_str, digits_sum = make_magic(five_digits)
    print("you entered the number:", five_digits)
    print("the digits of this number are:", digits_str)
    print("the sum of the digits is:", digits_sum)


if __name__ == '__main__':
    main()
