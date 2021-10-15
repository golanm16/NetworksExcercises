
def main():
    letters = 'aoieu'
    word = input('enter your string for bet lang: ')
    for letter in word:
        word.replace(letter, (letter + 'b' + letter))
    print(word)


if __name__ == '__main__':
    main()
