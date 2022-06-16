import random, sys

# set up the constants:
hearts = chr(9829) # ♥
diamonds = chr(9830) # ♦
spades = chr(9824) # ♠
clubs = chr(9827) # ♣
print(hearts, diamonds, spades, clubs)
print('little python game')

def main():
    print('''Blackjack, home-casino
 Rules:
 Try to get as close to 21 without going over.
 Kings, Queens, and Jacks are worth 10 points.
 Aces are worth 1 or 11 points.
 Cards 2 through 10 are worth their face value.
 (H)it to take another card.
 (S)tand to stop taking cards.
 On your first play, you can (D)ouble down to increase your bet
 but must hit exactly one more time before standing.
 In case of a tie, the bet is returned to the player.
 The dealer stops hitting at 17.
    ''')
    money = 5000
    while True: # game loop
        # check player's money
        if money <= 0:
            print("You are broke!")
            print("Good thing you weren't playing with real money")
            print('Thanks for playing!')
            sys.exit()
        # if he had money yet let him made a bet
        print('Money', money)
        bet = getBet(money)

        #give the dealer and player two cards from the deck each:
        deck = getDeck()
        dealerHand = [deck.pop(), deck.pop()]
        playerHand = [deck.pop(), deck.pop()]


        #possible player actions:
        print('Make your bet:', bet)
        while True: #keep looping until player stands or busts.
            displayHands(playerHand, dealerHand, False)
            print()

            #check if the player has bust:
            if getHandValue(playerHand) > 21:
                break

            # get the player's move, either H, S, or D
            move = getMove(playerHand, money - bet)

            #handle the player actions:
            if move == 'D':
                #player is doubling down, they can increase their bet
                additionalBet = min(bet, (money-bet))
                bet += additionalBet
                print(f'Bet increased to {bet}')
                print('Your bet at this round::',bet)

            if move in ('H','D'):
                #Hit/doubling down takes another card
                newCard = deck.pop()
                rank, suit = newCard
                print(f'You drew a {rank} of {suit}')
                playerHand.append(newCard)

                if getHandValue(playerHand) > 21:
                    #playes has busted, so we start a new game loop
                    continue

            if move in ('S','D'):
                # stands/doubling down stops the player's turn
                break
        #handle the dealer's actions:
        if getHandValue(playerHand)<=21:
            while getHandValue(dealerHand) <17:
                #dealer hits:
                print('dealer hits...')
                dealerHand.append(deck.pop())
                displayHands(playerHand, dealerHand, False)

                if getHandValue(dealerHand) > 21:
                    break # the dealer has busted


            #show final hands:
        print()
        print()
        print('RESULTS')
        playerValue = getHandValue(playerHand)
        dealerValue = getHandValue(dealerHand)
        displayHands(playerHand,dealerHand, True)
        if dealerValue > 21:
            print('Dealer busts! you win ${}!'.format(bet))
            money += bet
        elif (playerValue > 21):
            print('You lost! You busted')
            money -= bet
        elif playerValue < dealerValue:
            print('You lost! Dealer beat you')
            money -= bet

        elif playerValue > dealerValue:
            print('You won ${}!'.format(bet))
            money += bet
        elif playerValue == dealerValue:
            print("It's a tie. the bet is returned to you")

        input('Press enter to continue...')
        print()
        print()

def getBet(maxBet):
    '''Ask the player how muck they want to bet'''
    while True: #keep asking until the enter QUIt
        bet = input('Make your bet (Quit to end game): ').upper().strip()
        if bet == 'QUIT':
            print('thanks for playing!')
            sys.exit()
        if not bet.isdecimal():
            continue

        bet  = int(bet)
        if 1 <= bet <= maxBet:
            return bet

def getDeck():
    '''Return a list of (rank,suit) tuples for all 52 cards'''
    deck = []
    for suit in (hearts, diamonds, spades, clubs):
        for rank in range(2,11):
            deck.append((str(rank), suit))
        for rank in ('J','Q','K','A'):
            deck.append((rank, suit))
    random.shuffle(deck)
    return deck

def displayHands(playerHand, dealerHand, showDealerHand):
    '''Show the player's and dealer's cards
    Hide the dealer's first card if showdealerhand is False'''
    print()

    if showDealerHand:
        print("DEALER:", getHandValue(dealerHand))
        displayCards(dealerHand)
    else:
        print('DEALER: ???')
        displayCards(['BACKSIDE'] + dealerHand[1:])

    print('PLAYER:', getHandValue(playerHand))
    displayCards(playerHand)

def getHandValue(cards):
    '''Return the value of the cards. Face cards are worth 10,
    Ace worth 11 or 1 '''
    value = 0
    numberOfAces = 0

    for card in cards:
        rank = card[0] #card is a tuple like (rank, suit)
        if rank == 'A':
            numberOfAces += 1
            continue
        if rank in ('K','Q','J'):
            value+=10
            continue
        if rank in ('2','3','4','5','6','7','8','9','10'):
            value+=int(rank)

        # at once we added 1 for each ace. and then we checks if
        # we can add another 10 points and stay < 22 points
        # if it possible we use ace as 11 points

    value += numberOfAces
    for i in range(numberOfAces):
        if value + 10 <= 21:
            value += 10

    return value

def displayCards(cards):
    'Display all the cards in the cards list'
    rows = ['','','','','']
    for i, card in enumerate(cards):
        rows[0] += ' ___  '
        if card == 'BACKSIDE':
            # Print a card's back:
            rows[1] += '|## | '
            rows[2] += '|###| '
            rows[3] += '|_##| '
        else:
            rank, suit = card
            rows[1] += f'|{rank.ljust(2)} | '
            rows[2] += f'| {suit} | '
            rows[3] += f'|_{rank.rjust(2,"_")}| '
    #print each row on the screen
    for row in rows:
        print(row)

def getMove(playerHand, money):
    ''' Asks the player for their move and return 'H' for hit,
     'S' for stand and 'D' for double down'''
    while True:
        moves = ['(H)it', '(S)tand']
        # the player can double down on their first move,
        #which we can tell because they'll have exactly two cards:
        if len(playerHand) == 2 and money > 0:
            moves.append('(D)ouble down')
        # Get the player's move:
        movePrompt = ', '.join(moves) + '> '
        move = input(movePrompt).upper()
        if move in ('H', 'S'):
            return move
        if move == 'D' and '(D)ouble down' in moves:
            return move

if __name__ == '__main__':
    main()