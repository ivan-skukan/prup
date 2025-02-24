import tkinter as tk
import tkinter.ttk as ttk

class Application:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.title("Raytracer")
        self.main_window.geometry("800x600")

        # Create the notebook
        self.notebook = ttk.Notebook(self.main_window)
        self.notebook.pack(expand=1, fill='both')

        # Create file menu
        self.menu_bar = tk.Menu(self.main_window)
        self.main_window.config(menu=self.menu_bar)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New")
        self.file_menu.add_command(label="Open")
        self.file_menu.add_command(label="Save")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.main_window.quit)

        # Create edit menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Undo")
        self.edit_menu.add_command(label="Redo")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut")

        # Create tabs
        self.tab1 = tk.Frame(self.notebook)
        self.tab2 = tk.Frame(self.notebook)
        self.notebook.add(self.tab1, text='Tab 1')
        self.notebook.add(self.tab2, text='Tab 2')

        # Create canvas and place it in canvas_frame
        self.canvas_frame = tk.Frame(self.tab1)
        self.canvas_frame.pack(expand=True, fill="both", padx=10, pady=10)

        self.canvas = tk.Canvas(self.canvas_frame, width=600, height=400)
        self.canvas.pack(expand=True, fill="both")

        # Create control frame below canvas
        self.control_frame = tk.Frame(self.main_window)
        self.control_frame.pack(pady=10, fill="x")

        # Buttons in control frame
        self.start_button = ttk.Button(self.control_frame, text="Start", command=self.start_rendering)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.pause_button = ttk.Button(self.control_frame, text="Pause", command=self.pause_rendering)
        self.pause_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = ttk.Button(self.control_frame, text="Stop", command=self.stop_rendering)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        # Draw a rectangle on the canvas to test if it's working
        self.canvas.create_rectangle(50, 50, 150, 150, fill="blue")
        # Start the GUI
        self.main_window.mainloop()

    def start_rendering(self):
        print("Rendering started")

    def pause_rendering(self):
        print("Rendering paused")

    def stop_rendering(self):
        print("Rendering stopped")


if __name__ == "__main__":
    app = Application()
