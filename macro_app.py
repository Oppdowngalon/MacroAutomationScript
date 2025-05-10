import tkinter as tk
from tkinter import ttk, filedialog
import pyautogui
import time
import threading
import json

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
            self.action_list.delete(0, tk.END)
            for action in self.macro_actions:
                self.action_list.insert(tk.END, f"{action['type']}: {action['value']}")
            
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
        self.action_list.grid(row=0, column=0, padx=5, pady=5)

        add_action_button = ttk.Button(action_frame, text="Add Action", command=self.add_action_dialog)
        add_action_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        remove_action_button = ttk.Button(action_frame, text="Remove Action", command=self.remove_action)
        remove_action_button.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        # Settings Frame
        settings_frame = ttk.LabelFrame(self.root, text="Settings")
        settings_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        settings_frame.pack_propagate(False)
        settings_frame.update()

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

        # Control Frame
        control_frame = ttk.Frame(self.root)
        control_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.start_button = ttk.Button(control_frame, text="Start Macro", command=self.start_macro)
        self.start_button.grid(row=0, column=0, padx=5, pady=5)

        self.stop_button = ttk.Button(control_frame, text="Stop Macro", command=self.stop_macro, state=tk.DISABLED)
        self.stop_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.status_label = ttk.Label(control_frame, text="", font=('Arial', 10))
        self.status_label.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

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

        def show_mouse_coords():
            coord_window = tk.Toplevel(self.root)
            coord_window.title("Mouse Coordinates")
            coord_label = ttk.Label(coord_window, text="")
            coord_label.pack(padx=10, pady=10)

            def update_coords():
                x, y = pyautogui.position()
                coord_label.config(text=f"X: {x}, Y: {y}")
                coord_window.after(100, update_coords)

            update_coords()

        def update_mouse_coords(event=None):
            if action_type_combo.get() == "Click":
                show_mouse_coords()

        action_type_combo.bind("<<ComboboxSelected>>", update_mouse_coords)

        def add_action():
            action_type = action_type_combo.get()
            value = value_entry.get()
            self.macro_actions.append({"type": action_type, "value": value})
            self.action_list.insert(tk.END, f"{action_type}: {value}")
            dialog.destroy()

        add_button = ttk.Button(dialog, text="Add", command=add_action)
        add_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    def remove_action(self):
        selected_index = self.action_list.curselection()
        if selected_index:
            self.action_list.delete(selected_index)
            self.macro_actions.pop(selected_index[0])

    def start_macro(self):
        if not self.running:
            try:
                self.interval = float(self.interval_entry.get())
                self.loops = int(self.loops_entry.get())
                self.inter_loop_wait = float(self.inter_loop_wait_entry.get())
                self.pause_duration = float(self.pause_duration_entry.get())
                self.num_sets = int(self.num_sets_entry.get())
            except ValueError:
                print("Invalid interval or loop value")
                return

            self.running = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            time.sleep(5)
            threading.Thread(target=self.run_macro, daemon=True).start()

    def stop_macro(self):
        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def run_macro(self):
        total_sets = self.num_sets
        sets_completed = 0
        for set_num in range(total_sets):
            if not self.running:
                break
            next_set_start_time = time.localtime(time.time())
            next_set_start_str = time.strftime("%H:%M:%S", next_set_start_time)
            self.status_label.config(text=f"Starting set {set_num+1} of {total_sets}. Next set will start at {next_set_start_str}. Sets completed: {sets_completed}")
            self.root.update()
            total_loops = self.loops
            for i in range(total_loops):
                if not self.running:
                    break
                for action in self.macro_actions:
                    if not self.running:
                        break
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
                                x, y = map(int, value.split(","))
                                pyautogui.click(x, y)
                            else:
                                pyautogui.click()
                        elif action_type == "Move":
                            x, y = map(int, value.split(","))
                            pyautogui.moveTo(x, y)
                        time.sleep(self.interval)
                    except Exception as e:
                        print(f"Error executing action: {action}, {e}")
                        self.stop_macro()
                        return
                self.status_label.config(text=f"Loop {i+1} of {total_loops} completed in set {set_num+1} of {total_sets}. Sets completed: {sets_completed}")
                self.root.update()
                if i < total_loops - 1 and self.running:
                    time.sleep(self.inter_loop_wait)
            sets_completed += 1
            if set_num < total_sets - 1 and self.running:
                wait_minutes = self.pause_duration
                next_set_start_time = time.localtime(time.time() + wait_minutes * 60)
                next_set_start_str = time.strftime("%H:%M:%S", next_set_start_time)
                self.status_label.config(text=f"Waiting for {wait_minutes} minutes before next set. Next set will start at {next_set_start_str}. Sets completed: {sets_completed}")
                self.root.update()
                time.sleep(wait_minutes * 60)

        self.stop_macro()

if __name__ == "__main__":
    root = tk.Tk()
    app = MacroApp(root)
    root.mainloop()
