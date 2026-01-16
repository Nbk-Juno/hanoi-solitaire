import tkinter as tk

# Handle imports for both package and direct execution
try:
    from .gui import HanoiGUI
except ImportError:
    from gui import HanoiGUI


def main():
    """Launch the Hanoi Solitaire GUI."""
    root = tk.Tk()
    root.title("Hanoi Solitaire")
    root.geometry("900x750")
    root.resizable(False, False)
    root.configure(bg="#1a472a")  # Dark green background

    HanoiGUI(root)

    root.mainloop()


if __name__ == "__main__":
    main()
