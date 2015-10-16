# Edwin Ho - 73901628 - ICS 32 - Project 5 - Othello Graphical User Interface

import tkinter
import othello_logic

class PlayerOptions:
    def __init__(self, root):
        self._DEFAULT_FONT = ('Helvetica', 20)
        self._root_window = root
        self._option_window = tkinter.Toplevel()


        self._dimension_options = range(4,18,2)
        
        self._row_var = tkinter.IntVar()
        self._row_var.set(self._dimension_options[2])
        
        self._column_var = tkinter.IntVar()
        self._column_var.set(self._dimension_options[2])


        self._color_options = ("BLACK", "WHITE")

        self._first_move_var = tkinter.StringVar()
        self._first_move_var.set(self._color_options[0])

        self._upper_left_var = tkinter.StringVar()
        self._upper_left_var.set(self._color_options[1])


        self._win_options = ("MOST", "FEWEST")
        
        self._win_condition_var = tkinter.StringVar()
        self._win_condition_var.set(self._win_options[0])
        

        self._header = tkinter.Label(
            master = self._option_window, text = "Player Options",
            font = self._DEFAULT_FONT).grid(
                row = 0, column = 0, columnspan = 2, padx = 10, pady = 10)

        self._row_label = tkinter.Label(
            master = self._option_window, text = "Number of ROWS:",
            font = self._DEFAULT_FONT).grid(
                row = 1, column = 0, padx = 10, pady = 10,
                sticky = tkinter.W)

        self._column_label = tkinter.Label(
            master = self._option_window, text = "Number of COLUMNS:",
            font = self._DEFAULT_FONT).grid(
                row = 2, column = 0, padx = 10, pady = 10,
                sticky = tkinter.W)

        self._first_move_label = tkinter.Label(
            master = self._option_window, text = "First Move:",
            font = self._DEFAULT_FONT).grid(
                row = 3, column = 0, padx = 10, pady = 10,
                sticky = tkinter.W)

        self._upper_left_label = tkinter.Label(
            master = self._option_window,
            text = "Top Left Corner:",
            font = self._DEFAULT_FONT).grid(
                row = 4, column = 0, padx = 10, pady = 10,
                sticky = tkinter.W)

        self._win_condition = tkinter.Label(
            master = self._option_window, text = "Win condition:",
            font = self._DEFAULT_FONT).grid(
                row = 5, column = 0, padx = 10, pady = 10,
                sticky = tkinter.W)

        self._row_option = tkinter.OptionMenu(
            self._option_window, self._row_var,
            *self._dimension_options).grid(
                row = 1, column = 1, padx = 10, pady = 10,
                sticky = tkinter.E)

        self._column_option = tkinter.OptionMenu(
            self._option_window, self._column_var,
            *self._dimension_options).grid(
                row = 2, column = 1, padx = 10, pady = 10,
                sticky = tkinter.E)        
        
        self._first_move_option = tkinter.OptionMenu(
            self._option_window, self._first_move_var,
            *self._color_options).grid(
                row = 3, column = 1, padx = 10, pady = 10,
                sticky = tkinter.E)

        self._upper_left_option = tkinter.OptionMenu(
            self._option_window, self._upper_left_var,
            *self._color_options).grid(
                row = 4, column = 1, padx = 10, pady = 10,
                sticky = tkinter.E)

        self._win_condition_option = tkinter.OptionMenu(
            self._option_window, self._win_condition_var,
            *self._win_options).grid(
                row = 5, column = 1, padx = 10, pady = 10,
                sticky = tkinter.E)
        
        button_frame = tkinter.Frame(
            master = self._option_window)
        button_frame.grid(
            row = 6, column = 0, columnspan = 2,
            padx = 10, pady = 10,
            sticky = tkinter.SE)

        self._start_button = tkinter.Button(
            master = button_frame, text = 'Start',
            font = self._DEFAULT_FONT,
            command = self._on_start_clicked).grid(
                row = 0, column = 0, padx = 10, pady = 10)

        self._quit_button = tkinter.Button(
            master = button_frame, text = 'Cancel',
            font = self._DEFAULT_FONT,
            command = self._on_cancel_clicked).grid(
                row = 0, column = 1, padx = 10, pady = 10)


        self._option_window.rowconfigure(6, weight = 1)
        self._option_window.columnconfigure(0, weight = 1)
        self._option_window.columnconfigure(1, weight = 1)
        self._start_clicked = False
        
    def enable(self):
        '''Makes the player options window take over'''
        self._option_window.grab_set()
        self._option_window.wait_window()

    def _on_start_clicked(self):
        '''Saves chosen options as variables to pass onto the GUI'''
        self._start_clicked = True
        self._row_entered = self._row_var.get()
        self._column_entered = self._column_var.get()
        self._first_move_entered = self._first_move_var.get()
        self._upper_left_entered = self._upper_left_var.get()
        self._win_condition_entered = self._win_condition_var.get()
        self._option_window.destroy()

    def _on_cancel_clicked(self):
        '''Simply closes the options window'''
        self._option_window.destroy()

    def started(self):
        return self._start_clicked

    def rows(self):
        return self._row_entered

    def columns(self):
        return self._column_entered

    def first_turn(self):
        return self._first_move_entered

    def upper_left(self):
        return self._upper_left_entered

    def win_condition(self):
        return self._win_condition_entered
    

class OthelloApplication:
    def __init__(self):
        self._state = othello_logic.OthelloGameState()

        self._started = False

        self._root_window = tkinter.Tk()

        self._canvas = tkinter.Canvas(
            master = self._root_window, width = 600,
            height = 600, background = '#0AA114')

        self._canvas.bind('<Configure>', self._on_canvas_resized)
        self._canvas.bind('<Button 1>', self._on_canvas_clicked)

        
        self._canvas.grid(
            row = 1, column = 0,
            padx = 10, pady = 10,
            sticky = tkinter.NSEW)

        self._header_frame = tkinter.Frame(
            master = self._root_window,
            background = '#0AA114')
        self._header_frame.grid(
            row = 0, column = 0, padx = 10, pady = 10,
            sticky = tkinter.NSEW)

        self._new_game_button = tkinter.Button(
            master = self._header_frame, text = "New Game",
            command = self._on_new_game_clicked).grid(
                row = 0, column = 0, padx = 10, pady = 10,
                sticky = tkinter.N)

        self._root_window.rowconfigure(0, weight = 0)
        self._root_window.rowconfigure(1, weight = 1)
        self._root_window.columnconfigure(0, weight = 1)

    def start(self):
        self._root_window.mainloop()

    def _on_new_game_clicked(self):
        '''Pops up the options menu if the New Game button is clicked'''
        self._pop_up_options()
        
    def _pop_up_options(self):
        '''
        Calls the options pop up window and passes the chosen variables to
        the game logic
        '''
        player_options = PlayerOptions(self._root_window)
        player_options.enable()

        if player_options.started():
            self._ROWS = player_options.rows()
            self._COLUMNS = player_options.columns()
            colors = {"BLACK": self._state._BLACK, "WHITE": self._state._WHITE}

            self._state.set_board(self._ROWS, self._COLUMNS)
            self._state.set_turn(colors[player_options.first_turn()])
            self._state.set_center(colors[player_options.upper_left()])
            self._state.set_win_condition(player_options.win_condition())

            self._draw_board()
            self._started = True

    def _on_canvas_resized(self, event: tkinter.Event) -> None:
        '''Draws the board when the canvas is resized'''
        self._draw_board()

    def _on_canvas_clicked(self, event: tkinter.Event) ->  None:
        '''
        Manages when the mouse is clicked.  If it is a valid move, places a
        piece in the specified cell of the click
        '''
        if self._started:
            cell_width = self._canvas.winfo_width()/self._COLUMNS
            cell_height = self._canvas.winfo_height()/(self._ROWS+1)

            row = int(event.y/cell_height)-1
            column = int(event.x/cell_width)

            try:
                self._state.place_piece(row, column)
            except:
                pass

            self._draw_board()

            if self._state.winning_player() != self._state._NONE:
                self._win_pop_up()

            if not self._state.check_valid() and \
               self._state.winning_player() == self._state._NONE:
                self._pass_pop_up()




    def _draw_board(self) -> None:
        '''
        Draws the board, including the current turn and score, onto the
        canvas
        '''
        try:
            self._canvas.delete(tkinter.ALL)
            
            abs_size_x = self._canvas.winfo_width()
            abs_size_y = self._canvas.winfo_height()

            self._display_turn(abs_size_x, abs_size_y)
            self._display_score(abs_size_x, abs_size_y)
            for row in range(self._ROWS):
                for column in range(self._COLUMNS):
                    self._draw_cell(row, column, abs_size_x, abs_size_y)
        except:
            pass

    def _draw_cell(self, row, column, abs_size_x: int, abs_size_y: int) -> None:
        '''
        Draws a single cell of the board, including the piece (if any)
        inside the cell
        '''
        cell_width = abs_size_x/self._COLUMNS
        cell_height = abs_size_y/(self._ROWS+1)

        top_left_x = column * cell_width
        top_left_y = (row + 1) * cell_height
        bottom_right_x = (column + 1) * cell_width
        bottom_right_y = (row + 2) * cell_height

        self._canvas.create_rectangle(top_left_x, top_left_y,
                                      bottom_right_x, bottom_right_y)
        if self._state._board[row][column] != self._state._NONE:
            colors = {self._state._BLACK: "black", self._state._WHITE: "white"}
            self._canvas.create_oval(top_left_x, top_left_y,
                                     bottom_right_x, bottom_right_y,
                                     fill = colors[self._state._board[row][column]])   

    def _display_score(self, abs_size_x: int, abs_size_y: int):
        '''
        The score display at the top left and top right corners of the canvas
        '''
        cell_width = abs_size_x/self._COLUMNS
        cell_height = abs_size_y/(self._ROWS+1)
        font_size = int(abs_size_y/30)
        self._state.keep_score()
        self._canvas.create_oval(0,0,cell_width, cell_height,
                                 fill = "white")
                                 
        self._canvas.create_text(cell_width/2,cell_height/2,
                                 text = str(self._state._white_score),
                                 font = ('Helvetica', font_size),
                                 fill = "black")

        self._canvas.create_oval(abs_size_x - cell_width, 0,
                                 abs_size_x, cell_height,
                                 fill = "black")

        self._canvas.create_text(abs_size_x - cell_width/2, cell_height/2,
                                 text = str(self._state._black_score),
                                 font = ('Helvetica', font_size),
                                 fill = "white")
        
        
        
    

    def _display_turn(self, abs_size_x: int, abs_size_y: int) -> None:
        '''
        Displays the current turn at the top of the canvas.  The font size is
        dependent on the canvas's height.  Also changes to display the winner
        if the game is over.
        '''
        top_left_x = int(abs_size_x/2)
        size = int(abs_size_y/35)
        turn = {self._state._BLACK: "BLACK'S TURN",
                     self._state._WHITE: "WHITE'S TURN"}
        if self._state.winning_player() == self._state._NONE:
            turn_text = turn[self._state._turn]
        else:
            turn_text = "WINNER: {}".format(self._state.winning_player())
            
        self._canvas.create_text(top_left_x, 10,
                                 text = turn_text,
                                 font = ('Helvetica', size),
                                 anchor = tkinter.N,
                                 fill = "white")


    def _pass_pop_up(self):
        '''Pops up a window indiciating if a player has passed'''
        pop_up = tkinter.Toplevel()
        full_name = {self._state._BLACK: 'Black', self._state._WHITE: 'White'}
        tkinter.Message(pop_up, text = "{} passes.".format(
            full_name[self._state.pass_turn()])).grid(
                row = 0, column = 0, sticky = tkinter.S)
        tkinter.Button(pop_up, text = "OK", command=pop_up.destroy).grid(
            row = 1, column = 0, sticky = tkinter.N)

        pop_up.rowconfigure(0, weight = 1)
        pop_up.rowconfigure(1, weight = 1)
        pop_up.columnconfigure(0, weight = 1)
        
        pop_up.grab_set()
        pop_up.wait_window()



    def _win_pop_up(self):
        '''Pops up a window indicating which player has won'''
        self._win_window = tkinter.Toplevel()
        tkinter.Message(self._win_window, text = "WINNER: {}".format(
            self._state.winning_player()), width = 100).grid(
                row = 0, column = 0, columnspan = 2, sticky = tkinter.S)
        tkinter.Button(self._win_window,
                       text = "New Game",
                       command=self._new_game_after_win).grid(
                           row = 1, column = 0, padx = 10, pady = 10,
                           sticky = tkinter.NE)
        tkinter.Button(self._win_window,
                       text = "Close Game",
                       command=self._close_game_after_win).grid(
                           row = 1, column = 1, padx = 10, pady = 10,
                           sticky = tkinter.NW)

        self._win_window.rowconfigure(0, weight = 1)
        self._win_window.rowconfigure(1, weight = 1)
        self._win_window.columnconfigure(0, weight = 1)
        self._win_window.columnconfigure(1, weight = 1)
        
        self._win_window.grab_set()
        self._win_window.wait_window()

    def _new_game_after_win(self):
        '''A button command on the win pop up window to start a new game'''
        self._win_window.destroy()
        self._on_new_game_clicked()

    def _close_game_after_win(self):
        '''Closes the entire othello game'''
        self._win_window.destroy()
        self._root_window.destroy()
    
if __name__ == '__main__':
    OthelloApplication().start()
