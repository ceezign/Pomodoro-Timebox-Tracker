import tkinter as tk
from tkinter import ttk, messagebox
import time
import csv
from datetime import datetime

try:
    from plyer import notification  # For desktop notifications

    USE_NOTIFICATIONS = True
except ImportError:
    USE_NOTIFICATIONS = False  # Fallback to Tkinter alerts if plyer is not installed


# ==========================
# Pomodoro Timebox Tracker (Improved)
# ==========================
# Features:
#  - Start, Pause/Resume, Reset, and Skip controls
#  - Customizable Focus and Break lengths
#  - Optional Long Break after N focus sessions
#  - Optional task name field already included
#  - Fully commented for easy learning
#  - Countdown timer with progress bar
#  - Auto-switch between Focus and Break sessions
#  - Notifications (Desktop if plyer installed, else Tkinter popup)
#  - Session history saved to CSV file (task name optional)
# ==========================

class PomodoroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timebox Tracker")

        # ==========================
        # Variables (State Management)
        # ==========================
        self.focus_minutes = tk.IntVar(value=25)  # Default focus time: 25 min
        self.break_minutes = tk.IntVar(value=5)  # Default short break: 5 min
        self.long_break_minutes = tk.IntVar(
            value=15)  # Default long break: 15 min
        self.sessions_before_long = tk.IntVar(
            value=4)  # Take a long break after 4 focus sessions
        self.task_name = tk.StringVar()  # Optional task name input

        self.mode = "Focus"  # Current mode (Focus / Break / Long Break)
        self.remaining_seconds = 0  # Remaining countdown time
        self.running = False  # Timer state (running or paused)
        self.completed_sessions = 0  # Counter for finished focus sessions

        # Build the GUI
        self.create_widgets()

    def create_widgets(self):
        # Create all widgets in the Tkinter GUI.

        # Focus / Break input fields
        tk.Label(self.root, text="Focus (min):").grid(row=0, column=0)
        tk.Entry(self.root, textvariable=self.focus_minutes, width=5).grid(
            row=0, column=1)

        tk.Label(self.root, text="Break (min):").grid(row=0, column=2)
        tk.Entry(self.root, textvariable=self.break_minutes, width=5).grid(
            row=0, column=3)

        # Long break inputs
        tk.Label(self.root, text="Long Break (min):").grid(row=1, column=0)
        tk.Entry(self.root, textvariable=self.long_break_minutes,
                 width=5).grid(row=1, column=1)

        tk.Label(self.root, text="Sessions before Long Break:").grid(row=1,
                                                                     column=2)
        tk.Entry(self.root, textvariable=self.sessions_before_long,
                 width=5).grid(row=1, column=3)

        # Task name input (optional)
        tk.Label(self.root, text="Task (optional):").grid(row=2, column=0)
        tk.Entry(self.root, textvariable=self.task_name, width=30).grid(row=2,
                                                                        column=1,
                                                                        columnspan=3)

        # Mode label
        self.mode_label = tk.Label(self.root, text="Mode: Focus",
                                   font=("Arial", 12))
        self.mode_label.grid(row=3, column=0, columnspan=4)

        # Timer display
        self.timer_label = tk.Label(self.root, text="25:00",
                                    font=("Arial", 32))
        self.timer_label.grid(row=4, column=0, columnspan=4)

        # Progress bar
        self.progress = ttk.Progressbar(self.root, length=300,
                                        mode="determinate")
        self.progress.grid(row=5, column=0, columnspan=4, pady=10)

        # Completed sessions summary
        self.summary_label = tk.Label(self.root, text="Completed sessions: 0")
        self.summary_label.grid(row=6, column=0, columnspan=4)

        # Control buttons
        tk.Button(self.root, text="Start", command=self.start_timer).grid(
            row=7, column=0)
        tk.Button(self.root, text="Pause", command=self.pause_timer).grid(
            row=7, column=1)
        tk.Button(self.root, text="Resume", command=self.resume_timer).grid(
            row=7, column=2)
        tk.Button(self.root, text="Reset", command=self.reset_timer).grid(
            row=7, column=3)
        tk.Button(self.root, text="Skip", command=self.skip_session).grid(
            row=8, column=0, columnspan=4, pady=5)

    # ==========================
    # Timer Control Functions
    # ==========================
    def start_timer(self):
        # Start a new session depending on the mode (Focus, Break, Long Break).
        if self.mode == "Focus":
            self.remaining_seconds = self.focus_minutes.get() * 60
        elif self.mode == "Break":
            self.remaining_seconds = self.break_minutes.get() * 60
        else:  # Long Break
            self.remaining_seconds = self.long_break_minutes.get() * 60

        self.update_timer_display()
        self.running = True
        self.update_timer()

    def pause_timer(self):
        # Pause the countdown timer.
        self.running = False

    def resume_timer(self):
        # Resume the countdown timer if paused.
        if not self.running and self.remaining_seconds > 0:
            self.running = True
            self.update_timer()

    def reset_timer(self):
        # Reset the timer and return to default state.
        self.running = False
        self.remaining_seconds = 0
        self.mode = "Focus"
        self.timer_label.config(text=f"{self.focus_minutes.get():02d}:00")
        self.mode_label.config(text="Mode: Focus")
        self.progress['value'] = 0

    def skip_session(self):
        # Skip the current session immediately.
        self.running = False
        self.session_finished()

    # ==========================
    # Timer Update Logic
    # ==========================
    def update_timer(self):
        # Update the countdown every second.
        if self.running and self.remaining_seconds > 0:
            mins, secs = divmod(self.remaining_seconds, 60)
            self.timer_label.config(text=f"{mins:02d}:{secs:02d}")
            self.remaining_seconds -= 1

            # Update progress bar
            total_time = (
                             self.focus_minutes.get() if self.mode == "Focus"
                             else self.break_minutes.get() if self.mode == "Break"
                             else self.long_break_minutes.get()
                         ) * 60
            self.progress['value'] = ((
                                                  total_time - self.remaining_seconds) / total_time) * 100

            # Call this function again after 1 second
            self.root.after(1000, self.update_timer)
        elif self.running and self.remaining_seconds == 0:
            # Session finished
            self.session_finished()

    def session_finished(self):
        # Handle what happens when a session ends.
        if self.mode == "Focus":
            # Increase completed session counter
            self.completed_sessions += 1
            self.summary_label.config(
                text=f"Completed sessions: {self.completed_sessions}")

            # Log to CSV file
            self.log_session()

            # Notify user
            self.notify("Focus session complete!")

            # Decide between long break or short break
            if self.completed_sessions % self.sessions_before_long.get() == 0:
                self.mode = "Long Break"
            else:
                self.mode = "Break"

        elif self.mode in ["Break", "Long Break"]:
            self.notify("Break is over! Back to focus.")
            self.mode = "Focus"

        # Auto-start next session
        self.start_timer()

    # ==========================
    # Utility Functions
    # ==========================
    def update_timer_display(self):
        # Update timer label and mode label.
        mins, secs = divmod(self.remaining_seconds, 60)
        self.timer_label.config(text=f"{mins:02d}:{secs:02d}")
        self.mode_label.config(text=f"Mode: {self.mode}")
        self.progress['value'] = 0

    def notify(self, message):
        # Send a notification to the user.
        if USE_NOTIFICATIONS:
            notification.notify(title="Pomodoro Tracker", message=message,
                                timeout=5)
        else:
            messagebox.showinfo("Pomodoro Tracker", message)

    def log_session(self):
        # Save session details into a CSV file.
        with open("sessions.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                self.task_name.get() if self.task_name.get() else "No Task",
                self.focus_minutes.get()
            ])


# ==========================
# Run the Application
# ==========================
if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroApp(root)
    root.mainloop()
