#!/usr/bin/env ruby
require 'yaml'
require 'shoes'

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

Shoes.app(title: "Pentest Tool Selector", width: 300, height: 250) do
  stack(margin: 10) do
    para "Select a tool to run:"
    
    MAIN_MENU_ITEMS.each_with_index do |item, index|
      button item do
        if SUB_MENU_ITEMS.key?(item)
          window(title: "#{item} Options", width: 250, height: 150) do
            stack(margin: 10) do
              para "Select an option for #{item}:"
              SUB_MENU_ITEMS[item].each do |sub_item|
                button sub_item do
                  # Handle the sub-menu choice here
                end
              end
            end
          end
        else
          # Handle other main menu choices here
        end
      end
    end
  end
end
