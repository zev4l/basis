from UI.card import Card, CardSuit, CardRank
from pygame_cards.set import CardsSet

BiscaDeck = CardsSet(
    [
        Card(name="Two of Clubs", rank=CardRank.TWO, suit=CardSuit.CLUBS, value=1, points= 0),
        Card(name="Three of Clubs", rank=CardRank.THREE, suit=CardSuit.CLUBS, value=2, points= 0),
        Card(name="Four of Clubs", rank=CardRank.FOUR, suit=CardSuit.CLUBS, value=3, points= 0),
        Card(name="Five of Clubs", rank=CardRank.FIVE, suit=CardSuit.CLUBS, value=4, points= 0),
        Card(name="Six of Clubs", rank=CardRank.SIX, suit=CardSuit.CLUBS, value=5, points= 0),
        Card(name="Queen of Clubs", rank=CardRank.QUEEN, suit=CardSuit.CLUBS, value=6, points= 2),
        Card(name="Jack of Clubs", rank=CardRank.JACK, suit=CardSuit.CLUBS, value=7, points= 3),
        Card(name="King of Clubs", rank=CardRank.KING, suit=CardSuit.CLUBS, value=8, points= 4),
        Card(name="Seven of Clubs", rank=CardRank.SEVEN, suit=CardSuit.CLUBS, value=9, points= 10),
        Card(name="Ace of Clubs", rank=CardRank.ACE, suit=CardSuit.CLUBS, value=10, points= 11),

        Card(name="Two of Spades", rank=CardRank.TWO, suit=CardSuit.SPADES, value=1, points= 0),
        Card(name="Three of Spades", rank=CardRank.THREE, suit=CardSuit.SPADES, value=2, points= 0),
        Card(name="Four of Spades", rank=CardRank.FOUR, suit=CardSuit.SPADES, value=3, points= 0),
        Card(name="Five of Spades", rank=CardRank.FIVE, suit=CardSuit.SPADES, value=4, points= 0),
        Card(name="Six of Spades", rank=CardRank.SIX, suit=CardSuit.SPADES, value=5, points= 0),
        Card(name="Queen of Spades", rank=CardRank.QUEEN, suit=CardSuit.SPADES, value=6, points= 2),
        Card(name="Jack of Spades", rank=CardRank.JACK, suit=CardSuit.SPADES, value=7, points= 3),
        Card(name="King of Spades", rank=CardRank.KING, suit=CardSuit.SPADES, value=8, points= 4),
        Card(name="Seven of Spades", rank=CardRank.SEVEN, suit=CardSuit.SPADES, value=9, points= 10),
        Card(name="Ace of Spades", rank=CardRank.ACE, suit=CardSuit.SPADES, value=10, points= 11),

        Card(name="Two of Diamonds", rank=CardRank.TWO, suit=CardSuit.DIAMONDS, value=1, points= 0),
        Card(name="Three of Diamonds", rank=CardRank.THREE, suit=CardSuit.DIAMONDS, value=2, points= 0),
        Card(name="Four of Diamonds", rank=CardRank.FOUR, suit=CardSuit.DIAMONDS, value=3, points= 0),
        Card(name="Five of Diamonds", rank=CardRank.FIVE, suit=CardSuit.DIAMONDS, value=4, points= 0),
        Card(name="Six of Diamonds", rank=CardRank.SIX, suit=CardSuit.DIAMONDS, value=5, points= 0),
        Card(name="Queen of Diamonds", rank=CardRank.QUEEN, suit=CardSuit.DIAMONDS, value=6, points= 2),
        Card(name="Jack of Diamonds", rank=CardRank.JACK, suit=CardSuit.DIAMONDS, value=7, points= 3),
        Card(name="King of Diamonds", rank=CardRank.KING, suit=CardSuit.DIAMONDS, value=8, points= 4),
        Card(name="Seven of Diamonds", rank=CardRank.SEVEN, suit=CardSuit.DIAMONDS, value=9, points= 10),
        Card(name="Ace of Diamonds", rank=CardRank.ACE, suit=CardSuit.DIAMONDS, value=10, points= 11),

        Card(name="Two of Hearts", rank=CardRank.TWO, suit=CardSuit.HEARTS, value=1, points= 0),
        Card(name="Three of Hearts", rank=CardRank.THREE, suit=CardSuit.HEARTS, value=2, points= 0),
        Card(name="Four of Hearts", rank=CardRank.FOUR, suit=CardSuit.HEARTS, value=3, points= 0),
        Card(name="Five of Hearts", rank=CardRank.FIVE, suit=CardSuit.HEARTS, value=4, points= 0),
        Card(name="Six of Hearts", rank=CardRank.SIX, suit=CardSuit.HEARTS, value=5, points= 0),
        Card(name="Queen of Hearts", rank=CardRank.QUEEN, suit=CardSuit.HEARTS, value=6, points= 2),
        Card(name="Jack of Hearts", rank=CardRank.JACK, suit=CardSuit.HEARTS, value=7, points= 3),
        Card(name="King of Hearts", rank=CardRank.KING, suit=CardSuit.HEARTS, value=8, points= 4),
        Card(name="Seven of Hearts", rank=CardRank.SEVEN, suit=CardSuit.HEARTS, value=9, points= 10),
        Card(name="Ace of Hearts", rank=CardRank.ACE, suit=CardSuit.HEARTS, value=10, points= 11)
    ]
)
