#This file contains a simplified implementation of the game President.

#Need some logic for a chained clear (e.g. three people put down single kings consecutively, fourth can play their king out of turn to clear)

import random
import itertools
import time

class Card:
    """
    This class represents a card
    """
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = self.get_value()

    def get_value(self):
        """
        This function returns the value of the card
        """
        if self.rank == "A":
            return 14
        elif self.rank == "K":
            return 13
        elif self.rank == "Q":
            return 12
        elif self.rank == "J":
            return 11
        else:
            return int(self.rank)
    def __str__(self):
        """
        This function returns the string representation of the card
        """
        return str(self.rank) + self.suit
    def __repr__(self):
        """
        This function returns the string representation of the card
        """
        return str(self.rank) + self.suit
        

class Deck:
    """
    This class represents a deck of cards
    """
    def __init__(self):
        """
        This function initializes the deck of cards
        """
        self.deck = []
        for i in range(2, 11) + ["J", "Q", "K", "A"]:
            for j in ["Spades", "Hearts", "Diamonds", "Clubs"]:
                self.deck.append(Card(j,i))
        self.shuffle()

    def shuffle(self):
        """
        This function shuffles the deck of cards
        """
        random.shuffle(self.deck)

    def deal(self):
        """
        This function deals a card from the deck
        """
        return self.deck.pop()
    
    def is_empty(self):
        """
        This function checks if the deck is empty
        """
        return len(self.deck) == 0

class Hand:
    """
    This class represents a hand of cards
    """
    def __init__(self):
        """
        This function initializes the hand of cards
        """
        self.hand = []

    def add_card(self, card):
        """
        This function adds a card to the hand
        """
        self.hand.append(card)

    def play_card(self,card):
        """
        This function plays a card from the hand
        """
        self.hand.remove(card)

    def is_empty(self):
        """
        This function checks if the hand is empty
        """
        return len(self.hand) == 0
    
    def possible_moves(self):
        """
        This function returns the possible moves of the hand
        """
        moves = [[card] for card in self.hand]
        moves.append([])
        doubles = self.get_doubles()
        for double in doubles:
            moves.append(double)
        triples = self.get_triples()
        for triple in triples:
            moves.append(triple)
        quadruples = self.get_quadruples()
        for quadruple in quadruples:
            moves.append(quadruple)
        return moves
    
    def get_doubles(self):
        doubles = []
        for card1 in self.hand:
            for card2 in self.hand:
                if card1.rank == card2.rank and card1.suit != card2.suit:
                    #check if this pair is already in the list
                    if [card1,card2] not in doubles and [card2,card1] not in doubles:
                        doubles.append([card1,card2])
        return doubles
    
    def get_triples(self):
        triples = []
        for card1 in self.hand:
            for card2 in self.hand:
                for card3 in self.hand:
                    if card1.rank == card2.rank and card2.rank == card3.rank and card1.suit != card2.suit and card2.suit != card3.suit and card1.suit != card3.suit:
                        #check if any permutation of this triple is already in the list
                            found = False
                            for permutation in itertools.permutations([card1,card2,card3]):
                                if list(permutation) in triples:
                                    found = True
                                    break
                            if not found:
                                triples.append([card1,card2,card3])
        return triples
    
    def get_quadruples(self):
        quadruples = []
        for card1 in self.hand:
            for card2 in self.hand:
                for card3 in self.hand:
                    for card4 in self.hand:
                        if card1.rank == card2.rank and card2.rank == card3.rank and card3.rank == card4.rank and card1.suit != card2.suit and card1.suit != card3.suit and card1.suit != card4.suit and card2.suit != card3.suit and card2.suit != card4.suit and card3.suit != card4.suit:
                            #check if any permutation of this quadruple is already in the list
                            found = False
                            for permutation in itertools.permutations([card1,card2,card3,card4]):
                                if list(permutation) in quadruples:
                                    found = True
                                    break
                            if not found:
                                quadruples.append([card1,card2,card3,card4])
        return quadruples
    def __repr__(self):
        return str([str(card) for card in self.hand])

class Game:
    """
    This class represents a game of President
    """
    def __init__(self,num_players):
        """
        This function initializes the game of President
        """
        self.deck = Deck()
        self.num_players = num_players
        self.hands = [Hand() for i in range(self.num_players)]
        self.player_turn_idx = 0
        self.remaining_players = ["Player " + str(i) for i in range(self.num_players)]
        self.order_of_finish = []
        self.current_card = []
        self.skip_flag = False
        self.clear_flag = False

    def deal(self):
        """
        This function deals the cards to the players
        """
        player = 0
        while not self.deck.is_empty():
            self.hands[player].add_card(self.deck.deal())
            player = (player + 1) % self.num_players
        for hand in self.hands:
            print(hand)
        
    def play(self):
        """
        This function plays the game of President
        """
        self.deal()
        last_played = None
        last_play_finished = False
        while len(self.remaining_players) > 1:
            print("\n")
            print("Current player: " + str(self.remaining_players[self.player_turn_idx]))
            print("Player turn index" + str(self.player_turn_idx))
            print("Last played index: " + str(last_played))
            print("Remaining players: " + str(self.remaining_players))
            #time.sleep(0.5)
            if last_played == self.player_turn_idx:
                #all players have passed, clear the board
                self.current_card = []
                last_played = None
                player_finished = False
                print("Everyone passed, clearing the board")
            else:
                self.skip_flag = False
                self.clear_flag = False
                player_finished = False
                #Get action space for every player
                possible_actions = []
                action_takers = []
                for i in range(len(self.remaining_players)):
                    action_space = self.get_action_space(self.hands[i],i)
                    for action in action_space:
                        possible_actions.append(action)
                        action_takers.append(i)
                #Choose an action (to be refined)
                print('Action Space:')
                print(possible_actions)
                print('Action Takers:')
                print(action_takers)
                cards = possible_actions[0]
                action_taker = action_takers[0]
                #print(cards)
                #print(action_taker)
                # cards = random.choice(possible_actions)

                self.action_result(cards)
                for card in cards:
                    self.hands[action_taker].play_card(card)
                if self.hands[action_taker].is_empty():
                    #Player has cleared hand
                    print(self.remaining_players[action_taker] + " has cleared their hand")
                    self.remaining_players.pop(action_taker)
                    self.hands.pop(action_taker)
                    player_finished = True
                    last_played = None
                    last_play_finished = True

                #Advance player turn
                if self.clear_flag == True:
                    #Clear the board
                    print("Cleared the board")
                    self.current_card = []
                    if player_finished == True:                            
                        self.player_turn_idx = (action_taker) % len(self.remaining_players)             
                    else:
                        self.player_turn_idx = action_taker
                        last_play_finished = False
                    last_played = None
                elif self.skip_flag == True:
                    print("Skipped the next player")
                    #Skip the next player
                    self.current_card = cards
                    if player_finished == True: 
                        last_played = None
                        self.player_turn_idx = (self.player_turn_idx + 1) % len(self.remaining_players)
                    else:
                        last_played = action_taker
                        self.player_turn_idx = (self.player_turn_idx + 2) % len(self.remaining_players)
                        last_play_finished = False
                elif cards != []:
                    #Normal move
                    self.current_card = cards
                    if player_finished == True: 
                        last_played = None
                        self.player_turn_idx = (self.player_turn_idx) % len(self.remaining_players)
                    else:
                        last_played = action_taker
                        self.player_turn_idx = (self.player_turn_idx + 1) % len(self.remaining_players)
                        last_play_finished = False
                elif cards == []:
                    #Empty move
                    if last_play_finished:
                        last_played = self.player_turn_idx
                        last_play_finished = False
                    else:
                        self.player_turn_idx = (self.player_turn_idx + 1) % len(self.remaining_players)
                


    def is_valid_action(self,cards,player_idx):
        """
        This function checks if the action is valid given the current state of the game
        """
        if player_idx == self.player_turn_idx:
            if len(self.current_card) == 0:
                #Intial action
                return True
            elif len(cards)==0:
                #Pass action
                return True
            elif len(cards) + len(self.current_card) == 4 and self.current_card[0].rank == cards[0].rank:
                #Clear action
                return True
            elif len(cards) != len(self.current_card):
                return False
            elif cards[0].value >= self.current_card[0].value:
                return True
            else:
                return False
        else:
            if len(self.current_card) == 0:
                #Intial action
                return False
            elif len(cards) + len(self.current_card) == 4 and self.current_card[0].rank == cards[0].rank:
                #Clear action
                return True
            else:
                return False

    def action_result(self,cards):
        """
        This function determines the result of the action taken
        """
        print("Current card: " + str(self.current_card))
        print("Action taken: " + str(cards))
        if len(cards) == 4:
            #Clear action
            self.clear_flag = True
        if len(cards) != 0:   
            if len(self.current_card) > 0:
                if len(cards) + len(self.current_card) == 4 and self.current_card[0].rank == cards[0].rank:
                    #Clear action
                    self.clear_flag = True
                elif cards[0].rank == self.current_card[0].rank:
                    self.skip_flag = True


    def get_action_space(self,hand,player_idx):
        legalMoves = []
        possibleMoves = hand.possible_moves()
        for move in possibleMoves:
            if self.is_valid_action(move,player_idx):
                legalMoves.append(move)
        return legalMoves

game = Game(4)
game.play()