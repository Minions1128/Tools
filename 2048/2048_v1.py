#-*- coding:utf-8 -*-

import curses
from random import randrange, choice # generate and place new tile
from collections import defaultdict


letter_codes = [ord(ch) for ch in 'WASDRQwasdrq']
actions = ['Up', 'Left', 'Down', 'Right', 'Restart', 'Exit']
actions_dict = dict(zip(letter_codes, actions * 2))


def get_user_action(keyboard):
	# get user action
	char = "N"
	while char not in actions_dict:
		char = keyboard.getch()
	return actions_dict[char]


def transpose(field):
	"""
		example:
		1 2 3     1 1 1
		1 2 3 --> 2 2 2
		1 2 3     3 3 3
	"""
	return [list(r) for r in zip(*field)]


def invert(field):
	"""
		example:
		1 2 3     3 2 1
		1 2 3 --> 3 2 1
		1 2 3     3 2 1
	"""
	return [row[::-1] for row in field]


class GameField(object):
	def __init__(self, height=4, width=4, win=2048):
		self.height = height
		self.width = width
		self.win_value = 2048
		self.score = 0
		self.highscore = 0
		self.reset()

	def reset(self):
		"""
			keep highest score
			set score = 0
			clear field matrix to
			produce 2 or 4 randomly, twice
		"""
		if self.score > self.highscore:
			self.highscore = self.score
		self.score = 0
		self.field = [[0 for i in range(self.width)] for j in range(self.height)]
		self.spawn()
		self.spawn()

	def move(self, direction):
		"""
			use the LEFT direction expresses 4 directions:
			UP:		transpose(LEFT)
			DOWN:	transpose(inverse(LEFT))
			LEFT:	LEFT
			RIGHT:	inverse(LEFT)
			after move, it will produce a new element
		"""
		def move_row_left(row):
			# the basic movement
			def tighten(row):
				"""
					return a new row, 
					that squeeze non-zero elements together
				"""				
				new_row = [i for i in row if i != 0]
				new_row += [0 for i in range(len(row) - len(new_row))]
				return new_row

			def merge(row):
				"""
					return a new row, 
					that merge the same elements to zero and its double
				"""
				pair = False
				new_row = []
				for i in range(len(row)):
					if pair:
						new_row.append(2*row[i])
						self.score += 2 * row[i]
						pair = False
					else:
						if i + 1 < len(row) and row[i] == row[i+1]:
							pair = True
							new_row.append(0)
						else:
							new_row.append(row[i])
				assert len(new_row) == len(row)
				return new_row

			return tighten(merge(tighten(row)))

		moves = {}
		moves['Left'] = lambda field:					\
			[move_row_left(row) for row in field]
		moves['Right'] = lambda field:					\
			invert(moves['Left'](invert(field)))
		moves['Up'] = lambda field:						\
			transpose(moves['Left'](transpose(field)))
		moves['Down'] = lambda field:					\
			transpose(moves['Right'](transpose(field)))

		if direction in moves:
			if self.move_is_possible(direction):
				self.field = moves[direction](self.field)
				self.spawn()
				return True
			else:
				return False

	def is_win(self):
		return any(any(i>=self.win_value for i in row) for row in self.field)

	def is_gameover(self):
		return not any(self.move_is_possible(move) for move in actions)

	def draw(self, screen):
		"""
			draw the interface, include help info, gameover and win
			clear the screen first
			then, draw the info that the game need
		"""
		help_string1 = '(W)Up (S)Down (A)Left (D)Right'
		help_string2 = '     (R)Restart (Q)Exit'
		gameover_string = '           GAME OVER'
		win_string = '          YOU WIN!'

		def cast(string):
			# print to screen
			screen.addstr(string + '\n')

		def draw_hor_separator():
			# print the horizontal  field
			line = '+' + ('+------' * self.width + '+')[1:]
			separator = defaultdict(lambda:line)
			if not hasattr(draw_hor_separator, "counter"):
				draw_hor_separator.counter = 0
			cast(separator[draw_hor_separator])
			draw_hor_separator.counter += 1

		def draw_row(row):
			# print the row
			cast(''.join('|{: ^5} '.format(num) if num > 0 else '|      ' for num in row) + '|')

		screen.clear()
		cast('SCORE: ' + str(self.score))
		if 0 != self.highscore:
			cast('HGHSCORE: ' + str(self.highscore))
		for row in self.field:
			draw_hor_separator()
			draw_row(row)
		draw_hor_separator()
		if self.is_win():
			cast(win_string)
		else:
			if self.is_gameover():
				cast(gameover_string)
			else:
				cast(help_string1)
		cast(help_string2)

	def spawn(self):
		"""
			produce 2 or 4
			probability are 90% and 10% respectively
			set these two number to field matrix
		"""
		new_element = 4 if randrange(100) > 89 else 2
		(i, j) = choice([(i, j) for i in range(self.width) for j in range(self.height) if self.field[i][j] == 0])
		self.field[i][j] = new_element

	def move_is_possible(self, direction):
		# if the field is full and un_movable
		def row_is_left_movable(row):
			# if this row is movable
			def change(i):
				if row[i] == 0 and row[i+1] != 0:
					return True
				if row[i] != 0 and row[i+1] == row[i]:
					return True
				return False
			return any(change(i) for i in range(len(row)-1))

		check = {}
		check['Left'] = lambda field:						\
			any(row_is_left_movable(row) for row in field)
		check['Right'] = lambda field:						\
			check['Left'](invert(field))
		check['Up'] = lambda field:							\
			check['Left'](transpose(field))
		check['Down'] = lambda field:						\
			check['Right'](transpose(field))

		if direction in check:
			return check[direction](self.field)
		else:
			return False


def main(stdscr):
	"""
		5 kinds of state: Init, Game, Win, Gameover and Exit
		different states invoke different functions
		they are init(), not_game() and game() respectively
		Init: init() --> Game
		Game: game() --> Game, Win, Gameover, Exit
		Win: lambda:not_game('Win') --> Init, Exit
		Gameover: lambda:not_game('Gameover') --> Init, Exit
		Exit: exit the loop
	"""

	def init():
		"""
			reset the game
		"""
		game_field.reset()
		return 'Game'

	def not_game(state):
		"""
			draw the field
			get the user action
			if not restart or exit, keep the state
			else return init or exit
		"""
		game_field.draw(stdscr)
		action = get_user_action(stdscr)
		responses = defaultdict(lambda:state)
			# keep its original state
		responses['Restart'], responses['Exit'] = 'Init', 'Exit'
		return responses[action]

	def game():
		"""
			draw the field matrix
			get the user action
			if action == restart, reset the game
			if action == exit, exit
			if action == move(action), judge wim or lose
			else do nothing
		"""
		game_field.draw(stdscr)
		action = get_user_action(stdscr)
		if action == 'Restart':
			return 'Init'
		if action == 'Exit':
			return 'Exit'
		if game_field.move(action):
			if game_field.is_win():
				return 'Win'
			if game_field.is_gameover():
				return 'Gameover'
		return 'Game'

	state_actions = {
		'Init':init,
		'Win':lambda:not_game('Win'),
		'Gameover':lambda:not_game('Gameover'),
		'Game':game
		}

	curses.use_default_colors()
	game_field = GameField(win=32)

	state = 'Init'

	# state machine starts to work
	while state != 'Exit':
		state = state_actions[state]()


curses.wrapper(main)
