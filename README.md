# Study_Code

A macroeconomics practice quiz covering Gwartney, *Macroeconomics* 18th edition, chapters 1, 2 and 5–10. It has 200 multiple-choice questions (25 per chapter, written from the chapter slides), and every one comes with an explanation. I built it with Claude (vibe-coding) to study for my macro class and shared it with my classmates.

**Try it:** https://aurylo06.github.io/Study_Code/

## Features

- Exam-style mix in every chapter: 10 core-concept questions and 15 harder ones (scenarios, multi-step calculations, "spot the mistake", two-statement questions)
- Graphs (PPC, MB/MC, externalities, AD-AS shifts, loanable funds) and tables drawn right in the question, plus graphs in explanations that show the curve shift
- Explanations for every answer choice: why the right answer is right and why each wrong answer is wrong (shown in full after a miss, one tap away after a correct answer)
- **Practice exam:** 30 questions spread across all chapters, no feedback until you submit, an elapsed-time clock, and a full review afterwards
- **Graph drills:** interactive AD-AS diagrams where you shift AD, SRAS and LRAS yourself and get checked, including two-step long-run adjustments
- Pick which chapters to practice
- Answer choices are shuffled every time, so you learn the idea, not the letter
- Questions you miss come back later in the round until you get them right
- Your score counts first-try answers only, with a breakdown by chapter (under 75% is flagged)
- Missed questions are saved as "weak spots" so you can practice just those later
- **Save to notes** exports your weak spots as a study sheet (question, answer, explanation), using the share menu on phones or a text file download on computers
- Keyboard shortcuts: 1–4 to answer, Enter for the next question. Highlighting and copying text never picks an answer

## Files

| File | What it is |
| --- | --- |
| `index.html` | The landing page: a user guide with a button to start the quiz |
| `econ_quiz.html` | The web version of the quiz (one self-contained HTML file) |
| `econ_quiz.py` | The original command-line version in Python |

## Running it

**Web:** open the link above, or open `index.html` in any browser. No installs or accounts needed.

**Python:** standard library only.

```bash
python3 econ_quiz.py
```

On Windows, use `py econ_quiz.py`.

## Privacy

The web version saves weak spots in your browser's local storage, on your own device only. Your answers and scores never leave your device. The site counts anonymous usage (visits, time spent in the quiz, rounds started and finished) with [GoatCounter](https://www.goatcounter.com/), which uses no cookies and records no names, answers or scores. The Python version saves weak spots to `~/.econ_quiz_missed.json`.

## Feedback

Spotted a wrong answer? Email Aury Lomas at alomas5@lsu.edu with the question text and chapter.
