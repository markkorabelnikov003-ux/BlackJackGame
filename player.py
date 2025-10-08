from card import Card
from copy import deepcopy

class BasePlayer:
	def __init__(self):
		self.hand: list[Card] = []
	
	def take_cards(self, deck, amount: int):
		for card in deck.pull_cards(amount):
			self.hand.append(card)
	
	def get_cards(self):
		return deepcopy(self.hand)

	def show_hand(self):
		return str(self.hand)
	
	def count(self) -> int:
		cards = [card.get_value() for card in self.hand]
		aces = cards.count(11)
		raw_sum = sum(cards)

		while raw_sum > 21 and aces:
			aces -= 1
			raw_sum -= 10

		return raw_sum
	
	def count_raw(self) -> int:
		return sum([card.get_value() for card in self.hand])

	def hand_state(self) -> int:
		"""
		returns state of hand
		0 - nothing
		1 - blackjack
		2 - busted
		"""

		points = self.count()
		if points > 21:
			return 2
		elif points == 21:
			return 1
		return 0

	def reset_hand(self):
		self.hand.clear()


class Dealer(BasePlayer):	
	def is_enough(self) -> int:
		return self.count_raw() >= 17


class Player(BasePlayer):
	def __init__(self, chips: int = 1000):
		super().__init__()
		self.chips = chips
		self.bet = 0
	
	def set_bet(self, bet: int):
		self.bet = bet
	
	def lose(self) -> int:
		amount = self.bet
		self.chips -= self.bet
		self.bet = 0
		return amount
	
	def win(self) -> int:
		amount = self.bet
		self.chips += amount
		self.bet = 0
		return amount
	
	def win_natural(self) -> int:
		amount = int(self.bet * 1.5)
		self.chips += amount
		self.bet = 0
		return amount
