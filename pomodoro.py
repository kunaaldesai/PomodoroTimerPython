import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
import pygame
import time
import os
import sys

class PomodoroTimer:
    def __init__(self, master):
        self.master = master
        self.master.config(bg="#444444")

        pygame.mixer.init()

        self.pomodoro_length = 25 * 60
        self.short_break_length = 5 * 60
        self.long_break_length = 15 * 60
        self.current_time = 0
        self.running = False
        self.on_break = False
        self.break_count = 0

        if getattr(sys, 'frozen', False):
            base_dir = sys._MEIPASS
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))

        self.sound_file = os.path.join(base_dir, 'alarm.mp3')

        self.timer_label = tk.Label(master, font=('Arial', 20), bg="#444444", fg="white")
        self.timer_label.pack(pady=20)

        self.start_button = ttk.Button(master, text="Start", command=self.start_timer)
        self.start_button.pack()

        self.reset_button = ttk.Button(master, text="Reset", command=self.reset_timer)
        self.reset_button.pack(pady=10)

        self.pomo_label = ttk.Label(master, text="Pomodoro (mins)", background="#444444", foreground="white")
        self.pomo_label.pack(pady=5)
        self.pomo_entry = ttk.Entry(master)
        self.pomo_entry.insert(0, "25")
        self.pomo_entry.pack(pady=5)

        self.short_break_label = ttk.Label(master, text="Short Break (mins)", background="#444444", foreground="white")
        self.short_break_label.pack(pady=5)
        self.short_break_entry = ttk.Entry(master)
        self.short_break_entry.insert(0, "5")
        self.short_break_entry.pack(pady=5)

        self.long_break_label = ttk.Label(master, text="Long Break (mins)", background="#444444", foreground="white")
        self.long_break_label.pack(pady=5)
        self.long_break_entry = ttk.Entry(master)
        self.long_break_entry.insert(0, "15")
        self.long_break_entry.pack(pady=5)

        # Cycle count label
        self.cycle_label = tk.Label(master, text="Cycles Completed: 0", bg="#444444", fg="white")
        self.cycle_label.pack(pady=10)
        
        # Cycles until long break label
        self.until_long_break_label = tk.Label(master, text="Cycles until long break: 4", bg="#444444", fg="white")
        self.until_long_break_label.pack(pady=10)

        self.update_timer(self.pomodoro_length)

    def update_timer(self, time_remaining):
        minutes = time_remaining // 60
        seconds = time_remaining % 60
        self.timer_label.config(text=f"{minutes:02}:{seconds:02}")

    def start_timer(self):
        try:
            self.pomodoro_length = int(self.pomo_entry.get()) * 60
            self.short_break_length = int(self.short_break_entry.get()) * 60
            self.long_break_length = int(self.long_break_entry.get()) * 60
            if not self.running:
                self.running = True
                self.start_button.config(text="Pause", command=self.pause_timer)
                self.tick()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid minutes for all durations.")

    def pause_timer(self):
        self.running = False
        self.start_button.config(text="Resume", command=self.start_timer)

    def reset_timer(self):
        self.running = False
        self.on_break = False
        self.break_count = 0
        self.current_time = 0
        self.cycle_label.config(text="Cycles Completed: 0")
        self.until_long_break_label.config(text="Cycles until long break: 4")
        self.start_button.config(text="Start", command=self.start_timer)
        self.update_timer(self.pomodoro_length)

    def play_sound(self):
        if self.sound_file:
            pygame.mixer.music.load(self.sound_file)
            pygame.mixer.music.play()

    def tick(self):
        if self.running:
            if not self.on_break:
                time_remaining = self.pomodoro_length - self.current_time
            else:
                if self.break_count % 4 == 0:
                    time_remaining = self.long_break_length - self.current_time
                else:
                    time_remaining = self.short_break_length - self.current_time

            self.update_timer(time_remaining)
            self.current_time += 1

            if time_remaining <= 0:
                self.play_sound()
                self.break_count += 1
                self.on_break = not self.on_break
                self.current_time = 0
                if not self.on_break:
                    self.cycle_label.config(text=f"Cycles Completed: {self.break_count}")
                    cycles_until_long_break = 4 - (self.break_count % 4)
                    self.until_long_break_label.config(text=f"Cycles until long break: {cycles_until_long_break}")
                if self.break_count % 4 == 0:
                    self.cycle_label.config(text=f"Cycles Completed: {self.break_count} (Long Break!)")
                if self.on_break:
                    messagebox.showinfo("Time's up!", "Time for a break!")
                else:
                    messagebox.showinfo("Break's over!", "Time to get back to work!")
            self.master.after(1000, self.tick)

if __name__ == "__main__":
    root = ThemedTk(theme="adapta")  
    root.title("Pomodoro Timer")
    app = PomodoroTimer(master=root)
    root.mainloop()
