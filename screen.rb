#!/usr/bin/env ruby
require 'yaml'
require 'curses'

# Load configuration
CONFIG = YAML.load_file('config.yml')

# Initialize the screen for Curses
def init_screen
  Curses.init_screen
  Curses.start_color
  Curses.init_pair(1, Curses::COLOR_WHITE, Curses::COLOR_BLUE)
  Curses.stdscr.keypad(true)
  Curses.noecho
  Curses.cbreak
end

# Display the main menu
def display_menu
  menu = [
    '1. Nmap',
    '2. Nikto',
    '3. DirBuster',
    '4. GoBuster',
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

def display_nmap_sub_options
  options = [
    '1.1. Basic Scan',
    '1.2. Service Version Detection',
    '1.3. OS Detection'
  ]
  Curses.setpos(7, 6)
  Curses.addstr("Select an Nmap option:")
  options.each_with_index do |item, index|
    Curses.setpos(9 + index, 8)
    Curses.addstr(item)
  end
end

# ... [Add display functions for other tools' sub-options here]

# Get the user's choice from the menu or sub-menu
def get_user_input
  Curses.setpos(16, 2)
  Curses.addstr("Your choice: ")
  Curses.echo
  choice = Curses.getstr
  Curses.noecho
  choice
end

# Handle the user's choice and run the selected tool
def handle_choice(choice, target_ip)
  case choice
  when "1"
    display_nmap_sub_options
    sub_choice = get_user_input
    handle_nmap_sub_choice(sub_choice, target_ip)
  # ... [Handle main choices for other tools here]
  when "6"
    exit
  else
    Curses.setpos(18, 2)
    Curses.addstr("Invalid choice. Please select a number from the menu.")
  end
end

def handle_nmap_sub_choice(sub_choice, target_ip)
  case sub_choice
  when "1.1"
    # Run Nmap basic scan
    system("nmap #{target_ip}")
  when "1.2"
    # Run Nmap with service version detection
    system("nmap -sV #{target_ip}")
  when "1.3"
    # Run Nmap for OS detection
    system("nmap -O #{target_ip}")
  else
    Curses.setpos(18, 2)
    Curses.addstr("Invalid Nmap choice. Please select a valid sub-option.")
  end
end

# ... [Add handlers for other tools' sub-choices here]

# Main function
def main
  init_screen

  Curses.attron(Curses.color_pair(1))
  loop do
    display_menu
    choice = get_user_input
    handle_choice(choice, CONFIG['target_ip'])
  end
end

main
