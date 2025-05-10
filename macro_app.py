import tkinter as tk
from tkinter import ttk, filedialog
import pyautogui
import time
import threading
import json
from pynput import mouse # Added pynput

try:
    from ctypes import windll
    # Set process DPI awareness for Windows. 
    # 1 means System Aware. For Windows 8.1+
    # For Per-Monitor V2 awareness (more complex to handle): windll.shcore.SetProcessDpiAwarenessContext(-4) 
    windll.shcore.SetProcessDpiAwareness(1) 
except AttributeError:
    # Fallback for older Windows (Vista, 7) or if shcore is not available
    try:
        windll.user32.SetProcessDPIAware()
    except Exception as e_old:
        print(f"Info: Could not set DPI awareness (older method) - {e_old}")
except Exception as e:
    print(f"Info: Could not set DPI awareness - {e} (This is usually fine on non-Windows or if already set by other means)")

class MacroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Macro Automation")

        self.macro_actions = []
        self.interval = 0.1
        self.loops = 1
        self.inter_loop_wait = 0
        self.running = False

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.create_widgets()
        self.create_menu()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Save Actions", command=self.save_actions)
        file_menu.add_command(label="Load Actions", command=self.load_actions)
        menubar.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menubar)

    def save_actions(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if not file_path:
            return

        data = {
            "actions": self.macro_actions,
            "settings": {
                "interval": self.interval,
                "loops": self.loops,
                "inter_loop_wait": self.inter_loop_wait,
                "pause_duration": float(self.pause_duration_entry.get()),
                "num_sets": int(self.num_sets_entry.get())
            }
        }

        try:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=4)
            self.status_label.config(text=f"Actions saved to {file_path}")
        except Exception as e:
            self.status_label.config(text=f"Error saving file: {str(e)}")

    def _refresh_action_list(self):
        self.action_list.delete(0, tk.END)
        for action in self.macro_actions:
            self.action_list.insert(tk.END, f"{action['type']}: {action['value']}")

    def load_actions(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if not file_path:
            return

        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Load actions
            self.macro_actions = data.get('actions', [])
            self._refresh_action_list() # Use helper
            
            # Load settings
            settings = data.get('settings', {})
            self.interval = settings.get('interval', 0.1)
            self.loops = settings.get('loops', 1)
            self.inter_loop_wait = settings.get('inter_loop_wait', 0)
            
            # Update UI
            self.interval_entry.delete(0, tk.END)
            self.interval_entry.insert(0, str(self.interval))
            self.loops_entry.delete(0, tk.END)
            self.loops_entry.insert(0, str(self.loops))
            self.inter_loop_wait_entry.delete(0, tk.END)
            self.inter_loop_wait_entry.insert(0, str(self.inter_loop_wait))
            self.pause_duration_entry.delete(0, tk.END)
            self.pause_duration_entry.insert(0, str(settings.get('pause_duration', 0)))
            self.num_sets_entry.delete(0, tk.END)
            self.num_sets_entry.insert(0, str(settings.get('num_sets', 1)))
            
            self.status_label.config(text=f"Actions loaded from {file_path}")
        except Exception as e:
            self.status_label.config(text=f"Error loading file: {str(e)}")

    def create_widgets(self):
        self.style.configure('TLabel', background='#f2f2f2', foreground='#333', font=('Arial', 10))
        self.style.configure('TButton', background='#4CAF50', foreground='white', font=('Arial', 10))
        self.style.configure('TEntry', fieldbackground='#fff', foreground='#333', font=('Arial', 10))
        self.style.configure('TListbox', fieldbackground='#fff', foreground='#333', font=('Arial', 10), borderwidth=0, highlightthickness=0)
        self.style.configure('TLabelframe', background='#f2f2f2', bordercolor='#ddd', borderwidth=1)
        self.style.configure('TLabelframe.Label', background='#f2f2f2', foreground='#333', font=('Arial', 10, 'bold'))
        self.style.configure('TCombobox', fieldbackground='#fff', foreground='#333', font=('Arial', 10))

        # Action Frame
        action_frame = ttk.LabelFrame(self.root, text="Macro Actions")
        action_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.action_list = tk.Listbox(action_frame, width=50, height=10, relief='flat')
        self.action_list.grid(row=0, column=0, padx=5, pady=5, sticky="nsew") # Added sticky
        action_frame.grid_rowconfigure(0, weight=1) # Allow listbox to expand
        action_frame.grid_columnconfigure(0, weight=1) # Allow listbox to expand


        add_action_button = ttk.Button(action_frame, text="Add Action", command=self.add_action_dialog)
        add_action_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        remove_action_button = ttk.Button(action_frame, text="Remove Action", command=self.remove_action)
        remove_action_button.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        edit_action_button = ttk.Button(action_frame, text="Edit Action", command=self.edit_action_dialog)
        edit_action_button.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

        move_up_button = ttk.Button(action_frame, text="Move Up", command=self.move_action_up)
        move_up_button.grid(row=4, column=0, padx=5, pady=5, sticky="ew")

        move_down_button = ttk.Button(action_frame, text="Move Down", command=self.move_action_down)
        move_down_button.grid(row=5, column=0, padx=5, pady=5, sticky="ew")

        # Settings Frame
        settings_frame = ttk.LabelFrame(self.root, text="Settings")
        settings_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ewns") # Added sticky
        self.root.grid_columnconfigure(0, weight=1) # Allow action_frame to take space
        self.root.grid_columnconfigure(1, weight=1) # Allow settings_frame to take space
        self.root.grid_rowconfigure(0, weight=1) # Allow frames row to take space


        ttk.Label(settings_frame, text="Interval (sec):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.interval_entry = ttk.Entry(settings_frame)
        self.interval_entry.insert(0, "0.1")
        self.interval_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(settings_frame, text="Loops:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.loops_entry = ttk.Entry(settings_frame)
        self.loops_entry.insert(0, "1")
        self.loops_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(settings_frame, text="Wait Time Between Loops (sec):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.inter_loop_wait_entry = ttk.Entry(settings_frame)
        self.inter_loop_wait_entry.insert(0, "0")
        self.inter_loop_wait_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(settings_frame, text="Pause Duration (minutes):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.pause_duration_entry = ttk.Entry(settings_frame)
        self.pause_duration_entry.insert(0, "0")
        self.pause_duration_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(settings_frame, text="Number of Sets:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.num_sets_entry = ttk.Entry(settings_frame)
        self.num_sets_entry.insert(0, "1")
        self.num_sets_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
        
        settings_frame.grid_columnconfigure(1, weight=1) # Allow entry widgets to expand

        # Control Frame
        control_frame = ttk.Frame(self.root)
        control_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.start_button = ttk.Button(control_frame, text="Start Macro", command=self.start_macro)
        self.start_button.grid(row=0, column=0, padx=5, pady=5)

        self.stop_button = ttk.Button(control_frame, text="Stop Macro", command=self.stop_macro, state=tk.DISABLED)
        self.stop_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.status_label = ttk.Label(control_frame, text="", font=('Arial', 10))
        self.status_label.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        
        control_frame.grid_columnconfigure(1, weight=1) # Allow stop button and status label to expand

    def add_action_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Macro Action")

        ttk.Label(dialog, text="Action Type:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        action_type_combo = ttk.Combobox(dialog, values=["Type", "Press", "HotKey", "Click", "Move"])
        action_type_combo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        action_type_combo.set("Type")

        ttk.Label(dialog, text="Value:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        value_entry = ttk.Entry(dialog)
        value_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # "Capture Position" button for "Click" type
        capture_pos_button = ttk.Button(dialog, text="Capture Position", 
                                        command=lambda: self._start_coordinate_capture(value_entry, dialog))
        # Initially hidden, shown when "Click" is selected.
        # Placed on a new row, e.g. row 2, and Add/Cancel buttons shift to row 3.

        def toggle_capture_button_state(event=None):
            if action_type_combo.get() == "Click":
                capture_pos_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
            else:
                capture_pos_button.grid_remove()

        action_type_combo.bind("<<ComboboxSelected>>", toggle_capture_button_state)
        # Call once to set initial state
        toggle_capture_button_state() 

        def add_action():
            action_type = action_type_combo.get()
            value = value_entry.get()
            self.macro_actions.append({"type": action_type, "value": value})
            self._refresh_action_list() # Use helper
            dialog.destroy()

        # Add/Cancel buttons now on row 3
        add_button = ttk.Button(dialog, text="Add", command=add_action)
        add_button.grid(row=3, column=0, padx=5, pady=5) # Adjusted column span and placement
        
        cancel_button = ttk.Button(dialog, text="Cancel", command=dialog.destroy)
        cancel_button.grid(row=3, column=1, padx=5, pady=5) # Added cancel button

        dialog.grid_columnconfigure(1, weight=1)


    def remove_action(self):
        selected_index = self.action_list.curselection()
        if selected_index:
            self.macro_actions.pop(selected_index[0])
            self._refresh_action_list() # Use helper

    def edit_action_dialog(self):
        selected_index_tuple = self.action_list.curselection()
        if not selected_index_tuple:
            return # No item selected
            
        selected_index = selected_index_tuple[0]
        action = self.macro_actions[selected_index]
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Macro Action")

        ttk.Label(dialog, text="Action Type:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        action_type_combo = ttk.Combobox(dialog, values=["Type", "Press", "HotKey", "Click", "Move"])
        action_type_combo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        action_type_combo.set(action["type"])

        ttk.Label(dialog, text="Value:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        value_entry = ttk.Entry(dialog)
        value_entry.insert(0, action["value"])
        value_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # "Capture Position" button for "Click" type
        capture_pos_button_edit = ttk.Button(dialog, text="Capture Position", 
                                             command=lambda: self._start_coordinate_capture(value_entry, dialog))
        # Initially hidden, shown when "Click" is selected.
        # Placed on row 2, Update/Cancel buttons shift to row 3.

        def toggle_capture_button_state_edit(event=None):
            if action_type_combo.get() == "Click":
                capture_pos_button_edit.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
            else:
                capture_pos_button_edit.grid_remove()

        action_type_combo.bind("<<ComboboxSelected>>", toggle_capture_button_state_edit)
        # Call once to set initial state
        toggle_capture_button_state_edit()

        def update_action():
            new_type = action_type_combo.get()
            new_value = value_entry.get()
            self.macro_actions[selected_index] = {"type": new_type, "value": new_value}
            self._refresh_action_list() # Use helper
            # Reselect the item
            self.action_list.selection_set(selected_index)
            self.action_list.activate(selected_index)
            self.action_list.see(selected_index)
            dialog.destroy()

        # Update/Cancel buttons now on row 3
        update_button = ttk.Button(dialog, text="Update", command=update_action)
        update_button.grid(row=3, column=0, padx=5, pady=5) # Adjusted row

        cancel_button = ttk.Button(dialog, text="Cancel", command=dialog.destroy)
        cancel_button.grid(row=3, column=1, padx=5, pady=5) # Adjusted row
        
        dialog.grid_columnconfigure(1, weight=1)

    def _start_coordinate_capture(self, value_entry_widget, dialog_window):
        # This method will be called to capture a single mouse click globally
        # It needs to run the listener in a way that doesn't block Tkinter's main loop
        # and communicates the result back to the value_entry_widget.

        dialog_window.withdraw() # Hide the dialog

        # Define the click callback
        def on_click(x, y, button, pressed):
            if pressed: # Capture on mouse button press
                coords_str = f"{x},{y}"
                value_entry_widget.delete(0, tk.END)
                value_entry_widget.insert(0, coords_str)
                dialog_window.deiconify() # Show the dialog again
                self.status_label.config(text="") # Clear status on successful capture
                # Stop the listener after one click
                return False 
        
        # Start the listener
        # The listener runs in its own thread by default
        listener = mouse.Listener(on_click=on_click)
        listener.start()
        # No join here, as it would block. Listener stops itself.
        # We might need a way to inform the user that capture mode is active.
        # For now, hiding the dialog serves as an indicator.
        self.status_label.config(text="Click anywhere on screen to capture coordinates...")
        # Removed problematic self.root.after line


    def move_action_up(self):
        selected_index_tuple = self.action_list.curselection()
        if not selected_index_tuple:
            return
        selected_index = selected_index_tuple[0]

        if selected_index > 0:
            action = self.macro_actions.pop(selected_index)
            self.macro_actions.insert(selected_index - 1, action)
            self._refresh_action_list()
            self.action_list.selection_set(selected_index - 1)
            self.action_list.activate(selected_index - 1)
            self.action_list.see(selected_index - 1)


    def move_action_down(self):
        selected_index_tuple = self.action_list.curselection()
        if not selected_index_tuple:
            return
        selected_index = selected_index_tuple[0]

        if selected_index < len(self.macro_actions) - 1:
            action = self.macro_actions.pop(selected_index)
            self.macro_actions.insert(selected_index + 1, action)
            self._refresh_action_list()
            self.action_list.selection_set(selected_index + 1)
            self.action_list.activate(selected_index + 1)
            self.action_list.see(selected_index + 1)

    def start_macro(self):
        if not self.running:
            try:
                self.interval = float(self.interval_entry.get())
                self.loops = int(self.loops_entry.get())
                self.inter_loop_wait = float(self.inter_loop_wait_entry.get())
                self.pause_duration = float(self.pause_duration_entry.get())
                self.num_sets = int(self.num_sets_entry.get())
            except ValueError:
                self.status_label.config(text="Error: Invalid interval, loop, or wait value.")
                return

            if not self.macro_actions:
                self.status_label.config(text="No actions to run.")
                return

            self.running = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.status_label.config(text="Macro starting in 5 seconds...")
            self.root.after(5000, lambda: threading.Thread(target=self.run_macro, daemon=True).start())


    def stop_macro(self):
        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="Macro stopped by user.")

    def run_macro(self):
        total_sets_to_run = self.num_sets
        
        for current_set in range(1, total_sets_to_run + 1):
            if not self.running: break
            self.status_label.config(text=f"Running Set {current_set}/{total_sets_to_run}...")
            self.root.update_idletasks()

            total_loops_to_run = self.loops
            for current_loop in range(1, total_loops_to_run + 1):
                if not self.running: break
                self.status_label.config(text=f"Set {current_set}/{total_sets_to_run} - Loop {current_loop}/{total_loops_to_run}...")
                self.root.update_idletasks()

                for action_index, action in enumerate(self.macro_actions):
                    if not self.running: break
                    
                    # Highlight current action in listbox
                    self.action_list.selection_clear(0, tk.END)
                    self.action_list.selection_set(action_index)
                    self.action_list.activate(action_index)
                    self.action_list.see(action_index)
                    self.root.update_idletasks()

                    action_type = action["type"]
                    value = action["value"]
                    try:
                        if action_type == "Type":
                            pyautogui.typewrite(value)
                        elif action_type == "Press":
                            pyautogui.press(value)
                        elif action_type == "HotKey":
                            keys = value.split("+")
                            pyautogui.hotkey(*keys)
                        elif action_type == "Click":
                            if value:
                                x_phys, y_phys = map(int, value.split(","))
                                try:
                                    # Ensure root window is updated to get correct fpixels
                                    self.root.update_idletasks() 
                                    scale_factor = self.root.winfo_fpixels('1i') / 96.0
                                    if scale_factor <= 0: # Safety check
                                        scale_factor = 1.0
                                except Exception: 
                                    scale_factor = 1.0 # Default if detection fails
                                
                                # Multiply by scale_factor to counteract pyautogui's implicit division
                                x_adjusted = int(round(x_phys * scale_factor))
                                y_adjusted = int(round(y_phys * scale_factor))
                                pyautogui.click(x_adjusted, y_adjusted)
                            else:
                                pyautogui.click() # Click at current mouse position (no coords to adjust)
                        elif action_type == "Move":
                            x, y = map(int, value.split(","))
                            pyautogui.moveTo(x, y)
                        time.sleep(self.interval)
                    except Exception as e:
                        self.status_label.config(text=f"Error: {str(e)}. Stopping.")
                        self.stop_macro() # Ensure GUI updates
                        return
                
                if current_loop < total_loops_to_run and self.running:
                    self.status_label.config(text=f"Set {current_set}/{total_sets_to_run} - Waiting for next loop ({self.inter_loop_wait}s)...")
                    self.root.update_idletasks()
                    time.sleep(self.inter_loop_wait)
            
            if current_set < total_sets_to_run and self.running:
                self.status_label.config(text=f"Set {current_set}/{total_sets_to_run} completed. Waiting for next set ({self.pause_duration}m)...")
                self.root.update_idletasks()
                time.sleep(self.pause_duration * 60)

        if self.running: # If macro completed all sets and loops without interruption
            self.status_label.config(text="Macro finished.")
            self.stop_macro() # Ensure GUI updates to normal state

if __name__ == "__main__":
    root = tk.Tk()
    app = MacroApp(root)
    root.mainloop()
