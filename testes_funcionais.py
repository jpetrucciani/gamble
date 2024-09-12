import gamble

def test_deck():
    deck = gamble.Deck(shuffle=False)

    print("Cartas no baralho: ", deck.cards_left)
    print("Carta do topo: ", deck.top)
    print("Carta do fim: ", deck.bottom)

    print(deck.draw())
    print(deck.draw_hand(size = 5))

    deck2 = gamble.Deck(shuffle=True)
    hand1 = deck2.draw_hand()
    hand2 = deck.draw_hand()

    print(hand1)
    print(hand1.rank)
    print(hand2)
    print(hand2.rank)
    print(hand1 > hand2)

    hand3 = gamble.Hand.get("7c, 8c, 9c, Tc, Jc")
    print(hand3)
    print(hand3.rank)

def test_dice():
    dice = gamble.Dice("1d6")
    print(dice)

    print(dice.roll())
    print(dice.max)
    print(dice.min)
    print(dice.roll_many(2))
    # print(dice.max_of(2))
    print(dice.min_of(2))

def test_golf():
    YARDS = (
        332, 410, 357, 148, 431, 519, 338, 405, 283, 515, 348, 148, 446, 348, 380, 431, 217, 389
    )
    PAR = (4, 4, 4, 3, 4, 5, 4, 4, 4, 5, 4, 3, 4, 4, 4, 4, 3, 4)
    HANDICAP = (15, 3, 5, 17, 1, 9, 11, 7, 13, 6, 16, 18, 2, 14, 8, 4, 12, 10)
    HCC_DATA = list(zip(YARDS, PAR, HANDICAP, strict=True))

    holes = [gamble.Hole(index + 1, x[0], x[1], x[2]) for index, x in enumerate(HCC_DATA)]
    # print(len(holes))

    course = gamble.Course("Hillcrest", holes)
    # print(f"Course name: {course.name}")  # Esperado: "Hillcrest"
    # print(course.yards)

    player = gamble.Player("Alice", 10)
    # print(player)

    gamble.Group(course, player)
if __name__ == "__main__":
    # test_deck()
    # test_dice()
    test_golf()