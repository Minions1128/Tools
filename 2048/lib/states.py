from collections import defaultdict
from fields import GameField
from util import get_user_action

class State(object):

	def __init__(self, state, state_stdscr):
		self.game_field = GameField(win=32)
		self.state = state
		self.stdscr = state_stdscr
		self.state_actions = {
			'Init':self.init,
			'Win':lambda:self.not_game('Win'),
			'Gameover':lambda:self.not_game('Gameover'),
			'Game':self.game
		}

	def init(self):
		self.game_field.reset()
		self.state = 'Game'
		return

	def game(self):
		self.game_field.draw(self.stdscr)
		action = get_user_action(self.stdscr)
		if action == 'Restart':
			self.state = 'Init'
			return
		if action == 'Exit':
			self.state = 'Exit'
			return
		if self.game_field.move(action):
			if self.game_field.is_win():
				self.state = 'Win'
				return
			if self.game_field.is_gameover():
				self.state = 'Gameover'
				return
		self.state = 'Game'
		return

	def not_game(self, state_value):
		self.game_field.draw(self.stdscr)
		action = get_user_action(self.stdscr)
		responses = defaultdict(lambda:state_value)
		responses['Restart'], responses['Exit'] = 'Init', 'Exit'
		self.state = responses[action]
		return

	def state_main(self):
		self.state_actions[self.state]()