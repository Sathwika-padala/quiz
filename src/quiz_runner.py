from typing import List, Optional
from .question_model import Question
import csv
from datetime import datetime
from pathlib import Path


def run_interactive(questions: List[Question], export_csv: Optional[str] = None) -> None:
    print(f"Running quiz: {len(questions)} questions\n")
    correct = 0
    results = []
    for idx, q in enumerate(questions, start=1):
        print(f"{idx}. {q.text}")
        for oi, opt in enumerate(q.options):
            label = chr(ord("A") + oi)
            print(f"  {label}. {opt}")

        # Determine if stored answer is letter or text
        stored_answer = q.answer
        correct_letter = None
        correct_text = None
        if isinstance(stored_answer, str) and len(stored_answer) == 1 and stored_answer.isalpha():
            correct_letter = stored_answer.upper()
            try:
                correct_text = q.options[ord(correct_letter) - ord("A")]
            except Exception:
                correct_text = None
        else:
            correct_text = stored_answer

        while True:
            ans = input("Your answer (letter), or type 'skip'/'quit': ").strip()
            if not ans:
                print("Skipped\n")
                chosen_letter = ""
                chosen_text = ""
                is_correct = False
                break
            if ans.lower() in {"skip", "s"}:
                print("Skipped\n")
                chosen_letter = ""
                chosen_text = ""
                is_correct = False
                break
            if ans.lower() in {"quit", "q"}:
                print("Quitting quiz early.")
                # export partial results if requested
                if export_csv:
                    _write_results_csv(export_csv, results)
                    print(f"Saved partial results to {export_csv}")
                return
            # accept letter or full text
            a = ans.strip().upper()
            chosen_letter = ""
            chosen_text = ""
            if len(a) == 1 and a.isalpha():
                chosen_letter = a
                try:
                    chosen_text = q.options[ord(a) - ord("A")]
                except Exception:
                    chosen_text = ""
            else:
                chosen_text = ans

            if chosen_text == "":
                print("Invalid choice, please enter a valid option letter or 'skip'/'quit'.")
                continue

            # Determine correctness
            if correct_letter:
                is_correct = (chosen_letter.upper() == correct_letter)
            else:
                is_correct = (chosen_text == correct_text)

            if is_correct:
                print("Correct!\n")
                correct += 1
            else:
                # show correct answer (letter + text if available)
                if correct_letter and correct_text:
                    print(f"Incorrect. Answer: {correct_letter} ({correct_text})\n")
                elif correct_text:
                    print(f"Incorrect. Answer: {correct_text}\n")
                else:
                    print(f"Incorrect.\n")
            break

        results.append({
            "index": idx,
            "question": q.text,
            "chosen_letter": chosen_letter,
            "chosen_text": chosen_text,
            "correct_letter": correct_letter or "",
            "correct_text": correct_text or "",
            "is_correct": is_correct,
        })

    print(f"Score: {correct}/{len(questions)} ({correct/len(questions)*100:.1f}%)")

    if export_csv:
        _write_results_csv(export_csv, results)
        print(f"Saved results to {export_csv}")


def _write_results_csv(path: str, rows: List[dict]) -> None:
    fieldnames = [
        "timestamp",
        "index",
        "question",
        "chosen_letter",
        "chosen_text",
        "correct_letter",
        "correct_text",
        "is_correct",
    ]
    ts = datetime.utcnow().isoformat()
    write_header = not Path(path).exists()
    with open(path, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        for r in rows:
            row = {"timestamp": ts}
            row.update(r)
            writer.writerow(row)
