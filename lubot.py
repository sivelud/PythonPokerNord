import random
import copy
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

class botPlayer():
    def __init__(self):
        self.cards = []


ROYAL_FLUSH_VALUE =     900000014
STRAIGHT_FLUSH_VALUE =  900000000
FOUR_OF_A_KIND_VALUE =  800000000
FULL_HOUSE_VALUE =      700000000
FLUSH_VALUE =           600000000
STRAIGHT_VALUE =        500000000
THREE_OF_A_KIND_VALUE = 400000000
TWO_PAIR_VALUE =        300000000
PAIR_VALUE =            200000000

def assign_value_to_hand(hand, table_cards):
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
            # print(handValue)
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




def yourBot(gameState, yourPlayersIndex, yourHand):
    # print("\n\nåååååååååå--LUBOT--åååååååååå\n\n")
    move: str = "call"
    amount: int = 0

    # WRITE YOUR CODE HERE

    deck = Deck()

    wins = 0


    handCards = yourHand
    # n_players = len(gameState["players"])
    n_players = 0
    for player in gameState["players"]:
        if player["hasFolded"] == False:
            n_players += 1

    sim_players = []
    for i in range(0, n_players):
            bot_player = botPlayer()
            sim_players.append(bot_player)


    num_simulations = 10
    for i in range (0, num_simulations):
        deck.shuffle_and_reset()
        tablecards = gameState["table_cards"]
        


        # Fjerner hånden fra kortstokken
        for card in handCards:
            deck.deck.remove(card)

        # Fjerner bordkortene fra kortstokken
        for card in tablecards:
            if card != None:
                deck.deck.remove(card)

        for i in range(0,5):
            if tablecards[i] == None:
                tablecards[i] = deck.draw_card()

        # Lager sim av fiende spillere
        for i in range(len(sim_players)):
            sim_players[i].cards = [deck.draw_card(), deck.draw_card()]

        your_hand_val, yourType = assign_value_to_hand(handCards, tablecards)
        print("Your hand: ", handCards, "(" + yourType + ")")
        print()

        print("Table cards: ", tablecards)
        did_win = True
        for player in sim_players:
            hand_val, type = assign_value_to_hand(player.cards, tablecards)
            print("Their hand: ", player.cards, "(" + type + ")")
            # print("Their hand value: ", hand_val)
            # print("Your hand value: ", your_hand_val)
            if hand_val > your_hand_val:
                did_win = False
        if did_win:
            print("WINNER")
            wins += 1
    
    print("Won: ", wins, " out of ", num_simulations)

    
    check_ammount = 100
    # call_amount = 300
    raise_amount = 500
    allin_amount = 700

    # scew = 2

    # # skew the ammounts
    # check_ammount = int(check_ammount * scew)
    # call_amount = int(call_amount * scew)
    # raise_amount = int(raise_amount * scew)
    # allin_amount = int(allin_amount * scew)

    if wins > allin_amount:
        move = "allin"
        amount = 0
    elif wins > raise_amount:
        move = "raise"
        amount = 300
    # elif wins > call_amount:
    #     move = "call"
    #     amount = 0
    else:
        move = "check"
        amount = 0
    

                
                
            

    print("Wins: ", wins)

    # print hand
    # print("Hand: ", handCards)

    print("\n--------------------------------------------------åååååååååååååååååååååååååååå\n\n")
            

        

        


    


    return move, amount
    