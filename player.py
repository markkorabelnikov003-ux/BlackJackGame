from card import Card

class BasePlayer:
	def __init__(self):
		self.hand: list[Card] = []
	
	def take_cards(self, deck, amount: int):
		for card in deck.pull_cards(amount):
			self.hand.append(card)
	
	def get_cards(self):
		return self.hand.copy()

	def show_hand(self):
		print(self.hand)
	
	def count(self) -> int:
		cards = [card.get_value() for card in self.hand]
		aces = cards.count(11)
		raw_sum = sum(cards)

		while raw_sum > 21 and aces:
			aces -= 1
			raw_sum -= 10

		return raw_sum

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
	def count_soft(self) -> int:
		cards = [card.get_value() for card in self.hand]
		aces = cards.count(11)
		raw_sum = sum(cards)

		while raw_sum > 16 and aces:
			aces -= 1
			raw_sum -= 10

		return raw_sum


	def show_hand(self):
		print(f'Dealer\'s hand: {str(self.hand)[1:-1]}\t({self.count()})')

	def show_halfhand(self):
		print(f'Dealer\'s hand: {self.hand[0]}, ??\t(?)')


class Player(BasePlayer):
	def __init__(self, chips: int = 1000):
		super().__init__()
		self.chips = chips
		self.bet = 0
	
	def show_hand(self):
		print(f'Player\'s hand: {str(self.hand)[1:-1]}\t({self.count()})')
	
	def do_bet(self, bet: int):
		self.bet = bet
	
	def lose(self) -> int:
		amount = self.bet
		self.chips -= self.bet
		self.bet = 0
		return amount
	
	def win(self) -> int:
		amount = self.bet
		self.chips += self.bet
		self.bet = 0
		return amount
