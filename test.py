
from engine.structures import Rank,Suit,Card,Deck



def compare_cards( c1 :Card, c2:Card, current_suit :Suit, trump :Suit  ) :
        
        if (c1.suit  == c2.suit ):
            if (c1.rank  > c2.rank ):
                return 1
            elif (c2.rank > c1.rank ):
                return -1
            else : 
                return 0
        elif (c1.suit  == trump ): 
            return 1 
        elif (c2.suit ==  trump ): 
            return -1
        elif (c1.suit ==  current_suit ):
            return 1
        elif  (c2.suit  ==  current_suit ) : 
            return -1
                
        else : 
            if (c1.rank > c2.rank ):
                return 1 
            elif (c1.rank < c2.rank ):
                return -1
            else :
                return 0
            
            


table = [
    Card( Rank.Six , Suit. CLUBS),
    Card( Rank.Queen , Suit. CLUBS),
]

hand =  [
    Card( Rank.Three , Suit.CLUBS),
    Card( Rank.Five , Suit.DIAMONDS),
    Card( Rank.King , Suit. CLUBS)
    
]

suit = table[0].suit
trump = Suit.DIAMONDS


if (table ==  None ): 
    high_card =  None #its empty  
else :
    high_card =  table[0]

    for c in table : 
        if (compare_cards(high_card, c ,  suit,trump ) == -1 ):
            high_card =  c

good_play = False
play =  high_card

for card in hand : 
    if (compare_cards(play, card , suit,trump ) ==-1 ):         
        good_play =  True
        play = card
 

if (good_play ==False ):

    lowest  = hand[0]
    for c in hand : 
        if (compare_cards(lowest, card ,suit, trump ) == 1):
            lowest = card 
    play = lowest 
    
print (table )
print (hand)
print ("PLAY !!")
print (play)
