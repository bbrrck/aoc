from collections import defaultdict

with open("input.txt", "r") as f:
    lines = [x for x in f.read().strip("\n").split("\n")]


class Hand:
    def __init__(self, hand, bid, jokers: bool = False):
        if jokers:
            self.CARDS = [
                "A",
                "K",
                "Q",
                "T",
                "9",
                "8",
                "7",
                "6",
                "5",
                "4",
                "3",
                "2",
                "J",
            ]
        else:
            self.CARDS = [
                "A",
                "K",
                "Q",
                "J",
                "T",
                "9",
                "8",
                "7",
                "6",
                "5",
                "4",
                "3",
                "2",
            ]
        self.ORDER = {
            card: order
            for card, order in zip(self.CARDS, reversed(range(len(self.CARDS))))
        }
        self.hand = hand
        self.bid = int(bid)
        self.order = tuple([self.ORDER[card] for card in self.hand])
        if jokers:
            self.joker_counts()
        else:
            self.normal_counts()
        self.rank()

    def normal_counts(self):
        self.card_counts = defaultdict(int)
        for card in self.hand:
            self.card_counts[card] += 1
        self.n_distinct_cards = len(set(self.card_counts.keys()))
        self.counts = sorted(self.card_counts.values(), reverse=True)
        self.min_count = min(self.counts)
        self.max_count = max(self.counts)

    def joker_counts(self):
        self.card_counts = defaultdict(int)
        # Edge case
        if self.hand == "JJJJJ":
            self.hand = "AAAAA"
        for card in self.hand:
            self.card_counts[card] += 1
        J_count = 0
        if "J" in self.card_counts:
            J_count = self.card_counts["J"]
            del self.card_counts["J"]
        self.n_distinct_cards = len(set(self.card_counts.keys()))
        self.counts = sorted(self.card_counts.values(), reverse=True)
        self.min_count = min(self.counts)
        self.max_count = max(self.counts) + J_count

    def rank(self):
        if self.max_count == 5:
            # Five of a kind
            self.rank = 7
        elif self.max_count == 4:
            # Four of a kind
            self.rank = 6
        elif self.max_count == 3:
            if self.min_count == 2:
                # Full house
                self.rank = 5
            else:
                # Three of a kind
                self.rank = 4
        elif self.max_count == 2:
            if self.n_distinct_cards == 3:
                # Two of a kind
                self.rank = 3
            else:
                # One pair
                self.rank = 2
        else:
            # High card
            self.rank = 1
        self.value = self.rank * self.bid

    def __lt__(self, other):
        if self.rank == other.rank:
            return self.order < other.order
        return self.rank < other.rank

    def __repr__(self):
        return f"Hand: {self.hand}, Rank: {self.rank}, Order: {self.order}"


#### Parts 1 and 2
#### 1 = no jokers
#### 2 = with jokers
for jokers in [False, True]:
    hands = sorted([Hand(*line.split(" "), jokers=jokers) for line in lines])
    answer = sum([(rank + 1) * card.bid for rank, card in enumerate(hands)])
    print(answer)
