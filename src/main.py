import tkinter as tk

try:
    from .gui import HanoiGUI
except ImportError:
    from gui import HanoiGUI


def main():
    root = tk.Tk()
    root.title("Hanoi Solitaire")
    root.geometry("900x750")
    root.resizable(False, False)
    root.configure(bg="#1a472a")
    HanoiGUI(root)

    root.mainloop()


if __name__ == "__main__":
    main()
