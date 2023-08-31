import tkinter as tk
from tkinter import messagebox
import numpy as np

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.entries = []
        for i in range(25):
            row_entries = []
            for j in range(5):
                e = tk.Entry(self, width=5)
                e.grid(row=i, column=j)
                row_entries.append(e)
            self.entries.append(row_entries)

        self.calc_button = tk.Button(self)
        self.calc_button["text"] = "Calculate Path"
        self.calc_button["command"] = self.calculate_path
        self.calc_button.grid(row=26, column=0, columnspan=5)

    def calculate_path(self):
        matrix = []
        for row_entries in self.entries:
            row = []
            for e in row_entries:
                try:
                    val = int(e.get())
                    assert 0 <= val <= 5
                    row.append(val)
                except (ValueError, AssertionError):
                    messagebox.showerror("Invalid input", "Please enter integers between 0 and 5.")
                    return
            matrix.append(row)

        matrix = np.array(matrix)
        path = self.find_max_path(matrix)
        for i, j in path:
            self.entries[i][j].config(bg='yellow')

    @staticmethod
    def find_max_path(matrix):
        dp = np.zeros_like(matrix)
        dp[0, :] = matrix[0, :]
        for i in range(1, matrix.shape[0]):
            for j in range(matrix.shape[1]):
                if j == 0:
                    dp[i, j] = matrix[i, j] + max(dp[i-1, j], dp[i-1, j+1])
                elif j == matrix.shape[1] - 1:
                    dp[i, j] = matrix[i, j] + max(dp[i-1, j], dp[i-1, j-1])
                else:
                    dp[i, j] = matrix[i, j] + max(dp[i-1, j-1], dp[i-1, j], dp[i-1, j+1])

        path = []
        j = np.argmax(dp[-1, :])
        path.append((24, j))
        for i in range(24, 0, -1):
            if j == 0:
                j = np.argmax(dp[i-1, j:j+2])
            elif j == 4:
                j = np.argmax(dp[i-1, j-1:j+1]) + j - 1
            else:
                j = np.argmax(dp[i-1, j-1:j+2]) + j - 1
            path.append((i-1, j))

        return path

root = tk.Tk()
app = Application(master=root)
app.mainloop()
