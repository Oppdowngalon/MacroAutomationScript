# Macro Automation Application

This Python application provides a graphical interface for automating mouse and keyboard actions using Tkinter. It allows users to create complex automation sequences with precise timing control.

## Features

- **Action Sequencing**: Create sequences of actions including:
  - Typing text
  - Pressing keys
  - Using hotkeys (key combinations)
  - Mouse clicks at specific coordinates
  - Mouse movements to specific positions
- **Action Management**:
  - Add, edit, and remove actions
  - Reorder actions with drag-and-drop functionality
  - Set individual delays for each action
- **Save & Load**:
  - Save entire macro configurations (actions + settings) to JSON files
  - Load saved configurations from JSON files
- **Interactive Coordinate Capture**:
  - Click anywhere on screen to capture X,Y coordinates for mouse actions
- **Advanced Settings**:
  - Interval: Time (seconds) between actions
  - Loops: Number of times to repeat the sequence
  - Wait Time Between Loops: Delay after completing a loop
  - Pause Duration: Longer breaks between sets of loops
  - Number of Sets: How many looping cycles to execute
- **Execution Control**:
  - Start/stop macro execution at any time
  - Visual countdown before execution begins
- **Status Monitoring**:
  - Real-time status updates
  - Estimated time of completion (ETA)
- **DPI Scaling Support**:
  - Improved coordinate accuracy for multi-monitor setups with different display scaling

## Dependencies

The application requires the following Python packages:
- pyautogui
- pynput

Install them using:
```bash
pip install pyautogui pynput
```

## Installation

1. Ensure you have Python 3.6+ installed
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python macro_app.py
   ```

## Usage

1. **Adding Actions**:
   - Click "Add Action" and select an action type
   - For click actions, use "Capture Position" to record coordinates
   - Set individual delays for each action
   
2. **Managing Actions**:
   - Use the action list to view, edit, reorder, or remove actions
   - Drag actions to reorder them in the sequence

3. **Configuring Settings**:
   - Set the interval between actions (seconds)
   - Configure loop count and wait time between loops
   - Set pause duration and number of sets for longer automation sessions

4. **Saving/Loading**:
   - Use File > Save Actions to save your configuration
   - Use File > Load Actions to load a saved configuration

5. **Execution**:
   - Click "Start Macro" to begin (10-second countdown will start)
   - Click "Stop Macro" to halt execution at any time

### Action Types

| Type   | Description                                                                 | Example Values              |
|--------|-----------------------------------------------------------------------------|-----------------------------|
| Type   | Types the specified text                                                    | "Hello World"               |
| Press  | Presses a specific key                                                      | "enter", "tab", "a", "1"    |
| HotKey | Presses a combination of keys                                               | "ctrl+s", "alt+f4"          |
| Click  | Clicks at specified coordinates (use "Capture Position" or enter "X,Y")     | "100,200"                   |
| Move   | Moves mouse cursor to specified coordinates                                 | "300,400"                   |

## JSON Configuration

Macro configurations are saved in JSON format with the following structure:
```json
{
  "actions": [
    {
      "type": "Click",
      "value": "100,200",
      "delay": 0.5
    },
    {
      "type": "Type",
      "value": "Hello World",
      "delay": 0
    }
  ],
  "settings": {
    "interval": 0.1,
    "loops": 5,
    "inter_loop_wait": 1.0,
    "pause_duration": 5.0,
    "num_sets": 3
  }
}
```

## Building from Source (Optional)

To create a standalone executable:

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```
   
2. Build the executable:
   ```bash
   pyinstaller --noconsole --onefile macro_app.py
   ```
   
3. The executable will be in the `dist` folder

## File Structure

The application consists of:
- `macro_app.py`: Main application script
- `requirements.txt`: Dependency list
- `README.md`: Documentation (this file)

## Technical Notes

- Built with Python 3.9+ and Tkinter for the GUI
- Uses pyautogui for automation and pynput for global click capture
- Coordinates are based on your primary screen's top-left corner (0,0)
- Implements DPI awareness for accurate positioning on scaled displays
- Multi-threaded execution to keep the UI responsive during automation

## Troubleshooting

- **Coordinates not accurate on multi-monitor setups**:
  Ensure all displays have the same scaling percentage or adjust DPI awareness settings
- **Macro stops unexpectedly**:
  Check that no dialogs or notifications are interrupting the automation
- **Key presses not registering**:
  Ensure the target application has focus and is not blocked by other windows
