import tkinter as tk
from tkinter import ttk, messagebox

def generate_pattern():
    try:
        # Get input values
        input_val = int(entry_count.get())
        if input_val <= 0:
            raise ValueError
        
        mode = combo_mode.get()
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid positive integer.")
        return

    # 1 Y square always has 4 X squares in this pattern
    if mode == "Y squares":
        num_y = input_val
    else:
        # If X is specified, calculate how many Ys are needed (rounding up)
        num_y = (input_val + 3) // 4

    # Generate centers (Y) using the perfect packing lattice vectors: (1, -2) and (2, 1)
    centers = []
    search_range = int(num_y**0.5) + 3
    for i in range(-search_range, search_range + 1):
        for j in range(-search_range, search_range + 1):
            r = i * 1 + j * 2
            c = i * -2 + j * 1
            centers.append((r, c))
    
    # Sort by distance from origin (0,0) to ensure a tight, compact expansion
    centers.sort(key=lambda p: p[0]**2 + p[1]**2)
    chosen_centers = centers[:num_y]

    # Place cells in a dictionary to prevent duplicates and find grid boundaries
    grid = {}
    for r, c in chosen_centers:
        grid[(r, c)] = 'Y'
        # Cardinal neighbors
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if (r + dr, c + dc) not in grid:
                grid[(r + dr, c + dc)] = 'X'

    # Normalize coordinates to start from (0, 0) for GUI rendering
    min_r = min(r for r, c in grid.keys())
    min_c = min(c for r, c in grid.keys())
    max_r = max(r for r, c in grid.keys())
    max_c = max(c for r, c in grid.keys())

    # Clear previous canvas content
    canvas.delete("all")

    # Dynamic cell sizing based on grid size to fit the window
    grid_width = max_c - min_c + 1
    grid_height = max_r - min_r + 1
    cell_size = min(500 // grid_width, 500 // grid_height, 40)
    cell_size = max(cell_size, 15) # bound minimum size

    # Draw the grid cells
    for (r, c), val in grid.items():
        x1 = (c - min_c) * cell_size + 10
        y1 = (r - min_r) * cell_size + 10
        x2 = x1 + cell_size
        y2 = y1 + cell_size

        if val == 'Y':
            bg_color = "#3b82f6"  # Blue
            text_color = "white"
        else:
            bg_color = "#ef4444"  # Red
            text_color = "white"

        # Draw square
        canvas.create_rectangle(x1, y1, x2, y2, fill=bg_color, outline="#b91c1c" if val=='X' else "#1d4ed8", width=2)
        # Draw label text
        canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=val, fill=text_color, font=("Arial", int(cell_size * 0.4), "bold"))

# --- GUI Setup ---
root = tk.Tk()
root.title("Perfect Cross Tiling Generator")
root.geometry("600x650")  # Fixed syntax error here
root.resizable(True, True)

# Control Panel Frame
frame_controls = ttk.Frame(root, padding=10)
frame_controls.pack(fill=tk.X)

ttk.Label(frame_controls, text="Select Mode:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
combo_mode = ttk.Combobox(frame_controls, values=["Y squares", "X squares"], state="readonly", width=12)
combo_mode.set("Y squares")
combo_mode.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame_controls, text="Count:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
entry_count = ttk.Entry(frame_controls, width=10)
entry_count.insert(0, "4")  # Default to 4 like the image example
entry_count.grid(row=0, column=3, padx=5, pady=5)

btn_generate = ttk.Button(frame_controls, text="Generate Pattern", command=generate_pattern)
btn_generate.grid(row=0, column=4, padx=10, pady=5)

# Canvas Frame for Grid
canvas = tk.Canvas(root, bg="#ffffff", bd=2, relief=tk.SUNKEN)
canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Run initial generation
generate_pattern()

root.mainloop()