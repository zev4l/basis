from card import Card, CardSuit, CardRank
from pygame_cards.set import CardsSet

BiscaDeck = CardsSet(
    [
        Card(name="Two of Clubs", rank=CardRank.TWO, suit=CardSuit.CLUBS),
        Card(name="Three of Clubs", rank=CardRank.THREE, suit=CardSuit.CLUBS),
        Card(name="Four of Clubs", rank=CardRank.FOUR, suit=CardSuit.CLUBS),
        Card(name="Five of Clubs", rank=CardRank.FIVE, suit=CardSuit.CLUBS),
        Card(name="Six of Clubs", rank=CardRank.SIX, suit=CardSuit.CLUBS),
        Card(name="Seven of Clubs", rank=CardRank.SEVEN, suit=CardSuit.CLUBS),
        Card(name="Jack of Clubs", rank=CardRank.JACK, suit=CardSuit.CLUBS),
        Card(name="Queen of Clubs", rank=CardRank.QUEEN, suit=CardSuit.CLUBS),
        Card(name="King of Clubs", rank=CardRank.KING, suit=CardSuit.CLUBS),
        Card(name="Ace of Clubs", rank=CardRank.ACE, suit=CardSuit.CLUBS),

        Card(name="Two of Spades", rank=CardRank.TWO, suit=CardSuit.SPADES),
        Card(name="Three of Spades", rank=CardRank.THREE, suit=CardSuit.SPADES),
        Card(name="Four of Spades", rank=CardRank.FOUR, suit=CardSuit.SPADES),
        Card(name="Five of Spades", rank=CardRank.FIVE, suit=CardSuit.SPADES),
        Card(name="Six of Spades", rank=CardRank.SIX, suit=CardSuit.SPADES),
        Card(name="Seven of Spades", rank=CardRank.SEVEN, suit=CardSuit.SPADES),
        Card(name="Jack of Spades", rank=CardRank.JACK, suit=CardSuit.SPADES),
        Card(name="Queen of Spades", rank=CardRank.QUEEN, suit=CardSuit.SPADES),
        Card(name="King of Spades", rank=CardRank.KING, suit=CardSuit.SPADES),
        Card(name="Ace of Spades", rank=CardRank.ACE, suit=CardSuit.SPADES),

        Card(name="Two of Diamonds", rank=CardRank.TWO, suit=CardSuit.DIAMONDS),
        Card(name="Three of Diamonds", rank=CardRank.THREE, suit=CardSuit.DIAMONDS),
        Card(name="Four of Diamonds", rank=CardRank.FOUR, suit=CardSuit.DIAMONDS),
        Card(name="Five of Diamonds", rank=CardRank.FIVE, suit=CardSuit.DIAMONDS),
        Card(name="Six of Diamonds", rank=CardRank.SIX, suit=CardSuit.DIAMONDS),
        Card(name="Seven of Diamonds", rank=CardRank.SEVEN, suit=CardSuit.DIAMONDS),
        Card(name="Jack of Diamonds", rank=CardRank.JACK, suit=CardSuit.DIAMONDS),
        Card(name="Queen of Diamonds", rank=CardRank.QUEEN, suit=CardSuit.DIAMONDS),
        Card(name="King of Diamonds", rank=CardRank.KING, suit=CardSuit.DIAMONDS),
        Card(name="Ace of Diamonds", rank=CardRank.ACE, suit=CardSuit.DIAMONDS),

        Card(name="Two of Hearts", rank=CardRank.TWO, suit=CardSuit.HEARTS),
        Card(name="Three of Hearts", rank=CardRank.THREE, suit=CardSuit.HEARTS),
        Card(name="Four of Hearts", rank=CardRank.FOUR, suit=CardSuit.HEARTS),
        Card(name="Five of Hearts", rank=CardRank.FIVE, suit=CardSuit.HEARTS),
        Card(name="Six of Hearts", rank=CardRank.SIX, suit=CardSuit.HEARTS),
        Card(name="Seven of Hearts", rank=CardRank.SEVEN, suit=CardSuit.HEARTS),
        Card(name="Jack of Hearts", rank=CardRank.JACK, suit=CardSuit.HEARTS),
        Card(name="Queen of Hearts", rank=CardRank.QUEEN, suit=CardSuit.HEARTS),
        Card(name="King of Hearts", rank=CardRank.KING, suit=CardSuit.HEARTS),
        Card(name="Ace of Hearts", rank=CardRank.ACE, suit=CardSuit.HEARTS)
    ]
)
