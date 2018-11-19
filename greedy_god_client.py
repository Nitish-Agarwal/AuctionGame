import atexit

from client import Client
import time
import random
import sys

def check_game_status(state):
    if state['finished']:
        exit(0)

'''
The client will receive the following initial states from server.
    'artists_num': number of artists
    'required_count': number of items for artist to win
    'auction_items': list of auction items
    'player_count': number of players in the auction
-------------------------------------------------------------------
Then for each round, you will receive the game_state and current wealth,
game_state: 'finished': whether the game has finished
            'bid_item': auction item in last round
            'bid_winner': winner in last round (player_name(str))
            'winning_bid': winning bid in last round
            'remain_time': the time you have left
-------------------------------------------------------------------
You should return a whole number as the bid per turn.
'''

# key is player(me or opponent) and value is dict
# the dict mentioned above is : [key : item, value : number of art pieces accumulated]
opponentAndSelfData = dict()

# x is money player has
# n is number of remaining art pieces of current item
# l is dict [key: item, value: number of art pieces accumulated]
# N is required_items
# artists_num is total number of artists
def fun(x, n, l, N, artists_num, setAuctionItems, auction_items_from_now):
    """denom = 0
    for item in l:
        denom += (1.0/ (N - l[item]))
    itemsNotCounted = artists_num - len(l)
    denom += (itemsNotCounted * (1.0/ N))

    denom *= (n-1)
    denom += 1
    denom *= n
    return round(x / denom)"""
    ts = {}
    for item in setAuctionItems:
        ts[item] = 10000000

    for item in setAuctionItems:
        leftToAquire = N
        if item in l:
            leftToAquire -= l[item]
        for i in range(len(auction_items_from_now)):
            if auction_items_from_now[i] == item:
                if leftToAquire == 0:
                    print("this should not have had happened!")
                    exit(0)
                leftToAquire -= 1
                if leftToAquire == 0:
                    ts[item] = i
                    break

    denom = 0
    for item in setAuctionItems:
        if item == auction_items_from_now[0]:
            continue
        denom += (1.0/ts[item])
    denom *= ts[auction_items_from_now[0]]
    denom += 1
    denom *= n
    return round(x / denom)


### TODO Put your bidding algorithm here
def calculate_bid(game_state, wealth, wealth_table, name, auction_items, current_round, remaining_time, required_items, artists_num, setAuctionItems):
    '''
    'game_state': current game state
    'wealth': your current wealth
    'wealth_table': dictionary of wealth of each player like {'player_name': wealth, ...}
                    *Notice that player_name is a string. Invalid player will have wealth of -1.*
    '''
    
    
    if game_state:
        if game_state['bid_winner'] not in opponentAndSelfData:
            opponentAndSelfData[game_state['bid_winner']] = {game_state['bid_item'] : 1}
        else:
            if game_state['bid_item'] in opponentAndSelfData[game_state['bid_winner']]:
                opponentAndSelfData[game_state['bid_winner']][game_state['bid_item']] += 1
            else:
                opponentAndSelfData[game_state['bid_winner']][game_state['bid_item']] = 1

    print("who has what")
    print(opponentAndSelfData)
    #print("game state: ######################################")
    #print(game_state)
    #print("wealth: ############################################")
    #print(wealth)
    print("wealth_table: ##########################################")
    print(wealth_table)

    maxO = -1
    opponentFound = -1
    xo = 0
    no = 0
    lo = {}
    # xo, no and l are invalid if opponentFound == -1
    # search for opponent
    for opponent in opponentAndSelfData:
        # if not self
        if opponent == name:
            continue

        # x of opponent
        xo = wealth_table[opponent]
        # n of opponent
        no = required_count
        current_item = auction_items[current_round]
        data = opponentAndSelfData[opponent]
        if current_item in data:
            no -= data[current_item]
        # l of opponent is data

        # opponent st. f is satisfactory and xo is max
        if fun(xo, no, data, required_items, artists_num, setAuctionItems, auction_items[current_round:]) == xo and xo > maxO:
            maxO = xo
            opponentFound = opponent

    # atleast one opponent found
    if opponentFound != -1:
        if wealth < maxO + 1:
            print("############# 1 #########")
            print(wealth)
            return wealth
        else:
            opponent2 = -1
            for opponent in opponentAndSelfData:
                if opponent == name:
                    continue
                else:
                    if wealth_table[opponent] > maxO:
                        opponent2 = opponent
                        break
            if opponent2 != -1:
                if remaining_time > 12:
                    time.sleep(min(15.1, (remaining_time - 10) / 3))
            print("############# 2 #########")
            print(maxO + 1)
            return maxO + 1

    moneyToSpend = wealth
    n = required_items
    if name in opponentAndSelfData and auction_items[current_round] in opponentAndSelfData[name]:
        n -= opponentAndSelfData[name][auction_items[current_round]]
    l = {}
    if name in opponentAndSelfData:
        l = opponentAndSelfData[name]

    inner = fun(wealth, n, l, required_items, artists_num, setAuctionItems, auction_items[current_round:])
    sumOfAllOpponentsAndSelf = 0

    for opponent in opponentAndSelfData:
        sumOfAllOpponentsAndSelf += wealth_table[opponent]

    bestOpponent = -1
    maxOfBestOpponent = 0
    for opponent in opponentAndSelfData:
        if opponent == name:
            continue
        xo = wealth_table[opponent]
        if xo <= 0:
            continue
        no = required_count
        current_item = auction_items[current_round]
        lo = opponentAndSelfData[opponent]
        if current_item in lo:
            no -= lo[current_item]

        currentInner = int((wealth * fun(xo, no, lo, required_items, artists_num, setAuctionItems, auction_items[current_round:]))/(sumOfAllOpponentsAndSelf - xo))
        if maxOfBestOpponent < currentInner:
            maxOfBestOpponent = currentInner
            bestOpponent = opponent
    if bestOpponent != -1:
        if wealth_table[bestOpponent] > wealth:
            maxOfBestOpponent = int(maxOfBestOpponent * wealth / wealth_table[bestOpponent])
        elif inner < maxOfBestOpponent:
            maxOfBestOpponent = int(maxOfBestOpponent + inner * (wealth / wealth_table[bestOpponent] - 1))
            maxOfBestOpponent = min(maxOfBestOpponent, wealth_table[bestOpponent])
        inner = max(inner, maxOfBestOpponent)
    print("############# 3 #########")
    print(min(wealth, inner))
    return min(wealth, inner)

    #return random.randrange(0, wealth)
    
if __name__ == '__main__':

    ip = sys.argv[1]
    port = int(sys.argv[2])
    name = sys.argv[3] if len(sys.argv) == 4 else 'DiDi'

    client = Client(name, (ip, port))
    atexit.register(client.close)

    artists_num = client.artists_num
    required_count = client.required_count
    auction_items = client.auction_items
    player_count = client.player_count
    wealth_table = client.wealth_table
    setAuctionItems = set(auction_items)

    for opponent in wealth_table:
        opponentAndSelfData[opponent] = {}

    current_round = 0
    wealth = 100
    while True:
        print("current bid item: #########################")
        print(auction_items[current_round])
        print("\n\n")
        if current_round == 0:
            bid_amt = calculate_bid(None, wealth, wealth_table, name, auction_items, current_round, 100, required_count, artists_num, setAuctionItems)
        else:
            bid_amt = calculate_bid(game_state, wealth, game_state['wealth_table'], name, auction_items, current_round, game_state['remain_time'], required_count, artists_num, setAuctionItems)
        client.make_bid(auction_items[current_round], bid_amt)

        # after sending bid, wait for other player
        game_state = client.receive_round()
        game_state['remain_time'] = game_state['remain_time'][name]
        if game_state['bid_winner'] == name:
            wealth -= game_state['winning_bid']
        check_game_status(game_state)

        current_round += 1
