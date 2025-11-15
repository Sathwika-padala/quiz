"""CLI UI and terminal interface."""

from typing import List
import os


class CLIUI:
    """Terminal user interface."""

    @staticmethod
    def clear_screen():
        """Clear terminal screen."""
        os.system("clear" if os.name == "posix" else "cls")

    @staticmethod
    def print_header(text: str):
        """Print a formatted header."""
        print(f"\n{'='*60}")
        print(f" {text.center(58)}")
        print(f"{'='*60}\n")

    @staticmethod
    def print_menu(title: str, options: List[str]) -> int:
        """Display menu and get user choice."""
        CLIUI.print_header(title)
        for idx, option in enumerate(options, 1):
            print(f"{idx}. {option}")
        print()
        while True:
            try:
                choice = int(input("Enter your choice: "))
                if 1 <= choice <= len(options):
                    return choice
                print(f"Please enter a number between 1 and {len(options)}.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    @staticmethod
    def print_success(message: str):
        """Print success message."""
        print(f"✓ {message}")

    @staticmethod
    def print_error(message: str):
        """Print error message."""
        print(f"✗ {message}")

    @staticmethod
    def get_input(prompt: str, default: str = None) -> str:
        """Get user input with optional default."""
        if default:
            msg = f"{prompt} [{default}]: "
        else:
            msg = f"{prompt}: "
        result = input(msg).strip()
        return result or default

    @staticmethod
    def get_number_input(prompt: str, min_val: int = 1, max_val: int = 100) -> int:
        """Get validated number input."""
        while True:
            try:
                num = int(input(f"{prompt} ({min_val}-{max_val}): "))
                if min_val <= num <= max_val:
                    return num
                print(f"Please enter a number between {min_val} and {max_val}.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    @staticmethod
    def get_choice(prompt: str, options: List[str]) -> str:
        """Get user choice from list."""
        print(f"\n{prompt}")
        for idx, opt in enumerate(options, 1):
            print(f"  {idx}. {opt}")
        choice = CLIUI.get_number_input("Select", 1, len(options))
        return options[choice - 1]
