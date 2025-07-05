# Gear Design Tool Example

This repository contains a simple Python script to visualize involute gears.
The `gear_design_tool.py` script provides a GUI that lets you specify the
module, number of teeth and pressure angle for a spur gear. It then renders an
approximate tooth profile on a Tkinter canvas and allows exporting the point
coordinates as a CSV file.

## Requirements

The script only relies on the Python standard library (Tkinter and math). No
additional packages are needed.

## Usage

Run the script with Python:

```bash
python3 gear_design_tool.py
```

Fill in the parameters and press **Generate** to display the gear. Use
**Export CSV** to save the generated coordinates.
