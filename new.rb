#!/usr/bin/env ruby
require 'yaml'

#Removes curses/Disable curses

CONFIG = YAML.load_file('config.yml')

def init_screen
  Curses.init_screen
  Curses.start_color
  Curses.init_pair(1, Curses::COLOR_WHITE, Curses::COLOR_BLUE)
  Curses.stdscr.keypad(true)
  Curses.noecho
  Curses.cbreak
end

def display_menu
  menu = [
    '1. Nmap',
    '2. Nikto',
    '3. DirBuster (via Python)',
    '4. GoBuster (via Lua)',
    '5. SQLMap',
    '6. Exit'
  ]

  Curses.setpos(2, 2)
  Curses.addstr("Select a tool to run:")
  menu.each_with_index do |item, index|
    Curses.setpos(4 + index, 4)
    Curses.addstr(item)
  end
end

def get_user_input
  Curses.setpos(12, 2)
  Curses.addstr("Your choice: ")
  Curses.echo
  choice = Curses.getstr.to_i
  Curses.noecho
  choice
end

# ... [rest of the script functions]

def main
  init_screen

  Curses.attron(Curses.color_pair(1))
  loop do
    display_menu
    choice = get_user_input
    handle_choice(choice, "target_ip")  # Update with your target IP logic
  end
ensure
  Curses.close_screen
end

main
