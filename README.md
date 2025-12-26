
# Traffic Light Simulation and Queue Management System

This project simulates a smart 4-way traffic intersection designed for **Left-Hand Traffic** systems. The core objective of this project is to demonstrate efficient **Queue Management** using a **Priority Queue** algorithm.

Unlike standard traffic lights that use a fixed-timer, this system implements a **dynamic priority logic** i.e. Hysteresis control. This system specifically monitors the North-bound lane (Road A, Lane 2). If traffic congestion in this priority lane exceeds a critical threshold (10 vehicles), the system overrides the standard traffic signal cycle to flush the queue of that lane, optimizing traffic flow.

## Demo Output


## System Architecture
The project is designed with a **Producer-Consumer** architecture using file I/O as the communication buffer.

- `traffic_generator.py` acts as the **Producer** that randomly generates vehicles arrivals based on probability. It then writes vehicle IDs that are timestamped into buffer files in the `lane_data/` directory.

- `visualizer.py` acts as the **Consumer** that reads buffer files in the `lane_data` directory to spawn vehicles in the GUI. It renders the intersection along with the vehicles using the `pygame` module. It also executes the traffic light state machine and physics engine.


## Features
- **Priority Logic**: This system monitors the lane L2 of road A. If the queue length for that lane exceeds 10 vehicles, it triggers a "Priority Mode" that sets and holds the green light for AL2 lane until the queue drops to 5 or fewer vehicles.
- **Left-Hand Traffic (LHT)**: Vehicles follow LHT rules, standard in Nepal and the UK.
- **Real-time Visualization**: `visualizer.py` is built with `pygame`, which features visual cues for traffic light along with glowing effects, moving vehicles, and lane markings.
- **Dynamic Traffic Generation**: A separate generator script `traffic_generator.py` simulates varying vehicle loads by writing data to file buffers in real-time.
- **Metrics Tracking**: `metrics.py` tracks total vehicles served overall along with vehicles served per lane.

## Installation & Prerequisites

This project requires **Python 3.x** to run as intended. So, ensure you have **Python 3.x** installed.

You can check your installed Python version by typing the command `python --version` in the terminal.

1. **Install Dependencies**

The only external dependecy required is `pygame` for the visualization.
```bash
pip install pygame 
```
If you have multiple Python versions, use:
```bash
pip3 install pygame
```
The recommended method of installation is inside a **Virtual Environment**:
```bash
python -m venv venv
source venv/bin/activate    # for Linux/ macOS
venv\Scripts\activate       # for Windows
pip install pygame
```
On **Linux** systems, you can use different package managers to install `pygame`:
```bash
sudo pacman -S python-pygame       # Arch / Omarchy
sudo apt install python3-pygame    # Ubuntu / Debian
sudo dnf install python3-pygame    # Fedora
```

2. **Environment Setup**

Clone the repository:
```bash
git clone https://github.com/pxrbat/traffic-light-simulation-dsa.git
```
Ensure the folder looks like this:
```
/traffic-light-simulation-dsa/
    |── `lane_data`/  # Created automatically after running `traffic_generator.py`
    |── `src`/
        |── `intersection.py`
        |── `lane.py`
        |── `metrics.py`
        |── `priority_queue.py`
        |── `queue_ds.py`
        |── `road.py`
        |── `simulator.py`
        |── `traffic_generator.py`
        |── `traffic_light.py`
        |── `vehicle.py`
        |── `visualizer.py`
    |── `.gitignore`
    |── `README.md`
```
