import curses
from lib.states import State

def main(stdscr):

	curses.use_default_colors()

	state = State(state='Init', state_stdscr=stdscr)

	while state.state != 'Exit':
		state.state_main()

curses.wrapper(main)