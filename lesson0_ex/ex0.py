# name: golan matuf
# date: 20211007

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
    five_digits = input("please enter a five digit number: ")
    digits_str, digits_sum = make_magic(five_digits)
    print("you entered the number:", five_digits)
    print("the digits of this number are:", digits_str)
    print("the sum of the digits is:", digits_sum)


if __name__ == '__main__':
    main()
