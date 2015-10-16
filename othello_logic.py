# Edwin Ho - 73901628 - ICS 32 - Project 5 - Othello Game Logic


class InvalidOthelloMoveError(Exception):
    '''Raised whenever an invalid move is made'''
    pass

class OthelloGameOverError(Exception):
    '''
    Raised whenever an attempt is made to make a move after the game is
    already over
    '''
    pass


class OthelloGameState:

    
    def __init__(self):
        '''Sets the turn constants'''
        self._WHITE = "W"
        self._BLACK = "B"
        self._NONE = " "


        
    def set_board(self, rows: int, columns: int) -> None:
        '''
        Creates a new board with appropriate dimensions, raises an exception
        if rows or columns are less than 4 or greater than 16
        '''
        self._require_dimensions('ROW', rows)
        self._require_dimensions('COLUMN', columns)
        
        board = []

        for row in range(rows):
            board.append([])
            for col in range(columns):
                board[-1].append(self._NONE)

        self._board = board


    def set_turn(self, turn: str) -> None:
        '''Defines the turn attribute: either self._WHITE or self._BLACK'''
        self._turn = turn



    def set_center(self, top_left: str) -> None:
        '''
        Places the first four pieces in the center, with a user specified
        color in the top left corner
        '''
        rows = len(self._board)
        columns = len(self._board[0])
        row_center = int(rows/2)
        col_center = int(columns/2)
        self._board[row_center-1][col_center-1] = top_left
        self._board[row_center][col_center] = top_left
        self._board[row_center][col_center-1] = self._opposite(top_left)
        self._board[row_center-1][col_center] = self._opposite(top_left)


        
    def set_win_condition(self, win_condition: str) -> None:
        '''Defines the win condition: either "MOST" or "FEWEST"'''
        self._win_condition = win_condition



    def place_piece(self, row: int, column: int) -> None:
        '''
        The function for defining a move, requires the row and column indices
        for the board list
        '''
        self._require_game_not_over()
        self._require_valid_row_number(row)
        self._require_valid_column_number(column)
        
        if self._board[row][column] == self._NONE \
           and self._check_all_directions(row, column):
            self._flip_all_directions(row, column)
            self._board[row][column] = self._turn
            self._turn = self._opposite(self._turn)
        else:
            raise InvalidOthelloMoveError()


    def check_valid(self) -> bool:
        '''
        Checks all the cells on the board to see if the current turn has a
        valid move on the board
        '''
        result = []
        for row in range(len(self._board)):
            for col in range(len(self._board[row])):
                if self._board[row][col] == self._NONE:
                    result.append(self._check_all_directions(row, col))
        return True in result



    def pass_turn(self) -> str:
        '''Skips the current turn and returns the turn that was passed'''
        current_turn = self._turn
        self._turn = self._opposite(self._turn)
        return current_turn



    def keep_score(self) -> None:
        '''
        Calculates the score for each turn and saves each score as an
        attribute of the class
        '''
        white_score = 0
        black_score = 0
        for row in self._board:
            for col in row:
                if col == self._WHITE:
                    white_score += 1
                elif col == self._BLACK:
                    black_score += 1
        self._white_score = white_score
        self._black_score = black_score


        
    def winning_player(self) -> str:
        '''Returns the winner of the game'''
        winner = self._NONE

        if self._no_more_moves():        
            for row in range(len(self._board)):
                for col in range(len(self._board[row])):
                    if winner == self._NONE:
                        winner = self._find_winner()

        return winner



    def _no_more_moves(self) -> bool:
        '''Checks if both players can no longer move'''
        game_over = False
        current_turn = self._turn
        if not self.check_valid():
            self._turn = self._opposite(self._turn)
            game_over = not self.check_valid()
        self._turn = current_turn
        return game_over


    def _find_winner(self) -> str:
        '''Calculates who the winner is depending on the win condition'''
        full_name = {self._BLACK: 'BLACK', self._WHITE: 'WHITE'}
        if self._win_condition == "MOST":
            if self._black_score > self._white_score:
                return full_name[self._BLACK]
            elif self._white_score > self._black_score:
                return full_name[self._WHITE]
            else:
                return "TIE"
        elif self._win_condition == "FEWEST":
            if self._black_score < self._white_score:
                return full_name[self._BLACK]
            elif self._white_score < self._black_score:
                return full_name[self._WHITE]
            else:
                return "TIE"


    
    def _opposite(self, turn: str) -> str:
        '''Given the player whose turn it is now, returns the opposite player'''
        if turn == self._BLACK:
            return self._WHITE
        else:
            return self._BLACK


    def _flip_all_directions(self, row: int, col: int) -> None:
        '''
        Flips the pieces in all directions from the placed piece if there is
        another piece of the same color along the way
        '''
        for rowdelta in range(-1, 2):
            for coldelta in range(-1, 2):
                if self._check_one_direction(row, col, rowdelta, coldelta):
                    self._flip_one_direction(row, col, rowdelta, coldelta)



    def _flip_one_direction(self, row: int, col: int,
                            rowdelta: int, coldelta: int) -> None:
        '''
        Recursively changes the color of  each piece along the way in a
        given direction
        '''
        new_row = row + rowdelta
        new_col = col + coldelta
        if self._board[new_row][new_col] == self._opposite(self._turn):
            self._board[new_row][new_col] = self._turn
            self._flip_one_direction(new_row, new_col, rowdelta, coldelta)


        
    def _check_all_directions(self, row: int, col: int) -> bool:
        '''Returns True if the specified cell (row, col) has another piece
        in any direction with an opposite piece in between'''
        return self._check_one_direction(row, col, 0, 1) \
            or self._check_one_direction(row, col, 1, 1) \
            or self._check_one_direction(row, col, 1, 0) \
            or self._check_one_direction(row, col, 1, -1) \
            or self._check_one_direction(row, col, 0, -1) \
            or self._check_one_direction(row, col, -1, -1) \
            or self._check_one_direction(row, col, -1, 0) \
            or self._check_one_direction(row, col, -1, 1)



    def _check_one_direction(self, row: int, col: int,
                             rowdelta: int, coldelta: int) -> bool:
        '''
        Checks to see if a move in a certain cell is valid based on checking
        if it is followed by a series of opposite color pieces and capped off
        by a piece of the same color in a certain direction
        '''
        if self._adjacent(row, col, rowdelta, coldelta) == \
           self._opposite(self._turn):
            return self._go_onto_next(row, col, rowdelta, coldelta)



    def _go_onto_next(self, row: int, col: int,
                      rowdelta: int, coldelta: int) -> bool:
        '''
        Recursive function that checks every piece after the first adjacent
        piece in a single direction, stopping and returning True if one of the
        pieces along the way belongs to the current turn
        '''
        new_row = row + rowdelta
        new_col = col + coldelta
        if self._adjacent(new_row, new_col, rowdelta, coldelta) == \
           self._opposite(self._turn):
            return self._go_onto_next(new_row, new_col, rowdelta, coldelta)
        elif self._adjacent(new_row, new_col, rowdelta, coldelta) == self._turn:
            return True
        elif self._adjacent(new_row, new_col, rowdelta, coldelta) == self._NONE:
            return False



    def _adjacent(self, row: int, col: int, rowdelta: int, coldelta: int) -> str:
        '''
        Checks the piece immediately next to the specified cell and returns
        the piece's color
        '''
        if self._is_valid_column_number(col + coldelta) \
           and self._is_valid_row_number(row + rowdelta):
            return self._board[row + rowdelta][col + coldelta]
        else:
            return self._NONE


    def _require_game_not_over(self) -> None:
        '''
        Raises an OthelloGameOverError if the given game state represents
        a situation where the game is over (i.e., there is a winning player)
        '''
        if self.winning_player() != self._NONE:
            raise OthelloGameOverError()


    def _require_dimensions(self, dimension_type: str, dimension: int) -> None:
        '''
        Ensures that the row and column values are between 4 and 16
        '''
        if type(dimension) != int or not 4 <= dimension <= 16 or not dimension%2==0:
            raise ValueError("{} value must be int between 4 and 16".format(
                dimension_type))


    def _require_valid_row_number(self, row: int) -> None:
        '''Raises a ValueError if its parameter is not a valid row number'''
        if type(row) != int or not self._is_valid_row_number(row):
            raise ValueError('column_number must be int between 0 and {}'.format(
                len(self._board)))



    def _require_valid_column_number(self, column: int) -> None:
        '''Raises a ValueError if its parameter is not a valid column number'''
        if type(column) != int or not self._is_valid_column_number(column):
            raise ValueError('column_number must be int between 0 and {}'.format(
                len(self._board[0])))
        

    def _is_valid_row_number(self, row: int) -> bool:
        '''Returns True if the given row number is valid; returns False otherwise'''
        return 0 <= row < len(self._board)


    
    def _is_valid_column_number(self, column: int) -> bool:
        '''Returns True if the given column number is valid; returns False otherwise'''
        return 0 <= column < len(self._board[0])
