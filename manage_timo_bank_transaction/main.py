import tkinter as tk
from tkinter import ttk
from datetime import datetime
import calendar
import subprocess

def run_analysis():
    month = int(month_var.get())
    year = int(year_var.get())

    subprocess.run(["python", "email_analysis.py", str(month), str(year)])

# Giao diện chính
root = tk.Tk()
root.title("Phân tích giao dịch Timo")

tk.Label(root, text="Chọn tháng:").grid(row=0, column=0, padx=10, pady=10)
tk.Label(root, text="Chọn năm:").grid(row=1, column=0, padx=10, pady=10)

month_var = tk.StringVar()
year_var = tk.StringVar()

month_combo = ttk.Combobox(root, textvariable=month_var, values=[f"{i:02}" for i in range(1, 13)], width=10)
month_combo.grid(row=0, column=1)
month_combo.set(datetime.now().strftime("%m"))

current_year = datetime.now().year
year_combo = ttk.Combobox(root, textvariable=year_var, values=[str(current_year - i) for i in range(3)], width=10)
year_combo.grid(row=1, column=1)
year_combo.set(str(current_year))

analyze_btn = tk.Button(root, text="Phân tích", command=run_analysis)
analyze_btn.grid(row=2, column=0, columnspan=2, pady=20)

root.mainloop()
