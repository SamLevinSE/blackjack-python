import random

CARDS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')

RANKS = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
         '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10}


class Language:
    """Super class for keeping language related data"""

    def __init__(self):
        self.phrases = []

    def get_phrase(self, index):  # Returns phrases
        return self.phrases[index]

    def __str__(self):  # Returns printable string representation of the language
        return str(self.phrases)


class EnLang(Language):
    """ Language class for english """

    def __init__(self):  # data structure to store phrases
        self.phrases = ["\nLoading gaming...", "Player 1's cards: ", "Player 2's cards: ", "'s Hand: ",
                        "'s Hand total: ", "Turn: ", " Would you like to hit (H) or stand (S)? ", ": Please type 'H' or 'S' to\
                          continue.\n", "\nOne card has been added to ", "'s hand", "Player 1 Hand: ",
                        "Player 1 Hand Total: ", "Player 2 Hand: ", "Player 2 Hand Total: ", "Both players have ",
                        "! There is a tie!", "Player 1 has blackjack! Player 1 wins!",
                        "Player 2 has blackjack! Player 2 wins!", "\n<<< Player 1 Wins! >>>",
                        "\n<<< Player 2 Wins! >>>", ": you have gone over 21. Player 2\
                      wins!", ": you have gone over 21. Player 1\
                      wins!"]

    def get_phrase(self, index):  # Returns the value of card's rank
        return self.phrases[index]

    def __str__(self):  # Returns printable string representation of the language class
        return str(self.phrases)


class Card:
    """Card consists of one element in RANKS.
    This class is capable of returning the
    value of the rank and also returning a
    printable string representation of a card."""

    def __init__(self, rank, house):
        """rank refers to an element in RANKS.
        If the value exists in RANKS, initialize it.
        Else, print Invalid card: 'rank'"""
        if rank in RANKS:
            self.rank = rank
            self.house = house
        else:
            self.rank = None
            print("Invalid card: ", rank)

    def get_rank(self):  # Returns the value of card's rank
        return self.rank

    def __str__(self):  # Returns printable string representation of the card
        return self.house + str(self.rank)


class Player:
    """Hand consists of a list of cards.
    This class is capable of adding
    a card, returning the total value of the
    hand, printing face up cards, showing the
    player their full hand if they consent,
    checking if the player has a bust, and
    returning a printable representation
    of a hand."""

    def __init__(self):
        self.hand = []  # hand refers to a list of cards

    def add_card(self, card):
        self.hand.append(card)  # Adds a card to the list

    def get_value(self):  # Returns the value of a hand
        value = 0
        ace = 0
        for card in self.hand:
            value += RANKS[card.get_rank()]
            if str(card.get_rank()) == 'A':
                ace += 1
            for i in range(ace):
                if value <= 11:
                    """If the value of the hand is <= 11, we want an Ace to be worth 11 points.
                    Since 1 has already been added because 'A' : 1 in VALUES,
                    we only need to add 10 additional points"""
                    value += 10
        return value

    def print_face_up_cards(self):
        """Return cards visible to both players
        (everything except the first card)"""
        for i in range(1, (len(self.hand))):
            print(self.hand[i], end=' ')
        print()

    def show_hand(self):
        """Asks the player if they want to view their hand and
        proceeds accordingly"""
        global turn, lang
        print("\n", turn + lang.get_phrase(3), self, sep="")
        print(turn + lang.get_phrase(4), self.get_value(), sep="")
        print()

    # Check if the player's hand is over 21 (bust)
    def bust(self):
        global turn, playerBust, player1, player2, lang

        # If the player has a bust, proceed according to player
        if self.get_value() > 21:
            playerBust = True
            if turn == 'Player 1':
                print(turn + lang.get_phrase(20))
                print(lang.get_phrase(10), self)
                print(lang.get_phrase(11), self.get_value())
                print(lang.get_phrase(12), player2)
                print(lang.get_phrase(13), player2.get_value())
            if turn == 'Player 2':
                print(turn + lang.get_phrase(21))
                print(lang.get_phrase(10), player1)
                print(lang.get_phrase(11), player1.get_value())
                print(lang.get_phrase(12), self)
                print(lang.get_phrase(13), self.get_value())

    def __str__(self):  # Returns printable string representation of the hand
        cards = ''
        for card in self.hand:
            cards += str(card) + " "
        return cards.strip()


class Deck:
    """Deck consists of a list of cards.
    This class is capable of dealing a card to a hand,
    shuffling a deck, and returning a printable string
    representation of a deck"""

    def __init__(self):
        """deck refers to a list of cards.
        Since I am not accounting for suit,
        I add all of the cards 4 times to
        acheive the correct total"""
        self.deck = []
        houses = ['H', 'C', 'S', 'D']
        for i in range(4):
            for rank in RANKS:
                self.deck.append(Card(rank, houses[i]))

    def deal(self):
        """Deal a single card and remove it
        from the deck."""
        return self.deck.pop()

    def shuffle(self):
        random.shuffle(self.deck)  # Shuffle the deck.

    def __str__(self):
        # Returns printable string representation of the deck.
        cards = ''
        for card in self.deck:
            cards += str(card) + " "
        return cards.strip()


class Logic:
    @classmethod
    def player(cls, player, players_hand):
        """This function takes in the player and the player's hand.
         This function facilitates the logic of a single turn
        in blackjack"""
        global player1Stay, player2Stay, lang

        # Print whose turn it is
        print(lang.get_phrase(5) + player)

        # Ask the player if they want to view their hand and proceed accordingly
        players_hand.show_hand()

        # Ask the player if they want to hit or stay and proceed accordingly
        hit_or_stay = input(player + lang.get_phrase(6))

        # User input check
        while hit_or_stay.lower() != 'h' and hit_or_stay.lower() != 's':
            hit_or_stay = input(player + lang.get_phrase(7))

        if hit_or_stay.lower() == 'h':
            # Deal a card and add it to the hand
            players_hand.add_card(deck.deal())
            print(lang.get_phrase(8), player, lang.get_phrase(9), sep="")
            # Print player's face up cards
            """Ask the player if they want to view their hand and
            #proceed accordingly"""
            players_hand.show_hand()

        # Record if the player decides to stay
        elif hit_or_stay.lower() == 's':
            if player == 'Player 1':
                player1Stay = True
            if player == 'Player 2':
                player2Stay = True
        return

    @classmethod
    def check_outcome(cls):
        # Check results of the game when both players are done
        global player1, player2, lang
        # Print both player's hands and values
        print(lang.get_phrase(10), player1)
        print(lang.get_phrase(11), player1.get_value())
        print()
        print(lang.get_phrase(12), player2)
        print(lang.get_phrase(13), player2.get_value())

        # Print outcome if there is a tie or a winner
        if player1.get_value() == player2.get_value():
            print(lang.get_phrase(14), player1.get_value(), lang.get_phrase(15), sep='')
        elif player1.get_value() == 21:
            print(lang.get_phrase(16))
        elif player2.get_value() == 21:
            print(lang.get_phrase(17))
        else:
            print(lang.get_phrase(18) if player1.get_value() > player2.get_value() else lang.get_phrase(19))


if __name__ == '__main__':
    def blackjack():
        global player1Stay, player2Stay, playerBust, turn, deck, player1, player2, Language, lang
        logic = Logic()
        print(Language)
        if str(Language).lower() == 'en':
            print('English')
            lang = EnLang()

        # Shuffle the deck
        deck.shuffle()

        for i in range(2):
            # Deal two cards to each player's hand
            player1.add_card(deck.deal())
            player2.add_card(deck.deal())
        print(lang.get_phrase(0))

        while (not player1Stay or not player2Stay) and not playerBust:
            """While either player has not "stayed" and neither player's hand is
            over 21 (bust), game continues
            Print both player's  cards"""
            print(lang.get_phrase(1), end='')
            player1.show_hand()
            print(lang.get_phrase(2), end='')
            player2.show_hand()
            print()

            # Facilitate the respective player's
            # turn and check if they have a bust
            if turn == 'Player 1':
                logic.player(turn, player1)
                player1.bust()
            else:
                logic.player(turn, player2)
                player2.bust()

            # Change turns
            if turn == 'Player 1' and not player2Stay:
                turn = 'Player 2'
            elif turn == 'Player 2' and not player1Stay:
                turn = 'Player 1'

        if not playerBust:
            # If both players have stayed, check the outcome to finish the game
            logic.check_outcome()


    # Global variables
    deck = Deck()
    player1Stay = False
    player2Stay = False
    playerBust = False
    turn = 'Player 1'
    player1 = Player()
    player2 = Player()
    Language = "en"  # input("enter en for english or cz for czech ")
    lang = None

    blackjack()
