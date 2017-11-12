# Python-Keyboard-Simulator

A simple Python script for simulating and listening for keystrokes in a Windows environment. When toggled on via backtick, it simulates a predefined rotation of keystrokes until toggled off.

## About

The leveling rotation for an Arcanist in FF14 is so boring that I looked for a way to simulate keystrokes in Python. Once I worked through that, I needed a way to toggle the script off and on so I could chat or take over when needed.

### Pros

- Simulation of keystrokes in a Windows environment.
- Simplistic rotation of keystrokes based on damage per second. Useful for basic MMO ability rotations or other repetitive tasks.
- Independent threads for simulating and listening for keystrokes

### Cons/To Do

- Read from a config file to determine keystrokes and their characteristics; currently hard coded.
- Improve the rotation algorithm so it can handle more advanced MMO features (currently only damage of time effects and direct damage)
- Improve the rotation aglorithm so it re-evaluates the order of keys to press based on context
