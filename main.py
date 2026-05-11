import os
import sys

# Import functions from both modules
from install_icons import download_and_extract_icons
from create_shortcut import main as create_shortcut_main


def clear_screen():
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def show_menu():
    """Display the main menu."""
    print("\n" + "=" * 50)
    print("           Merlin's Icon Manager")
    print("=" * 50)
    print("\n1. Install/Update Icons")
    print("2. Create a Shortcut")
    print("3. Exit")
    print("\n" + "-" * 50)


def main():
    """Main launcher menu."""
    while True:
        show_menu()
        choice = input("\nEnter your choice (1-3): ").strip()

        if choice == "1":
            print("\n" + "-" * 50)
            print("Installing/Updating Icons...")
            print("-" * 50)
            download_and_extract_icons()
            input("\nPress Enter to return to menu...")

        elif choice == "2":
            print("\n" + "-" * 50)
            print("Create a Shortcut")
            print("-" * 50)
            create_shortcut_main()
            input("\nPress Enter to return to menu...")

        elif choice == "3":
            print("\nExiting... Goodbye!")
            sys.exit(0)

        else:
            print("\nInvalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        input("Press Enter to exit...")
        sys.exit(1)
