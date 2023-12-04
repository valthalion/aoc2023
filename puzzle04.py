testing = False


def read_data():
    filename = 'puzzle04_test.in' if testing else 'puzzle04.in'
    cards = {}
    with open(filename, 'r') as f:
        for card, line in enumerate(f, start=1):
            _, numbers = line.strip().split(': ')
            winning, playing = (set(int(n) for n in nums.split()) for nums in numbers.split(' | '))
            cards[card] = {'winning': winning, 'playing': playing, 'won': 1}
    return cards


def match(card):
    return len(card['playing'] & card['winning'])


def score(card):
    matches = match(card)
    if matches == 0:
        return 0
    return 2 ** (matches - 1)


def process(cards):
    for card, card_data in cards.items():
        matches = match(card_data)
        if matches:
            for other_card in range(card + 1, card + 1 + matches):
                cards[other_card]['won'] += card_data['won']


def part_1():
    cards = read_data()
    return sum(score(card) for card in cards.values())


def part_2():
    cards = read_data()
    process(cards)
    return sum(card['won'] for card in cards.values())
