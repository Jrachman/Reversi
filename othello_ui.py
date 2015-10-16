# Edwin Ho - 73901628 - ICS 32 - Project 4 - Othello User Interface
import othello_logic


def _ask_choice(message: str, correct_choices: str) -> str:
    '''
    Generic function that asks the user a "message" and checks if the user choice
    is a valid selection
    '''
    while True:
        choice = input(message)
        if choice not in correct_choices:
            print("Sorry, '{}' is not a valid choice".format(choice))
        else:
            return choice



def _get_dimensions(row_or_column: str) -> int:
    '''
    Asks the user to specify the dimensions depending on the parameter - ROWS
    or COLUMNS and ensures that the inputs are between 4 and 16
    '''
    while True:
        dimension = input("Please enter an EVEN number of {} (4-16) you wish to have (default=8): ".format(
            row_or_column))
        if len(dimension) == 0:
            return 8
        try:
            dimension = int(dimension)
        except ValueError:
            print("\nThat is not a valid integer\n")
        else:
            if 4 <= dimension <= 16:
                return dimension
            else:
                print("\nInvalid dimensions: must be even numbers between 4x4 and 16x16\n")

                
def get_board(state: othello_logic.OthelloGameState) -> None:
    '''
    Asks the user for both the ROWS and COLUMNS and makes the game board
    attribute in the game state.
    '''
    rows = _get_dimensions('ROWS')
    columns = _get_dimensions('COLUMNS')
    state.set_board(rows, columns)



def get_start_turn(state: othello_logic.OthelloGameState) -> None:
    '''Ask the user to specify whether white or black starts first'''
    turn = {'1': state._BLACK, '2': state._WHITE, '': state._BLACK}
    choice = _ask_choice("""\nPlease specify which player starts first (default=BLACK):
1) BLACK\n2) WHITE\n""","12")
    state.set_turn(turn[choice])




def get_top_left_start(state: othello_logic.OthelloGameState) -> None:
    '''
    Asks the user to specify what piece should start in the top left corner
    '''
    top_left = {'1': state._BLACK, '2': state._WHITE, '': state._WHITE}
    choice = _ask_choice("""\nPlease specify the color of the top left corner of the center (default=WHITE):
1) BLACK\n2) WHITE\n""", "12")
    state.set_center(top_left[choice])


def get_win_condition(state: othello_logic.OthelloGameState) -> None:
    '''
    Asks th user to specify what the win condition of the game will be:
    the player who has the most or least pieces
    '''
    win_condition = {'1': "MOST", "2": "FEWEST", "": "MOST"}
    choice = _ask_choice("""\nPlease specify which player will win (default=MOST):
1) The Player with the MOST Pieces\n2) The Player with the FEWEST Pieces\n""", "12")
    state.set_win_condition(win_condition[choice])
    


def draw_board(state: othello_logic.OthelloGameState) -> None:
    '''
    Draws the game board and adds lettering and numbering on the edges
    as coordinates
    '''
    full_name = {state._BLACK: 'BLACK', state._WHITE: 'WHITE'}
    
    state.keep_score()
    print("\n {}: {}    |    {}: {}\n".format(full_name[state._WHITE],
                                              state._white_score,
                                              full_name[state._BLACK],
                                              state._black_score))
    row_num = 0
    for row in state._board:
        row_num += 1
        print("{:2}".format(row_num), end=" ")
        for col in row:
            if col == state._NONE:
                print("~", end=" ")
            else:
                print(col, end=" ")
        print()
        
    ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
    print("  ", end=" ")
    for columns in range(len(state._board[0])):
        print(ALPHABET[columns], end=" ")


def get_move(state: othello_logic.OthelloGameState) -> None:
    '''
    Asks the user to specify a move and places the appropriate piece
    on the specified cell
    '''
    full_name = {state._BLACK: 'BLACK', state._WHITE: 'WHITE'}
    if not state.check_valid():
        print("\n{} passes\n".format(full_name[state.pass_turn()]))
    print("\n\nIt is {}'s turn".format(full_name[state._turn]))
    ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
    while True:
        move = input("Please specify a cell - {letter}{number}: ").strip().lower()
        try:
            column = ALPHABET.index(move[0])
            row = int(move[1:].strip())-1
            return state.place_piece(row, column)
        except:
            print("\n'{}' is an invalid move.\n".format(move))


def welcome_banner() -> None:
    '''The program's header that introduces the title and instructions'''
    print("{}Othello{}\n".format("+"*10,"+"*10))
    print("\nPress [ENTER] to select defaults.\n")

    
def start() -> othello_logic.OthelloGameState:
    '''
    Calls all the beginning input functions that ask the user to specify how the
    game state will start off
    '''
    state = othello_logic.OthelloGameState()
    
    welcome_banner()
    
    get_board(state)
    get_start_turn(state)
    get_top_left_start(state)
    get_win_condition(state)
    
    return state


if __name__ == '__main__':
    state = start()
    
    while state.winning_player() == state._NONE:
        draw_board(state)
        get_move(state)
    draw_board(state)
    print("\nWINNER: {}".format(state.winning_player()))
