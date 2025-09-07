import random
import sys
from typing import Tuple

# Word/phrase pools
_BASIC_WORDS = [
    "python", "hangman", "testing", "thread", "monotonic",
    "fixture", "queue", "assert", "module", "package",
]

_INTERMEDIATE_PHRASES = [
    "test driven development",
    "unit testing tools",
    "clean code practices",
    "keep it simple",
    "never trust the clock",
]

# Validation function
def is_valid_word_or_phrase(candidate: str) -> Tuple[bool, str]:
    """
    Returns (ok, reason). Validates using wordfreq if available, otherwise falls back to a heuristic.
    """
    try:
        from wordfreq import zipf_frequency  # type: ignore
        tokens = [t for t in candidate.split() if any(ch.isalpha() for ch in t)]
        if not tokens:
            return False, "No alphabetic tokens"
        rare = [t for t in tokens if zipf_frequency(t.lower(), "en") <= 1.0]
        if len(rare) == len(tokens):
            return False, "All tokens appear too rare"
        return True, "Validated by wordfreq"
    except ImportError:
        if any(ch.isalpha() for ch in candidate):
            return True, "Heuristic validation"
        return False, "No letters found"

# Random pickers
def random_basic() -> str:
    return random.choice(_BASIC_WORDS)

def random_intermediate() -> str:
    return random.choice(_INTERMEDIATE_PHRASES)

# ASCII art stages for wrong guesses
HANGMAN_STAGES = [
    """
     +---+
     |   |
         |
         |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
         |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
     |   |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|   |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
    /    |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
    / \\  |
         |
    =========
    """
]

def play_hangman(use_intermediate: bool = False):
    secret = random_intermediate() if use_intermediate else random_basic()
    valid, reason = is_valid_word_or_phrase(secret)
    if not valid:
        print(f"Selected word/phrase invalid ({reason}), picking from basic words.")
        secret = random_basic()

    secret = secret.lower()
    guessed_letters = set()
    wrong_guesses = set()
    max_wrong = len(HANGMAN_STAGES) - 1

    while True:
        # Display current hangman stage
        print(HANGMAN_STAGES[len(wrong_guesses)])
        
        # Show word progress
        display = ' '.join(
            ch if (not ch.isalpha()) or ch in guessed_letters else '_'
            for ch in secret
        )
        print("Word:", display)
        print("Wrong guesses:", ' '.join(sorted(wrong_guesses)))
        print(f"Guesses left: {max_wrong - len(wrong_guesses)}")

        # Check for win or loss
        if all(not ch.isalpha() or ch in guessed_letters for ch in secret):
            print("🎉 You won! The word was:", secret)
            break
        if len(wrong_guesses) >= max_wrong:
            print("😞 You lost! The word was:", secret)
            break

        # Player input
        guess = input("Guess a letter: ").strip().lower()
        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a single alphabetic character.")
            continue
        if guess in guessed_letters or guess in wrong_guesses:
            print("You've already guessed that letter.")
            continue

        # Evaluate guess
        if guess in secret:
            guessed_letters.add(guess)
            print("Good guess!")
        else:
            wrong_guesses.add(guess)
            print("Wrong!")

if __name__ == "__main__":
    mode = input("Choose difficulty—(B)asic or (I)ntermediate: ").strip().lower()
    play_hangman(use_intermediate=(mode == 'i'))
