import tkinter as tk
from Sonicator_Setup import Arduino_Sonicator
import PyTime_master.GS_timing as timing
from tkinter import messagebox
import serial


def process():

    try: 
        input_cycle_reps = int(cycle_reps.get())
        input_time_on = float(time_on.get())
        input_time_off = float(time_off.get())
        input_voltage = float(voltage.get())
    except ValueError:
        messagebox.showwarning("Error","Error: Please enter numeric values.")
        return
    
    inputs = [
        input_cycle_reps,
        input_time_on,
        input_time_off,
        input_voltage
    ]
    
    print(input_voltage)
    
    output_label.config(text = "Setting voltage")
    try:
        sonicator = Arduino_Sonicator()
    except:
        messagebox.showwarning("Error","Error: COM Port not connected.")
        return
    sonicator.set_initial_voltage()
    
    sonicator.set_ADC_value(value = input_voltage)
    for i in range(input_cycle_reps):
        output_label.config(text = f"Sonication Cycle {i+1}")
        root.update()
        sonicator.turn_sonicator_horn_on()
        timing.delay(input_time_on*1000)
        sonicator.turn_sonicator_horn_off()
        timing.delay(input_time_off*1000)

    sonicator.turn_sonicator_horn_off()
    sonicator.close_serial_port()
    
    output_label.config(text="Completed")

def start_process():
    # Disable the "Start" button during process
    start_button.config(state=tk.DISABLED)

    # Check if any inputs are missing
    if any([
        cycle_reps.get() == "",
        time_on.get() == "",
        time_off.get() == "",
        voltage.get() == ""
    ]):
        # Display error message if any input is missing
        messagebox.showwarning("Error","Error: Please fill out all inputs")
    else:
        # Call the process function if all inputs are provided
        process()
        output_label.config(text="Completed")  # Process completed message

    # Enable the "Start" button after completion or error
    start_button.config(state=tk.NORMAL)




root = tk.Tk()
root.geometry("155x340")
root.title("Sonicator Controller")
root.iconbitmap("Transparent_Icon.ico")
root.tk.call("source", "sun-valley.tcl")
root.tk.call("set_theme", "dark")

# Input labels

label2 = tk.Label(root, text="Input Cycle Repetitions:")
label2.grid(padx = 5,pady = 5)
# label2.pack()
cycle_reps = tk.Entry(root)
cycle_reps.grid(padx = 5,pady = 5)

label3 = tk.Label(root, text="Input Time On (s):")
label3.grid(padx = 5,pady = 5)
time_on = tk.Entry(root)
time_on.grid(padx = 5,pady = 5)

label4 = tk.Label(root, text="Input Time Off (s):")
label4.grid(padx = 5,pady = 5)
time_off = tk.Entry(root)
time_off.grid(padx = 5,pady = 5)

label5 = tk.Label(root, text="Input Voltage (2-5 V):")
label5.grid(padx = 5,pady = 5)
voltage = tk.Entry(root)
voltage.grid(padx = 5,pady = 5)

# Start button
start_button = tk.Button(root, text="Start", command=start_process)
start_button.grid(padx = 5,pady = 5)

# Output label
output_label = tk.Label(root, text="")
output_label.grid(padx = 5,pady = 5)

root.mainloop()
