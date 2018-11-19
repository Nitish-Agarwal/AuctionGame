# HPS - Auction Game Architecture
## Introduction
This is the architecture for the auction game.

## Description
A sealed bid auction will take place. In the auction, there are k artists. Each of <i>m<i> players wants to obtain n works of one artist -- any artist is fine -- before anyone else does.

All players start out with 100 units of money. The artists of the first thousand items to go up to auction is generated randomly, but the list of those artists is given to each player's program at the beginning of the auction.

In round j, item j in the list goes up for auction. Bids are whole numbers. The winner of the round is the player with the highest bid (provided that player has sufficent funds, otherwise the player's bid is transformed to 0). If several players all make the highest bid (perhaps after transformation), then the winner of the round is the first of those players to enter the bid. The winner of a round pays the amount of his bid. (Real estate auctions happen that way). All players are told who won the bid and what that player paid. The amount paid is subtracted from the number of units left for that player.

Here is an example. Suppose there are two players (m = 2), four artists (k = 4), and the number of items that must be obtained is 3 (n = 3). Suppose that the first several items are: t2 t3 t4 t4 t4 t2 t3 t4 t2 t4 t2 t2 t2 t3 t4.

Consider the following history:
```
player 1 wins t2 with 22
player 1 wins t3 with 15
player 0 wins t4 with 33
player 0 wins t4 with 33

player 1 wins t4 with 34
player 1 wins t2 with 22
player 1 wins t3 with 0
player 0 wins t4 with 8 (AND WINS THE GAME)
```

## Get Started
```
Python3:
To start auction game, run start_game.py with following arguments:
    python start_game.py -h <host> [-p <port> -t <seconds>] m k n

where:
    h is the IP address to listen
    p is the port to run server on (Default: 9000)
    t is the game time in seconds (Default: 120)
    m is the number of players (for p is taken by port...)
    k is the number of artists
    n is the number of items that must be obtained

Then run the client as:
    python sample_client.py <host_ip> <port> [<name>]

When running multiple clients, the order of first round is the order of the clients entering the game, then the order will be determined by the order of clients returning the bids.
```

## Client
A sample_client.py has been provided as reference. Client will receive the following initial states from server.

```
'artists_num': number of artists
'required_count': number of items for artist to win
'auction_items': list of auction items
'player_count': number of players in the auction
```

It should return an integer as the bid per turn.

## Game State
Then for each round, you will receive the game_state and current wealth,
```
game_state: 'finished': whether the game has finished
            'bid_item': auction item of last round
            'bid_winner': winner of last round (player_name(str))
            'winning_bid': winning bid of last round
            'wealth_table': dictionary of wealth of each player
                            {'player_name': wealth, ...}
            'remain_time': the time you have left
```                        
