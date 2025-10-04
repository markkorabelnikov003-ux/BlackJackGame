class Card:
	def __init__(self, suit: str, name):
		"""
		suits: Hearts, Spades, Diamonds, Clubs ♤ ♡ ♢ ♧
		names: (2-10), J, Q, K, A
		"""

		self.suit = suit
		self.name = name
		self.value = 0

		try:
			self.value = int(name)
		except ValueError:
			self.value = 10 if name in 'JQK' else 11

	def get_value(self):
		return self.value
	
	def check(self):
		return '1.0'

	def __repr__(self):
		return f'{self.suit}/{self.name}'
