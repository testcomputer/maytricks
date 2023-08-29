#!/usr/bin/env ruby

def display_menu
    puts "\nSelect a tool to run:"
    puts "1. Nmap"
    puts "2. Nikto"
    puts "3. DirBuster (via Python)"
    puts "4. GoBuster (via Lua)"
    puts "5. SQLMap"
    puts "6. Exit"
  end

  def handle_choice(choice, target)
    case choice
    when 1
      puts "Optional Nmap parameters (just hit enter for default):"
      params = gets.chomp
      cmd = "nmap #{params} #{target} > logs/nmap_#{target}.log"
      system(cmd)
      puts "Nmap scan completed and logged to logs/nmap_#{target}.log"
    when 2
      cmd = "nikto -h #{target} > logs/nikto_#{target}.log"
      system(cmd)
      puts "Nikto scan completed and logged to logs/nikto_#{target}.log"
    when 3
      system("python3 dirbuster.py #{target} > logs/dirbuster_#{target}.log")
      puts "DirBuster scan completed and logged to logs/dirbuster_#{target}.log"
    when 4
      system("lua gobuster.lua #{target} > logs/gobuster_#{target}.log")
      puts "GoBuster scan completed and logged to logs/gobuster_#{target}.log"
    when 5
      puts "Optional SQLMap parameters (e.g., --dbs, just hit enter for default):"
      params = gets.chomp
      cmd = "sqlmap -u #{target} #{params} > logs/sqlmap_#{target}.log"
      system(cmd)
      puts "SQLMap scan completed and logged to logs/sqlmap_#{target}.log"
    when 6
      puts "Exiting..."
      exit
    else
      puts "Invalid choice"
    end
  end

  def main
    Dir.mkdir('logs') unless Dir.exist?('logs')  # Create logs directory if it doesn't exist

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
