import random


"""
deck = ["2♠", "3♠", "4♠", "5♠", "6♠", "7♠", "8♠", "9♠", "T♠", "J♠", "Q♠", "K♠", "A♠",
        "2♥", "3♥", "4♥", "5♥", "6♥", "7♥", "8♥", "9♥", "T♥", "J♥", "Q♥", "K♥", "A♥",
        "2♦", "3♦", "4♦", "5♦", "6♦", "7♦", "8♦", "9♦", "T♦", "J♦", "Q♦", "K♦", "A♦",
        "2♣", "3♣", "4♣", "5♣", "6♣", "7♣", "8♣", "9♣", "T♣", "J♣", "Q♣", "K♣", "A♣"]

example_yourHand = ["5♠", "8♠"]



example_gameState = {
    "players": [
        {
            "name": "Jens", 
            "stack": 1000, # the amount of money the player has
            "bet": 0, # the amount of money the player has bet this round
            "hasFolded": False # if the player has folded
        },
        {
            "name": "Abraham",
            "stack": 900, 
            "bet": 0,
            "hasFolded": False
            
        },
        {
            "name": "Jonas",
            "stack": 1100,
            "bet": 0,
            "hasFolded": False
        },
        {
            "name": "Berit",
            "stack": 200,
            "bet": 0,
            "hasFolded": False
        }
    ],
    "table_cards": ["2♠", None, None, None, None], # None is a card that is not yet revealed
    "dealer": 0, # index of the player that is the dealer
    "small_blind_player": 1, # index of the player that is the small blind
    "big_blind_player": 2, # index of the player that is the big blind
    "small_blind_amount": 10,
    "big_blind_amount": 20,
    "min_raise": 10,
    "max_raise": None,
}
"""


"""
gameState: dict
A dictionary representing the current game state, as seen above

yourPlayersIndex: int
If you are the first player in the list (Jens in the example_gameState), yourPlayersIndex will be 0

yourHand: list[str]
A list of two strings, each representing a card in your hand

The allowed output for move is one of these: ["fold", "check", "raise", "call", "allin"]

The allowed output for amount is a positive integar, that is not larger than your stack (and not smaller than the min_raise if you are raising)
If move is raise, amount is the amount to raise by, if not, amount is ignored.
"""
def raiseBot(gameState, yourPlayersIndex, yourHand):
    move: str = "raise"
    amount: int = 200

    return move, amount

def callBot(gameState, yourPlayersIndex, yourHand):
    move: str = "call"
    amount: int = 0

    return move, amount

def checkBot(gameState, yourPlayersIndex, yourHand):
    move: str = "check"
    amount: int = 0

    return move, amount

def foldBot(gameState, yourPlayersIndex, yourHand):
    move: str = "fold"
    amount: int = 0

    return move, amount

def allinBot(gameState, yourPlayersIndex, yourHand):
    move: str = "allin"
    amount: int = 0

    return move, amount


def manualBot(gamesState, yourPlayersIndex, yourHand):
    move = -1
    movarr = ["fold", "check", "raise", "call", "allin"]
    print("\nfold: 0\ncheck: 1\nraise: 2\ncall: 3\nallin: 4")
    while move < 0 or move > 4:
        move = int(input("Enter move: "))

    print(movarr[move], "selected")
    amount = input("Enter ammount: ")
    # if amount is none, or not a integer, set it to 0 :
    if not amount:
        amount = 0
    if isinstance(amount, int) == False:
        amount = 0
    move = movarr[move]
    print("Ammount:", amount)

    return move, amount

def randomBot(gameState, yourPlayersIndex, yourHand):
    
    move: str = random.choice(["fold", "check", "raise", "call", "allin"])
    amount: int = 0

    return move, amount