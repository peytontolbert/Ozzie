class MainMenu:
    def __init__(self):
        self.options = [
            "create_agent",
            "load_agent",
            "run_scenario",
            "exit"
        ]

    def initialize(self):
        # Initialize any necessary components
        print("Initializing Main Menu...")
        # You can add more initialization logic here if needed
        # For example, loading configuration, setting up logging, etc.
        self.display_welcome_message()

    def display_welcome_message(self):
        print("Welcome to the Virtual Environment")
        print("==================================")
        print("This system allows you to create, load, and run scenarios with AI agents.")
        print("Please select an option from the menu to get started.")

    def display(self):
        print("\nMain Menu:")
        for i, option in enumerate(self.options, 1):
            print(f"{i}. {option.replace('_', ' ').title()}")
        
        while True:
            try:
                choice = int(input("Enter your choice: "))
                if 1 <= choice <= len(self.options):
                    return self.options[choice - 1]
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def handle_selection(self, selection):
        # This method can be implemented to handle the selection directly in the MainMenu class
        # For now, we'll just print the selection
        print(f"Selected option: {selection}")
        # The actual handling is done in the VirtualEnvironment class

# Usage example
if __name__ == "__main__":
    menu = MainMenu()
    menu.initialize()
    selection = menu.display()
    menu.handle_selection(selection)