# Memory card-flip matching game using Tkinter
##

# import
##
from Tkinter import *
import random


# globals
##
CARD_WIDTH = 65
CARD_HEIGHT = 100
DISTINCT_CARDS = 8


# classes
##
class Card(object):
    """ represents each card in the matching game, keeping track of face-value, state (hidden or exposed), drawing the cards and keeping track of which card is selected via mouse click """
    def __init__(self, num, exp, loc):
        self.number = num
        self.exposed = exp
        self.location = loc
        
    # definition of getter for number
    def get_number(self):
        return self.number
    
    # check whether Card is exposed
    def is_exposed(self):
        return self.exposed
    
    # expose the Card
    def expose_Card(self):
        self.exposed = True
    
    # hide the Card       
    def hide_Card(self):
        self.exposed = False
        
    # string method for Cards    
    def __str__(self):
        return "Number is " + str(self.number) + ", exposed is " + str(self.exposed)    

    # draw method for Cards
    def draw_Card(self, canvas):
        loc = self.location
        card_corners = (loc[0], loc[1], loc[0] + CARD_WIDTH, loc[1] - CARD_HEIGHT)

        if self.exposed:
            text_location = [loc[0] + 0.5 * CARD_WIDTH, loc[1] - 0.45 * CARD_HEIGHT]
            canvas.create_rectangle(card_corners, fill='white', outline='black')
            canvas.create_text(text_location, font=('Helvetica', 55), text=str(self.number), fill='black')
        else:
            canvas.create_rectangle(card_corners, fill='green', outline='black')
            
    # selection method for Cards
    def is_selected(self, event):
        inside_horiz = self.location[0] <= event.x < self.location[0] + CARD_WIDTH
        inside_vert = self.location[1] - CARD_HEIGHT <= event.y <= self.location[1]
        return  inside_horiz and inside_vert


class MemoryGame(Frame):
    """ implements the game """
    # globals
    global deck, game_state, turn, DISTINCT_CARDS, CARD_WIDTH, CARD_HEIGHT

    game_state = 0  # int, game_state of game:
                        # 0:  beginning of game
                        # 1:  1 card has been picked/shown
                        # 2:  2 cards have been picked/shown
    turn = 1        # keeps track of number of turns

    # set up deck
    card_numbers = range(1, DISTINCT_CARDS + 1) * 2
    random.shuffle(card_numbers)
    deck = [Card(card_numbers[i], False, [CARD_WIDTH * i, CARD_HEIGHT]) for i in range(2 * DISTINCT_CARDS)]
    
    def __init__(self, parent=None, **kw):
        """ initialize Frame and global variables """
        Frame.__init__(self,parent, kw)
        self.deck = deck
        self. game_state =  game_state
        self.turn = turn

    def makeWidgets(self):
        """ create widgets """
        #  Consider moving buttons and label here
        pass
        

    def Reset(self):
        for card in self.deck:
            self.exposed = False
        self.turn = 1
        self.game_state = 0
    
    def mouseHandler(self, event):
        """ handles user input, manages game state and status of cards """
        global game_state, turn, c1_index, c2_index, w

        # TESTS click functionality
        print "Clicked at ", event.x, event.y

        for card in deck:
            if card.is_selected(event):
                clicked_card = card
                
        if clicked_card.is_exposed():
            return
        
        clicked_card.expose_Card()
        
        # handle game states
        if game_state == 0:
            c1_index = clicked_card
            game_state = 1
    
        if game_state == 1:
            c2_index = clicked_card
            game_state = 2
    
        if game_state == 2 and c2_index is not c1_index:
            c2_index.hide_Card()
            c1_index.hide_Card()
            game_state = 1
            turn += 1
    
        draw(w)

           
# draw handler
##
def draw(canvas):
    for Card in deck:
        Card.draw_Card(canvas)
    

# start frame and game
##
def main():
    global w, turn

    root = Tk()
    root.configure(background='black')
    game = MemoryGame(root)
    game.pack(side=TOP)

    w = Canvas(root, width=16*CARD_WIDTH, height=CARD_HEIGHT)
    w.bind("<Button-1>", game.mouseHandler)
    
    draw(w)

    Button(root, text='Reset', command=game.Reset).pack(side=LEFT)
    Button(root, text='Quit', command=root.quit).pack(side=LEFT)
    Label(root, text='Turn: ' + str(turn), font=('Helvetica',12), fg='white', bg='black').pack(side=LEFT)
    w.pack()
        
    root.mainloop()

if __name__ == '__main__':
    main()
