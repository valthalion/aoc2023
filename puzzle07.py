from collections import Counter


testing = True


deck = '23456789TJQKA'
values = {card: val for val, card in enumerate(deck)}
joker_deck = 'J23456789TQKA'
joker_values = {card: val for val, card in enumerate(joker_deck)}


class Hand:
    def __init__(self, cards, bid, use_jokers=False):
        card_values = joker_values if use_jokers else values
        self.cards = tuple(card_values[card] for card in cards)
        self.bid = bid
        self.use_jokers = use_jokers
        self.power = self._power(cards)

    def _power(self, cards):
        counts = Counter(cards)
        if self.use_jokers and 'J' in counts and counts['J'] < 5:
            jokers = counts['J']
            del counts['J']
        else:
            jokers = 0
        power = sorted(counts.values(), reverse=True)
        power[0] += jokers
        return tuple(power)

    def __lt__(self, other):
        if self.power < other.power:
            return True
        if self.power > other.power:
            return False
        return self.cards < other.cards

    def __le__(self, other):
        if self.power < other.power:
            return True
        if self.power > other.power:
            return False
        return self.cards <= other.cards

    def __gt__(self, other):
        if self.power > other.power:
            return True
        if self.power < other.power:
            return False
        return self.cards > other.cards

    def __ge__(self, other):
        if self.power > other.power:
            return True
        if self.power < other.power:
            return False
        return self.cards >= other.cards

    def __eq__(self, other):
        return self.power == other.power and self.cards == other.cards

    def __ne__(self, other):
        if self.power != other.power:
            return True
        return self.cards != other.cards

    def __repr__(self):
        faces = joker_deck if self.use_jokers else deck
        return f'{''.join(faces[card] for card in self.cards)} ({self.bid})'


def read_data(use_jokers=False):
    filename = 'puzzle07_test.in' if testing else 'puzzle07.in'
    hands = []
    with open(filename, 'r') as f:
        for line in f:
            cards, bid = line.strip().split()
            hands.append(Hand(cards, int(bid), use_jokers))
    return hands


def part_1():
    hands = sorted(read_data())
    return sum(rank * hand.bid for rank, hand in enumerate(hands, start=1))


def part_2():
    hands = sorted(read_data(use_jokers=True))
    return sum(rank * hand.bid for rank, hand in enumerate(hands, start=1))
