"""Option shuffler for quiz questions."""

import random
from typing import List, Tuple


def shuffle_options(options: List[str], correct_answer: str) -> Tuple[List[str], str]:
    """
    Shuffle options and return new answer letter.

    Args:
        options: List of option texts.
        correct_answer: Original answer (letter or text).

    Returns:
        (shuffled_options, new_answer_letter)
    """
    # Determine which option is correct (by index or text)
    correct_text = None
    if isinstance(correct_answer, str) and len(correct_answer) == 1 and correct_answer.isalpha():
        idx = ord(correct_answer.upper()) - ord("A")
        if 0 <= idx < len(options):
            correct_text = options[idx]
    else:
        correct_text = correct_answer

    shuffled = list(options)
    random.shuffle(shuffled)

    # Find new position of correct answer
    try:
        new_idx = shuffled.index(correct_text)
    except ValueError:
        new_idx = 0

    new_answer_letter = chr(ord("A") + new_idx)
    return shuffled, new_answer_letter
