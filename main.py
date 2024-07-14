import copy
import random
import matplotlib.pyplot as plt

NUMBER_OF_ROUNDS = 1
STACK = 1000

SMALL_BLIND = 10
BIG_BLIND = 20

from exampleBots import raiseBot
from exampleBots import manualBot
from exampleBots import checkBot
from exampleBots import callBot
from exampleBots import foldBot
from exampleBots import allinBot
from lubot import yourBot as lubot
from stupid import yourBot as stupid
PLAYERS_manual = [
    {
        "name": "manualBot",
        "bot": manualBot,
        "stack": STACK *10
    },
    # {
    #     "name": "raiseBot",
    #     "bot": raiseBot,
    #     "stack": STACK
    # },
    {
        "name": "callBot",
        "bot": callBot,
        "stack": STACK
    },
    {
        "name": "callBot2",
        "bot": callBot,
        "stack": STACK
    },
    # {
    #     "name": "checkBot",
    #     "bot": checkBot,
    #     "stack": STACK
    # },
    # {
    #     "name": "foldBot",
    #     "bot": foldBot,
    #     "stack": STACK
    # },
    # {
    #     "name": "allinBot",
    #     "bot": allinBot,
    #     "stack": STACK
    # },
    # {
    #     "name": "allin2",
    #     "bot": allinBot,
    #     "stack": STACK
    # }
]

PLAYERS_auto =     [
    {
        "name": "raiseBot",
        "bot": raiseBot,
        "stack": STACK
    },
    {
        "name": "checkBot",
        "bot": checkBot,
        "stack": STACK
    },
    {
        "name": "callBot",
        "bot": callBot,
        "stack": STACK
    },
    {
        "name": "foldBot",
        "bot": foldBot,
        "stack": STACK
    },
    # {
    #     "name": "allinBot",
    #     "bot": allinBot,
    #     "stack": STACK
    # },
    {
        "name": "lubot",
        "bot": lubot,
        "stack": STACK
    },
    {
        "name": "callBot2",
        "bot": callBot,
        "stack": STACK
    },
    {
        "name": "stupid",
        "bot": stupid,
        "stack": STACK
    },
    #manual
    # {
    #     "name": "manualBot",
    #     "bot": manualBot,
    #     "stack": STACK
    # },

    ]

PLAYERS = PLAYERS_auto

def test_total_money(players, total, id):
    total_money = 0
    for player in players:
        total_money += player.stack
        total_money += player.bet
    assert total_money == total, "\n\nTotal money (" + str(total_money) + ") is not the same as the total stack (" + str(total)+") of the players. id:(" + str(id) + ")"


# def test_scenario_split_pot():
#     game = GameEngine()
#     game.players = []

    
#     assert False, "\n\nSplit pot scenario not implemented"


class Deck():
    def __init__(self):
        self.original_deck = ["2♠", "3♠", "4♠", "5♠", "6♠", "7♠", "8♠", "9♠", "T♠", "J♠", "Q♠", "K♠", "A♠",
                    "2♥", "3♥", "4♥", "5♥", "6♥", "7♥", "8♥", "9♥", "T♥", "J♥", "Q♥", "K♥", "A♥",
                    "2♦", "3♦", "4♦", "5♦", "6♦", "7♦", "8♦", "9♦", "T♦", "J♦", "Q♦", "K♦", "A♦",
                    "2♣", "3♣", "4♣", "5♣", "6♣", "7♣", "8♣", "9♣", "T♣", "J♣", "Q♣", "K♣", "A♣"]
        self.deck = copy.deepcopy(self.original_deck)
        self.shuffle_and_reset()
    
    def shuffle_and_reset(self):
        self.deck = copy.deepcopy(self.original_deck)
        random.shuffle(self.deck)
        
    def draw_card(self):
        assert len(self.deck) > 0, "\n\nDeck is empty, cannot draw card"
        return self.deck.pop(0)


ROYAL_FLUSH_VALUE =     900000014
STRAIGHT_FLUSH_VALUE =  900000000
FOUR_OF_A_KIND_VALUE =  800000000
FULL_HOUSE_VALUE =      700000000
FLUSH_VALUE =           600000000
STRAIGHT_VALUE =        500000000
THREE_OF_A_KIND_VALUE = 400000000
TWO_PAIR_VALUE =        300000000
PAIR_VALUE =            200000000
    


class GameEngine():
    def __init__(self):
        self.players = []
        self.initPlayers()
        self.init_total_stack()
        print("Total pot: ", self.total_pot)
        self.deck = Deck()
        self.table_cards = [None, None, None, None, None]
        self.dealer = random.randint(0, len(self.players) - 1)
        self.small_blind_amount = SMALL_BLIND
        self.big_blind_amount = BIG_BLIND
        self.rotate_dealer_and_blinds()
        self.min_raise = 1
        self.max_raise = None

    def init_total_stack(self):
        total = 0
        for player in self.players:
            total += player.stack
        self.total_pot = total
        
        
    
    def initPlayers(self):
        for player in PLAYERS:
            self.players.append(Player(player["name"], player["bot"], player["stack"]))
    
    def generate_gamestate(self):
        return {
            "players": [player.playerState() for player in self.players],
            "table_cards": self.table_cards,
            "dealer": self.dealer,
            "small_blind_player": self.small_blind_player,
            "big_blind_player": self.big_blind_player,
            "small_blind_amount": self.small_blind_amount,
            "big_blind_amount": self.big_blind_amount,
            "min_raise": self.min_raise,
            "max_raise": self.max_raise,
        }
    
    def print_gamestate(self):
        pot = 0
        for player in self.players:
            pot += player.bet

        print("\n---------------------------------------------------------------")
        print(f"{'PlayerName':<15}{'Bet':<10}{'Stack':<10}{'HasFolded':<15}{'IsAllIn':<10}")
        for player in self.players:
            print(f"{player.name:<15}{player.bet:<10}{player.stack:<10}{str(player.hasFolded):<15}{str(player.isAllIn):<10}")
        print("\nTotal pot:", str(pot),"")
        print("---------------------------------------------------------------\n")

    def print_table_cards(self):
        print("\nTable:", self.table_cards, "\n")
    
    def deal_cards(self):
        self.deck.shuffle_and_reset()
        for player in self.players:
            player.hand = [self.deck.draw_card(), self.deck.draw_card()]
        self.table_cards = [None, None, None, None, None]

    def player_play(self, player):
        print()
        move, amount = player.play(self.generate_gamestate(), self.players.index(player))
        if move == "raise":
            print("Player", player.name, " has played:", move, amount)
        else:
            print("Player", player.name, " has played:", move)

        print()
        return move
    
    def reset_bet_fold_and_allin(self):
        for player in self.players:
            player.bet = 0
            player.hasFolded = False
            player.isAllIn = False

            assert player.stack > 0, "\n\nPlayer stack is 0 or less, player: " + player.name + " stack: " + str(player.stack)

    def rotate_dealer_and_blinds(self):
        if len(self.players) > 2:
            self.dealer = (self.dealer + 1) % len(self.players)
            self.small_blind_player = (self.dealer + 1) % len(self.players)
            self.big_blind_player = (self.small_blind_player + 1) % len(self.players)
            
        else:
            self.dealer = (self.dealer + 1) % len(self.players)
            self.small_blind_player = (self.dealer) % len(self.players)
            self.big_blind_player = (self.small_blind_player + 1) % len(self.players)
        

    # skal:
    # - dele ut kort
    # - betale blinds
    # - prompt player for move
    # - legge ut kort på bordet
    def play_round(self):
        print("\n-----Starting new round-----\n")
        self.deal_cards()
        self.reset_bet_fold_and_allin()
        self.rotate_dealer_and_blinds()

        # Small blind
        self.players[self.small_blind_player].payBlind(self.small_blind_amount)
        # Big blind
        self.players[self.big_blind_player].payBlind(self.big_blind_amount)
        # playing_player = dealer index + 1 modulo number of players

        playing_player = (self.big_blind_player + 1) % len(self.players)

        has_matched_n = -1
        previous_highest_bet = 0
        while True:

            next_bid_round = False
            # Check if all except one player has folded
            n_folded = 0
            for player in self.players:
                if player.hasFolded:
                    n_folded += 1
            if n_folded == len(self.players) - 1:
                self.score_winner()
                return

            # Find highest bet
            highest_bet = 0
            for player in self.players:
                if player.bet > highest_bet:
                    highest_bet = player.bet

            # Check if all players have matched the highest bet, or if it has increased
            if highest_bet > previous_highest_bet:
                previous_highest_bet = highest_bet
                has_matched_n = 0


            # Sees if all the players have matched the highest bet
            if previous_highest_bet == highest_bet and has_matched_n == len(self.players):
                print("All players have matched the highest bet")
                next_bid_round = True
                has_matched_n = 0
           
            has_matched_n += 1

            self.print_gamestate()

            

            if not next_bid_round:
                if self.players[playing_player].hasFolded:
                    print("Player", self.players[playing_player].name, "has already folded")
                    playing_player = (playing_player + 1) % len(self.players)
                
                elif self.players[playing_player].isAllIn:
                    print("Player", self.players[playing_player].name, "is already all in")
                    playing_player = (playing_player + 1) % len(self.players)
                
                # elif self.players[playing_player].bet == highest_bet:
                #     if highest_bet == self.big_blind_amount:
                #         self.player_play(self.players[playing_player])
                #         playing_player = (playing_player + 1) % len(self.players)
                #     else:
                #         print("Player", self.players[playing_player].name, "has already matched the highest bet")
                #         playing_player = (playing_player + 1) % len(self.players)
                    
                else:
                    self.print_table_cards()
                    if self.players[playing_player].name == "manualBot":
                        self.players[playing_player].print_hand()
                    self.player_play(self.players[playing_player])
                    playing_player = (playing_player + 1) % len(self.players)

            else:
                print("\n- Next bid round -\n")
                # Deal next cards:
                if self.table_cards[0] is None:
                    self.table_cards[0] = self.deck.draw_card()
                    self.table_cards[1] = self.deck.draw_card()
                    self.table_cards[2] = self.deck.draw_card()
                elif self.table_cards[3] is None:
                    self.table_cards[3] = self.deck.draw_card()
                elif self.table_cards[4] is None:
                    self.table_cards[4] = self.deck.draw_card()
                    
                elif self.table_cards[4] is not None:
                    self.score_winner()
                    return
                else:
                    assert False, "\n\nError in next_bid_round. (no condition met)"
                playing_player = (self.dealer + 1) % len(self.players)
                has_matched_n = 0

        assert False, "\n\nError in play_round (reached end)"

    
    def stack_graph(self):
        # use matplotlib to plot the stack of the players
    #     sums = list(range(2, 13))  # Possible sums from 2 to 12
    # plt.bar(sums, counts, tick_label=sums)
    # plt.xlabel('Sum of Two Dice')
    # plt.ylabel('Count')
    # plt.title('Two Dice Roll Simulation')
    # plt.show()

        players = self.players
        names = []
        stacks = []
        for player in players:
            names.append(player.name)
            stacks.append(player.stack)
        # plt.bar(sums, counts, tick_label=sums)
        plt.bar(names, stacks)
        plt.xlabel('Player')
        plt.ylabel('Stack')
        plt.title('Stack of players')
        plt.show()
        return
    






    def score_winner(self):

        for i in range(5):
            if self.table_cards[i] is None:
                self.table_cards[i] = self.deck.draw_card()
        test_total_money(self.players, self.total_pot, 1)

        self.print_table_cards()


        for player in self.players:
            player.print_hand()



        pot = 0
        for player in self.players:
            pot += player.bet

        candidates = []
        for player in self.players:
            if not player.hasFolded:
                player.can_win_ammount = player.bet * len(self.players)
                score, move = self.assign_value_to_hand(player.hand, self.table_cards)
                player.win_type = move
                player.handScore = score
                candidates.append(player)
        assert len(candidates) > 0, "\n\nERROR No candidates for winner"

        while pot > 0:

            # Find the winners
            winner = candidates[0]
            highest_hand = 0
            for player in candidates:
                score = player.handScore
                if score > highest_hand:
                    winner = player
                    highest_hand = score
            if pot > winner.can_win_ammount:
                winner.stack += winner.can_win_ammount
                pot -= winner.can_win_ammount
            else:
                winner.stack += pot
                pot = 0
            print("Winner: ", winner.name, ":", winner.hand, " (", winner.win_type, ")" )
            candidates.remove(winner)
            if len(candidates) <= 0:
                winner.stack += pot
                pot = 0

            
            
                

                

            

            

            
            
            


        # Reset the bet of players
        for player in self.players:
            player.bet = 0            

        self.print_gamestate()
        test_total_money(self.players, self.total_pot, 2)
        return

























        
        # # More than 1 winner
        # if number_of_winners > 1:

        #     # find all the winners
        #     winners = []
        #     for player in candidates:
        #         score, hand_type = self.assign_value_to_hand(player.hand, self.table_cards)
        #         if score == highest_hand:
        #             winners.append(player)
        #     for winner_p in winners:
        #         print("Winner:", winner_p.name, ":", winner_p.hand)

        #     # Sort the players based on how close after the dealer they are
        #     winners.sort(key=lambda x: (self.players.index(x) - self.dealer) % len(self.players))

        #     pot = 0
        #     for player in self.players:
        #         pot += player.bet
        #         player.bet = player.bet*2
        #         # player.bet = 0
            
        #     lastpot = -1
        #     infinateloop = 0
        #     while pot > 0:
        #         if pot == lastpot:
        #             infinateloop += 1
        #             if infinateloop > 5:
        #                 assert False, "\n\nInfinateloop in pot split"
        #         else:
        #             infinateloop = 0
        #         lastpot = pot
                
        #         print("Pot: ", pot)
        #         # print winners
        #         for winnerr in winners:
        #             if winnerr.bet > 0:
        #                 winnerr.stack += 1
        #                 winnerr.bet -= 1
        #                 pot -= 1
        #                 # print("giving 1 pot to: ", winnerr.name, ". he now has ", winnerr.stack)
        #             else:
        #                 print("removing winner: ", winnerr.name)
        #                 print("Their bet was not high enough to win any more of the pot")
        #                 print("They now have: ", winnerr.stack)

        #                 winners.remove(winnerr)

                




        # # 1 winner
        # else:
            
        #     pot = 0
        #     winner_bet = winner.bet
        #     for player in self.players:
        #         if player.bet > winner_bet:
        #             pot += winner_bet
        #             player.bet -= winner_bet
        #             player.stack += player.bet
        #             player.bet = 0
        #         else:
        #             pot += player.bet
        #             player.bet = 0
        
        #     print("Winner: ", winner.name)
        #     print("wins the pot: ", pot)
        #     winner.stack += pot
        

        # # assert False, "Split implementation not finished"


 
    
    def assign_value_to_hand(self, hand, table_cards):
        highest_hand = 0
        highest_hand_type = "High card"

        tmp_cards = hand + table_cards
        # print (tmp_cards)
        # print()

        cards = []

        for card in tmp_cards:
            tmp_card_val = card[0]
            if tmp_card_val == "T":
                tmp_card_val = "10"
            elif tmp_card_val == "J":
                tmp_card_val = "11"
            elif tmp_card_val == "Q":
                tmp_card_val = "12"
            elif tmp_card_val == "K":
                tmp_card_val = "13"
            elif tmp_card_val == "A":
                tmp_card_val = "14"
            else:
                tmp_card_val = "0" + str(tmp_card_val)
            
            cards.append(tmp_card_val + card[-1])
        
        cards.sort(key=lambda x: int(x[:-1]))           
        
        #Look for flush
        suits = {}
        for card in cards:
            if card[-1] in suits:
                suits[card[-1]] += 1
            else:
                suits[card[-1]] = 1
        most_common_suit = max(suits, key=suits.get)
        most_common_suit_n = suits[most_common_suit]

        if most_common_suit_n >= 5:

            straight_flush = []
            for card in cards:
                if card[-1] == most_common_suit:
                    # if straight_flush[len(straight_flush)     see if the card is one higher than the last card
                    if len(straight_flush) > 0:
                        if int(card[:-1]) == int(straight_flush[-1][:-1]) + 1:
                            straight_flush.append(card)
                        else:
                            straight_flush = [card]
                    else:
                        straight_flush.append(card)
            if len(straight_flush) >= 5:

                handValue = STRAIGHT_FLUSH_VALUE + int(straight_flush[-1][:-1])

    # ROYAL STRAIGHT FLUSH ---------------------------
                if handValue == ROYAL_FLUSH_VALUE:
                    # print("Royal straight flush")
                    # print(straight_flush)
                    if handValue > highest_hand:
                        highest_hand_type = "Royal straight flush"
                        highest_hand = handValue
                
                else:
    # STRAIGHT FLUSH ---------------------------
                    # print("Straight flush")
                    # print(straight_flush)
                    if handValue > highest_hand:
                        highest_hand_type = "Straight flush"
                        highest_hand = handValue

    # FLUSH ---------------------------
            # print("Flush")
            # print(most_common_suit)
            # handValue = FLUSH_VALUE + all the 5 highest cards in hand
            handValue = FLUSH_VALUE
            # all the 5 highest cards in hand, that are of the same suit, gets added to hand value
            multiplier = 10000
            for card in reversed(cards):
                if card[-1] == most_common_suit:
                    handValue += int(card[:-1])*multiplier
                    multiplier = int(multiplier / 10)
                    if multiplier == 0:
                        break
            print(handValue)
            if handValue > highest_hand:
                highest_hand_type = "Flush"
                highest_hand = handValue

    # FOUR OF A KIND ---------------------------
        values = {}
        for card in cards:
            if card[:-1] in values:
                values[card[:-1]] += 1
            else:
                values[card[:-1]] = 1
        most_common_value = max(values, key=values.get)
        most_common_value_n = values[most_common_value]
        if most_common_value_n == 4:
            # print("Four of a kind")
            # print(most_common_value)
            highest_card = 0
            for card in cards:
                if card[:-1] != most_common_value:
                    if int(card[:-1]) > highest_card:
                        highest_card = int(card[:-1])
            # print("Highest card: ", highest_card)
            handValue = FOUR_OF_A_KIND_VALUE + int(most_common_value)*100 + highest_card
            if handValue > highest_hand:
                highest_hand_type = "Four of a kind"
                highest_hand = handValue

        if most_common_value_n == 3:
    # FULL HOUSE ---------------------------
            for card in cards:
                if card[:-1] != most_common_value:
                    if values[card[:-1]] == 2:
                        # print("Full house")
                        # print(most_common_value, card[:-1])
                        handValue = FULL_HOUSE_VALUE + int(most_common_value)*100 + int(card[:-1])
                        if handValue > highest_hand:
                            highest_hand_type = "Full house"
                            highest_hand = handValue
                    
    # THREE OF A KIND ---------------------------
            highest_card = 0
            seccound_highest_card = 0

            for card in cards:
                if card[:-1] != most_common_value:
                    if int(card[:-1]) > highest_card:
                        seccound_highest_card = highest_card
                        highest_card = int(card[:-1])
                    elif int(card[:-1]) > seccound_highest_card:
                        seccound_highest_card = int(card[:-1])
            
            # print("Three of a kind")
            # print(most_common_value)
            handValue = THREE_OF_A_KIND_VALUE + int(most_common_value)*100 + highest_card*10 + seccound_highest_card
            if handValue > highest_hand:
                highest_hand_type = "Three of a kind"
                highest_hand = handValue
    
    # TWO PAIR ---------------------------
        if most_common_value_n == 2:
            seccound_most_common_value = 0
            for card in cards:
                if card[:-1] != most_common_value:
                    if values[card[:-1]] == 2:
                        seccound_most_common_value = card[:-1]
                        break
            highest_card = 0
            for card in cards:
                if card[:-1] != most_common_value and card[:-1] != seccound_most_common_value:
                    if int(card[:-1]) > highest_card:
                        highest_card = int(card[:-1])
            if seccound_most_common_value != 0:

                # print("Two pair")
                # print(most_common_value, seccound_most_common_value)
                handValue = TWO_PAIR_VALUE + int(most_common_value)*100 + int(seccound_most_common_value)*100 + highest_card
                if handValue > highest_hand:
                    highest_hand_type = "Two pair"
                    highest_hand = handValue
            else:
    # PAIR ---------------------------
                # print("Pair")
                # print(most_common_value)
                handValue = PAIR_VALUE + int(most_common_value)*10000 + highest_card

                multiplier = 1000
                for card in reversed(cards):
                    if card[:-1] != most_common_value:
                        handValue += int(card[:-1])*multiplier
                        multiplier = int(multiplier / 10)
                        if multiplier == 0:
                            break

                if handValue > highest_hand:
                    highest_hand_type = "Pair"
                    highest_hand = handValue
            


    # STRAIGHT ---------------------------
        straight = []
        for card in cards:
            if len(straight) > 0:
                if int(card[:-1]) == int(straight[-1][:-1]) + 1:
                    straight.append(card)
                else:
                    straight = [card]
            else:
                straight.append(card)
        if len(straight) >= 5:
            # print("Straight")
            # print(straight)
            handValue = STRAIGHT_VALUE + int(straight[-1][:-1])
            if handValue > highest_hand:
                highest_hand_type = "Straight"
                highest_hand = handValue


    # HIGH CARD ---------------------------
        handValue = 0
        multiplier = 10000
        for card in reversed(cards):
            handValue += int(card[:-1])*multiplier
            multiplier = int(multiplier / 10)
            if multiplier == 0:
                break
        if handValue > highest_hand:
            highest_hand = handValue
        
        # print(highest_hand_type)
        # print("-----------------")
        return highest_hand, highest_hand_type


    def run_sim(self):
        for i in range(NUMBER_OF_ROUNDS):
            self.play_round()
            if i % 10 == 0:
                self.big_blind_amount = self.big_blind_amount *2
                self.small_blind_amount = self.small_blind_amount *2

            # self.stack_graph()
            
            self.print_gamestate()
            
            test_total_money(self.players, self.total_pot, 3)
    
            n = 0
            while n < len(self.players):
                if self.players[n].stack == 0:
                    print("Player ", self.players[n].name, " is out of money, and leaves the table")
                    self.players.remove(self.players[n])
                else:
                    n += 1

            test_total_money(self.players, self.total_pot, 4)

            self.rotate_dealer_and_blinds()
 
            if len(self.players) == 1:
                print("\n------------------------------------------\n     WINNER:\n    ", self.players[0].name)
                print("\n    Stack: ", self.players[0].stack,)
                print("------------------------------------------")
                
                return
                    
        



class Player():
    def __init__(self, name, botFunction, stack):
        self.name = name
        print("Player:", name, "joined the game")
        assert len(name) > 0 and len(name) <= 12, "\n\nPlayer name must be between 1 and 12 characters long"
        self.botFunction = botFunction
        self.hand = [None, None]
        self.stack = stack
        self.bet = 0
        self.hasFolded = False
        self.isAllIn = False
        self.hasPlayedThisCheckRound = False

    #replace print
    def __str__(self):
        return self.name
    
    def playerState(self):
        return {
            "name": self.name,
            "stack": self.stack,
            "bet": self.bet,
            "hasFolded": self.hasFolded
        }
    
    def print_hand(self):
        print("\n"+ str(self.name), "hand:", self.hand, "\n")
    
    def payBlind(self, amount):
        if amount >= self.stack:
            print("Blind amount is more than or equal to stack. Going allin for player:", self.name)
            self.bet += self.stack
            self.stack = 0
            self.isAllIn = True
        else:
            self.stack -= amount
            self.bet += amount
        

    def play(self, gameState, yourPlayersIndex):
        hand = copy.deepcopy(self.hand)
        state = copy.deepcopy(gameState)
        index = copy.deepcopy(yourPlayersIndex)
        try:
            move, amount = self.botFunction(state, index, hand)
        except Exception as e:
            print("CRASHED BOT: ", self.name)
            move = "fold"
            amount = 0

        # Output validation
        possible_moves = ["fold", "check", "call", "raise", "allin"]

        if move not in possible_moves:
            print("BOT ERROR in possible moves, for player: ", self.name)
            self.hasFolded = True
            return "fold", 0

        # FOLD
        if move == "fold":
            self.hasFolded = True
            return "fold", 0
        
        # CHECK
        if move == "check":
            # see if the player can check
            highest_bet = 0
            for player in state["players"]:
                if player["bet"] > highest_bet:
                    highest_bet = player["bet"]
            if highest_bet > self.bet:
                print("BOT ERROR, check when there is a higher bet, player:", self.name)
                self.hasFolded = True
                return "fold", 0
            return "check", 0
        
        # RAISE
        if move == "raise":
            if amount is None:
                print("BOT ERROR, raise amount is None, player:", self.name)
                self.hasFolded = True
                return "fold", 0
            else:
                amount = int(amount)
            
            if amount < state["min_raise"]:
                if amount == self.stack:
                    print("Not enough money in stack for thee raise, goes all in, player:", self.name)
                    self.bet += self.stack
                    self.stack = 0
                    self.isAllIn = True
                    return "allin", 0
                else:
                    print("BOT ERROR, raise amount is less than min_raise, player:", self.name)
                    self.hasFolded = True
                    return "fold", 0
            if state["max_raise"] is not None:
                if amount > state["max_raise"]:
                    print("BOT ERROR, raise amount is more than max_raise, player:", self.name)
                    self.hasFolded = True
                    return "fold", 0
            if amount > self.stack:
                print("Raise amount is more than stack, player:", self.name, "goes all in")
                self.bet += self.stack
                self.stack = 0
                self.isAllIn = True
                return "allin", 0
            
            # see if the raise is as much or more than largest bet
            highest_bet = 0
            for player in state["players"]:
                if player["bet"] > highest_bet:
                    highest_bet = player["bet"]
            if amount < highest_bet:
                print("Raise amount is less than highest bet. Folding. player:", self.name)
                self.hasFolded = True
                return "fold", 0
            
            
            self.stack -= amount
            self.bet += amount
            return "raise", amount
        
        # CALL
        if move == "call":
            # find call ammount by looking at the highest bet
            highest_bet = 0
            for player in state["players"]:
                if player["bet"] > highest_bet:
                    highest_bet = player["bet"]
            call_amount = highest_bet - self.bet
            if call_amount >= self.stack:
                print("Call amount is more than stack, going all in. player:", self.name)
                self.bet += self.stack
                self.stack = 0
                self.isAllIn = True
                return "allin", 0
            else:
                self.stack -= call_amount
                self.bet += call_amount
                return "call", call_amount
            
        # ALLIN
        if move == "allin":
            if self.stack == 0:
                # print("BOT ERROR, allin with no stack, player:", self.name)
                self.isAllIn = True
                return "allin", 0
            self.bet += self.stack
            self.stack = 0
            self.isAllIn = True
            return "allin", 0
        
        print("CODE_ERROR, reached end: ", self.name)
        self.hasFolded = True
        return "fold", 0



if __name__ == '__main__':
    game = GameEngine()
    game.run_sim()