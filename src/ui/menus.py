"""Main menu and navigation."""

from src.ui.cli_ui import CLIUI
from src.creators.quiz_creator import QuizCreator
from src.runners.quiz_runner import QuizRunner
from src.runners.adaptive_engine import AdaptiveEngine
from src.utils.leaderboard_handler import LeaderboardHandler
from src.utils.pdf_exporter import PDFExporter
from src.utils.file_handler import load_json
from src.config import LEADERBOARD_FILE, PDF_DIR
from pathlib import Path


class Menu:
    """Main application menu."""

    def __init__(self):
        self.creator = QuizCreator()
        self.leaderboard = LeaderboardHandler(LEADERBOARD_FILE)
        self.pdf_exporter = PDFExporter(PDF_DIR)
        self.username = None

    def start(self):
        """Start the application."""
        CLIUI.clear_screen()
        self._get_username()
        self._main_menu()

    def _get_username(self):
        """Get username for leaderboard."""
        self.username = CLIUI.get_input("Enter your name")
        if not self.username:
            self.username = "Anonymous"

    def _main_menu(self):
        """Main menu loop."""
        while True:
            try:
                choice = CLIUI.print_menu(
                    "Quiz Generator",
                    [
                        "Generate Quiz by Topic",
                        "Generate Quiz by Difficulty",
                        "View Leaderboard",
                        "View My History",
                        "Settings",
                        "Exit",
                    ],
                )

                if choice == 1:
                    self._generate_by_topic()
                elif choice == 2:
                    self._generate_by_difficulty()
                elif choice == 3:
                    self._view_leaderboard()
                elif choice == 4:
                    self._view_my_history()
                elif choice == 5:
                    self._settings()
                elif choice == 6:
                    print("Goodbye!")
                    break
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                CLIUI.print_error(f"An error occurred: {str(e)}")

    def _generate_by_topic(self):
        """Generate quiz by topic."""
        categories = self.creator.get_available_categories()
        if not categories:
            CLIUI.print_error("No topics available.")
            return

        topic = CLIUI.get_choice("Select a topic", categories)
        count = CLIUI.get_number_input("How many questions", 1, 20)
        title = CLIUI.get_input("Quiz title", f"{topic} Quiz")

        try:
            quiz = self.creator.create_quiz_by_topic(title, topic, count)
            path = self.creator.save_quiz(quiz)
            CLIUI.print_success(f"Quiz created: {path}")

            # Run quiz
            if input("Run quiz now? (y/n): ").lower() == "y":
                self._run_quiz(quiz)
        except Exception as e:
            CLIUI.print_error(str(e))

    def _generate_by_difficulty(self):
        """Generate quiz by difficulty."""
        difficulties = self.creator.get_available_difficulties()
        if not difficulties:
            CLIUI.print_error("No difficulties available.")
            return

        difficulty = CLIUI.get_choice("Select difficulty", difficulties)
        count = CLIUI.get_number_input("How many questions", 1, 20)
        title = CLIUI.get_input("Quiz title", f"{difficulty.capitalize()} Quiz")

        try:
            quiz = self.creator.create_quiz_by_difficulty(title, difficulty, count)
            path = self.creator.save_quiz(quiz)
            CLIUI.print_success(f"Quiz created: {path}")

            if input("Run quiz now? (y/n): ").lower() == "y":
                self._run_quiz(quiz)
        except Exception as e:
            CLIUI.print_error(str(e))

    def _run_quiz(self, quiz):
        """Run a quiz."""
        runner = QuizRunner(quiz)
        try:
            analytics = runner.run()
            
            # Save score
            self.leaderboard.add_score(
                self.username,
                quiz.title,
                analytics.correct_count(),
                analytics.total_questions(),
            )
            CLIUI.print_success("Score saved to leaderboard!")

            # Export option
            if input("Export as PDF? (y/n): ").lower() == "y":
                pdf_path = self.pdf_exporter.export_results_as_pdf(quiz.title, runner.results)
                CLIUI.print_success(f"Exported to {pdf_path}")

        except KeyboardInterrupt:
            print("\nQuiz cancelled.")

    def _view_leaderboard(self):
        """Display leaderboard."""
        print()
        print(self.leaderboard.display_leaderboard(10))
        input("Press Enter to continue...")

    def _view_my_history(self):
        """Display user's quiz history."""
        history = self.leaderboard.get_user_history(self.username)
        if not history:
            print(f"\nNo quizzes taken yet.")
        else:
            print(f"\nYour Quiz History ({self.username}):")
            print(f"{'Quiz':<25} {'Score':<10} {'%':<8} {'Date':<20}\n")
            for h in history:
                quiz = h.get("quiz_title", "Unknown")[:25]
                score = h.get("score", 0)
                total = h.get("total", 0)
                pct = h.get("percentage", 0)
                date = h.get("timestamp", "Unknown")[:19]
                print(f"{quiz:<25} {score}/{total:<8} {pct:.1f}%  {date}")
        input("\nPress Enter to continue...")

    def _settings(self):
        """Settings menu (placeholder)."""
        CLIUI.print_menu("Settings", ["Coming soon!", "Back"])
