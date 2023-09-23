#!/usr/bin/env ruby
require 'yaml'
require 'curses'
require 'shoes'

# Constants
MAIN_MENU_ITEMS = [
  'Nmap',
  'Nikto',
  'GoBuster',
  'SQLMap',
  'Exit'
].freeze

SUB_MENU_ITEMS = {
  'Nmap' => ['Quick Scan', 'Full Scan'],
  'Nikto' => ['Quick Scan', 'Full Scan'],
  'GoBuster' => ['Directory Scan', 'File Scan'],
  'SQLMap' => ['Provide Command List']
}

CONFIG = YAML.load_file('config.yml')

# Initialize the screen for curses
def init_screen
  Curses.init_screen
  Curses.start_color
  Curses.init_pair(1, Curses::COLOR_WHITE, Curses::COLOR_BLUE)
  Curses.stdscr.keypad(true)
  Curses.noecho
  Curses.cbreak
end

# Create the main window for the menu
def create_main_window
  height = MAIN_MENU_ITEMS.size + 4
  width = MAIN_MENU_ITEMS.map(&:length).max + 6
  top = (Curses.lines - height) / 2
  left = (Curses.cols - width) / 2
  win = Curses::Window.new(height, width, top, left)
  win.keypad(true)
  win.box('|', '-')
  win.setpos(1, 2)
  win.addstr("Select a tool to run:")
  win
end

# Display the given menu items
def display_menu(win, items)
  items.each_with_index do |item, index|
    win.setpos(3 + index, 4)
    win.addstr("#{index + 1}. #{item}")
  end
  win.refresh
end

# Get user input from the menu
def get_user_input(win)
  win.setpos(win.maxy - 1, 2)
  win.addstr("Your choice: ")
  Curses.echo
  choice = win.getstr.to_i
  Curses.noecho
  choice
end

# Handle the main menu choice
def handle_choice(choice, target_ip)
  case choice
  when 1..3
    tool = MAIN_MENU_ITEMS[choice - 1]
    display_sub_menu(tool, target_ip)
  when 4
    # Prompt user for SQLMap command list
    Curses.setpos(16, 2)
    Curses.addstr("Provide a comma-separated list of SQLMap commands:")
    Curses.echo
    commands = Curses.getstr.split(',')
    Curses.noecho
    # Process the commands (you can add logic here to handle the commands)
  when 5
    # Exit the program
    exit
  else
    Curses.setpos(18, 2)
    Curses.addstr("Invalid choice. Please select a valid option.")
  end
end

# Display the sub-menu for a given tool
def display_sub_menu(tool, target_ip)
  win = create_main_window
  win.setpos(1, 2)
  win.addstr("Select a scan type for #{tool}:")
  display_menu(win, SUB_MENU_ITEMS[tool])
  choice = get_user_input(win)
  # Handle the sub-menu choice (you can add logic here to handle the specific scan types)
end

# Main execution
def main
  init_screen
  win = create_main_window

  loop do
    display_menu(win, MAIN_MENU_ITEMS)
    choice = get_user_input(win)
    handle_choice(choice, "target_ip")  # Update with your target IP logic
  end
ensure
  win.close if win
  Curses.close_screen
end

main
