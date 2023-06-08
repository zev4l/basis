# BASIS
> Bisca Agent Strategy Intelligent System, a multi-agent platform for implementing AI-driven strategies in the game of Bisca. 

This repository hosts our project for the course of Autonomous Agents and Multi-Agent Systems (AASMA) @ Instituto Superior Técnico for the year of 2022/2023.
### Authorship
#### Alameda, Group 30
* José Almeida (IST1105793)
* Pedro Moço (IST105773)
* Tiago Teodoro (IST1105720)

### Installation
This project is written in Python and makes use of a few external modules for purposes of UI and statistical plotting. Python 3.11 or newer is recommended.

In order to install all required dependencies, perform the following command at the project root.
```bash
pip install -r requirements.txt
```
> **Note**: change `pip` for `pip3` if the former isn't registered in your `$PATH`.

### Usage
#### UI
In order to interact with the platform via user-interface, you can launch it from the root of the project as follows.
```bash
./basis.py
```
> **Note**: In case this doesn't work, prefix it with `python` or `python3`.

#### Engine
The game engine offers a comprehensible interface, a simple example of using the internal engine is provided at `example.py`.

### Simulation
`simulate.py` is an included script that allows you to run simulations over the BASIS Multi-Agent Platform. It provides a command-line interface to specify simulation parameters and visualize the results. 

The simulation framework gathers and exposes metrics for each player such as total wins/draws/losses, win-rate, average points per game, and highest points obtained in a single trick.

> **Note**: Simulation doesn't support `Human` players, as its grand objective is to obtain data relative to long-term comparison of agent types. 

#### Syntax Overview

The script supports the following command-line arguments:

```plaintext
--iterations <int>      Number of simulations to run (default: 1000)
--delay <int>           Delay in seconds between each round (default: 0)
--player <type>         Player types to include (choices: all available agent types: RandomAgent, SimplyGreedyAgent, MinimizePointLossGreedyAgent, MPLGreedyTrumpSaveAgent, MPLGreedyTrumpBasedAgent)
--graph                 Display graph of simulation results
--interpolate           Interpolate graph for smoother visualization (useful for large number of iterations)
--save                  Saves obtained metrics to a JSON file
```

#### Examples
> **Note**: If, for some reason, the following instructions don't work for you, or you want to use a specific version of Python, prefix them with e.g. `python` or `python3`.

1. Run simulation with default parameters (1000 iterations with 2 `RandomAgent` and 2 `SimpleGreedyAgent`):
   ```bash
   ./simulate.py
   ```

2. Run simulation with specific player types:
   ```bash
   ./simulate.py --player RandomAgent SimpleGreedyAgent
   ```

3. Run 50 iterations and display the graph of simulation results:
   ```bash
   ./simulate.py --iterations 50 --graph --interpolate
   ```
   * The `--graph` option will display two sets of graphs in different tabs, one regarding overall player statistics, and another regarding per-iteration player statistics.

4. Run 10000 iterations with graph interpolation for smoother visualization, using specific agents, saving the obtained metrics to a JSON file:
   ```bash
   ./simulate.py --iterations 10000 --graph --interpolate --save --player RandomAgent SimpleGreedyAgent MinimizePointLossGreedyAgent MPLGreedyTrumpSaveAgent
   ```

> **Note** The `--interpolate` option is only valid if `--graph` is specified.

---