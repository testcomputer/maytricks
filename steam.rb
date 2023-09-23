#!/usr/bin/env ruby
require 'yaml'
require 'curses'

MENU_ITEMS = [
  'Nmap',
  'Nikto',
  'DirBuster (via Python)',
  'GoBuster (via Lua)',
  'SQLMap',
  'Exit'
].freeze

CONFIG = YAML.load_file('config.yml')

def init_screen
  Curses.init_screen
  Curses.start_color
  Curses.init_pair(1, Curses::COLOR_WHITE, Curses::COLOR_BLUE)
  Curses.stdscr.keypad(true)
  Curses.noecho
  Curses.cbreak
end

def create_main_window
  height = MENU_ITEMS.size + 4
  width = MENU_ITEMS.map(&:length).max + 6
  top = (Curses.lines - height) / 2
  left = (Curses.cols - width) / 2
  win = Curses::Window.new(height, width, top, left)
  win.keypad(true)
  win.box('|', '-')
  win.setpos(1, 2)
  win.addstr("Select a tool to run:")
  win
end

def display_menu(win)
  MENU_ITEMS.each_with_index do |item, index|
    win.setpos(3 + index, 4)
    win.addstr("#{index + 1}. #{item}")
  end
  win.refresh
end

def get_user_input(win)
  win.setpos(MENU_ITEMS.size + 3, 2)
  win.addstr("Your choice: ")
  win.echo
  choice = win.getstr.to_i
  win.noecho
  choice
end

def handle_choice(choice, target_ip)
  case choice
  when 1..5
    # Handle tool choice
  when 6
    # Exit the program
    exit
  else
    Curses.setpos(14, 2)
    Curses.addstr("Invalid choice. Please select a valid option.")
  end
end

def main
  init_screen
  win = create_main_window

  loop do
    display_menu(win)
    choice = get_user_input(win)
    handle_choice(choice, "target_ip")  # Update with your target IP logic
  end
ensure
  win.close if win
  Curses.close_screen
end

main
