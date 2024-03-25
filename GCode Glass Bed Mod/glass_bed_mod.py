import tkinter as tk
from tkinter import filedialog, ttk

class GCodeEditor:
    # Initializes the GCodeEditor class
    def __init__(self, root):
        self.root = root
        self.setup_ui()
        self.filename = ''

    # Sets up the UI elements
    def setup_ui(self):
        self.root.title('GCode Layer Configuration Editor')
        self.root.geometry('700x500')
        self.root.configure(bg='#333')

        self.layer_option = tk.StringVar()
        self.layer_option.set("Layer 1")  # default value
        self.layer_options = ['Layer 1', 'Layer 2', 'Layer 3']
        self.layer_menu = ttk.Combobox(self.root, textvariable=self.layer_option, values=self.layer_options, state="readonly", font=('Arial', 12))
        self.layer_menu.pack(pady=20)
        self.layer_menu.bind("<<ComboboxSelected>>", self.update_fields)

        self.fields = {}
        for setting in ["Print Speed", "Nozzle Temperature", "Bed Temperature"]:
            self.create_field(setting)
        
        self.open_button = tk.Button(self.root, text="Open GCode File", command=self.open_file, fg='white', bg='#666', font=('Arial', 12))
        self.open_button.pack(pady=10)

        self.save_button = tk.Button(self.root, text="Save GCode File", command=self.save_file, fg='white', bg='#666', font=('Arial', 12))
        self.save_button.pack(pady=10)

        # Initialize fields with default values for layer 1
        self.update_fields(None)

    # Creates a field for the given setting
    def create_field(self, setting):
        frame = tk.Frame(self.root, bg='#333')
        frame.pack(pady=10)

        label = tk.Label(frame, text=setting, bg='#333', fg='white', font=('Arial', 12))
        label.pack(side=tk.LEFT, padx=10)

        entry_var = tk.StringVar()
        entry = tk.Entry(frame, textvariable=entry_var, bg='#fff', fg='#000', font=('Arial', 12))
        entry.pack(side=tk.RIGHT, padx=10)
        self.fields[setting] = entry_var

    # Updates the fields with the selected layer's settings
    def update_fields(self, event):
        # Hardcoding layer defaults directly within the update function
        layer_defaults = {
            "Layer 1": {"Print Speed": "5", "Nozzle Temperature": "215", "Bed Temperature": "70"},
            "Layer 2": {"Print Speed": "40", "Nozzle Temperature": "210", "Bed Temperature": "65"},
            "Layer 3": {"Print Speed": "150", "Nozzle Temperature": "200", "Bed Temperature": "60"}
        }
        layer = self.layer_option.get()
        for setting, entry_var in self.fields.items():
            entry_var.set(layer_defaults[layer][setting])

    # Handles opening the GCode file
    def open_file(self):
        self.filename = filedialog.askopenfilename(filetypes=[("GCode Files", "*.gcode"), ("All Files", "*.*")])
        if self.filename:
            print(f"File opened: {self.filename}")

    # Handles saving and modifying the GCode file
    def save_file(self):
        if not self.filename:
            print("No file loaded")
            return
        
        # Hardcoding layer defaults directly within the save function
        layer_defaults = {
            "Layer 1": {"Print Speed": "5", "Nozzle Temperature": "215", "Bed Temperature": "70"},
            "Layer 2": {"Print Speed": "40", "Nozzle Temperature": "210", "Bed Temperature": "65"},
            "Layer 3": {"Print Speed": "150", "Nozzle Temperature": "200", "Bed Temperature": "60"}
        }

        # Hardcoding the identifiers for our custom settings in the G-code
        setting_identifiers = ["; Set Nozzle Temperature", "; Set Bed Temperature", "; Set Print Speed"]

        with open(self.filename, 'r') as file:
            lines = file.readlines()

        layer_count = -1
        modified_lines = []
        for line in lines:
            if line.startswith(';LAYER:'):
                layer_count += 1
            if layer_count < 3:
                # If the line contains any of our setting identifiers, skip adding it to modified_lines
                if not any(identifier in line for identifier in setting_identifiers):
                    modified_lines.append(line)
            else:
                modified_lines.append(line)

        layer_count = -1
        for i, line in enumerate(modified_lines):
            if line.startswith(';LAYER:'):
                layer_count += 1
                if layer_count <= 2:  # Modify only for the first three layers
                    layer_settings = layer_defaults[f"Layer {layer_count + 1}"]
                    # Inserting actual G-code for temperature changes and an example print speed change
                    settings_string = f"M104 S{layer_settings['Nozzle Temperature']} ; Set Nozzle Temperature\nM140 S{layer_settings['Bed Temperature']} ; Set Bed Temperature\nG1 F{layer_settings['Print Speed']} ; Set Print Speed\n; Adjustments for Layer {layer_count + 1}\n"
                    modified_lines[i] = modified_lines[i] + settings_string
                else: # Use Layer 3 settings for all subsequent layers
                    layer_settings = layer_defaults["Layer 3"]
                    # Ensuring that the print speed setting is applied only where specified, without duplicating it unnecessarily
                    settings_string = f"M104 S{layer_settings['Nozzle Temperature']} ; Set Nozzle Temperature\nM140 S{layer_settings['Bed Temperature']} ; Set Bed Temperature\n; Adjustments for subsequent layers\n"
                    modified_lines[i] = modified_lines[i] + settings_string
        
        # Open GCode file and write the modified lines
        with open(self.filename, 'w') as file:
            file.writelines(modified_lines)
        print(f"Settings saved to file: {self.filename}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GCodeEditor(root)
    root.mainloop()
