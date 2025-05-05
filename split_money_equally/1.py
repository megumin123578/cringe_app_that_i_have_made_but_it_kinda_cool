import tkinter as tk
from tkinter import messagebox

def calculate():
    raw_data = text_input.get("1.0", tk.END).strip().split('\n')
    people = []
    total = 0

    try:
        for line in raw_data:
            name, amount = line.split(',')
            amount = float(amount.strip())
            people.append((name.strip(), amount))
            total += amount
    except:
        messagebox.showerror("Input Error", "Hãy nhập theo định dạng: tên, số tiền (mỗi dòng 1 người)")
        return

    per_person = total / len(people)
    output_lines = [f"Tổng cộng: {total:.2f} đ", f"Mỗi người cần đóng: {per_person:.2f} đ", ""]

    balances = {name: round(amount - per_person, 2) for name, amount in people}
    givers = [(name, -bal) for name, bal in balances.items() if bal < 0]
    takers = [(name, bal) for name, bal in balances.items() if bal > 0]

    transactions = []

    g_index = 0
    t_index = 0

    while g_index < len(givers) and t_index < len(takers):
        giver_name, giver_owes = givers[g_index]
        taker_name, taker_gets = takers[t_index]
        amount = round(min(giver_owes, taker_gets), 2)

        transactions.append(f"{giver_name} trả {taker_name}: {amount:.2f} đ")

        givers[g_index] = (giver_name, round(giver_owes - amount, 2))
        takers[t_index] = (taker_name, round(taker_gets - amount, 2))

        if givers[g_index][1] == 0:
            g_index += 1
        if takers[t_index][1] == 0:
            t_index += 1

    result_output.delete("1.0", tk.END)
    result_output.insert(tk.END, "\n".join(output_lines + transactions))


# ----- GUI Setup -----
root = tk.Tk()
root.title("Chia Tiền Công Bằng")
root.geometry("500x500")

tk.Label(root, text="Nhập tên và số tiền (mỗi dòng 1 người, dạng: Tên, số tiền):").pack(pady=5)
text_input = tk.Text(root, height=10, width=60)
text_input.pack(pady=5)

tk.Button(root, text="Tính Chia Tiền", command=calculate, bg="#4CAF50", fg="white").pack(pady=10)

result_output = tk.Text(root, height=15, width=60)
result_output.pack(pady=10)

root.mainloop()
