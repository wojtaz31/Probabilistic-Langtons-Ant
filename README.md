# Probabilistic Langton's Ant

An advanced cellular automaton simulator that allows you to create stochastic variants of the classic Langton's Ant. The tool features a built-in graphical user interface (GUI) for creating advanced rulesets for simulations and supports JSON configuration files.

## Installation

I recommend using the `uv` package manager to setup the project.

### Option 1: Using `uv` (Recommended)

```bash
git clone https://github.com/wojtaz31/Probabilistic-Langtons-Ant.git
cd Probabilistic-Langtons-Ant
uv sync
```

### Option 2: Using `pip` (Traditional)

```bash
git clone [https://github.com/yourusername/stochastic-langtons-ant.git](https://github.com/yourusername/stochastic-langtons-ant.git)
cd stochastic-langtons-ant

python -m venv .venv
.venv\Scripts\activate
# For macOS/Linux: source .venv/bin/activate

pip install -e .
```

## Running the Simulation

To launch a clean interface and build the grid from scratch:

**Using `uv`:**
```bash
uv run main_gui.py
```

**Using `pip`:**
```bash
python main_gui.py
```

### Ready-to-use Variants (Rulesets)
The recommended way to start is by loading one of the provided examples. The program will automatically load the rules and start the simulation.

Example commands (using `uv`):
```bash
uv run main_gui.py --ruleset examples/classic_ruleset.json
uv run main_gui.py --ruleset examples/quantum_drunkard.json
```
*(If using pip, simply replace `uv run` with `python`)*

---

## Guide to advanced Rule Builder (GUI)

The program allows you to create complex rules directly. To build your own rule using GUI, follow these steps:

1. **Launch the Builder:** In the main side panel, scroll to the bottom and click the `[+] Open Rule Builder` button.
2. **Step 1: Base Color:** Determine on which grid tile color the new rule should act. 
   * *Tip:* The grid is white by default, so your first rule should always target the color `RGB (255, 255, 255)`.
3. **Step 2: Direction Probabilities:** Select an action from the dropdown menu (e.g., Turn Left, Straight) and enter its weight as a decimal fraction (e.g., `0.5`). Click **Add Action**. 
   * **Requirement:** The sum of the probabilities of all added actions must equal exactly `1.0`.
4. **Step 3: Color Probabilities:** Choose what color the tile will turn into after the ant leaves it. If the desired color is not in the panel, select `[+ Add New Color]` to use the color picker. Add weights accordingly. 
   * **Requirement:** The sum of the probabilities of the color changes must also equal exactly `1.0`.
5. **Save:** Click the large **SAVE AND VALIDATE RULE** button. The application will verify if the mathematical distributions are correct.
6. **Add an Ant:** Return to the main panel, click `Add Ant to board`, adjust the speed (`Delay` to 0, `Steps` to e.g., 5 for a smoother/faster visual effect), and click **START SIMULATION**.
   * *Tip:* You can add new Ants while the simulation is running.