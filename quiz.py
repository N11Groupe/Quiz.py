#!/usr/bin/env python3
"""
quiz.py - A simple command-line quiz application with timer and scoring.

Author: Your Name
Date: 2025-05-20
"""

import json
import time
import sys
from pathlib import Path

# Terminal colors (only if supported)
USE_COLOR = sys.stdout.isatty()

class Colors:
    CYAN = '\033[96m' if USE_COLOR else ''
    YELLOW = '\033[93m' if USE_COLOR else ''
    GREEN = '\033[92m' if USE_COLOR else ''
    RED = '\033[91m' if USE_COLOR else ''
    MAGENTA = '\033[95m' if USE_COLOR else ''
    RESET = '\033[0m' if USE_COLOR else ''

# Emojis for UI
EMOJI_QUESTION = "❓"
EMOJI_CORRECT = "✅"
EMOJI_WRONG = "❌"
EMOJI_CLOCK = "⏰"
EMOJI_SCORE = "🏆"
EMOJI_PROGRESS = "📊"

def load_questions(filename):
    """Load questions from a JSON file."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"{Colors.RED}Error loading questions file: {e}{Colors.RESET}")
        sys.exit(1)

def print_header(score, current, total, elapsed):
    """Print the quiz header with progress, score, and elapsed time."""
    print(f"{Colors.CYAN}{'═'*60}{Colors.RESET}")
    print(f"{Colors.YELLOW}Quiz Progress: {Colors.MAGENTA}{current}/{total} "
          f"{Colors.YELLOW}| Score: {Colors.GREEN}{score} "
          f"{Colors.YELLOW}| Time Elapsed: {Colors.CYAN}{elapsed:.1f}s {EMOJI_CLOCK}{Colors.RESET}")
    print(f"{Colors.CYAN}{'═'*60}{Colors.RESET}")

def print_question(question, index, total, score, elapsed):
    """Display a question and its options."""
    print_header(score=score, current=index+1, total=total, elapsed=elapsed)
    print(f"{Colors.MAGENTA}{EMOJI_QUESTION} Q{index+1}: {question['question']}{Colors.RESET}")
    for i, option in enumerate(question['options']):
        print(f"  {Colors.YELLOW}{i+1}.{Colors.RESET} {option}")
    print()

def get_answer(num_options):
    """Prompt user for an answer, validate input, and return index."""
    while True:
        ans = input(f"{Colors.GREEN}Your answer (1-{num_options}): {Colors.RESET}").strip()
        if ans.isdigit():
            ans_int = int(ans)
            if 1 <= ans_int <= num_options:
                return ans_int - 1
        print(f"{Colors.RED}Invalid input. Please enter a number between 1 and {num_options}.{Colors.RESET}")

def print_feedback(is_correct, correct_answer):
    """Print feedback for the user's answer."""
    if is_correct:
        print(f"{Colors.GREEN}{EMOJI_CORRECT} Correct! Nice job! 🎉{Colors.RESET}")
    else:
        print(f"{Colors.RED}{EMOJI_WRONG} Wrong! The correct answer was: {Colors.YELLOW}{correct_answer}{Colors.RESET}")

def print_final_score(score, total, total_time):
    """Display the final score and a motivational message."""
    percent = (score / total) * 100
    print(f"\n{Colors.CYAN}{'='*60}{Colors.RESET}")
    print(f"{Colors.MAGENTA}{EMOJI_SCORE} Quiz Complete! Your Score: {Colors.GREEN}{score}/{total} "
          f"({percent:.1f}%) {EMOJI_PROGRESS}{Colors.RESET}")
    print(f"{Colors.CYAN}Total Time Taken: {Colors.YELLOW}{total_time:.1f} seconds{Colors.RESET}")

    if percent == 100:
        print(f"{Colors.MAGENTA}🎉 Perfect score! You're a true quiz master! 🧠🔥{Colors.RESET}")
    elif percent >= 75:
        print(f"{Colors.GREEN}Great job! You're very knowledgeable! 🎓👏{Colors.RESET}")
    elif percent >= 50:
        print(f"{Colors.YELLOW}Good effort! Keep practicing! 💪{Colors.RESET}")
    else:
        print(f"{Colors.RED}Keep studying and you'll get better! 📚{Colors.RESET}")

    print(f"{Colors.CYAN}{'='*60}{Colors.RESET}\n")

def main():
    """Main quiz loop."""
    # Use the questions.json file in the same directory as this script
    questions_file = Path(__file__).parent / "questions.json"
    questions = load_questions(questions_file)
    total_questions = len(questions)
    score = 0
    start_time = time.time()

    for idx, question in enumerate(questions):
        elapsed = time.time() - start_time
        print_question(question, idx, total_questions, score, elapsed)
        question_start = time.time()

        user_choice = get_answer(len(question['options']))

        time_taken = time.time() - question_start
        chosen_answer = question['options'][user_choice]
        is_correct = (chosen_answer == question['answer'])
        if is_correct:
            score += 1

        print_feedback(is_correct, question['answer'])
        print(f"{Colors.CYAN}You answered in {time_taken:.2f} seconds {EMOJI_CLOCK}{Colors.RESET}\n")
        time.sleep(1)

    total_time = time.time() - start_time
    print_final_score(score, total_questions, total_time)

if __name__ == "__main__":
    main()
