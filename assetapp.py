import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from datetime import datetime

def calculate_depreciated_value(purchase_cost, eol_months, purchase_date, current_date):
    purchase_date = datetime.strptime(purchase_date, "%Y-%m-%d")
    current_date = datetime.strptime(current_date, "%Y-%m-%d")

    age_in_months = (current_date.year - purchase_date.year) * 12 + (current_date.month - purchase_date.month)
    depreciated_value = purchase_cost - (purchase_cost / eol_months * age_in_months)
    depreciated_value = max(depreciated_value, 0)

    return depreciated_value, age_in_months

def update_eol_display(*args):
    eol_option = eol_var.get()
    if eol_option in ["MAC", "WIN"]:
        eol_months = 48 if eol_option == "MAC" else 36
    else:
        eol_months = custom_eol_entry.get()
        try:
            eol_months = int(eol_months) if eol_months else 0
        except ValueError:
            eol_months = 0

    eol_display_label.config(text=f"{eol_months} months")

def add_entry():
    try:
        purchase_costs = purchase_cost_entry.get()
        purchase_dates = purchase_date_entry.get()

        purchase_costs = [float(cost.strip()) for cost in purchase_costs.split(",") if cost.strip()]
        purchase_dates = [date.strip() for date in purchase_dates.split(",") if date.strip()]

        if len(purchase_costs) != len(purchase_dates):
            messagebox.showerror("Input Error", "The number of purchase costs must match the number of purchase dates.")
            return

        eol_option = eol_var.get()

        if eol_option in ["MAC", "WIN"]:
            eol_months = 48 if eol_option == "MAC" else 36
        else:
            eol_months = custom_eol_entry.get()
            eol_months = int(eol_months) if eol_months.isdigit() else 0

        current_date = current_date_entry.get_date()
        current_date_str = current_date.strftime("%Y-%m-%d")

        # Insert a blank row for separation if there are existing entries
        if entries_tree.get_children():
            entries_tree.insert("", tk.END, values=("", "", "", "", "", ""))

        for purchase_cost, purchase_date in zip(purchase_costs, purchase_dates):
            try:
                purchase_date_obj = datetime.strptime(purchase_date, "%Y-%m-%d")
                purchase_date_str = purchase_date_obj.strftime("%Y-%m-%d")
                depreciated_value, age_in_months = calculate_depreciated_value(purchase_cost, eol_months, purchase_date_str, current_date_str)

                entries_tree.insert("", tk.END, values=(
                    purchase_cost,
                    eol_months,
                    purchase_date_str,
                    current_date_str,
                    age_in_months,
                    f"{depreciated_value:.2f}"
                ))
            except ValueError:
                messagebox.showerror("Input Error", f"Invalid date format for: {purchase_date}")

        # Clear input fields
        purchase_cost_entry.delete(0, tk.END)
        purchase_date_entry.delete(0, tk.END)
        custom_eol_entry.delete(0, tk.END)

    except ValueError as e:
        messagebox.showerror("Input Error", f"Invalid input: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def add_selected_date():
    selected_date = purchase_date_calendar.get_date()
    selected_date_str = selected_date.strftime("%Y-%m-%d")

    current_dates = purchase_date_entry.get()
    if current_dates:
        new_dates = current_dates + "," + selected_date_str
    else:
        new_dates = selected_date_str

    purchase_date_entry.delete(0, tk.END)
    purchase_date_entry.insert(0, new_dates)

def edit_selected_entry():
    selected_item = entries_tree.selection()
    if not selected_item:
        messagebox.showerror("Selection Error", "No entry selected for editing.")
        return

    item = entries_tree.item(selected_item)
    values = item['values']

    # Pre-fill the inputs with selected row's values
    purchase_cost_entry.delete(0, tk.END)
    purchase_cost_entry.insert(0, values[0])

    purchase_date_entry.delete(0, tk.END)
    purchase_date_entry.insert(0, values[2])

    custom_eol_entry.delete(0, tk.END)
    custom_eol_entry.insert(0, values[1])

    def save_edits():
        try:
            new_cost = float(purchase_cost_entry.get())
            new_date = purchase_date_entry.get()
            new_eol = int(custom_eol_entry.get()) if custom_eol_entry.get().isdigit() else 0

            current_date = current_date_entry.get_date()
            current_date_str = current_date.strftime("%Y-%m-%d")

            new_depreciated_value, new_age_in_months = calculate_depreciated_value(new_cost, new_eol, new_date, current_date_str)

            entries_tree.item(selected_item, values=(
                new_cost,
                new_eol,
                new_date,
                current_date_str,
                new_age_in_months,
                f"{new_depreciated_value:.2f}"
            ))

            purchase_cost_entry.delete(0, tk.END)
            purchase_date_entry.delete(0, tk.END)
            custom_eol_entry.delete(0, tk.END)
        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid input: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    save_button = tk.Button(edit_frame, text="Save Changes", command=save_edits)
    save_button.pack(side=tk.LEFT, padx=5)

# Apply customization
def apply_customization():
    font_color = color_var.get()
    font_size = int(size_var.get())
    font_style = style_var.get()

    for widget in root.winfo_children():
        widget_type = widget.winfo_class()
        if widget_type in ['Label', 'Button', 'Entry']:
            widget.config(fg=font_color, font=(font_style, font_size))

# Right-click menu
def open_customization_menu(event):
    customization_menu.post(event.x_root, event.y_root)

# Customization window
def open_customization_window():
    customization_window = tk.Toplevel(root)
    customization_window.title("Customize Appearance")
    customization_window.geometry("300x200")

    tk.Label(customization_window, text="Font Color:").grid(row=0, column=0, padx=10, pady=5)
    tk.OptionMenu(customization_window, color_var, "black", "red", "green", "blue", "purple").grid(row=0, column=1, padx=10, pady=5)

    tk.Label(customization_window, text="Font Size:").grid(row=1, column=0, padx=10, pady=5)
    tk.Spinbox(customization_window, from_=8, to=36, textvariable=size_var).grid(row=1, column=1, padx=10, pady=5)

    tk.Label(customization_window, text="Font Style:").grid(row=2, column=0, padx=10, pady=5)
    tk.OptionMenu(customization_window, style_var, "Helvetica", "Arial", "Times New Roman", "Courier New").grid(row=2, column=1, padx=10, pady=5)

    tk.Button(customization_window, text="Apply", command=apply_customization).grid(row=3, column=0, columnspan=2, pady=10)

# Initialize the main window
root = tk.Tk()
root.title("Asset Depreciation Calculator")

# Initialize customization variables
#color_var = tk.StringVar(value="black")
#size_var = tk.StringVar(value="12")
#style_var = tk.StringVar(value="Helvetica")

# Create customization menu
#customization_menu = tk.Menu(root, tearoff=0)
#customization_menu.add_command(label="Customize Appearance", command=open_customization_window)

root.bind("<Button-3>", open_customization_menu)

# Remaining GUI code...
tk.Label(root, text="Purchase Costs (INR, separate multiple values with commas):").grid(row=0, column=0, padx=10, pady=5)
purchase_cost_entry = tk.Entry(root)
purchase_cost_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Purchase Dates (YYYY-MM-DD, separated by commas):").grid(row=1, column=0, padx=10, pady=5)
purchase_date_entry = tk.Entry(root)
purchase_date_entry.grid(row=1, column=1, padx=10, pady=5)

purchase_date_calendar = DateEntry(root, date_pattern='yyyy-mm-dd', width=20)
purchase_date_calendar.grid(row=2, column=1, padx=10, pady=5)

add_date_button = tk.Button(root, text="Add Selected Date", command=add_selected_date)
add_date_button.grid(row=2, column=2, padx=10, pady=5)

tk.Label(root, text="Select Platform:").grid(row=3, column=0, padx=10, pady=5)
eol_var = tk.StringVar(root)
eol_var.set("")
eol_var.trace("w", update_eol_display)
eol_options = ["MAC", "WIN", "Custom"]
eol_menu = tk.OptionMenu(root, eol_var, *eol_options)
eol_menu.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Custom EOL Months:").grid(row=4, column=0, padx=10, pady=5)
custom_eol_entry = tk.Entry(root)
custom_eol_entry.grid(row=4, column=1, padx=10, pady=5)

eol_frame = tk.Frame(root)
eol_frame.grid(row=5, column=2, padx=10, pady=5)

eol_label = tk.Label(eol_frame, text="EOL:", font=("Helvetica", 14))
eol_label.pack(side=tk.LEFT)

eol_display_label = tk.Label(eol_frame, text=" ", font=("Helvetica", 14), borderwidth=2, relief="solid", width=10)
eol_display_label.pack(side=tk.LEFT)

tk.Label(root, text="Current Date:").grid(row=6, column=0, padx=10, pady=5)
current_date_entry = DateEntry(root, date_pattern='yyyy-mm-dd', width=20)
current_date_entry.grid(row=6, column=1, padx=10, pady=5)

tk.Button(root, text="SUBMIT", command=add_entry).grid(row=7, column=0, columnspan=3, pady=10)
tk.Button(root, text="Edit Selected Entry", command=edit_selected_entry).grid(row=8, column=0, columnspan=3, pady=10)

edit_frame = tk.Frame(root)
edit_frame.grid(row=9, column=1, padx=5, pady=5)

columns = ("Purchase Cost", "EOL Months", "Purchase Date", "Current Date", "Age (Months)", "Depreciated Value")
entries_tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    entries_tree.heading(col, text=col)
    entries_tree.column(col, anchor="center", width=130)

entries_tree.grid(row=10, column=0, columnspan=3, pady=10)

root.mainloop()

