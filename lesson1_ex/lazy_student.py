# author: golan matuf
# date: 12.10.21 (20211014)
# python lazy_student.py homework.txt solutions.txt

TEXT_FILE_TYPE = '.txt'
NUMBER_OF_ARGUMENTS = 2


def check_file(file):
    from os.path import exists
    # check that file exists
    if not exists(file):
        return False, "file does not exist"
    # check that  file extension is '.txt'
    if not file.endswith(TEXT_FILE_TYPE):
        return False, r"file extension is not " + TEXT_FILE_TYPE
    return True, "no error"


def solve_homework(homework_files, solutions_file):
    print("doing homework...")

    return True, 'no error detected while doing homework'


def main():
    import sys
    # remove self argument
    files = sys.argv[1:]
    print(files)
    solutions_file_name = "solutions.txt"
    # script must have NUMBER_OF_ARGUMENTS or NUMBER_OF_ARGUMENTS-1 to work
    if len(files) > NUMBER_OF_ARGUMENTS or len(files) < NUMBER_OF_ARGUMENTS-1:
        print('FAILED! script must have {0} or {1} arguments, exiting...'
              .format(NUMBER_OF_ARGUMENTS-1, NUMBER_OF_ARGUMENTS))
        return
    make_solutions_file = False

    # start checking if script needs to generate solutions file
    # if the user input includes the solutions file, check the file and that it exists
    if len(files) == NUMBER_OF_ARGUMENTS:
        file_ok, error_message = check_file(files[-1])
        if not file_ok:
            print("error in solutions file.")
            if files[-1].endswith(TEXT_FILE_TYPE):
                generate_custom_file = input("do you want to generate file: " + files[-1] + " for solutions? Y/N\n")
                correct_input = False
                while not correct_input:
                    if generate_custom_file.lower() == 'n':
                        print("script will generate solutions.txt file.")

                        # remove redundant file from files list
                        files = files[:1]
                        make_solutions_file = True
                        correct_input = True
                    elif generate_custom_file.lower() == 'y':
                        print("script will generate",  files[-1], "file.")
                        solutions_file_name = files[-1]
                        make_solutions_file = True
                        correct_input = True
                    else:
                        generate_custom_file = input("wrong input. enter again (Y/N/y/n):\n")
        else:
            solutions_file_name = files[-1]

    # if the user didn't input solutions file, make a solutions file
    if len(files) == NUMBER_OF_ARGUMENTS-1:
        print("solutions file not found.\nscript will generate solutions.txt file.")
        make_solutions_file = True

    # check if "solutions.txt" file already exists in the path
    # if exists, ask to override
    if make_solutions_file:
        file_exists, error_message = check_file(solutions_file_name)

        # if the file exists ask user if he wants to override it
        # if he doesn't want, exit the script
        if file_exists:
            override_file = input("the script will override " + solutions_file_name + " do you wish to continue? Y/N\n")
            if override_file.lower() == 'n':
                print("you chose not to override", solutions_file_name, "exiting...")
                return
            else:
                print("overriding file:", solutions_file_name)
        else:
            open(solutions_file_name, 'w').close()
            print("file", solutions_file_name, "created")

            # with open(solutions_file_name, 'w'):
            #     print("file", solutions_file_name, "created")
        files.append(solutions_file_name)

    for file in files:
        file_ok, error_message = check_file(file)
        if not file_ok:
            print("error in file:", error_message, "\nexiting...")
            return

    homework_successful, homework_error = solve_homework(files[:1], files[-1])
    if not homework_successful:
        print("something went wrong with the homework error:", homework_error)
        print("exiting script...")
        return

    print("success! your homework are ready and solved in", solutions_file_name, "file!")
    input("press enter to exit...")


if __name__ == '__main__':
    main()
