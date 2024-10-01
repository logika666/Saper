import random


class Saper:
    def __init__(self, rows, cols, mines):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.board = [[' ' for _ in range(cols)] for _ in range(rows)]
        self.visible = [[' ' for _ in range(cols)] for _ in range(rows)]
        self.flags = [[' ' for _ in range(cols)] for _ in range(rows)]
        self.game_over = False
        self.generate_mines()

    def generate_mines(self):
        mines_placed = 0
        while mines_placed < self.mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            if self.board[row][col] != 'M':
                self.board[row][col] = 'M'
                mines_placed += 1
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == 'M':
                    continue
                self.board[r][c] = self.count_mines(r, c)

    def count_mines(self, row, col):
        mine_count = 0
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if 0 <= r < self.rows and 0 <= c < self.cols and self.board[r][c] == 'M':
                    mine_count += 1
        return str(mine_count) if mine_count > 0 else ' '

    def display_board(self):
        print("   " + " ".join(str(i) for i in range(self.cols)))
        for i in range(self.rows):
            print(f"{i}  " + " ".join(self.visible[i]))

    def open_cell(self, row, col):
        if self.flags[row][col] != ' ':
            print("Сначала снимите отметку!")
            return

        if self.board[row][col] == 'M':
            self.game_over = True
            print("Вы попали на мину!!!Игра окончена!")
            return

        self.reveal(row, col)

        if self.is_win():
            print("Вы выиграли!")

    def reveal(self, row, col):
        if self.visible[row][col] != ' ':
            return

        self.visible[row][col] = self.board[row][col]

        if self.board[row][col] == ' ':
            for r in range(row - 1, row + 2):
                for c in range(col - 1, col + 2):
                    if 0 <= r < self.rows and 0 <= c < self.cols:
                        self.reveal(r, c)

    def mark_flag(self, row, col):
        if self.visible[row][col] == ' ':
            self.flags[row][col] = 'F' if self.flags[row][col] == ' ' else ' '

    def mark_question(self, row, col):
        if self.visible[row][col] == ' ':
            self.flags[row][col] = '?' if self.flags[row][col] == ' ' else ' '

    def is_win(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] != 'M' and self.visible[r][c] == ' ':
                    return False
        return True


cols = int(input('введите столбцы '))
rows = int(input('введите строки '))
diff = input('введите сложность - min, mid, overkill ')
if diff == 'min':
    diff_cood = 2.5
elif diff == 'mid':
    diff_cood = 2.0
elif diff == 'overkill':
    diff_cood = 1.5
else:
    diff_cood = 1

mines = (rows * cols) // diff_cood
print (mines)
game = Saper(cols, rows, int(mines))

while not game.game_over:
    game.display_board()
    command = input("Введите команду (open/flag) и координаты (row col): ").split()

    if len(command) == 3:
        action, row, col = command[0], int(command[1]), int(command[2])
        if action == "open":
            game.open_cell(row, col)
        elif action == "flag":
            game.mark_flag(row, col)
        else:
            print("Неизвестное действие!")
