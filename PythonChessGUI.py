import PySimpleGUI as sg
import chess as chess
import os

APP_NAME = 'PychessAI'
###################################################################################
# nomi pezzi
BLANK = 0
PAWNB = 1
KNIGHTB = 2
BISHOPB = 3
ROOKB = 4
KINGB = 5
QUEENB = 6
PAWNW = 7
KNIGHTW = 8
BISHOPW = 9
ROOKW = 10
KINGW = 11
QUEENW = 12

initial_board = [[ROOKB, KNIGHTB, BISHOPB, QUEENB, KINGB, BISHOPB, KNIGHTB, ROOKB],
                 [PAWNB, ] * 8,
                 [BLANK, ] * 8,
                 [BLANK, ] * 8,
                 [BLANK, ] * 8,
                 [BLANK, ] * 8,
                 [PAWNW, ] * 8,
                 [ROOKW, KNIGHTW, BISHOPW, QUEENW, KINGW, BISHOPW, KNIGHTW, ROOKW]]

IMAGE_PATH = 'images/pieces'  # path to the chess pieces

blank = os.path.join(IMAGE_PATH, 'blank.png')
bishopB = os.path.join(IMAGE_PATH, 'bB.png')
bishopW = os.path.join(IMAGE_PATH, 'wB.png')
pawnB = os.path.join(IMAGE_PATH, 'bP.png')
pawnW = os.path.join(IMAGE_PATH, 'wP.png')
knightB = os.path.join(IMAGE_PATH, 'bN.png')
knightW = os.path.join(IMAGE_PATH, 'wN.png')
rookB = os.path.join(IMAGE_PATH, 'bR.png')
rookW = os.path.join(IMAGE_PATH, 'wR.png')
queenB = os.path.join(IMAGE_PATH, 'bQ.png')
queenW = os.path.join(IMAGE_PATH, 'wQ.png')
kingB = os.path.join(IMAGE_PATH, 'bK.png')
kingW = os.path.join(IMAGE_PATH, 'wK.png')

images = {BISHOPB: bishopB, BISHOPW: bishopW, PAWNB: pawnB, PAWNW: pawnW,
          KNIGHTB: knightB, KNIGHTW: knightW,
          ROOKB: rookB, ROOKW: rookW, KINGB: kingB, KINGW: kingW,
          QUEENB: queenB, QUEENW: queenW, BLANK: blank}

key_to_position = {(0, 0): 'a8', (0, 1): 'b8', (0, 2): 'c8', (0, 3): 'd8', (0, 4): 'e8', (0, 5): 'f8', (0, 6): 'g8',
                   (0, 7): 'h8',
                   (1, 0): 'a7', (1, 1): 'b7', (1, 2): 'c7', (1, 3): 'd7', (1, 4): 'e7', (1, 5): 'f7', (1, 6): 'g7',
                   (1, 7): 'h7',
                   (2, 0): 'a6', (2, 1): 'b6', (2, 2): 'c6', (2, 3): 'd6', (2, 4): 'e6', (2, 5): 'f6', (2, 6): 'g6',
                   (2, 7): 'h6',
                   (3, 0): 'a5', (3, 1): 'b5', (3, 2): 'c5', (3, 3): 'd5', (3, 4): 'e5', (3, 5): 'f5', (3, 6): 'g5',
                   (3, 7): 'h5',
                   (4, 0): 'a4', (4, 1): 'b4', (4, 2): 'c4', (4, 3): 'd4', (4, 4): 'e4', (4, 5): 'f4', (4, 6): 'g4',
                   (4, 7): 'h4',
                   (5, 0): 'a3', (5, 1): 'b3', (5, 2): 'c3', (5, 3): 'd3', (5, 4): 'e3', (5, 5): 'f3', (5, 6): 'g3',
                   (5, 7): 'h3',
                   (6, 0): 'a2', (6, 1): 'b2', (6, 2): 'c2', (6, 3): 'd2', (6, 4): 'e2', (6, 5): 'f2', (6, 6): 'g2',
                   (6, 7): 'h2',
                   (7, 0): 'a1', (7, 1): 'b1', (7, 1): 'c1', (7, 3): 'd1', (7, 4): 'e1', (7, 5): 'f1', (7, 6): 'g1',
                   (7, 7): 'h1'}


###########################################################################
class Move:
    def __init__(self, move_state, fr_pos, to_pos, color, image):
        self.move_state = move_state
        self.fr_pos = fr_pos
        self.to_pos = to_pos
        self.color = color
        self.image = image
        self.move_str = ''

    def switch(self):
        if self.move_state == 0:
            self.move_state = 1
        else:
            self.move_state = 0
        print(self.move_state)
    def to_string(self, key):
        self.move_str += key_to_position.get(key)
    def clear_str(self):
        self.move_str = ''


class GUI:
    '''
    move state -> 0 = the piece to move is selected
                  1 = the destination button is selected
    '''
    def __init__(self, w_size, is_white):
        self.w_size = w_size
        self.is_white = is_white

        self.black_square_color = '#b58863'
        self.white_square_color = '#f1d9b5'
        self.highlited_white_square_color = '#e6b82e'
        self.highlited_black_square_color = '#9e7700'

        self.window = self.create_window(APP_NAME,
                                         self.render_window(),
                                         (800, 600))
        self.psg_board = initial_board

    def render_window(self):
        board_layout = self.render_board(True)
        menu_layout = self.render_right_menu()

        layout = [[self.render_upper_menu()],
                  [sg.Column(board_layout), sg.Column(menu_layout)]]
        return layout

    def render_board(self, is_white):
        layout = []

        colors = [self.white_square_color, self.black_square_color]

        if is_white:
            # Save the board with black at the top
            start = 0
            end = 8
            step = 1
        else:
            start = 7
            end = -1
            step = -1
        for i in range(start, end, step):
            row = []
            for j in range(start, end, step):
                color = colors[(i + j) % 2]
                row.append(self.create_button(color=color,
                                              image=images.get(initial_board[i][j]),
                                              key=(i, j)))
            layout.append(row)
        return layout

    def create_button(self, color, image, key):
        return sg.Button('', image_filename=image,
                         size=(2, 2),
                         pad=(0, 0),
                         border_width=0,
                         button_color=('white', color),
                         key=key)

    def render_upper_menu(self):
        menu_def = [['File'],
                    ['Edit'],
                    ['Help']]
        return sg.Menu(menu_def)

    def render_right_menu(self):
        layout = [
            [sg.Text('Move History:')],
            [sg.Multiline(autoscroll=True, disabled=True, size=(200, 500), key='--MOVE HISTORY--')]
        ]
        return layout

    def create_window(self, name, layout, size):
        window = sg.Window(name,
                           layout=layout,
                           size=size,
                           resizable=False,
                           default_button_element_size=(12, 1),
                           auto_size_buttons=False)
        return window
    def redraw_board(self, window):
        """
        Redraw board at start and afte a move.
        :param window:
        :return:
        """
        for i in range(8):
            for j in range(8):
                color = self.black_square_color if (i + j) % 2 else \
                        self.white_square_color
                piece_image = images[self.psg_board[i][j]]
                elem = window.FindElement(key=(i, j))
                elem.Update(button_color=('white', color),
                            image_filename=piece_image)

    def update_psg_board(self, move_list):
        i, j = move_list[0]
        k, l = move_list[1]
        self.psg_board[k][l] = self.psg_board[i][j]
        self.psg_board[i][j] = BLANK



class ChessProcessor:
    board = chess.Board()

    def validate_move(self, move):
        ret = False
        if self.board.is_legal(chess.Move.from_uci(move)):
            ret = True
        return ret

class ChessGame:
    chess_processor = None
    gui = None
    move = None

    def __init__(self, gui_size, is_white):

        self.chess_processor = ChessProcessor()
        self.gui = GUI(w_size=gui_size, is_white=is_white)
        self.move = Move(0, None, None, None, None)

    def run(self):

        window = self.gui.window
        while True:
            event, values = window.read(timeout=500)
            if type(event) is tuple:
                self.move_piece(event)
            elif event in ('Quit', sg.WIN_CLOSED):
                break
        window.Close()

    def move_piece(self, button):

        window = self.gui.window
        self.gui.redraw_board(window)
        if self.move.move_state == 0: #then is the first piece selected
            self.move.fr_pos = button
            self.move.color = window[button].ButtonColor
            self.move.image = window[button].ImageFilename
            window[button].update(button_color=('white', self.gui.highlited_white_square_color))
            self.move.switch()
            self.move.to_string(button)

        elif self.move.move_state == 1 and self.move.fr_pos != button:
            #need to validate move with chess processor
            self.move.to_string(button)
            self.move.to_pos = button

            if self.chess_processor.validate_move(self.move.move_str):
                print(self.move.image)
                window[button].update(image_filename=self.move.image)
                #window[self.move.fr_pos].update(button_color=self.move.color, image_filename=blank)
                self.gui.update_psg_board([self.move.fr_pos, button])
                print(self.move.move_str)
                self.chess_processor.board.push(chess.Move.from_uci(self.move.move_str))
                self.move.clear_str()

            else: #if validation fails then reset move
                print('invalid move')
                window[self.move.fr_pos].update(button_color=self.move.color)
                self.move.clear_str()
            self.move.switch()
            self.gui.redraw_board(window)

def main():
    game = ChessGame((800,600), True)
    game.run()


if __name__ == "__main__":
    main()
