"""
Author: Alex Phillips
Date Written: October 2019
Description: A fully functioning game of Klondike (Solitaire) with added features
"""
import random
from random import randrange
import tkinter as tk
from tkinter import ttk
import sys

def redirector(inputStr): #Once called, outputs all IDLE to the textbox created by tkinter
        textbox.insert(tk.END, inputStr)

class Deque: #Very similar Deque class to the origianl assignment, with printall() and peek_last() removed due to them being unused by my extension. Used as the stacks of cards in my solitaire game
        def __init__(self):
                self.items = []
                
        def add_front(self, item):
                self.items.append(item)
                
        def add_rear(self, item):
                self.items.insert(0, item)
                
        def remove_front(self):
                return self.items.pop(-1)
        
        def remove_rear(self):
                return self.items.pop(0)
        
        def size(self):
                return len(self.items)
        
        def peek(self):
                return self.items[-1]

        def peeklast(self): 
                return self.items[0]
        

class Game: #Designed to act as an initialiser and handler for button presses in tkinter (Handles input in general)
        def __init__(self): #Creates the original card list prior to being shuffled and flipped
                values = []
                for suit in ["C", "D", "S", "H"]:
                        for value in range(1, 14):
                                values.append(Cards(value, suit))
                self.values = values
                
        def initialization_screen(self): #Called at the bottom of the page to create a part of the intro display
                print("--------------------------------------------------------------------------------")
                print("************************************|KLONDIKE|**********************************")
                print("--------------------------------------------------------------------------------")
                print("*************************|PRESS DISPLAY TO GET STARTED|*************************")
                self.get_help() #Calls get_help() to extend the intro display to give rules and instructions for the game
                
        def start_reset(self, num = 0): #Creates the first game and all other non-reset games as well as the game run by the AI to compete against
                ai_values = []
                for values in self.values:
                        values.reset_state()
                random.shuffle(self.values) #Shuffles cards to create a new and random experience for the player
                self.game = Solitaire(list(self.values)) #Creates the game to be played by the user
                for elm in self.values:
                        card_copy = Cards(elm.value, elm.suit) #Creates new cards with identical values and suits to prevent flipping cards from the AI to user games
                        if elm.state == 1:
                                card_copy.card_state()
                        ai_values.append(card_copy)
                self.ai_game = Solitaire(ai_values) #Creates a game and runs the 'AI', algorithm, to attempt to win the game
                self.ai_move_lst = self.ai_game.auto_complete(1)
                if self.ai_game.IsComplete() == False:
                        self.ai_status = "Loss"
                else:
                        self.ai_status = "Win"
                if num == 0: #Upon initiallisation the intro display would be printed on without a unique variable being passed to the function, num == 1, in this one case
                        self.display_game()
                        
        def next_state(self): #Collects inputted data from tkinter once make move is pressed to attempt to advance the game
                c1 = comboFrom.current()
                c2 = comboTo.current()
                self.game.move(c1, c2)
                self.display_game()
                
        def rotate(self): #Simply redirects the next card button to the users game to rotate Stack 7
                self.game.rotate()
                self.display_game()
                
        def get_help(self): #Simple print function designed to help the player understand the user interface and how their interactions with it affect the game
                print("--------------------------------------------------------------------------------")
                print("**************************************|HELP|************************************")
                print("--------------------------------------------------------------------------------")
                print("                                     |BUTTON|                                   ")
                print("1: 'Start/Reset' wipes the screen/previous game and starts a new game")
                print("2: 'Move From' selects the stack you wish to move cards from")
                print("3: 'Move To' selects the stack you wish to move cards to")
                print("4: 'Make Move' initiates the selected move stacks and counts as 1 move")
                print("5: 'Next Card' rotates the rotating pile labelled as 'Stack 7'")
                print("6: 'Get Help' return this menu in case you get stuck")
                print("7: 'Get Hint' finds a possible move, if none are available you have lost")
                print("8: 'Auto Complete' uses 'Get Hint' with a simple algorithim to 'solve' the game")
                print("9: 'Display' shows your game, 'Display AI Game' shows the AI's Game")
                print("                                   |GAMEPLAY|                                   ")
                print("1: The top left shows the AI's performance on your game, with turns/game status")
                print("2: Removing a card in Stacks 0-6 reveals the card beneath")
                print("3: Empty Stacks 0-6 can only have a king (13) placed there")
                print("4: Stacks 8-11 should contain the full ascending suits to win the game, (1-13)")
                print("5: The objective is to move all cards from Stacks 0-7 to 8-11 and beat the AI")
                print("--------------------------------------------------------------------------------")
                
        def get_hint(self): #Takes the button press of Get Hint, detects values, if any, and prints a message to the player on what move they can make
                values = self.game.hint()
                self.display_game()
                if values == None:
                        if self.game.IsComplete() == True: #Assesing if the game is over
                                self.game.end_game(1)
                        else:
                                self.game.end_game(0)
                else:
                        print ("There is a move from {} to {}".format(values[0], values[1]))
                        
        def auto_complete(self): #Simple redirection of the auto complete button to within the Solitaire Class function
                self.game.auto_complete()
                self.display_game()
                
        def restart(self): #Due to the shuffle in start/restart, which is necassary for a new game, restart turns cards to hidden and recreates the game the user was just playing
                for values in self.values:
                        values.reset_state()
                self.game = Solitaire(list(self.values))
                self.display_game()
                
        def display_game(self): #Clears the output textbox and then displays the user game with minor facts about the AI's game
                textbox.delete("1.0", tk.END)
                self.game.display(self.ai_game.turn, self.ai_status)
                if self.game.IsComplete() == True: #Checks if the game is won
                        self.game.end_game(1)
                        
        def display_ai_game(self): #Clears the output textbox and then displays the AI game with every move made displayed beneath to follow yourself or to comb over to see the algorithm in effect
                textbox.delete("1.0", tk.END)
                self.ai_game.display()
                if self.ai_game.IsComplete() == True:
                        self.ai_game.end_game(1)
                else:
                        self.ai_game.end_game(0)
                print ("The moves of the AI to reach the point it did are:")
                print()
                for elm in self.ai_move_lst:
                        print(elm)
                        

class Cards: #Needed rather than a value to help distinguish colour, suit and state (hidden or revealed)
        def __init__(self, value, suit): #Assigns value and suit, notbly automatically makes the cards hidden
                self.value = value
                self.suit = suit
                self.state = 0
                
        def suit_value(self): #Returns 'value' of suits, black % 2 = 0 | red % 2 = 1, for usage within the game (Primarily when moving/hints)
                if self.suit == "C":
                        return 0
                if self.suit == "D":
                        return 1
                if self.suit == "S":
                        return 2
                if self.suit == "H":
                        return 3
                
        def card_state(self): #Flips card to revealed
                self.state = 1
                
        def reset_state(self): #Flips card to hidden
                self.state = 0
                
        def print_card(self): #Returns string for cards, 'empty_card' returns empty string, hidden returns ***** and revealead show value and suit
                if self.value == 999:
                        return ("")
                elif self.state == 1:
                        return str(self.value) + " " + self.suit
                else:
                        return ("*****")
                

class Solitaire: #Actual game of Solitaire which relies on Game Class for input, deque for the stack structure and cards for interactions between the stacks
        def __init__(self, ncards): #Creates the game with the correct cards in each pile, also reveals those exposed in the game piles
                self.turn = 0
                self.stacks = []
                nums = 0
                for i in range(12):
                        self.stacks.append(Deque())
                        nums += 1
                        for x in range(nums):
                                if nums < 8:
                                        if x == nums - 1:
                                                ncards[0].card_state()
                                        self.stacks[i].add_front(ncards.pop(0))
                while len(ncards) != 0: #Remainder is added to rotating pile revealed
                        ncards[0].card_state()
                        self.stacks[7].add_front(ncards.pop(0))
                empty_card = Cards(999, "H") #'Empty Card' to help give the rotating pile the proper aesthetic of Solitaire
                empty_card.card_state()
                self.stacks[7].add_front(empty_card)
                
        def move(self, c1, c2): #Move to and from function, c1 = move from and c2 = move to (Extra spaces between blocks of code for clarification)
                if self.stacks[c1].size() == 0 or c2 == 7 or c1 == c2: #Asseses error conditions that break the game or produce errors and ignores them
                        return
                if self.stacks[c1].peek().value == 999:
                        return
                self.turn += 1 #Increases the turn counter even if it fails past the error conditions
                to_add = []
                
                if c2 > 7: #Needs there own special instance due to the empty stack needing to be filled by 1, an ace, and suit_value needing to be equal and placed on ascending order when not empty
                        if self.stacks[c2].size() >= 1:
                                if self.stacks[c1].peek().suit_value() == self.stacks[c2].peek().suit_value() and self.stacks[c1].peek().value - 1 == self.stacks[c2].peek().value:
                                        self.stacks[c2].add_front(self.stacks[c1].remove_front()) #Removes front of stack c1 to add to the front of stack c2
                                        if c1 == 7: #To help preserve the aesthetic of Solitaire by revealing the past card in the rotating pile
                                                self.stacks[c1].add_front(self.stacks[c1].remove_rear())
                        elif self.stacks[c1].peek().value == 1:
                                self.stacks[c2].add_front(self.stacks[c1].remove_front())
                                if c1 == 7:
                                        self.stacks[c1].add_front(self.stacks[c1].remove_rear())
                
                elif c1 == 7: #A unique condition as multiple cards cannot be removed at once and the past card of the rotating pile must be shown
                        if self.stacks[c2].size() >= 1: #Due to the prior condition c2 < 7, it follows it must be going into the game piles and must be assesed to meet those conditions
                                if self.stacks[c1].peek().suit_value() % 2 != self.stacks[c2].peek().suit_value() % 2 and self.stacks[c1].peek().value + 1 == self.stacks[c2].peek().value:
                                        self.stacks[c2].add_front(self.stacks[c1].remove_front())
                                        self.stacks[c1].add_front(self.stacks[c1].remove_rear())
                        elif self.stacks[c1].peek().value == 13: #As it's going into game piles and empty stack c2 means stack c1 must have a 13, king, at the front
                                self.stacks[c2].add_front(self.stacks[c1].remove_front())
                                self.stacks[c1].add_front(self.stacks[c1].remove_rear())
                                
                else: #Now it generally will be dealing with inter game pile conditions and thus reads through the stacks to see if multiple cards are wanting to be moved, from high to low
                        if c1 > 7:
                                if self.stacks[c2].size() >= 1: #Must be moving to game pile as c2 > 7, just stops multiple cards being removed from a stack to the game piles
                                        if self.stacks[c1].peek().suit_value() % 2 != self.stacks[c2].peek().suit_value() % 2 and self.stacks[c1].peek().value + 1 == self.stacks[c2].peek().value:
                                                self.stacks[c2].add_front(self.stacks[c1].remove_front())
                        elif self.stacks[c2].size() >= 1:
                                for elm in self.stacks[c1].items:
                                        if elm.state != 0: #Hidden cards are invalid and not counted
                                                if elm.suit_value() % 2 != self.stacks[c2].peek().suit_value() % 2 and elm.value + 1 == self.stacks[c2].peek().value:
                                                        to_add = self.stacks[c1].items[self.stacks[c1].items.index(elm):] #Removes section of items to be added to the desired stack
                                                        self.stacks[c1].items = self.stacks[c1].items[:self.stacks[c1].items.index(elm)]
                        else: #If it is empty it follows a 13, a king, must be found to append to
                                for elm in self.stacks[c1].items:
                                        if elm.state != 0:
                                                if elm.value == 13:
                                                        to_add = self.stacks[c1].items[self.stacks[c1].items.index(elm):] #Removes section of items to be added to the desired stack
                                                        self.stacks[c1].items = self.stacks[c1].items[:self.stacks[c1].items.index(elm)]
                        for elm in to_add: #Adds those extra items to Stack c2
                                self.stacks[c2].add_front(elm)
                                
                if self.stacks[c1].size() != 0:
                        self.stacks[c1].peek().card_state() #If a card has been revealed by the action it will now be revealed to the user/player/AI
                        
        def rotate(self): #Simple rotation in the rotating pile to reveal a new card
                if self.stacks[7].peek() == self.stacks[7].peeklast():
                        pass
                elif self.stacks[7].size() > 1:
                        self.stacks[7].add_rear(self.stacks[7].remove_front())
                        
        def hint(self, auto = 0):
                if auto == 0: #If the AI is accesing this it will not incur turn penalties
                        self.turn += 1
                for c1 in [6,5,4,3,2,1,0,7]: #Prioritised for stacks generally featuring more hidden cards with rotating last (Major effect)
                        for c2 in [11,10,9,8,0,1,2,3,4,5,6]: #Prioritised for ascending stacks in the top right to finish the game (Major effect), then from generally more empty slot to greater slots(Small/No effect)
                                
                                if self.stacks[c1].size() == 0 or c2 == c1: #Checks for error conditions and ignores
                                        pass
                                elif c2 > 7: #Identical to move(), bar the fact no actual change occurs. Instead it returns the possible meoves
                                        if self.stacks[c2].size() >= 1:
                                                if self.stacks[c1].peek().suit_value() == self.stacks[c2].peek().suit_value() and self.stacks[c1].peek().value - 1 == self.stacks[c2].peek().value:
                                                        return [c1,c2]
                                        elif self.stacks[c1].peek().value == 1:
                                                return [c1,c2]
                                
                                elif c1 == 7: #Due to the nature of the rotating pile it is iterated through multiple times to ensure no actual moves remain, due to the nature of the pile this adds minimal time due to the small quantity of values
                                        original = self.stacks[c1].peek()
                                        cond = 0
                                        while (self.stacks[c1].peek().value != original.value and self.stacks[c1].peek().suit_value() != original.suit_value()) or cond < 3:
                                                if self.stacks[c1].peek().value == 999:
                                                        pass
                                                elif self.stacks[c2].size() >= 1:
                                                        if self.stacks[c1].peek().suit_value() % 2 != self.stacks[c2].peek().suit_value() % 2 and self.stacks[c1].peek().value + 1 == self.stacks[c2].peek().value:
                                                                return [c1,c2]
                                                elif self.stacks[c1].peek().value == 13 and c2 < 7:
                                                        return [c1,c2]
                                                if original == self.stacks[c1].peek():
                                                        cond += 1
                                                self.rotate() #Rotates the pile for the next c1 to be assesed, once one is found it returns it with the value showing in the game
                                
                                else: #Identical to move(), bar the fact no actual change occurs. Instead it returns the possible meoves
                                        if self.stacks[c2].size() >= 1:
                                                for elm in self.stacks[c1].items:
                                                        if elm.state != 0:
                                                                if elm.suit_value() % 2 != self.stacks[c2].peek().suit_value() % 2 and elm.value + 1 == self.stacks[c2].peek().value:
                                                                        return [c1,c2]
                                                                else:
                                                                        break
                                        else:
                                                for elm in self.stacks[c1].items:
                                                        if elm.state != 0:
                                                                if elm.value == 13 and self.stacks[c1].items.index(elm) != 0:
                                                                        return [c1,c2]
                return None
        
        def auto_complete(self, cond = 0): #Manipulates the hint function by repeatedly calling it and making moves based on its recommendations
                move_lst = []
                breaker = 0
                while self.IsComplete() != True:
                        while self.IsComplete() != True:
                                vals = self.hint(1)
                                if vals == None: #Once hint returns None it breaks out of the list
                                        break
                                if cond == 1: #For the AI it saves the moves made to display later
                                        move_lst.append("The AI moved from {} to {}".format(vals[0], vals[1]))
                                self.move(vals[0], vals[1])
                        num = randrange(9) #To ensure there is no more moves the rotating pile is randomly switched up and this must fail multiple times to break out for assesment by IsComplete and end_game()
                        for nums in range(num):
                                self.rotate()
                        breaker += 1
                        if breaker == 50:
                                break
                return move_lst
        
        def display(self, ai_turn = "N/A", status = "N/A"): #Creates the primary display for both the AI games and the user's game, if it is the user it is passed information about the AI and the succesfulness of its' game
                print("************************************|KLONDIKE|**********************************")
                self.x_width = 11
                display_list = []
                length_list = []
                x_width_string = "{:^" + str(self.x_width) + "}" #Creates the standard spacing of each column to keep things aligned
                string = x_width_string * 7 #Creates the formatible string for each line
                print(string.format("AI = {}".format(status),"You","Stack 7","Stack 8","Stack 9","Stack 10","Stack 11"))
                for elm in self.stacks[7:]: #Formats the upper stacks, which appear first, and outputs them to the tkinter textbox
                        if elm == self.stacks[7]:
                                print(x_width_string.format("Turn: {}".format(ai_turn)), end="")
                                print(x_width_string.format("Turn: {}".format(self.turn)), end="")
                                if elm.size() >= 1:
                                        print(x_width_string.format(elm.peek().print_card()), end="")
                                else:
                                        print (x_width_string.format("Empty"), end="") #Due to the lack of cards from the beginning, empty helps emphasize that cards can be moved there
                        elif elm.size() >= 1:
                                print(x_width_string.format(elm.peek().print_card()), end="")
                        else:
                                print (x_width_string.format("Empty"), end="")
                print()
                print("--------------------------------------------------------------------------------")
                print(string.format("Stack 0","Stack 1","Stack 2","Stack 3","Stack 4","Stack 5","Stack 6"))
                for nums in range(7): #Creates lists of the displays lines and another list with the lengths of those within
                        display_list.append(self.stacks[nums].items)
                        length_list.append(len(display_list[nums]))
                for nums in range(max(length_list)): #Then formats the element printed (Card Class) or an empty string if greater than what is within the stack
                        for elm in self.stacks[:7]:
                                if elm.size() > nums:
                                        print(x_width_string.format(elm.items[nums].print_card()), end="")
                                else:
                                        print(x_width_string.format(""), end="")
                        print()
                        
        def IsComplete(self): #Asseses the game being played and determines if it finished
                for nums in range(8):
                        if nums == 7:
                                if self.stacks[nums].size() > 1: #Should contain the 'empty card'
                                       return False 
                        elif self.stacks[nums].size() >= 1:
                                return False
                return True
        
        def end_game(self, condition): #Should the game deemed finshed by IsComplete(), the condition will equal 1. If hint returns None the condition will equal 0
                if condition == 1:
                        print("--------------------------------------------------------------------------------")
                        print("********************************|CONGRATUALATIONS|******************************")
                        print("************************************|YOU HAVE|**********************************")
                        print("**************************************|WON!|************************************")
                        print("--------------------------------------------------------------------------------")
                if condition == 0:
                        print("--------------------------------------------------------------------------------")
                        print("************************************|YOU HAVE|**********************************")
                        print("**************************************|LOST|************************************")
                        print("--------------------------------------------------------------------------------")
                        

base_game = Game() #Initialises the game for commands to map to
base_game.start_reset(1) #Creates a game with the display not outputing, due to (1)

app = tk.Tk() 
app.title("KLONDIKE - Alex Phillips") #Title and window size
app.geometry('900x500')

load_file_button = ttk.Button(app, text="Start/Reset", command=base_game.start_reset) #The next functions map buttons to the appropriate commands and places them on the user-interface
load_file_button.grid(column=0, row=0)

label2 = tk.Label(app, text = "Move From:")
label2.grid(column=1, row=0)
comboFrom = ttk.Combobox(app,  values=["0","1","2","3","4","5","6","7","8","9","10","11"])
comboFrom.grid(column=2, row=0)
comboFrom.current(0)

label3 = tk.Label(app, text = "Move To:")
label3.grid(column=3, row=0)
comboTo = ttk.Combobox(app,  values=["0","1","2","3","4","5","6","7","8","9","10","11"])
comboTo.grid(column=4, row=0)
comboTo.current(1)

action = ttk.Button(app, text="Make Move", command=base_game.next_state)  
action.grid(column=5,row=0)
action = ttk.Button(app, text="Next Card", command=base_game.rotate)  
action.grid(column=6,row=0)
action = ttk.Button(app, text="Get Help", command=base_game.get_help)  
action.grid(column=7,row=0)
action = ttk.Button(app, text="Get Hint", command=base_game.get_hint)  
action.grid(column=8,row=0)
action = ttk.Button(app, text="Auto Complete", command=base_game.auto_complete)  
action.grid(column=9,row=0)
action = ttk.Button(app, text="Replay/Restart", command=base_game.restart)  
action.grid(column=0,row=3)
action = ttk.Button(app, text="Display", command=base_game.display_game)  
action.grid(column=8,row=3) 
action = ttk.Button(app, text="Display AI Game", command=base_game.display_ai_game)  
action.grid(column=9,row=3)

textbox = tk.Text(app)
textbox.grid(column=0, row=1, columnspan=9,padx=2, pady=2)

sys.stdout.write = redirector #Redirects all output in IDLE to the created textbox made by tkinter

base_game.initialization_screen() #Now that output has been redirected, the intialization screen can be printed to display on loading

app.mainloop()
