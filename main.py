import player
from deck import Deck
from time import sleep


class BlackJackGame:
	def __init__(self):
		self.deck = Deck()
		self.player = player.Player()
		self.dealer = player.Dealer()
		self.players = [self.dealer, self.player]
		self.running = True

	def run(self):
		print('\n⎛⎝( ` ᢍ ´ )⎠⎞ᵐᵘʰᵃʰᵃ\n' + '='*15 + ' Welcome to the Blackjack game! ' + '='*15 + '\n')
		sleep(1)
		while self.running:
			self.dealer.reset_hand()
			self.player.reset_hand()

			self.get_ready()
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
		end = True  # flag for ending the round
		match self.get_game_result():
			case 0:
				print('\nThe game is continuing (つ≖_≖)つ')
				end = False
			case 1:
				print('\nDealer won cause you\'ve busted!')
				self.dealer.show_hand()
				print(f'\nYou have lost {self.player.lose()} chips... (ㅠ﹏ㅠ)')
			case 2:
				print('\nBlackjack! Dealer has won with')
				self.dealer.show_hand()
				print(f'\nYou have lost {self.player.lose()} chips... (ㅠ﹏ㅠ)')
			case 3:
				print('\nYou won cause the dealer have busted!')
				self.dealer.show_hand()
				print(f'\nYou have earned {self.player.win()} chips')
			case 4:
				print('\nBlackjack! You have won! Congrats ദ്ദി ˉ͈̀꒳ˉ͈́ )✧')
				self.dealer.show_hand()
				print(f'\nYou have earned {self.player.win()} chips')
			case 5:
				print('\nCRAZY! You both got blackjacks (◉ _ ◉)')
				self.dealer.show_hand()
				print('\nYou haven\'t lost any chips')

		return end

	def get_ready(self):
		print('Are you ready to play? (y/n)')
				
		# цикл инпута
		while True:
			user_choice = input('>> ')

			match user_choice:
				case 'y':
					break
				case 'n':
					print('\nByyyyeee! ˃̵ᴗ˂̵')
					self.stop()
					break
	
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
				sleep(1)
				print(f'You\'ve lost {self.player.lose()} chips... (⸝⸝⸝-﹏-⸝⸝⸝)')
			case 1:
				print(f'\nNeither you nor the dealer had blackjack. But YOU were closer to 21 by {dealer_d-player_d} points!')
				sleep(1)
				print(f'You\'ve earned {self.player.win()} chips! Congrats ٩(ˊᗜˋ*)و')
			case 2:
				print(f'\nIt\'s a TIE!!! (⊙ _ ⊙ )')
				sleep(1)
				print(f'You won\'t be charged. You better beat him next time ლ(ಠ益ಠლ)')

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
		game_state = self.check_game()
		while not game_state and hitting:
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
			game_state = self.check_game()
		
		return bool(game_state)

	def dealer_take_turn(self) -> bool:
		if self.dealer.count_soft() > 16:
			print('\nLook\'s like dealer already has more than 16 points. Lets count the results (·•᷄_•᷅ )')
			return False
		
		while not (game_state := self.check_game()) and self.dealer.count_soft() <= 16:
			self.dealer.take_cards(self.deck, 1)
			self.dealer.show_hand()
			sleep(2)

		game_state = self.check_game()
		
		return bool(game_state)
                

	def stop(self):
		quit()


if __name__ == '__main__':
	game = BlackJackGame()
	game.run()
	input('The program has stopped')
