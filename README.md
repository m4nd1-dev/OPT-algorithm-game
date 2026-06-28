# OPT Algorithm Game

A fun and interactive desktop puzzle game built with Python to help users learn the Optimal Page Replacement (OPT) algorithm.

This project turns a classic operating systems concept into a visual game where players fill in the page frames step by step and compare their answers with the correct OPT decisions.

## 🎮 What is this project?

The OPT (Optimal) page replacement algorithm is used in operating systems to decide which page to replace when a new page arrives and no free frames are available. This game lets you practice that idea by:

- generating a reference string of page requests,
- presenting a 3-frame simulation grid,
- asking you to fill in the correct page contents for each step,
- and showing the OPT-based replacements and explanations after you check your answers.

## ✨ Features

- Interactive GUI built with Python and Tkinter
- Dark-themed interface using ttkbootstrap
- Randomly generated reference strings
- Step-by-step puzzle gameplay
- Immediate feedback on correct and incorrect entries
- Explanation panel showing OPT decisions
- Copy reference string support

## 🧠 How to play

1. Run the game.
2. Enter a custom reference string (space-separated integers) or leave it blank to generate a random one.
3. Click “New Game”.
4. Fill the grid with the correct page numbers for each frame and time step.
5. Use blank, “-”, or “_” for empty cells.
6. Click “Check Answers” to see your results and the algorithm explanation.

## 🛠️ Requirements

- Python 3.8+
- ttkbootstrap

Install the dependency with:

```bash
pip install ttkbootstrap
```

## ▶️ Run the project

From the project folder, run:

```bash
python "OPT Algorithm game code.py"
```

## 📁 Project files

- `OPT Algorithm game code.py` — main game application
- `OPT Algorithm game.spec` — PyInstaller spec file for packaging the app
- `build/` — compiled build output
- `dist/` — packaged distribution files

## 🚀 Future ideas

- Add difficulty levels
- Add score tracking and timer
- Add sound effects and animations
- Support more frame counts
- Add a leaderboard or challenge mode

## 🙌 About

This project is a simple educational game designed to make the OPT algorithm easier to understand through hands-on interaction.
