import tkinter as tk
from tkinter import messagebox, scrolledtext
import random
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def generate_reference_string(length=10, page_range=6):
    return [random.randint(0, page_range - 1) for _ in range(length)]

def optimal_victim(frames, future_refs):
    farthest_index = -1
    victim_index = 0
    for idx, page in enumerate(frames):
        try:
            next_use = future_refs.index(page)
        except ValueError:
            return idx
        if next_use > farthest_index:
            farthest_index = next_use
            victim_index = idx
    return victim_index

def simulate_opt(frames_count, refs):
    frames = [None] * frames_count
    table = [[None for _ in range(len(refs))] for _ in range(frames_count)]
    steps = []
    for i, page in enumerate(refs):
        action = ""
        if page not in frames:
            if None in frames:
                empty = frames.index(None)
                frames[empty] = page
                action = f"Step {i+1}: Insert page {page} into empty frame {empty+1}"
            else:
                future = refs[i + 1:]
                victim = optimal_victim(frames, future)
                replaced = frames[victim]
                frames[victim] = page
                action = f"Step {i+1}: Replace page {replaced} with {page} in frame {victim+1} (OPT)"
        else:
            action = f"Step {i+1}: Page {page} already in frame"
        steps.append(action)
        for r in range(frames_count):
            table[r][i] = frames[r]
    return table, steps

class OPTPuzzleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("OPT Algorithm Puzzle Game")
        self.root.geometry("950x600")
        self.root.resizable(False, False)
        self.frames_count = 3
        self.ref_length = 10
        self.page_range = 6

        self.reference = []
        self.correct_table = []
        self.opt_steps = []
        self.entries = [[None]*self.ref_length for _ in range(self.frames_count)]
        self.game_started = False

        root_style = ttk.Style("darkly")
        self.bg = root_style.colors.bg

        main_frame = ttk.Frame(root, padding=20)
        main_frame.pack(fill="both", expand=True)

        top_frame = ttk.Frame(main_frame)
        top_frame.pack(pady=6)

        ttk.Button(top_frame, text="New Game", bootstyle=PRIMARY, command=self.new_game).pack(side="left", padx=6)
        ttk.Button(top_frame, text="Check Answers", bootstyle=SUCCESS, command=self.check_answers).pack(side="left", padx=6)

        ref_frame = ttk.Frame(main_frame)
        ref_frame.pack(pady=8)
        ttk.Label(ref_frame, text="Reference String:", font=("Segoe UI", 10, "bold"), foreground="white").pack(side="left", padx=(0,8))
        self.ref_entry = ttk.Entry(ref_frame, width=70, font=("Consolas", 11))
        self.ref_entry.pack(side="left")
        ttk.Button(ref_frame, text="Copy", bootstyle=INFO, command=self.copy_reference).pack(side="left", padx=4)

        self.grid_frame = ttk.Frame(main_frame)
        self.grid_frame.pack(pady=14)

        self.result_label = ttk.Label(main_frame, text="", font=("Segoe UI", 11, "bold"), foreground="white")
        self.result_label.pack(pady=6)

        instr = (
            "Fill the 3×N grid with page numbers.\n"
            "Use blank or '-' where no page is in that frame.\n"
            "Empty cells that should stay empty are counted as correct.\n"
            "Below panel explains mistakes and OPT decisions.\n"
            "After entering a value, cursor moves automatically to the next cell."
        )
        ttk.Label(main_frame, text=instr, font=("Segoe UI", 9), foreground="white").pack(pady=(0,6))

        self.explain_text = scrolledtext.ScrolledText(main_frame, width=110, height=10, font=("Consolas", 10), bg="#2b2b2b", fg="white")
        self.explain_text.pack(pady=4)

        self.vcmd = (root.register(self.validate_entry), "%P")

    def validate_entry(self, P):
        if P == "" or P.strip() in "-_":
            return True
        return len(P.strip()) == 1 and P.strip().isdigit()

    def parse_reference_input(self):
        txt = self.ref_entry.get().strip()
        if not txt:
            return generate_reference_string(self.ref_length, self.page_range)
        try:
            nums = [int(x) for x in txt.split()]
            return nums
        except ValueError:
            messagebox.showerror("Error", "Reference string must contain only integers separated by spaces.")
            return None

    def new_game(self):
        user_ref = self.parse_reference_input()
        if not user_ref:
            return
        self.reference = user_ref
        self.ref_length = len(self.reference)

        self.ref_entry.configure(state="readonly")
        self.game_started = True

        for widget in self.grid_frame.winfo_children():
            widget.destroy()
        self.entries = [[None]*self.ref_length for _ in range(self.frames_count)]
        self.result_label.config(text="")
        self.explain_text.delete("1.0", tk.END)

        self.correct_table, self.opt_steps = simulate_opt(self.frames_count, self.reference)

        ttk.Label(self.grid_frame, text="", width=8).grid(row=0, column=0)
        for i, ref in enumerate(self.reference):
            ttk.Label(self.grid_frame, text=str(ref), width=5, relief="ridge",
                      bootstyle=INFO, anchor="center", font=("Segoe UI", 10, "bold")).grid(row=0, column=i+1, padx=2, pady=2)

        for r in range(self.frames_count):
            ttk.Label(self.grid_frame, text=f"Frame {r+1}:", font=("Segoe UI", 10, "bold"),
                      foreground="white").grid(row=r+1, column=0, sticky="e", padx=4)
            for c in range(self.ref_length):
                e = ttk.Entry(self.grid_frame, width=5, justify="center", font=("Consolas", 10),
                              validate="key", validatecommand=self.vcmd)
                e.grid(row=r+1, column=c+1, padx=2, pady=2)
                e.insert(0, "")
                self.entries[r][c] = e
                e.bind("<KeyRelease>", lambda event, row=r, col=c: self.auto_next_cell(event, row, col))

    def auto_next_cell(self, event, row, col):
        val = self.entries[row][col].get().strip()
        if val == "" or (len(val) == 1 and (val.isdigit() or val in "-_")):
            next_row = row + 1
            next_col = col
            if next_row >= self.frames_count:
                next_row = 0
                next_col = col + 1
            if next_col < self.ref_length:
                self.entries[next_row][next_col].focus_set()

    def _is_blank_input(self, s: str):
        return s == "" or s.strip() in "-_"

    def copy_reference(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(" ".join(str(x) for x in self.reference))
        self.root.update()

    def check_answers(self):
        if not self.reference:
            messagebox.showinfo("Info", "Start a new game first.")
            return

        correct = 0
        total = self.frames_count * self.ref_length
        self.explain_text.delete("1.0", tk.END)

        for r in range(self.frames_count):
            for c in range(self.ref_length):
                user_raw = self.entries[r][c].get()
                user_text = user_raw.strip()
                user_blank = self._is_blank_input(user_text)
                correct_val = self.correct_table[r][c]

                explanation = ""
                if correct_val is None:
                    if user_blank:
                        self.entries[r][c].config(bootstyle=SUCCESS)
                        correct += 1
                    else:
                        self.entries[r][c].config(bootstyle=DANGER)
                        explanation = f"Step {c+1}, Frame {r+1}: Should be empty."
                else:
                    if user_blank:
                        self.entries[r][c].config(bootstyle=DANGER)
                        explanation = f"Step {c+1}, Frame {r+1}: Missing page {correct_val}."
                    else:
                        try:
                            user_int = int(user_text)
                        except ValueError:
                            self.entries[r][c].config(bootstyle=DANGER)
                            explanation = f"Step {c+1}, Frame {r+1}: Invalid entry, expected {correct_val}."
                            continue
                        if user_int == correct_val:
                            self.entries[r][c].config(bootstyle=SUCCESS)
                            correct += 1
                        else:
                            self.entries[r][c].config(bootstyle=DANGER)
                            explanation = f"Step {c+1}, Frame {r+1}: Wrong page {user_int}, should be {correct_val}."

                if explanation:
                    self.explain_text.insert(tk.END, explanation + "\n")

        self.explain_text.insert(tk.END, "\n-- OPT Algorithm Decisions --\n")
        for step in self.opt_steps:
            self.explain_text.insert(tk.END, step + "\n")

        self.result_label.config(text=f"Correct cells: {correct}/{total}", foreground="white")

        if correct == total:
            messagebox.showinfo("Success", "All cells correct! You can now enter a new reference.")
            self.ref_entry.configure(state="normal")
            self.game_started = False

def main():
    root = ttk.Window(themename="darkly")
    app = OPTPuzzleGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
