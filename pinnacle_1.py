import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from calendar import monthrange, month_name
import datetime

class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calendar and Reminder App")
        self.current_month = datetime.datetime.now().month
        self.current_year = datetime.datetime.now().year
        self.reminders = {}
        self.create_widgets()

    def create_widgets(self):
        self.header = tk.Label(self.root, text=f"{month_name[self.current_month]} {self.current_year}", font=('Helvetica', 16))
        self.header.pack()

        self.calendar_frame = tk.Frame(self.root)
        self.calendar_frame.pack()

        self.update_calendar()

        self.reminder_button = tk.Button(self.root, text="Add Reminder", command=self.add_reminder)
        self.reminder_button.pack()

        self.view_reminders_button = tk.Button(self.root, text="View Reminders", command=self.view_reminders)
        self.view_reminders_button.pack()

    def update_calendar(self):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        days = monthrange(self.current_year, self.current_month)[1]
        weekday_start = datetime.datetime(self.current_year, self.current_month, 1).weekday()
        
        for day in ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]:
            tk.Label(self.calendar_frame, text=day).grid(row=0, column=["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"].index(day))

        for day in range(1, days + 1):
            day_label = tk.Label(self.calendar_frame, text=day, borderwidth=1, relief="solid", padx=10, pady=5)
            day_label.grid(row=(day + weekday_start - 1) // 7 + 1, column=(day + weekday_start - 1) % 7)
            day_label.bind("<Button-1>", lambda e, d=day: self.show_date(d))

    def show_date(self, day):
        date = datetime.date(self.current_year, self.current_month, day)
        messagebox.showinfo("Selected Date", f"You selected {date.strftime('%Y-%m-%d')}")

    def add_reminder(self):
        day = simpledialog.askinteger("Input", "Enter day of the month:")
        if not (1 <= day <= monthrange(self.current_year, self.current_month)[1]):
            messagebox.showerror("Invalid Input", "Please enter a valid day.")
            return
        reminder = simpledialog.askstring("Input", f"Enter reminder for {day}/{self.current_month}/{self.current_year}:")
        if reminder:
            date = datetime.date(self.current_year, self.current_month, day)
            if date in self.reminders:
                self.reminders[date].append(reminder)
            else:
                self.reminders[date] = [reminder]
            messagebox.showinfo("Reminder Added", f"Reminder for {date} added.")

    def view_reminders(self):
        date = simpledialog.askstring("Input", "Enter date (YYYY-MM-DD):")
        try:
            date_obj = datetime.datetime.strptime(date, '%Y-%m-%d').date()
            reminders = self.reminders.get(date_obj, [])
            if reminders:
                messagebox.showinfo("Reminders", "\n".join(reminders))
            else:
                messagebox.showinfo("No Reminders", "No reminders for this date.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid date in YYYY-MM-DD format.")

if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarApp(root)
    root.mainloop()
