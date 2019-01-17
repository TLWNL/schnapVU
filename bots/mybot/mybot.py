"""
RandomBot -- A simple strategy: enumerates all legal moves, and picks one
uniformly at random.
"""

# Import the API objects
from api import State
from api import Deck
from api import util
import random


class Bot:

    def __init__(self):
        pass

    def get_move(self, state):
        # type: (State) -> tuple[int, int]
        """
        Function that gets called every turn. This is where to implement the strategies.
        Be sure to make a legal move. Illegal moves, like giving an index of a card you
        don't own or proposing an illegal mariage, will lose you the game.
       	TODO: add some more explanation
        :param State state: An object representing the gamestate. This includes a link to
            the states of all the cards, the trick and the points.
        :return: A tuple of integers or a tuple of an integer and None,
            indicating a move; the first indicates the card played in the trick, the second a
            potential spouse.
        """

        # All legal moves
        moves = state.moves()
        moves_str = state.moves()
        for index, move in enumerate(moves_str):
            moves_str[index] = util.get_card_name(moves_str[index][0])
        print(moves_str)

        # Current hand
        curr_hand = state.hand()

        # Moves of the same suit
        moves_same_suit = []

        # All trump moves in hand
        moves_trump_suit = []

        # Moves of different suits
        moves_diff_suit = []

        # Current player
        me = state.whose_turn()

        # Get all trump suit moves available
        for index, move in enumerate(moves):

            if move[0] is not None and Deck.get_suit(move[0]) == state.get_trump_suit():
                moves_trump_suit.append(move)

        # Show any marriage in your hand
        possible_mariages = moves.Deck.get_possible_mariages(me)
        if possible_mariages is not None and state.get_opponents_played_card() is not None:
            return possible_mariages[0]


        # Opponent is on lead
        if state.get_opponents_played_card() is not None:

            # Stock is open
            if state.get_stock_size() != 0:

                # If possible win a non trump trick by following suit without breaking up a marriage
                opponent_played = state.get_opponents_played_card()
                opponent_played_suit = Deck.get_suit(opponent_played)

                if opponent_played_suit != state.get_trump_suit():
                    # enumerate though list for all moves of same suit as opponents move
                    # (taken from bully.py)
                    for index, move in enumerate(moves):
                        if move[0] is not None and Deck.get_suit(move[0]) == Deck.get_suit(
                                state.get_opponents_played_card()):
                            moves_same_suit.append(move)

                    # Sort the indices for ease (may not be necessary)
                    moves_same_suit.sort()

                    # If you can win the hand, win it with the highest card possible
                    if moves_same_suit[0] > state.get_opponents_played_card() and len(moves_same_suit) is not None:
                        return moves_same_suit[0]

                    # If you cannot win the hand by matching suit, trump with your lowest if opponent leads with ace/10
                    # elif statement can be simplified by using modulo!
                    elif state.get_opponents_played_card() == 0 or 5 or 10 or 15 or 2 or 6 or 11 or 16:
                        return moves_trump_suit[len(moves_trump_suit) -1]

                # Opponent played trump suit
                else:
                    # Get possible moves, not including trump cards
                    for index, move in enumerate(moves):
                        if move[0] is not None and Deck.get_suit(move[0]) != Deck.get_suit(
                                state.get_opponents_played_card()):
                            moves_diff_suit.append(move)

                    # Sort the indices for ease
                    moves_same_suit.sort()

                    for i in range(len(moves_diff_suit)):
                        # Discard a jack for some non trump suit
                        if moves_diff_suit[i] == 4 or 9 or 14 or 19:
                            return moves_diff_suit[i]

                    # for now just discard your lowest card of another suit
                    return moves_diff_suit[len(moves_diff_suit)-1]
        # You are on lead -- TO_DO
        else:
            # DON'T LEAD WITH A TRUMP!
            # IF ITS THE FIRST TURN, PLAY A ACE OR 10 OF NON-TRUMP!

            # Use your jack to exchange the trump on the table
            if curr_hand.deck.can_exchange(me) is True:
                # Find the trump jack in the hand
                jack_index = curr_hand.deck.get_trump_jack_index()
                curr_hand.deck.exchange_trump(jack_index)

            # If it is the first turn, play ace or 10 of non-trump if possible
            if state.get_stock_size() == 10:
                for i in range(0,5):
                    if moves[i] == 0 or 5 or 10 or 2 or 6 or 11 or 16 and Deck.get_suit(moves[i]) != curr_hand.get_trump_suit():
                        return moves[i]

            # Change this!
            return moves[0]


        """
        When the opponent is on lead and the stock is open: - BASICALLY DONE
            If you can, always win a nontrump trick by following suit (dont break up marriage tho) Y - DO THE MARRIAGE TING DO
            If possible, win by ten or ace of that suit. Always pick the higher card if you have adjacent cards to win a trick Y
            Adjacent = the intervening cards have already been played. 
            If opponent leads a nontrump ace or ten, trump that shit. Y 
            If opponents leads a trump or card you dont want, discard a jack for some nontrump suit, or a queen or king if you have already seen its marriage partner
            Try to retain a second card as protection in the suit where you hold a ten (king prefered). - TODO
        
        When you are on lead and the stock is open - STILL NEEDS A LOT OF WORK
            Dont lead with a trump, opponent doesnt have to follow suit. 
            Lead with nontrump jack, or a queen or king where you've already seen its marriage partner played. 
            Choose lower of the adjacent cards to play.
        
        Marriages and trump exchange
            Use your jack to exchange the trump on the table and/or show any marriage in your hand at the earliest possible opportunity
            ! If you can play a def winning card, and then a marriage; bringing your total to > 66, do that instead of marriage
            ! Stock closed, and you are on lead holding a marriage and top trumps, if your opponent neither holds the ace nor ten, pull
                the opponents trumps before showing the marriage.
        
        When the stock is no longer open
            If one player has control over the remaining trump suit, that player should play just enough to pull opponents trumps.
            After trumps are pulled, play highest nontrump cards/
            If opponent still has trumps you cannot pull, force it by leading a card (low) that she no longer holds.
        """

