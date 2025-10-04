from card import Card
from random import shuffle


class Deck:
	def __init__(self):
		self.deck_list = []
	
	def create_new(self):
		self.deck_list.clear()
		for suit in ['♤', '♡', '♢', '♧']:
			for name in list(range(2, 11)) + list('JQKA'):
				self.deck_list.append(Card(suit, name))
			
	def shuffle(self):
		shuffle(self.deck_list)
	
	def get_deck(self):
		return self.deck_list.copy()

	def pull_cards(self, n=1):
		res = []

		for _ in range(n):
			res.append(self.deck_list.pop())
		
		return res
