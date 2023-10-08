# Snake

## to install and run:
run `pip install -r requirements.txt` (= install pygame)

then create a file 'Snake/settings.py' inside the top-level folder 'Snake' with following content:

```
from pathlib import Path

SOURCE = Path("")
```

then create a file 'Snake/highscore.json' inside the top-level folder 'Snake' with following content:

```
{}
```

then run `python3 Snake/menu.py`


## keys in game:
- in singleplayer-mode:
  **LEFT**, **RIGHT**, **UP**, **DOWN** for directions and **SPACE** for boost
- in multiplayer-mode:
  - green snake: **LEFT**, **RIGHT**, **UP**, **DOWN** for directions and **CTRL (RIGHT)** for boost
  - purple snake: **A**, **D**, **W**, **S** for directions and **CTRL (LEFT)** for boost
