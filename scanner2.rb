#!/usr/bin/env ruby

def display_menu
  puts "\nSelect a tool to run:"
  puts "1. Nmap"
  puts "2. Nikto"
  puts "3. DirBuster"
  puts "4. GoBuster"
  puts "5. SQLMap"
  puts "6. Exit"
end

def handle_choice(choice, target)
  case choice
  when 1
    execute_command("nmap", target, "Optional Nmap parameters (just hit enter for default):")
  when 2
    execute_command("nikto -h", target)
  when 3
    execute_command("REPLACE WITH DEFAULT DIRBUSTER COMMAND", target)
  when 4
    execute_command("REPLACE WITH GOBUSTER DEFAULT COMMAND", target)
  when 5
    execute_command("sqlmap -u", target, "Optional SQLMap parameters (e.g., --dbs, just hit enter for default):")
  when 6
    puts "Exiting..."
    exit
  else
    puts "Invalid choice"
  end
end

def execute_command(base_cmd, target, prompt = nil)
  params = ""
  if prompt
    puts prompt
    params = gets.chomp
  end
  cmd = "#{base_cmd} #{params} #{target} > logs/#{base_cmd.split.first}_#{target}.log"
  system(cmd)
  puts "#{base_cmd.split.first.capitalize} scan completed and logged to logs/#{base_cmd.split.first}_#{target}.log"
end

def main
  Dir.mkdir('logs') unless Dir.exist?('logs')  # Ensure logs directory exists

  loop do
    puts "\nEnter the target IP or domain (or 'exit' to quit):"
    target = gets.chomp
    break if target.downcase == 'exit'

    display_menu
    choice = gets.chomp.to_i
    handle_choice(choice, target)
  end
end

main
