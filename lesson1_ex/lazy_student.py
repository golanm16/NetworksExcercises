# author: golan matuf
# date: 12.10.21 (20211014)
# python lazy_student.py homework.txt solutions.txt

TEXT_FILE_TYPE = '.txt'
NUMBER_OF_ARGUMENTS = 2
OPERATORS = '/*-+'


# assert (check_numbers('12345')) is True
# assert (check_numbers('abcde')) is False
# assert (check_numbers('123')) is False
# assert (check_numbers('')) is False
# assert (check_numbers('0000000000')) is False
# assert (check_numbers('a')) is False
# assert (check_numbers('1234O')) is False


def check_functions():
    # region check checkfile
    try:
        # this asserts can be easily manipulated
        # i wont let you have the satisfaction ;)
        assert (check_file('file.txt')) == (True, "no error")
        assert (check_file('file0.txt')) == (False, "file does not exist")
        assert (check_file('file.ospf')) == (False, "file extension is not " + TEXT_FILE_TYPE)
        assert (check_file('file')) == (False, "file extension is not " + TEXT_FILE_TYPE)
        assert (check_file('file0')) == (False, "file does not exist")
    finally:
        pass
    # endregion
    # region check check_valid_homework
    assert (check_valid_homework('1 + 3')) \
           == (True, 'no error')
    assert (check_valid_homework('1+ 3')) \
           == (False, " : error: one or more of the operands is not a number\n")
    assert (check_valid_homework('1 + a')) \
           == (False, " : error: one or more of the operands is not a number\n")
    assert (check_valid_homework('+ + 1')) \
           == (False, " : error: one or more of the operands is not a number\n")
    assert (check_valid_homework('O + 1')) \
           == (False, " : error: one or more of the operands is not a number\n")
    assert (check_valid_homework('1 + ¹²³')) \
           == (False, " : error: one or more of the operands is not a number\n")
    assert (check_valid_homework('1 | 1')) \
           == (False, " : error: the operator is not in the list of recognized operators\n")
    assert (check_valid_homework('1 1 1')) \
           == (False, " : error: the operator is not in the list of recognized operators\n")
    assert (check_valid_homework('1+11')) \
           == (False, " : error: hw_line not following the homework convention: operand1 operator operand2\n")
    assert (check_valid_homework('1 +   1')) \
           == (False, " : error: hw_line not following the homework convention: operand1 operator operand2\n")
    assert (check_valid_homework('1- 0')) \
           == (False, " : error: hw_line not following the homework convention: operand1 operator operand2\n")
    assert (check_valid_homework('1 * -1')) \
           == (False, " : error: one or more of the operands is not a number\n")
    # endregion


def check_file(file):
    """
    get a file and check if the file exists and ends with TEXT_FILE_TYPE
    :param file: given file
    :return: file exists and ends with wanted extension
    """
    from os.path import exists
    # check that file exists
    if not exists(file):
        return False, "file does not exist"
    # check that  file extension is '.txt'
    if not file.endswith(TEXT_FILE_TYPE):
        return False, "file extension is not " + TEXT_FILE_TYPE
    return True, "no error"


def check_valid_homework(hw_line):
    """
    check that a line is a relevant exercise that is like
        operand1 operator operand2
    :param hw_line: homework exercise
    :return: True if upholds the standards for homework
    """
    ops = hw_line.split(' ')
    line_error = 'no error'
    errors_detected = False
    print(ops)
    if len(ops) == 3:
        if ops[0].isdecimal() and ops[2].isdecimal() and ops[1] in OPERATORS:
            if ops[1] == r'/' and str(ops[2]) == '0':
                errors_detected = True
                line_error = " : error: can't divide by zero\n"
            # else:
            #     solutions_file.write(hw_line + ' = ' + str(round(eval(hw_line), 4)) + '\n')
        elif not ops[0].isdecimal() or not ops[2].isdecimal():
            # one of the operands is not a number
            errors_detected = True
            line_error = " : error: one or more of the operands is not a number\n"
        elif ops[1] not in OPERATORS:
            # the operator is not in the list of known operators
            errors_detected = True
            line_error = " : error: the operator is not in the list of recognized operators\n"
        else:
            # unexpected error
            errors_detected = True
            line_error = " : error: unknown error\n"
    else:
        # invalid exercise, can't solve
        errors_detected = True
        line_error = " : error: hw_line not following the homework convention: operand1 operator operand2\n"

    # return True if there were no errors detected in the line
    return not errors_detected, line_error


def get_solution(hw_line):
    """
    solve the exercise in the given line
    exercise must be already checked
    :param hw_line: homework exercise
    :return: solved exercise rounded to max 4 digits after point
    """
    return str(round(eval(hw_line), 4))


def solve_homework(homework_file_names, solutions_file_name):
    """
    given already checked files that exists and has suitable extension(TEXT_FILE_TYPE),
     the function go line by line and solve every exercise than you can
    :param homework_file_names: the file names of the homework
                                usually 1
    :param solutions_file_name: the file name to write the solutions to
    :return: True if there was no errors in the homework files
    """
    solutions_file = open(solutions_file_name, 'w')
    errors_detected = False
    for file_name in homework_file_names:
        hw_file = open(file_name, 'r')
        for line in hw_file:
            # remove the \n from the end of the line
            hw_line = line.rstrip()
            line_valid, error_message = check_valid_homework(hw_line)
            # append the exercise to the start of what to write in the file
            write_to_file = hw_line
            if line_valid:
                # append the solution
                write_to_file += ' = ' + get_solution(hw_line) + '\n'
            else:
                # append the error received while checking the line
                errors_detected = True
                write_to_file += error_message
            solutions_file.write(write_to_file)
        hw_file.close()
    solutions_file.close()
    # return True if no errors were detected
    return not errors_detected


def main():
    check_functions()
    import sys
    # remove self reference argument
    files = sys.argv[1:]
    solutions_file_name = "solutions.txt"

    # script must have NUMBER_OF_ARGUMENTS or NUMBER_OF_ARGUMENTS-1 to work
    if len(files) > NUMBER_OF_ARGUMENTS or len(files) < NUMBER_OF_ARGUMENTS - 1:
        print('FAILED! script must have {0} or {1} arguments, exiting...'
              .format(NUMBER_OF_ARGUMENTS - 1, NUMBER_OF_ARGUMENTS))
        return
    make_solutions_file = False

    # start checking if script needs to generate solutions file
    # if the user input includes the solutions file, check the file and that it exists
    if len(files) == NUMBER_OF_ARGUMENTS:
        file_ok, error_message = check_file(files[-1])
        if file_ok:
            solutions_file_name = files[-1]
        else:
            # the user entered a solutions file in calling the script ,
            # but it is not valid
            print("error in solutions file.")
            if files[-1].endswith(TEXT_FILE_TYPE):
                # if the file is in the correct extension than ask to generate the file
                generate_custom_file = input("do you want to generate file: " + files[-1] + " for solutions? Y/N\n")
                while True:
                    # wait for a valid answer from user
                    if generate_custom_file.lower() == 'n':
                        print("script will generate default solutions.txt file.")
                        make_solutions_file = True
                        # remove redundant file from files list
                        files = files[:1]
                        break
                    elif generate_custom_file.lower() == 'y':
                        print("script will generate custom", files[-1], "file.")
                        solutions_file_name = files[-1]
                        make_solutions_file = True
                        break
                    else:
                        generate_custom_file = input(r"wrong input. enter again (Y/N/y/n):" + '\n')

    # if the user didn't input solutions file, make a solutions file
    if len(files) == NUMBER_OF_ARGUMENTS - 1:
        print("solutions file not found.\nscript will generate solutions.txt file.")
        make_solutions_file = True

    # check if solutions file already exists in the path
    # if exists, ask to override
    if make_solutions_file:
        file_exists, error_message = check_file(solutions_file_name)

        # if the file exists ask user if he wants to override it
        # if he doesn't want, exit the script
        if file_exists:
            override_file = input("the script will override " + solutions_file_name
                                  + " do you wish to continue? Y/N\n")
            while True:
                if override_file.lower() == 'n':
                    print("you chose not to override", solutions_file_name, "exiting...")
                    return
                elif override_file.lower() == 'y':
                    print("overriding file:", solutions_file_name)
                    break
                else:
                    override_file = input(r"wrong input. enter again (Y/N/y/n):" + '\n')
        else:
            open(solutions_file_name, 'w').close()
            print("file", solutions_file_name, "created")

            # with open(solutions_file_name, 'w'):
            #     print("file", solutions_file_name, "created")
        files.append(solutions_file_name)

    # check that all files in files pass our conventions
    for file in files:
        file_ok, error_message = check_file(file)
        if not file_ok:
            print("error in file:", error_message, "\nexiting...")
            return

    # after checking that all the files exist and follow our convention, solve the homework
    # split between homework(files[:1]) and solutions(files[-1])
    print("doing homework...")
    homework_successful = solve_homework(files[:1], files[-1])

    if homework_successful:
        print("success! your homework are ready and solved in", solutions_file_name, "file!")
    else:
        # there was an error in the homework file
        print("something went wrong with the homework.\nwe did what we could,"
              "but check", solutions_file_name, "file for details")
    input("press enter to exit...")


if __name__ == '__main__':
    main()
