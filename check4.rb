require 'shoes'

Shoes.app(title: "All-in-One Pentest Tool", width: 400, height: 300) do
  background white
  stack(margin: 10) do
    title "Pentest Tool Selector"

    # Dropdown menu for tool selection
    list_box items: ["Nmap", "Nikto", "GoBuster", "SQLMap"], choose: "Select a tool" do |list|
      @selected_tool.text = "Selected tool: #{list.text}"
    end

    @selected_tool = para "Selected tool: None"

    # Input field for target
    para "Target IP/URL:"
    @target = edit_line

    # Button to run the selected tool
    button "Run" do
      # Placeholder logic for running the selected tool
      # You can expand this with actual command execution logic
      alert("Running #{@selected_tool.text} on #{@target.text}")
    end
  end
end
