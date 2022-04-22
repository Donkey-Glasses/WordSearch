from string import ascii_uppercase
from typing import Optional
from fpdf import FPDF

import random


WORD_LIST_FILE = 'words.txt'
WORD_COUNT = 8
COLUMN_COUNT = 10
ROW_COUNT = 10
FONT = 'Courier'
FONT_SIZE = 40


class Letter:
    def __init__(self, letter: str, is_word: bool = False, x_pos: Optional[int] = None, y_pos: Optional[int] = None):
        self.letter = letter
        self.is_word = is_word
        self.x_pos = x_pos
        self.y_pos = y_pos


class Board:
    def __init__(self, word_list: list, col_count: int = COLUMN_COUNT, row_count: int = ROW_COUNT):
        self.word_list = word_list
        self.column_count = col_count
        self.row_count = row_count
        self.board_lists = []
        for i in range(self.row_count):
            new_list = []
            new_list.extend([" " for _ in range(self.column_count)])
            self.board_lists.append(new_list)
        for word in self.word_list:
            self.place_word(word)
        self.fill_board()

    def place_word(self, word: str):
        def _verify_placement(characters):
            place = True
            for spot in characters:
                if spot != ' ':
                    # print('hit!')
                    place = False
            return place

        orientation = random.choice(['horizontal', 'vertical'])
        match orientation:
            case 'horizontal':
                row = random.randint(0, self.row_count - 1)
                col = random.randint(0, self.column_count - len(word) - 1)
                #  print(word, row, col)
                potentials = [self.board_lists[row][c] for c in range(col, col + len(word))]
                if _verify_placement(potentials):
                    for letter in word:
                        self.board_lists[row][col] = letter.upper()
                        col += 1
                else:
                    self.place_word(word)
            case 'vertical':
                row = random.randint(0, self.row_count - len(word) - 1)
                col = random.randint(0, self.column_count - 1)
                # print(word, row, col)
                potentials = [self.board_lists[r][col] for r in range(row, row + len(word))]
                if _verify_placement(potentials):
                    for letter in word:
                        self.board_lists[row][col] = letter.upper()
                        row += 1
                else:
                    self.place_word(word)

    def fill_board(self):
        for row in self.board_lists:
            for index, item in enumerate(row):
                if item == ' ':
                    row[index] = random.choice(ascii_uppercase)


def read_words(filename):
    def _char_split(word):
        return [char for char in word]

    with open(filename) as wf:
        blob = wf.read()
        return [_char_split(w) for w in blob.split()]


def pick_words(word_list):
    return random.choices(word_list, k=WORD_COUNT)


def write_to_file(board: Board):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font(FONT, size=FONT_SIZE)
    # Word List
    word_list = [''.join(word) for word in board.word_list]
    while len(word_list) > 1:
        word_pair = f'{word_list.pop()}\t\t\t\t\t\t{word_list.pop()}'
        pdf.cell(200, 14, txt=word_pair, ln=2, align='C')
    if len(word_list) == 1:
        pdf.cell(200, 10, txt=word_list[0], ln=2, align='C')
    for _ in range(0, int(len(word_list) / 2)):
        pdf.cell(200, 14, txt=word_list.pop(), ln=2, align='C')
        pdf.cell(200, 14, txt=word_list.pop(), ln=1, align='C')
    # pdf.cell(200, 10, txt='\t'.join(word_list), ln=1, align='C')
    # Write word search
    pdf.cell(200, 10, txt='', ln=2, align='C')  # Blank line
    for index, row in enumerate(board.board_lists, 3):
        pdf.cell(200, 14, txt='\t'.join(row), ln=2, align='C')

    pdf.output('OUTPUT.pdf')


if __name__ == "__main__":
    words = read_words(filename=WORD_LIST_FILE)
    picked_words = pick_words(words)
    board = Board(word_list=picked_words)
    print(picked_words)
    for item in board.board_lists:
        print(f'{item}\n')
    write_to_file(board)
