import player
from iomodule import Message, sleep

from deck import Deck


class BlackJackGame:
	def __init__(self):
		self.running = True
		self.minimal_bet = 100
		self.starting_money = 500

		self.deck = Deck()
		self.player = player.Player(self.starting_money)
		self.dealer = player.Dealer()

	def run(self):
		Message.starting()
		while self.running:
			self.dealer.reset_hand()
			self.player.reset_hand()

			# if not ready, check the self.running parameter
			if not Message.getting_ready(self.is_enough, self.stop):
				continue
			Message.placing_bet(self.place_bet, self.player.chips)
			Message.starting_round()

			self.deck.create_new()
			self.deck.shuffle()

			self.player.take_cards(self.deck, 2)
			self.dealer.take_cards(self.deck, 2)

			Message.show_hand(self.dealer, 'Dealer', half=True)
			Message.show_hand(self.player, 'Player')
			
			game_state = Message.player_taking_turn(self.player_hit, self.player, self.get_game_state())
			# if player busted
			if game_state == 1:
				Message.ending_round(self.dealer, self.player, game_state)
				continue
			Message.show_hand(self.dealer, 'Full dealer')
			
			Message.dealer_taking_turn(self.dealer_hit, self.dealer)
			
			game_state = self.get_game_state()
			if Message.checking_game(game_state):
				Message.ending_round(self.dealer, self.player, game_state)
				continue
			
			game_res = Message.final_counting(self.count_diff)
			Message.ending_round(self.dealer, self.player, game_res)
	
	def place_bet(self, amount: int) -> int:
		"""
		returns
		0 - bet accepted
		1 - too small
		2 - too much
		3 - bet accepted (full in)
		"""

		if amount < self.minimal_bet:
			return 1
		elif amount > self.player.chips:
			return 2
		elif amount == self.player.chips:
			self.player.do_bet(amount)
			return 3
		
		self.player.do_bet(amount)
		return 0
	
	def get_game_state(self) -> int:
		"""
		returns game result
		0 - nothing
		1 - dealer won (player busted)
		2 - dealer won (blackjack)
		3 - player won (dealer busted)
		4 - player won (blackjack)
		5 - tie
		"""
		
		res = 0
		states = [p.hand_state() for p in (self.dealer, self.player)]
		# if dealer and player have blackjack
		if states[0] == states[1] == 1:
			res = 5
		# dealer busted
		elif states[0] == 2:
			res = 3
		# player busted
		elif states[1] == 2:
			res = 1
		# dealer blackjacked
		elif states[0] == 1:
			res = 2
		# player blackjacked
		elif states[1] == 1:
			res = 4
		
		return res

	def count_diff(self) -> int:
		return self.player.count() - self.dealer.count()

	def player_hit(self) -> int:
		self.player.take_cards(self.deck, 1)
		return self.get_game_state()

	def dealer_hit(self) -> int:
		self.dealer.take_cards(self.deck, 1)
		return self.get_game_state()

	def is_enough(self) -> bool:
		"""does the player have enough money to play"""

		if self.player.chips >= self.minimal_bet:
			return True
		
		self.running = False
		return False
	
	def stop(self):
		self.running = False


if __name__ == '__main__':
	game = BlackJackGame()
	try:
		game.run()
	except KeyboardInterrupt:
		...
	
	Message.quitting()
