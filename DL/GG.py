import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from datetime import datetime

class TaskQuestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Quest - Gamify Your Tasks")
        self.tasks = []
        self.points = 0
        self.streak = 0
        self.level = 1
        self.health = 100

        # Main frame
        self.frame = ttk.Frame(self.root, padding=15)
        self.frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.frame, text="Add a new task with deadline (format: task:YYYY-MM-DD):").grid(row=0, column=0, sticky=tk.W)

        self.task_entry = ttk.Entry(self.frame, width=40)
        self.task_entry.grid(row=1, column=0, sticky=tk.W, pady=5)
        self.add_btn = ttk.Button(self.frame, text="Add Task", command=self.add_task)
        self.add_btn.grid(row=1, column=1, sticky=tk.W, padx=5)

        self.tasks_list_label = ttk.Label(self.frame, text="Tasks:")
        self.tasks_list_label.grid(row=2, column=0, sticky=tk.W, pady=(10,0))

        self.tasks_frame = ttk.Frame(self.frame)
        self.tasks_frame.grid(row=3, column=0, columnspan=2, sticky=tk.NSEW)
        self.tasks_scrollbar = ttk.Scrollbar(self.tasks_frame)
        self.tasks_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tasks_listbox = tk.Listbox(self.tasks_frame, width=60, height=12, yscrollcommand=self.tasks_scrollbar.set)
        self.tasks_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.tasks_scrollbar.config(command=self.tasks_listbox.yview)

        self.complete_btn = ttk.Button(self.frame, text="Complete Task", command=self.complete_task)
        self.complete_btn.grid(row=4, column=0, sticky=tk.W, pady=5)
        self.delete_btn = ttk.Button(self.frame, text="Delete Task", command=self.delete_task)
        self.delete_btn.grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)

        self.status_frame = ttk.Frame(self.frame)
        self.status_frame.grid(row=5, column=0, columnspan=2, sticky=tk.EW, pady=10)
        self.points_label = ttk.Label(self.status_frame, text=f"Points: {self.points}")
        self.points_label.pack(side=tk.LEFT, padx=5)
        self.level_label = ttk.Label(self.status_frame, text=f"Level: {self.level}")
        self.level_label.pack(side=tk.LEFT, padx=5)
        self.streak_label = ttk.Label(self.status_frame, text=f"Streak: {self.streak}")
        self.streak_label.pack(side=tk.LEFT, padx=5)
        self.health_label = ttk.Label(self.status_frame, text=f"Health: {self.health}")
        self.health_label.pack(side=tk.LEFT, padx=5)
        self.progress_label = ttk.Label(self.status_frame, text="Progress to next level:")
        self.progress_label.pack(side=tk.LEFT, padx=(15,5))
        self.level_progress = ttk.Progressbar(self.status_frame, length=150, maximum=100)
        self.level_progress.pack(side=tk.LEFT)

        # Menu Bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        self.gamify_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Gamify Features", menu=self.gamify_menu)
        self.gamify_menu.add_command(label="View Achievements", command=self.view_achievements)
        self.gamify_menu.add_command(label="Customize Avatar", command=self.customize_avatar)

        # Achievement flags
        self.achievements = {
            "Task Master": False,
            "Night Owl": False,
            "First Quest": False,
            "Streak 5": False,
            "Level 5": False
        }
        self.avatar = { "hat": "None", "color": "Blue" }

        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(3, weight=1)

    def add_task(self):
        task_text = self.task_entry.get().strip()
        if ":" not in task_text or len(task_text.split(":")) < 2:
            messagebox.showerror("Input Error", "Please enter task in the format: task:YYYY-MM-DD")
            return
        task, deadline = task_text.split(":", 1)
        task = task.strip()
        deadline = deadline.strip()
        quest_flag = messagebox.askyesno("Quest Task", "Mark this task as a 'Quest' for extra rewards?")
        self.tasks.append({"task": task, "deadline": deadline, "completed": False, "quest": quest_flag})
        display_text = f"{task} (Due: {deadline})" + (" [Quest]" if quest_flag else "")
        self.tasks_listbox.insert(tk.END, display_text)
        self.task_entry.delete(0, tk.END)

    def complete_task(self):
        selected = self.tasks_listbox.curselection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a task to complete.")
            return
        index = selected[0]
        task = self.tasks[index]
        if task["completed"]:
            messagebox.showinfo("Info", "This task is already completed.")
            return
        today = datetime.now().date()
        try:
            deadline_date = datetime.strptime(task["deadline"], "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Date Error", "Deadline date format is incorrect. Use YYYY-MM-DD.")
            return
        on_time = today <= deadline_date
        if on_time:
            reward_points = 10
            self.streak += 1
            if task["quest"]:
                reward_points += 10
                if not self.achievements["First Quest"]:
                    self.achievements["First Quest"] = True
                    messagebox.showinfo("Achievement Unlocked!", "You unlocked the 'First Quest' achievement!")
        else:
            reward_points = 5
            self.streak = 0
            self.health -= 10
            if self.health < 0:
                self.health = 0
        # Night Owl achievement (if completed after 10PM)
        if datetime.now().hour >= 22 and not self.achievements["Night Owl"]:
            self.achievements["Night Owl"] = True
            messagebox.showinfo("Achievement Unlocked!", "You unlocked the 'Night Owl' achievement!")
        self.points += reward_points
        task["completed"] = True
        display_text = f"{task['task']} (Completed)" + (" [Quest]" if task["quest"] else "")
        self.tasks_listbox.delete(index)
        self.tasks_listbox.insert(index, display_text)
        self.level = 1 + self.points // 100
        self.check_achievements()
        self.update_status()

    def delete_task(self):
        selected = self.tasks_listbox.curselection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a task to delete.")
            return
        index = selected[0]
        self.tasks_listbox.delete(index)
        del self.tasks[index]

    def update_status(self):
        self.points_label.config(text=f"Points: {self.points}")
        self.level_label.config(text=f"Level: {self.level}")
        self.streak_label.config(text=f"Streak: {self.streak}")
        self.health_label.config(text=f"Health: {self.health}")
        self.level_progress['value'] = (self.points % 100)

    def check_achievements(self):
        if self.streak >= 5 and not self.achievements["Streak 5"]:
            self.achievements["Streak 5"] = True
            messagebox.showinfo("Achievement Unlocked!", "You unlocked the '5-day Streak' achievement!")
        if self.level >= 5 and not self.achievements["Level 5"]:
            self.achievements["Level 5"] = True
            messagebox.showinfo("Achievement Unlocked!", "You unlocked the 'Level 5' achievement!")
        if all(t["completed"] for t in self.tasks) and self.tasks and not self.achievements["Task Master"]:
            self.achievements["Task Master"] = True
            messagebox.showinfo("Achievement Unlocked!", "You unlocked the 'Task Master' achievement!")

    def view_achievements(self):
        achievements_text = "Achievements:\n"
        for a, unlocked in self.achievements.items():
            achievements_text += f"- {a}: {'Unlocked' if unlocked else 'Locked'}\n"
        messagebox.showinfo("Achievements", achievements_text)

    def customize_avatar(self):
        color = simpledialog.askstring("Avatar Color", "Enter your avatar color (e.g., Blue, Red, Green):", initialvalue=self.avatar["color"])
        if color:
            self.avatar["color"] = color
        hat = simpledialog.askstring("Avatar Hat", "Enter hat style (None, Cap, Wizard, Crown):", initialvalue=self.avatar["hat"])
        if hat:
            self.avatar["hat"] = hat
        messagebox.showinfo("Avatar Updated", f"Avatar set to Color: {self.avatar['color']}, Hat: {self.avatar['hat']}")

def main():
    root = tk.Tk()
    app = TaskQuestApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
