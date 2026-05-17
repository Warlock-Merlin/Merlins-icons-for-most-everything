import os
import sys

# Import version info
from version import __version__, __app_name__

# Import functions from both modules
from generate_manifest import generate_manifest
from install_icons import download_and_extract_icons
from create_shortcut import main as create_shortcut_main


def clear_screen():
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def show_menu():
    """Display the main menu."""
    print("\n" + "=" * 50)
    print(f"           {__app_name__} v{__version__}")
    print("=" * 50)
    print("\n1. Install/Update Icons")
    print("2. Create a Shortcut")
    print("3. Refresh icon manifest")
    print("4. Exit")
    print("\n" + "-" * 50)


def main():
    """Main launcher menu."""
    while True:
        clear_screen()
        show_menu()
        choice = input("\nEnter your choice (1-4): ").strip()

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
            print("\n" + "-" * 50)
            print("Refresh icon manifest")
            print("-" * 50)
            generate_manifest()
            input("\nPress Enter to return to menu...")

        elif choice == "4":
            print("\nExiting... Goodbye!")
            sys.exit(0)

        else:
            print("\nInvalid choice. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        try:
            if sys.stdin is not None and sys.stdin.isatty():
                input("Press Enter to exit...")
        except Exception:
            pass
        sys.exit(1)
