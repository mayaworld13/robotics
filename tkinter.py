import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

theta_i = 0
theta_f = 0
T = 0

root = tk.Tk()
root.title("Polynomial Motion Profile Calculator")
root.configure(bg='orange')

def calculate():
    global theta_i, theta_f, T
    try:
        theta_i = float(entry_theta_i.get())
        theta_f = float(entry_theta_f.get())
        T = float(entry_T.get())

        if T == 0:
            messagebox.showerror("Error", "Time duration (T) cannot be zero.")
            return

        a = theta_i
        b = 0

        if T != 0:
            c = 3 * (theta_f - theta_i) / T ** 2
            d = -2 * (theta_f - theta_i) / T ** 3
        else:
            c = 0
            d = 0

        t = np.linspace(0, T, 1000)
        theta = a + b * t + c * t ** 2 + d * t ** 3
        theta_dot = b + 2 * c * t + 3 * d * t ** 2
        theta_double_dot = 2 * c + 6 * d * t

        if c == 0:
            t_max_velocity = float('inf')  
        else:
            t_max_velocity = -b / (2 * c)
        V_max = b + 2 * c * t_max_velocity + 3 * d * t_max_velocity ** 2
        A_max = 2 * c

        
        ax1.clear()
        ax1.plot(t, theta)
        ax1.set_title('Joint Position vs. Time')
        ax1.set_xlabel('Time (s)')
        ax1.set_ylabel('Position (degrees)')
        canvas_widget1.draw()

        ax2.clear()
        ax2.plot(t, theta_dot)
        ax2.set_title('Joint Velocity vs. Time')
        ax2.set_xlabel('Time (s)')
        ax2.set_ylabel('Velocity (degrees/s)')
        canvas_widget2.draw()

        ax3.clear()
        ax3.plot(t, theta_double_dot)
        ax3.set_title('Joint Acceleration vs. Time')
        ax3.set_xlabel('Time (s)')
        ax3.set_ylabel('Acceleration (degrees/s^2)')
        canvas_widget3.draw()

        lbl_v_max.config(text=f"Maximum Velocity (V_max): {V_max:.2f} degrees/s")
        lbl_a_max.config(text=f"Maximum Acceleration (A_max): {A_max:.2f} degrees/s^2")

    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please enter valid numerical values.")

def clear():
    global theta_i, theta_f
    entry_theta_i.delete(0, tk.END)
    entry_theta_f.delete(0, tk.END)
    entry_T.delete(0, tk.END)

    ax1.clear()
    ax1.set_title('Joint Position vs. Time')
    canvas_widget1.draw()

    ax2.clear()
    ax2.set_title('Joint Velocity vs. Time')
    canvas_widget2.draw()

    ax3.clear()
    ax3.set_title('Joint Acceleration vs. Time')
    canvas_widget3.draw()

    lbl_v_max.config(text="")
    lbl_a_max.config(text="")

frame = ttk.Frame(root)
frame.grid(column=0, row=0, padx=10, pady=10)

font = ("Helvetica", 12, "bold")
custom_style = ttk.Style()
custom_style.configure('Bold.TButton', font=font, foreground='blue')

lbl_theta_i = ttk.Label(frame, text="Initial Position (degrees):")
lbl_theta_i.grid(column=0, row=0, sticky=tk.W, pady=10)
lbl_theta_i.config(font=font)

entry_theta_i = ttk.Entry(frame)
entry_theta_i.grid(column=1, row=0, pady=10)

lbl_theta_f = ttk.Label(frame, text="Final Position (degrees):")
lbl_theta_f.grid(column=0, row=1, sticky=tk.W, pady=10)
lbl_theta_f.config(font=font)

entry_theta_f = ttk.Entry(frame)
entry_theta_f.grid(column=1, row=1, pady=10)

lbl_T = ttk.Label(frame, text="Time Duration (s):")
lbl_T.grid(column=0, row=2, sticky=tk.W, pady=10)
lbl_T.config(font=font)

entry_T = ttk.Entry(frame)
entry_T.grid(column=1, row=2, pady=10)

btn_calculate = ttk.Button(frame, text="Calculate", command=calculate, width=20, style='Bold.TButton')
btn_calculate.grid(column=0, row=3, columnspan=2, pady=10)

btn_clear = ttk.Button(frame, text="Clear", command=clear, width=20, style='Bold.TButton')
btn_clear.grid(column=0, row=4, columnspan=2, pady=10)

figure1 = plt.Figure(figsize=(5, 4.5))
ax1 = figure1.add_subplot(111)
canvas_widget1 = FigureCanvasTkAgg(figure1, master=root)
canvas_widget1.get_tk_widget().grid(row=1, column=0, pady=10)

figure2 = plt.Figure(figsize=(5, 4.5))
ax2 = figure2.add_subplot(111)
canvas_widget2 = FigureCanvasTkAgg(figure2, master=root)
canvas_widget2.get_tk_widget().grid(row=1, column=1, pady=10)

figure3 = plt.Figure(figsize=(5, 4.5))
ax3 = figure3.add_subplot(111)
canvas_widget3 = FigureCanvasTkAgg(figure3, master=root)
canvas_widget3.get_tk_widget().grid(row=1, column=2, pady=10)

lbl_v_max = ttk.Label(frame, text="", font=font)
lbl_v_max.grid(column=0, row=5, columnspan=2, pady=10)

lbl_a_max = ttk.Label(frame, text="", font=font)
lbl_a_max.grid(column=0, row=6, columnspan=2)

root.mainloop()
