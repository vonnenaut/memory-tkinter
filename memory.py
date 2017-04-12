# Memory card-flip matching game using Tkinter
##

# import
##
import Tkinter as tk
import random

# globals
##
CARD_WIDTH = 65
CARD_HEIGHT = 100
DISTINCT_CARDS = 8
canvas = None


# classes
##
class Card(object):
    """ represents each card in the matching game, keeping track of face-value, state (hidden or exposed), drawing the cards and keeping track of which card is selected via mouse click.  Instantiated in MemoryGame class. """

    # globals
    ##
    global CARD_WIDTH, CARD_HEIGHT, deck

    def __init__(self, num, exp, loc):
        self.number = num
        self.exposed = exp
        self.location = loc
   
    def get_number(self):
        return self.number
    
    # check whether Card is exposed
    def is_exposed(self):
        return self.exposed
    
    # expose the Card
    def expose_Card(self):
        self.exposed = True
        draw(canvas, deck)
    
    # hide the Card       
    def hide_Card(self):
        self.exposed = False
        draw(canvas, deck)

    def __str__(self):
        return "Number is " + str(self.number) + ", exposed is " + str(self.exposed)    

    def draw_Card(self, canvas):
        """ draws cards as a green rectangle if hidden, or white with black numbering if exposed.  Called by draw() function. """
        loc = self.location
        card_corners = (loc[0], loc[1], loc[0] + CARD_WIDTH, loc[1] - CARD_HEIGHT)

        if self.exposed:
            text_location = [loc[0] + 0.5 * CARD_WIDTH, loc[1] - 0.45 * CARD_HEIGHT]
            canvas.create_rectangle(card_corners, fill='white', outline='black')
            canvas.create_text(text_location, font=('Helvetica', 55), text=str(self.number), fill='black')
        else:
            canvas.create_rectangle(card_corners, fill='green', outline='black')
            
    def is_selected(self, event):
        """ helper method for MemoryGame.mouseHandler() to check if a card has been clicked """
        inside_horiz = self.location[0] <= event.x < self.location[0] + CARD_WIDTH
        inside_vert = self.location[1] - CARD_HEIGHT <= event.y <= self.location[1]
        return  inside_horiz and inside_vert


# main application class
##
class MemoryGame(tk.Frame):
    """ implements the game """
    # globals
    ##
    global DISTINCT_CARDS, CARD_WIDTH, CARD_HEIGHT, deck

    deck = []
    # set up face values for the cards
    card_numbers = range(1, DISTINCT_CARDS + 1) * 2
    # shuffle the values
    random.shuffle(card_numbers)   
    # instantiate deck as a list of instances of the Card class
    deck = [Card(card_numbers[i], False, [i * CARD_WIDTH, CARD_HEIGHT]) for i in range(2 * DISTINCT_CARDS)]
   
    def __init__(self, parent, *args, **kwargs):
        """ initialize Frame and global variables """
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.deck = deck  
        self.game_state =  0        # int, self.game_state of game:
                                    # 0:  beginning of game
                                    # 1:  1 card has been picked/shown
                                    # 2:  2 cards have been picked/shown
        self.turn = 1               # keeps track of number of turns
        self.label_string = tk.StringVar()   # used to update the label for turn number
        self.label_string.set("Turn: " + str(self.turn)) 
        self.makeWidgets()
        self.clicked_card = None
        self.card1 = None
        self.card2 = None

    def makeWidgets(self):
        """ set up GUI, i.e., create widgets """
        # globals
        global CARD_WIDTH, CARD_HEIGHT        
    
        # bind an event listener to the canvas and add the canvas to the root frame
        canvas.bind("<Button-1>", self.mouseHandler)
        canvas.pack()
        # add buttons to the frame
        tk.Button(root, text='Reset', command=self.Reset).pack(side="left")
        tk.Button(root, text='Quit', command=root.quit).pack(side="left")
        # add label which updates based on turn number
        tk.Label(root, textvariable=self.label_string, font=('Helvetica',12), fg='white', bg='black').pack(side="left")
        # now draw everything
        draw(canvas, self.deck)        

    def Reset(self):
        for card in self.deck:
            card.hide_Card()
        self.turn = 1
        self.label_string.set("Turn: " + str(self.turn))
        self.game_state = 0
        draw(canvas, self.deck)
    
    def mouseHandler(self, event):
        """ handles user input, manages game state and status of cards """
        for card in self.deck:
            if card.is_selected(event):
                self.clicked_card = card
                
                if self.clicked_card.is_exposed():
                    return
        
                self.clicked_card.expose_Card()        
        
        # handle game states
        if self.game_state == 0:
            self.card1 = self.clicked_card
            self.game_state = 1
    
        elif self.game_state == 1:
            self.card2 = self.clicked_card
            self.game_state = 2
            
        else: 
            if self.card2.get_number() != self.card1.get_number():
                self.card2.hide_Card()
                self.card1.hide_Card()
            self.card1 = self.clicked_card
            self.game_state = 1
            self.turn += 1
            self.label_string.set("Turn: " + str(self.turn))
            

# draw handler
##
def draw(canvas, deck):
    """ draws cards on canvas """
    for card in deck:
        card.draw_Card(canvas)    

# start frame and game
##
if __name__ == '__main__':
    root = tk.Tk()
    root.configure(background='black')
    
    # create canvas for drawing cards    
    canvas = tk.Canvas(root, width=16*CARD_WIDTH, height=CARD_HEIGHT)    

    # tk magic follows here
    MemoryGame(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
