# author: golan matuf
# date: 12.10.21 (20211014)
# python lazy_student.py homework.txt solutions.txt

NUMBER_OF_ARGUMENTS = 2

def check_files(homework_file, solutions_file):
    from os.path import exists
    # check that both files exists
    if not exists(homework_file) or not exists(solutions_file):
        return False, "some of the files does no exist"
    # check that both files extensions are '.txt'
    if not homework_file.endswith('.txt') or not solutions_file.endswith('.txt'):
        return False, r"one or more files extensions are not '.txt'"
    return True, "no error"


def solve_homework(homework_file, solutions_file):



def main():
    import sys
    if len(sys.argv) != NUMBER_OF_ARGUMENTS:
        print('script must have two files! ,exiting...')
        return
    files_ok, error_message = check_files(sys.argv[0], sys.argv[1])
    if not files_ok:
        print("error in files:", error_message)
    solve_homework(sys.argv[0], sys.argv[1])

if __name__ == '__main__':
    main()
