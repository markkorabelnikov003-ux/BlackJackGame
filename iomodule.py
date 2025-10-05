from time import sleep

class Message:
	def starting():
		print('\n⎛⎝( ` ᢍ ´ )⎠⎞ᵐᵘʰᵃʰᵃ\n')
		print('='*15 + ' Welcome to the Blackjack game! ' + '='*15 + '\n')
		sleep(1)

	def quitting():
		input('\n\nThe program has stopped. Press enter to quit')

	def getting_ready(is_enough_func, shutdown_func) -> bool:
		"""returns True if the user is ready to play, False otherwise"""

		if not is_enough_func():
			print(
				"""Looks like you\'ve lost all your money.
Remember, gambling is bad, especially when you dont know how to gamble properly >:D
We will glad to see you again, but firstly earn some more money""")
			shutdown_func()
			return False

		print('Are you ready to play? (y/n)')

		# цикл инпута
		while True:
			user_choice = input('>> ')

			match user_choice:
				case 'y':
					return True
				case 'n':
					print('\nByyyyeee! ˃̵ᴗ˂̵')
					sleep(1)
					shutdown_func()
					return False

	def placing_bet(bet_func, chips_has: int):
		print(f'\nIt\'s time to place a bet... (you have {chips_has} chips)')
		sleep(1)
		
		res = 1
		while res in (1, 2):
			try:
				user_bet = int(input('>> '))
				res = bet_func(user_bet)
				
				match res:
					case 0:
						print('\nThe bet has been placed')
					case 1:
						print('\nThe bet can\'t be under 100 chips honey (⸝⸝> ᴗ•⸝⸝)')
					case 2:
						print('\nYou can\'t place more chips you have silly (•ᴗ<˶)✧₊ ⊹')
					case 3:
						print('\nGoing Full-in? You\'re a risky guy! (⌐■_■)')
				
				sleep(1)
			except ValueError:
				...
	
	def show_hand(player_obj, person: str, half=False):
		hand = player_obj.get_cards()

		if half:
			print(f'{person}\'s hand: {hand[0]}, ??\t(?)')
		else:
			print(f'{person}\'s hand: {str(hand)[1:-1]}\t({player_obj.count()})')
		sleep(0.5)
	
	def checking_game(game_state) -> bool:
		match game_state:
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
		sleep(1)
		
		return bool(game_state)

	def player_taking_turn(player_hit_func, player_obj, cur_state: int) -> int:
		hitting = True
		game_state = cur_state

		# цикл взятия карт
		while hitting and not game_state:
			print('\nChoose: hit or stand? (h/s)')
			sleep(0.5)

			# цикл инпута
			while True:
				user_input = input('>> ')

				if user_input == 'h':
					sleep(1)

					game_state = player_hit_func()
					Message.show_hand(player_obj, 'Player')
					sleep(1)

					Message.checking_game(game_state)
					break
				elif user_input == 's':
					sleep(1)
					
					hitting = False
					break

		return bool(game_state)
	
	def dealer_taking_turn(dealer_hit_func, dealer_obj):
		if dealer_obj.is_enough():
			print('\nLook\'s like dealer already has more than 16 points. Let\'s count the results (·•᷄_•᷅ )')
			sleep(2)
			return
		
		print('\nDealer begins to take cards:')
		sleep(2)
		while not dealer_obj.is_enough():
			dealer_hit_func()
			Message.show_hand(dealer_obj, 'Dealer')
			sleep(1)
		print('\nDealer stops taking the cards')

	def final_counting(count_diff_func) -> int:
		"""1 - dealers win, 3 - players win, 5 - tie"""

		diff = count_diff_func()
		result = 0

		if diff > 0:
			print(f'\nYOU were closer to 21 by {diff} points! The win is yours!')
			result = 3
		elif diff < 0:
			print(f'\nThe dealer was closer to 21 by {abs(diff)} points... The luck is not on your side')
			result = 1
		else:
			print(f'\nYou have the same amount of points. It\'s a TIE!!! (⊙ _ ⊙ )')
			result = 5
		
		sleep(2)
		return result

	def ending_round(dealer_obj, player_obj, game_state: int):
		Message.show_hand(dealer_obj, 'Dealer')

		if game_state in (1, 2):
			print(f'\nYou have lost {player_obj.lose()} chips... (ㅠ﹏ㅠ)')
		elif game_state in (3, 4):
			print(f'\nYou have earned {player_obj.win()} chips  ٩(ˊᗜˋ*)و')
		else:
			print('\nYou haven\'t lost any chips')
		sleep(2)
		
		print('\nFinal hands:')
		sleep(0.5)
		Message.show_hand(dealer_obj, 'Dealer')
		Message.show_hand(player_obj, 'Player')
		
		print('\n' + '='*5 + ' The round has ended ' + '='*5 + '\n')
		sleep(2)

	def starting_round():
		print('\n' + '='*5 + ' The round has started ' + '='*5 + '\n')
