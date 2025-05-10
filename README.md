# Macro Automation Script

This script allows you to automate mouse and keyboard actions using a user-friendly graphical interface built with Tkinter.

## Features

*   **Define Action Sequences:** Add various actions like typing, key presses, hotkeys, mouse clicks, and mouse movements.
*   **Action Management:**
    *   **Add Actions:** Easily add new actions to your sequence.
    *   **Edit Actions:** Modify the type or value of existing actions.
    *   **Remove Actions:** Delete actions from the sequence.
    *   **Reorder Actions:** Use "Move Up" and "Move Down" buttons to change the order of actions.
*   **Save & Load:**
    *   Save your entire macro sequence (actions and settings) to a JSON file.
    *   Load previously saved macros to reuse them. (Accessible via File menu)
*   **Interactive Click Coordinate Capture:**
    *   For "Click" actions, a "Capture Position" button allows you to click anywhere on your screen to automatically record the X,Y coordinates.
*   **Flexible Settings:**
    *   **Interval:** Time (seconds) between each action.
    *   **Loops:** Number of times the entire action sequence will repeat.
    *   **Wait Time Between Loops:** Delay (seconds) after one full sequence loop completes and before the next begins.
    *   **Pause Duration:** Time (minutes) to pause between sets of loops.
    *   **Number of Sets:** How many times the entire looping cycle (including pauses) should run.
*   **Execution Control:** Start and stop the macro at any time.
*   **Status Display:** View the current status and progress of the macro execution.
*   **DPI Scaling Aware (Windows):** Includes logic to improve coordinate accuracy for "Click" actions in multi-monitor setups with different display scaling percentages.

## How to Use

1.  **Prerequisites:** Ensure you have Python installed, along with the necessary libraries.
    ```bash
    pip install pyautogui pynput
    ```
2.  **Run the Script:**
    ```bash
    python macro_app.py
    ```
3.  The GUI will open.
    *   Use the "Add Action", "Edit Action", "Remove Action", "Move Up", "Move Down" buttons to manage your macro sequence.
    *   For "Click" actions, use the "Capture Position" button in the Add/Edit dialog.
    *   Configure settings (Interval, Loops, etc.) in the right-hand panel.
    *   Use "File > Save Actions" to save your work and "File > Load Actions" to load it.
    *   Click "Start Macro" to run. Click "Stop Macro" to halt execution.

### Action Types

*   **Type:** Types the specified text.
*   **Press:** Presses a specific key. Common key names include:
    *   Special keys: `enter`, `esc`, `space`, `tab`, `backspace`, `delete`, `insert`
    *   Navigation: `home`, `end`, `pageup`, `pagedown`, `up`, `down`, `left`, `right`
    *   Modifier keys: `ctrl`, `alt`, `shift`, `win` (Windows key), `command` (Mac), `option` (Mac)
    *   Function keys: `f1`, `f2`, ..., `f12`
    *   Toggle keys: `capslock`, `numlock`, `scrolllock`
    *   Others: `printscreen`
    *   Alphanumeric keys (e.g., `a`, `b`, `1`, `2`) can also be used.
*   **HotKey:** Presses a combination of keys (e.g., `ctrl+s`, `alt+f4`). Separate keys with `+`.
*   **Click:** Performs a mouse click. Use the "Capture Position" button to set coordinates, or manually enter as "X,Y". If no coordinates are provided, it clicks at the current mouse position.
*   **Move:** Moves the mouse cursor to "X,Y" coordinates.

## Building from Source (Optional)

If you wish to create a standalone executable:
1.  Install PyInstaller: `pip install pyinstaller`
2.  Navigate to the script's directory in your terminal.
3.  Run PyInstaller with the provided spec file (`macro_app.spec`), or generate a new one:
    ```bash
    pyinstaller --noconsole --onefile macro_app.py
    ```
    (You can add `--add-data "icon.ico:."` or other options if needed). The executable will be in the `dist` folder.

## Notes

*   The script uses `tkinter` for the GUI, `pyautogui` for automation, and `pynput` for global click capture.
*   For "Click" and "Move" actions, coordinates are based on your primary screen's top-left corner being (0,0).
*   On Windows, the script attempts to be DPI aware to improve coordinate accuracy on scaled displays.
