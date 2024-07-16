import random
import copy

# Constants for hand evaluation
ROYAL_FLUSH_VALUE = 900000014
STRAIGHT_FLUSH_VALUE = 900000000
FOUR_OF_A_KIND_VALUE = 800000000
FULL_HOUSE_VALUE = 700000000
FLUSH_VALUE = 600000000
STRAIGHT_VALUE = 500000000
THREE_OF_A_KIND_VALUE = 400000000
TWO_PAIR_VALUE = 300000000
PAIR_VALUE = 200000000

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

def assign_value_to_hand(hand, table_cards):
    highest_hand = 0
    highest_hand_type = "High card"
    tmp_cards = hand + table_cards
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
    
    # Look for flush
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
                if len(straight_flush) > 0:
                    if int(card[:-1]) == int(straight_flush[-1][:-1]) + 1:
                        straight_flush.append(card)
                    else:
                        straight_flush = [card]
                else:
                    straight_flush.append(card)
        if len(straight_flush) >= 5:
            handValue = STRAIGHT_FLUSH_VALUE + int(straight_flush[-1][:-1])
            if handValue == ROYAL_FLUSH_VALUE:
                if handValue > highest_hand:
                    highest_hand_type = "Royal straight flush"
                    highest_hand = handValue
            else:
                if handValue > highest_hand:
                    highest_hand_type = "Straight flush"
                    highest_hand = handValue

        handValue = FLUSH_VALUE
        multiplier = 10000
        for card in reversed(cards):
            if card[-1] == most_common_suit:
                handValue += int(card[:-1])*multiplier
                multiplier = int(multiplier / 10)
                if multiplier == 0:
                    break
        if handValue > highest_hand:
            highest_hand_type = "Flush"
            highest_hand = handValue

    values = {}
    for card in cards:
        if card[:-1] in values:
            values[card[:-1]] += 1
        else:
            values[card[:-1]] = 1
    most_common_value = max(values, key=values.get)
    most_common_value_n = values[most_common_value]
    if most_common_value_n == 4:
        highest_card = 0
        for card in cards:
            if card[:-1] != most_common_value:
                if int(card[:-1]) > highest_card:
                    highest_card = int(card[:-1])
        handValue = FOUR_OF_A_KIND_VALUE + int(most_common_value)*100 + highest_card
        if handValue > highest_hand:
            highest_hand_type = "Four of a kind"
            highest_hand = handValue

    if most_common_value_n == 3:
        for card in cards:
            if card[:-1] != most_common_value:
                if values[card[:-1]] == 2:
                    handValue = FULL_HOUSE_VALUE + int(most_common_value)*100 + int(card[:-1])
                    if handValue > highest_hand:
                        highest_hand_type = "Full house"
                        highest_hand = handValue
                    
        highest_card = 0
        second_highest_card = 0
        for card in cards:
            if card[:-1] != most_common_value:
                if int(card[:-1]) > highest_card:
                    second_highest_card = highest_card
                    highest_card = int(card[:-1])
                elif int(card[:-1]) > second_highest_card:
                    second_highest_card = int(card[:-1])
        
        handValue = THREE_OF_A_KIND_VALUE + int(most_common_value)*100 + highest_card*10 + second_highest_card
        if handValue > highest_hand:
            highest_hand_type = "Three of a kind"
            highest_hand = handValue

    if most_common_value_n == 2:
        second_most_common_value = 0
        for card in cards:
            if card[:-1] != most_common_value:
                if values[card[:-1]] == 2:
                    second_most_common_value = card[:-1]
                    break
        highest_card = 0
        for card in cards:
            if card[:-1] != most_common_value and card[:-1] != second_most_common_value:
                if int(card[:-1]) > highest_card:
                    highest_card = int(card[:-1])
        if second_most_common_value != 0:
            handValue = TWO_PAIR_VALUE + int(most_common_value)*100 + int(second_most_common_value)*100 + highest_card
            if handValue > highest_hand:
                highest_hand_type = "Two pair"
                highest_hand = handValue
        else:
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
        handValue = STRAIGHT_VALUE + int(straight[-1][:-1])
        if handValue > highest_hand:
            highest_hand_type = "Straight"
            highest_hand = handValue

    handValue = 0
    multiplier = 10000
    for card in reversed(cards):
        handValue += int(card[:-1])*multiplier
        multiplier = int(multiplier / 10)
        if multiplier == 0:
            break
    if handValue > highest_hand:
        highest_hand = handValue

    return highest_hand, highest_hand_type

def yourBot(gameState, yourPlayersIndex, yourHand):
    move: str = "call"
    amount: int = 0

    deck = Deck()
    wins = 0

    handCards = yourHand
    n_players = len(gameState["players"])

    sim_players = []
    for i in range(n_players):
        bot_player = botPlayer()
        sim_players.append(bot_player)

    for _ in range(1000):
        deck.shuffle_and_reset()
        tablecards = gameState["table_cards"]

        for card in handCards:
            deck.deck.remove(card)
        for card in tablecards:
            if card:
                deck.deck.remove(card)

        for i in range(len(tablecards)):
            if tablecards[i] is None:
                tablecards[i] = deck.draw_card()

        for i in range(len(sim_players)):
            sim_players[i].cards = [deck.draw_card(), deck.draw_card()]

        your_hand_val, _ = assign_value_to_hand(handCards, tablecards)
        did_win = True
        for player in sim_players:
            hand_val, _ = assign_value_to_hand(player.cards, tablecards)
            if hand_val > your_hand_val:
                did_win = False
                break
        if did_win:
            wins += 1

    check_amount = 100
    call_amount = 350
    raise_amount = 400
    allin_amount = 550

    skew = 2
    check_amount = int(check_amount * skew)
    call_amount = int(call_amount * skew)
    raise_amount = int(raise_amount * skew)
    allin_amount = int(allin_amount * skew)

    if wins > allin_amount:
        move = "allin"
        amount = 0
    elif wins > raise_amount:
        move = "raise"
        amount = gameState["min_raise"] if gameState["min_raise"] > 300 else 300
    elif wins > call_amount:
        move = "call"
        amount = 0
    else:
        move = "check"
        amount = 0

    return move, amount
