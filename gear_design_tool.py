# Gear Design Tool using Tkinter
import tkinter as tk
from tkinter import filedialog, messagebox
import math
import csv


class GearDesigner(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gear Design Tool")
        self.geometry("800x600")

        # Parameters frame
        params = tk.Frame(self)
        params.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        tk.Label(params, text="Module:").grid(row=0, column=0, sticky=tk.W)
        self.module_var = tk.DoubleVar(value=1.0)
        tk.Entry(params, textvariable=self.module_var, width=10).grid(row=0, column=1)

        tk.Label(params, text="Teeth:").grid(row=0, column=2, sticky=tk.W)
        self.teeth_var = tk.IntVar(value=20)
        tk.Entry(params, textvariable=self.teeth_var, width=10).grid(row=0, column=3)

        tk.Label(params, text="Pressure Angle (deg):").grid(row=0, column=4, sticky=tk.W)
        self.angle_var = tk.DoubleVar(value=20.0)
        tk.Entry(params, textvariable=self.angle_var, width=10).grid(row=0, column=5)

        tk.Button(params, text="Generate", command=self.generate).grid(row=0, column=6, padx=5)
        tk.Button(params, text="Export CSV", command=self.export_csv).grid(row=0, column=7, padx=5)

        # Canvas for drawing gear
        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.points = []

    def generate(self):
        m = self.module_var.get()
        z = self.teeth_var.get()
        alpha = math.radians(self.angle_var.get())
        self.points = compute_gear_points(m, z, alpha)
        self.draw_points(self.points)

    def draw_points(self, pts):
        self.canvas.delete("all")
        if not pts:
            return
        # Determine scale
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        max_r = max(max(abs(x) for x in xs), max(abs(y) for y in ys))
        # Leave some padding
        pad = 20
        w = int(self.canvas.winfo_width())
        h = int(self.canvas.winfo_height())
        scale = min((w-2*pad)/(2*max_r), (h-2*pad)/(2*max_r))
        cx = w/2
        cy = h/2
        # Convert to canvas coords
        canvas_pts = []
        for x, y in pts:
            canvas_pts.append(cx + x*scale)
            canvas_pts.append(cy - y*scale)
        self.canvas.create_polygon(canvas_pts, outline="black", fill="", width=1)

    def export_csv(self):
        if not self.points:
            messagebox.showerror("Error", "No gear data to export")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV","*.csv")])
        if not path:
            return
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["x", "y"])
            writer.writerows(self.points)
        messagebox.showinfo("Saved", f"Points saved to {path}")


def involute_angle(r, base_r):
    if r < base_r:
        return 0
    t = math.sqrt(r*r - base_r*base_r) / base_r
    return t - math.atan(t)


def compute_gear_points(module, teeth, alpha_rad, points_per_tooth=30):
    pitch_radius = module * teeth / 2.0
    base_radius = pitch_radius * math.cos(alpha_rad)
    outer_radius = pitch_radius + module
    root_radius = pitch_radius - 1.25 * module
    pitch_angle = 2 * math.pi / teeth

    pts = []
    for i in range(teeth):
        angle_base = i * pitch_angle
        # left flank
        for j in range(points_per_tooth + 1):
            r = base_radius + (outer_radius - base_radius) * j / points_per_tooth
            th = angle_base - pitch_angle/4 + involute_angle(r, base_radius)
            x = r * math.cos(th)
            y = r * math.sin(th)
            pts.append((x, y))
        # right flank
        for j in range(points_per_tooth, -1, -1):
            r = base_radius + (outer_radius - base_radius) * j / points_per_tooth
            th = angle_base + pitch_angle/4 - involute_angle(r, base_radius)
            x = r * math.cos(th)
            y = r * math.sin(th)
            pts.append((x, y))
        # root arc to next tooth
        next_angle = (i + 1) * pitch_angle - pitch_angle/4
        for j in range(points_per_tooth):
            th = angle_base + pitch_angle/4 + (next_angle - (angle_base + pitch_angle/4)) * (j / points_per_tooth)
            x = root_radius * math.cos(th)
            y = root_radius * math.sin(th)
            pts.append((x, y))
    return pts


if __name__ == "__main__":
    app = GearDesigner()
    app.mainloop()
