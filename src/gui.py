import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

try:
    from .game import HanoiGame
except ImportError:
    from game import HanoiGame


class HanoiGUI:
    def __init__(self, root):
        self.root = root
        self.game = HanoiGame()

        self.CARD_WIDTH = 140
        self.CARD_HEIGHT = 190
        self.PILE_X_POSITIONS = [150, 350, 550]
        self.PILE_Y = 180
        self.CARD_STACK_OFFSET = 35

        self.dragged_items = []
        self.drag_source_pile = None
        self.drag_offset_x = 0
        self.drag_offset_y = 0

        self.game_won = False

        self.card_images = {}
        self._load_card_images()

        self._setup_ui()
        self._draw_game_state()

    def _load_card_images(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        assets_path = os.path.join(project_root, "assets", "images", "Heart Suit")

        card_files = {
            "A": "card_hearts_A.png",
            "2": "card_hearts_02.png",
            "3": "card_hearts_03.png",
            "4": "card_hearts_04.png",
            "5": "card_hearts_05.png",
            "6": "card_hearts_06.png",
            "7": "card_hearts_07.png",
            "8": "card_hearts_08.png",
            "9": "card_hearts_09.png",
            "empty": "card_empty.png",
        }

        for rank, filename in card_files.items():
            filepath = os.path.join(assets_path, filename)
            if os.path.exists(filepath):
                img = Image.open(filepath)
                img = img.resize(
                    (self.CARD_WIDTH, self.CARD_HEIGHT), Image.Resampling.LANCZOS
                )
                self.card_images[rank] = ImageTk.PhotoImage(img)

    def _setup_ui(self):
        title_label = tk.Label(
            self.root,
            text="Hanoi Solitaire",
            font=("Arial", 24, "bold"),
            bg="#1a472a",
            fg="white",
        )
        title_label.pack(pady=10)

        self.move_label = tk.Label(
            self.root, text="Moves: 0", font=("Arial", 14), bg="#1a472a", fg="white"
        )
        self.move_label.pack()

        self.canvas = tk.Canvas(self.root, width=850, height=550, bg="#2d5a3d")
        self.canvas.pack(pady=20)

        self.canvas.bind("<Button-1>", self._on_mouse_press)
        self.canvas.bind("<B1-Motion>", self._on_mouse_motion)
        self.canvas.bind("<ButtonRelease-1>", self._on_mouse_release)

        button_frame = tk.Frame(self.root, bg="#1a472a")
        button_frame.pack(pady=10)

        new_game_btn = tk.Button(
            button_frame,
            text="New Game",
            command=self._new_game,
            font=("Arial", 12, "bold"),
            width=12,
            bg="#4CAF50",
            fg="black",
            activebackground="#45a049",
            activeforeground="black",
            bd=0,
            highlightthickness=0,
            relief="flat",
        )
        new_game_btn.pack(side=tk.LEFT, padx=10)

        undo_btn = tk.Button(
            button_frame,
            text="Undo",
            command=self._undo_move,
            font=("Arial", 12, "bold"),
            width=12,
            bg="#ff9800",
            fg="black",
            activebackground="#e68900",
            activeforeground="black",
            bd=0,
            highlightthickness=0,
            relief="flat",
        )
        undo_btn.pack(side=tk.LEFT, padx=10)

    def _draw_game_state(self):
        self.canvas.delete("all")

        for pile_idx, pile in enumerate(self.game.piles):
            x = self.PILE_X_POSITIONS[pile_idx]

            if pile.is_empty():
                if "empty" in self.card_images:
                    self.canvas.create_image(
                        x,
                        self.PILE_Y,
                        image=self.card_images["empty"],
                        anchor="nw",
                        tags="placeholder",
                    )
            else:
                for card_idx, card in enumerate(pile.cards):
                    y = self.PILE_Y + card_idx * self.CARD_STACK_OFFSET
                    self._draw_card(x, y, card, pile_idx, card_idx)

        self.move_label.config(text=f"Moves: {self.game.move_count}")

        if self.game_won:
            self._draw_win_overlay()

    def _draw_card(self, x, y, card, pile_idx, card_idx):
        if card.rank in self.card_images:
            self.canvas.create_image(
                x,
                y,
                image=self.card_images[card.rank],
                anchor="nw",
                tags=("card", f"pile_{pile_idx}", f"card_{card_idx}"),
            )

    def _on_mouse_press(self, event):
        items = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
        if not items:
            return

        item_id = items[-1]
        tags = self.canvas.gettags(item_id)

        if "card" not in tags:
            return

        pile_tags = [t for t in tags if t.startswith("pile_")]
        if not pile_tags:
            return

        pile_idx = int(pile_tags[0].split("_")[1])

        pile = self.game.piles[pile_idx]
        if pile.is_empty():
            return

        card_tags = [t for t in tags if t.startswith("card_")]
        if not card_tags:
            return

        card_idx = int(card_tags[0].split("_")[1])

        if card_idx != pile.size() - 1:
            return

        self.dragged_items = []
        for canvas_item in self.canvas.find_all():
            item_tags = self.canvas.gettags(canvas_item)
            if f"pile_{pile_idx}" in item_tags and f"card_{card_idx}" in item_tags:
                self.dragged_items.append(canvas_item)

        if not self.dragged_items:
            return

        self.drag_source_pile = pile_idx

        main_rect = self.dragged_items[0]
        coords = self.canvas.coords(main_rect)
        self.drag_offset_x = event.x - coords[0]
        self.drag_offset_y = event.y - coords[1]

        for item in self.dragged_items:
            self.canvas.tag_raise(item)

    def _on_mouse_motion(self, event):
        if not self.dragged_items:
            return

        new_x = event.x - self.drag_offset_x
        new_y = event.y - self.drag_offset_y

        main_rect = self.dragged_items[0]
        old_coords = self.canvas.coords(main_rect)
        old_x = old_coords[0]
        old_y = old_coords[1]

        dx = new_x - old_x
        dy = new_y - old_y

        for item in self.dragged_items:
            self.canvas.move(item, dx, dy)

    def _on_mouse_release(self, event):
        if not self.dragged_items:
            return

        drop_pile_idx = None
        for i, x in enumerate(self.PILE_X_POSITIONS):
            if x <= event.x <= x + self.CARD_WIDTH + 100:
                drop_pile_idx = i
                break

        if drop_pile_idx is not None:
            move_successful = self.game.make_move(self.drag_source_pile, drop_pile_idx)

            if move_successful:
                if self.game.is_game_won():
                    self.game_won = True
                    self._draw_win_overlay()

        self.dragged_items = []
        self.drag_source_pile = None

        self._draw_game_state()

    def _new_game(self):
        self.game_won = False
        self.game.reset()
        self._draw_game_state()

    def _undo_move(self):
        success = self.game.undo()

        if not success:
            messagebox.showinfo("Undo", "No moves to undo!")
        else:
            self._draw_game_state()

    def _draw_win_overlay(self):
        self.canvas.create_rectangle(
            0,
            0,
            850,
            550,
            fill="#000000",
            stipple="gray50",
            tags="win_overlay",
        )

        self.canvas.create_rectangle(
            225,
            175,
            625,
            375,
            fill="white",
            outline="#4CAF50",
            width=3,
            tags="win_overlay",
        )

        self.canvas.create_text(
            425,
            230,
            text="Congratulations!",
            font=("Arial", 28, "bold"),
            fill="#4CAF50",
            tags="win_overlay",
        )

        self.canvas.create_text(
            425,
            280,
            text=f"You won in {self.game.move_count} moves!",
            font=("Arial", 16),
            fill="black",
            tags="win_overlay",
        )

        self.canvas.create_rectangle(
            325,
            315,
            525,
            355,
            fill="#4CAF50",
            outline="#45a049",
            width=2,
            tags=("win_overlay", "play_again_btn"),
        )

        self.canvas.create_text(
            425,
            335,
            text="Play Again",
            font=("Arial", 14, "bold"),
            fill="black",
            tags=("win_overlay", "play_again_btn"),
        )

        self.canvas.tag_bind(
            "play_again_btn", "<Button-1>", lambda e: self._play_again()
        )

        self.canvas.tag_bind(
            "play_again_btn",
            "<Enter>",
            lambda e: self.canvas.itemconfig("play_again_btn", fill="#45a049"),
        )
        self.canvas.tag_bind(
            "play_again_btn",
            "<Leave>",
            lambda e: self.canvas.itemconfig("play_again_btn", fill="#4CAF50"),
        )

    def _play_again(self):
        self.game_won = False
        self.canvas.delete("win_overlay")
        self._new_game()
