import player
from deck import Deck
from time import sleep


class BlackJackGame:
	def __init__(self):
		self.running = True
		self.minimal_bet = 100
		self.starting_money = 500
		self.ver = '0.9'

		self.deck = Deck()
		self.player = player.Player(self.starting_money)
		self.dealer = player.Dealer()
		self.players = [self.dealer, self.player]

	def run(self):
		print(f'version: {self.ver}')
		print('\n⎛⎝( ` ᢍ ´ )⎠⎞ᵐᵘʰᵃʰᵃ\n' + '='*15 + ' Welcome to the Blackjack game! ' + '='*15 + '\n')
		sleep(1)
		while self.running:
			self.dealer.reset_hand()
			self.player.reset_hand()

			if self.get_ready():
				continue
			self.place_bet()
			print('\n' + '='*5 + ' The round has started ' + '='*5 + '\n')

			self.deck.create_new()
			self.deck.shuffle()

			self.player.take_cards(self.deck, 2)
			self.dealer.take_cards(self.deck, 2)

			self.dealer.show_halfhand()
			self.player.show_hand()
			
			if self.player_take_turn():
				print('\n' + '='*5 + ' The round has ended ' + '='*5 + '\n')
				continue
			
			if self.dealer_take_turn():
				print('\n' + '='*5 + ' The round has ended ' + '='*5 + '\n')
				continue
			
			self.force_end_game()

			print('\n' + '='*5 + ' The round has ended ' + '='*5 + '\n')
	
	def check_game(self) -> bool:
		res = self.get_game_result()
		match res:
			case 0:
				print('\nThe game is continuing (つ≖_≖)つ')
			case 1:
				print('\nDealer won cause you\'ve busted!')
			case 2:
				print('\nBlackjack! Dealer has won with')
			case 3:
				print('\nYou won cause the dealer have busted!')
			case 4:
				print('\nBlackjack! You have won! Congrats')
			case 5:
				print('\nCRAZY! You both got blackjacks (◉ _ ◉)')

		if res:
			self.dealer.show_hand()
		sleep(1)
		if res in (1, 2):
			print(f'\nYou have lost {self.player.lose()} chips... (ㅠ﹏ㅠ)')
		elif res in (3, 4):
			print(f'\nYou have earned {self.player.win()} chips  ദ്ദി ˉ͈̀꒳ˉ͈́ )✧')
		elif res == 5:
			print('\nYou haven\'t lost any chips')
		else:
			# if the game is continuing (res == 0)
			return False

		return True

	def get_ready(self) -> bool:
		if self.player.chips < self.minimal_bet:
			print(
				"""Looks like you\'ve lost all your money.
Remember, gambling is bad, especially when you dont know how to gamble properly >:D
We will glad to see you again, but firstly earn some more money""")
			self.running = False
			return True

		print('Are you ready to play? (y/n)')

		# цикл инпута
		while True:
			user_choice = input('>> ')

			match user_choice:
				case 'y':
					return False
				case 'n':
					print('\nByyyyeee! ˃̵ᴗ˂̵')
					self.running = False
					return True
	
	def place_bet(self):
		print(f'\nIt\'s time to place a bet... (you have {self.player.chips} chips)')
		sleep(1)

		while True:
			try:
				user_bet = int(input('>> '))
				
				if user_bet < 100:
					print('\nThe bet can\'t be under 100 chips honey (⸝⸝> ᴗ•⸝⸝)')
					sleep(0.5)
					continue
				elif user_bet > self.player.chips:
					print('\nYou can\'t place more chips you have silly (•ᴗ<˶)✧₊ ⊹')
					sleep(0.5)
					continue
				break
			except ValueError:
				...
		
		self.player.do_bet(user_bet)
		print('The bet has been placed')
		sleep(1)
	
	def get_states(self) -> list[int]:
		res = []
		
		for player in self.players:
			res.append(player.hand_state())

		return res

	def get_game_result(self) -> int:
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
		states = self.get_states()
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

	def force_end_game(self) -> int:
		"""
		returns
		0 - dealer is closer to 21
		1 - player is closer to 21
		2 - it is a tie
		"""
		
		res = 0
		player_d = 21 - self.player.count()  # d stands for distance to the 21
		dealer_d = 21 - self.dealer.count()

		if player_d == dealer_d:
			res = 2
		elif player_d < dealer_d:
			res = 1
		
		match res:
			case 0:
				print(f'\nNeither you nor the dealer had blackjack. However he was closer to 21 by {player_d-dealer_d} points...')
				sleep(2)
				print(f'You\'ve lost {self.player.lose()} chips... (⸝⸝⸝-﹏-⸝⸝⸝)')
			case 1:
				print(f'\nNeither you nor the dealer had blackjack. But YOU were closer to 21 by {dealer_d-player_d} points!')
				sleep(2)
				print(f'You\'ve earned {self.player.win()} chips! Congrats ٩(ˊᗜˋ*)و')
			case 2:
				print(f'\nIt\'s a TIE!!! (⊙ _ ⊙ )')
				sleep(2)
				print(f'You won\'t be charged. You better beat him next time ლ(ಠ益ಠლ)')

		sleep(1)
		print('\nFinal hands:')
		self.dealer.show_hand()
		self.player.show_hand()

		return res

	def player_take_turn(self) -> bool:
		"""
		players_points = self.players[1].count()

		while players_points <= 20:
			flag = False
			if players_points == 21:
				print('You won!')
				break
			elif players_points > 21:
				print('Dealer won!')
				break
			while True:
				user_choice = input('Взять карту или остановиться? h/s \n >> ')
				
				match user_choice:
					case 'h':
						self.player.take_cards(self.deck, 1)
						self.player.show_hand()
						break
					case 's':
						flag = True
						break
			if flag:
				break
		"""

		hitting = True
		while not (game_state := self.check_game()) and hitting:
			print('\nChoose: hit or stand? (h/s)')

			while True:
				user_input = input('>> ')

				if user_input == 'h':
					self.player.take_cards(self.deck, 1)
					self.player.show_hand()
					sleep(1)
					break
				elif user_input == 's':
					hitting = False
					break
		
		return bool(game_state)

	def dealer_take_turn(self) -> bool:
		if self.dealer.count_soft() > 16:
			self.dealer.show_hand()
			print('\nLook\'s like dealer already has more than 16 points. Lets count the results (·•᷄_•᷅ )')
			sleep(2)
			return False
		
		game_state = 0
		while not game_state and self.dealer.count_soft() <= 16:
			self.dealer.take_cards(self.deck, 1)
			self.dealer.show_hand()
			sleep(2)
			game_state = self.check_game()
		
		return bool(game_state)


if __name__ == '__main__':
	game = BlackJackGame()
	try:
		game.run()
	except KeyboardInterrupt:
		input('\n\nThe program has stopped. Press enter to quit')
