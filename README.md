# Meet MinePy
A '17 take on a 70s game !

[![forthebadge](http://forthebadge.com/images/badges/made-with-python.svg)](http://forthebadge.com) [![forthebadge](http://forthebadge.com/images/badges/contains-technical-debt.svg)](http://forthebadge.com)


<center> <img src="screenshots/minesweeper_demo.gif" alt="MinePy – Sayan Goswami"/> </center>

### What's cool ?
- Modular approach with OOP - game, board and cell
- Tunable parameters (use `constants.py`)
- Flood fill algorithm
- Multi-threading to avoid render blocking

### Build & run

1. Install [python_sdl](https://github.com/renpy/pygame_sdl2) for your platform
2. Clone the `conda` environment using `conda env create -f environment.yml`
3. Activate the environment - `source activate minesweeper_pygame`
4. Run the game !
    - `python3 game.py`

### Dependencies
- `pygame_sdl2`

### Todo

- [ ] Implement flagging system
