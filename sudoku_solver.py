from tkinter import *
from constants import *
from functools import partial

window = Tk()
window.title('Sudoku Solver')
window.geometry('600x500')

buttons = []


def cycle_button(button):
    if button['text'] == ' ':
        button['text'] = '1'
    elif button['text'] == '9':
        button['text'] = ' '
    else:
        button['text'] = str(int(button['text']) + 1)


def can_place(board, i, j, c):
    for p in range(9):
        for q in range(9):
            if board[i][p] == c or board[p][j] == c:
                return False
    for p in range(int(i/3)*3, (int(i/3)+1)*3):
        for q in range(int(j/3)*3, (int(j/3)+1)*3):
            if board[p][q] == c:
                return False
    return True


def find_next(board):
    for p in range(9):
        for q in range(9):
            if board[p][q] == ' ':
                return p, q
    return -1, -1


def char_range(c1, c2):
    for c in range(ord(c1), ord(c2)+1):
        yield chr(c)


def valid_board(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] != ' ':
                c, board[i][j] = board[i][j], ' '
                if not can_place(board, i, j, c):
                    board[i][j] = c
                    return False
                board[i][j] = c
    return True


def is_solved(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == ' ':
                return False
            c, board[i][j] = board[i][j], ' '
            if not can_place(board, i, j, c):
                board[i][j] = c
                return False
            board[i][j] = c
    return True


def solve(board):
    i, j = find_next(board)
    if i == -1:
        return True
    
    for c in char_range('1', '9'):
        if can_place(board, i, j, c):
            board[i][j] = c
            buttons[i][j]['text'] = c
            if solve(board):
                return True
            board[i][j] = ' '
            buttons[i][j]['text'] = ' '
    
    return False


def solve_button():
    board = []
    for i in range(9):
        board.append([])
        for j in range(9):
            board[i].append(buttons[i][j]['text'])
    
    if valid_board(board) and (is_solved(board) or solve(board)):
        print('Solved!')
    else:
        print('Unsolvable')


def clear_button():
    for i in range(9):
        for j in range(9):
            buttons[i][j]['text'] = ' '


def run():
    for i in range(9):
        buttons.append([])
        for j in range(9):
            b = Button(window, width=BUTTON_WIDTH, height=BUTTON_HEIGHT, text=' ')
            b.config(command=partial(cycle_button, b))
            b.grid(row=i, column=j)
            buttons[i].append(b)

    solve_btn = Button(window, width=10, height=BUTTON_HEIGHT, text='SOLVE', command=solve_button)
    solve_btn.grid(row=4, column=9)

    clear_btn = Button(window, width=10, height=BUTTON_HEIGHT, text='CLEAR', command=clear_button)
    clear_btn.grid(row=5, column=9)

    window.mainloop()


if __name__ == '__main__':
    run()
