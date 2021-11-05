from random import choice

class Game:
    def __init__(self):
        self.deck = Deck()
        self.players = []
        num_players = int(input("Input number of players: "))
        for i in range(num_players):
            self.players.append(Player(self))
        self.players.append(Player(self, True))
        play_game(self)
    
    
    def deal(self):
        for i in range(2):
            for player in self.players:
                player.hand.append(self.deck.cards.pop(0))
            i += 1

    def find_winners(self):
        differences = []
        w = 0
        for player in self.players:
           differences.append(21 - player.get_total())
        dealer_diff = differences.pop(-1)
        if dealer_diff < 0:
            for i in range(len(differences)):
                if differences[i] >= 0:
                    print(f"Congradulations, Player {i+1}, you won this hand!")
                    w += 1
        elif dealer_diff == 0:
            for i in range(len(differences)):
                if differences[i] == 0:
                    print(f"Player {i+1}, this round is a pull for you.")
                    w += 1
        else:
            for i in range(len(differences)):
                if differences[i] < dealer_diff and differences[i] >= 0:
                    print(f"Congradulations, Player {i+1}, you won this hand!")
                    w += 1
        
        if w == 0 and len(differences) == 1:
            print("Sorry, but you are a LOSER!!!!")
        elif w == 0:
            print("Wow. Looks like all of you are LOSERS!!!!!")
        elif w != len(differences):
            print("Sorry, but the rest of you are LOSERS!!!!!")

    def clear_hands(self):
        for player in self.players:
            player.busted = False
            player.blackjack = False
            while player.hand:
                del player.hand[0]

    def check_deck(self):
        if len(self.deck.cards) < len(self.players)*5:
            print("Putting all cards back in deck...")
            self.deck = Deck()
    
    def round(self):
        self.clear_hands()
        self.check_deck()
        self.deck.shuffle()
        self.deal()
        for player in self.players:
            if player.dealer:
                print(f"\nThe Dealer's Top Card is:\n{player.hand[0]}")
            else:
                print(f"\nPlayer {self.players.index(player)+1}'s Hand:")
                for card in player.hand:
                    print(card)
        
        for i in range(len(self.players)):
            self.players[i].turn(i+1)

        self.find_winners()



        

class Deck:

    def __init__(self):
        self.cards = []
        self.suits = ['clubs','diamonds','hearts','spades']
        for suit in self.suits:
            for num in range(1,14):
                self.card = Card(suit, num)
                self.cards.append(self.card)

    def shuffle(self):
        shuffled_cards = []
        while self.cards:
            shuffled_card = self.cards.pop(choice(range(len(self.cards))))
            shuffled_cards.append(shuffled_card)
        self.cards = shuffled_cards
            
class Player:

    def __init__(self, game, dealer=False):
        self.hand = []
        self.game = game
        self.dealer = dealer
        self.busted = False
        self.blackjack = False

    def get_total(self):
        total = 0
        for card in self.hand:
            total += card.num
        return total


    def turn(self, player_num):
        if self.dealer:
            print("\n"+"=~"*25+'=')
            print("Dealer's turn:")
            print("=~"*25+'=')
            self.show_hand()
            if self.get_total() == 21:
                print("Blackjack!")
                self.blackjack = True
            while self.get_total() < 17:
                self.hit()
            print(f"\ndealer's final total is {self.get_total()}\n")
        else:
            print("\n"+"=~"*25+'=')
            print(f"Player {player_num}'s Turn: ")
            print("=~"*25+'=')
            self.show_hand()
            if self.get_total() == 21:
                print("Blackjack!")
                self.blackjack = True
            while not self.busted and not self.blackjack:
                if self.get_total() > 21:
                    print(f"\nSo sorry, you've busted! Your final total is {self.get_total()}")
                    self.busted = True
                    break
                if self.get_total() == 21:
                    print(f"\nyour final total is {self.get_total()}")
                    break
                print("\nWhat would you like to do? ")
                action = input("Enter 'hit' or 'stand': ")
                if action == 'hit':
                    self.hit()
                elif action == 'stand':
                    print(f"\nyour final total is {self.get_total()}")
                    break
                else:
                    print("Invalid input. Please try again.")

    def hit(self):
        self.hand.append(self.game.deck.cards.pop(0))
        self.show_hand()
    
    def show_hand(self):
        print("\nPlayer's Hand:")
        for card in self.hand:                    
            print(card)
                
                


class Card:

    def __init__(self, suit, num):
        self.suit = suit
        self.num = num

    def __str__(self):
        return f"{self.num} of {self.suit}"

def play_game(my_game):
    play = True
    while play:
        my_game.round()
        again = input("Would you like to play again? (y/n): ").lower()
        if again == 'n':
            play = False





my_game = Game()